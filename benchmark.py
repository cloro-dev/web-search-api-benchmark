"""Run a QA benchmark against search APIs and measure accuracy and latency.

Datasets (--dataset):
  simpleqa     SimpleQA Verified, 1,000 questions (default)
  verticalrtk  Tako VerticalRTK fast set, commit f3f8628. The 17 rows with a
               capture timestamp or a forecast are dropped (their answers drift
               in hours), so 138 rows remain.
  freshqa      FreshQA, April 21, 2026 version, TEST split. Fast-changing rows
               and rows past their next_review date are dropped (the gold
               answers are older than the run), so 358 rows remain.
  frames       Google FRAMES, 824 multi-hop questions (Apache-2.0).
  sealqa       SealQA Seal-Hard, 254 questions (Apache-2.0). The 111 Seal-0
               questions are a subset; the topic column marks them.
  finsearchcomp FinSearchComp T2 (simple historical lookup), the 119 Global
               rows (CC-BY-4.0). The Greater China rows are in Chinese and
               T1 needs live prices, so they are not used.
  obnews       Openbenchmarks company-news public set, 100 questions.

Setup, the same for every provider: one search call per question (the
question text is the query, unchanged), 10 results, the provider's default
search mode. A reader LLM answers from the results only. The OpenAI
simple-evals grader prompt grades each answer.

When you give more than one provider, the calls are interleaved: each
question goes to every provider before the next question starts. Thus time
of day and network changes affect all providers equally.

Providers and keys:
  cloro     CLORO_API_KEY     Google results + AI Overview
  cloro-noaio CLORO_API_KEY   Google results only (no AI Overview requested or read)
  cloro-2p  CLORO_API_KEY     as cloro, with pages=2: up to 20 organic results
  serpapi   SERPAPI_KEY       Google results + AI Overview (follows page_token)
  tavily    TAVILY_API_KEY    search_depth=basic
  exa       EXA_API_KEY       type=auto, highlights
  parallel  PARALLEL_API_KEY  default mode
  brave     BRAVE_API_KEY     extra_snippets=true

Read-only variants (no search call). They read the saved raw response of
another provider in the same --out folder, so run that provider first:
  cloro-reread    raw/cloro, the cloro format again (a control for reader noise)
  cloro-drop-aio  raw/cloro, without the AI Overview block
  cloro-organic   raw/cloro, the organic titles, links and snippets only
  cloro-json      raw/cloro, the full "result" object as JSON
  cloro-2p-page1  raw/cloro-2p, the cloro format with page 1 organic results only
  cloro-top5      raw/cloro, the cloro format with the top 5 organic results only
  cloro-aio-only  raw/cloro, the AI Overview block only
  cloro-aio-last  raw/cloro, the cloro format with the AI Overview last
  cloro-no-snippet raw/cloro, the cloro format with organic titles and links only (no description)
  cloro-no-url    raw/cloro, the cloro format without the organic links
  cloro-no-title  raw/cloro, the cloro format without the organic titles
  cloro-minimal   raw/cloro, the AI Overview and the organic descriptions only
  cloro-crawl-top-half, cloro-crawl-all
                  raw/cloro, the organic results with no AI Overview, plus the page text
                  of the top half or all page-1 organic links (run crawl_pages.py first;
                  use --max-context-chars to give room for the pages)
  cloro-desc-only raw/cloro, the organic descriptions only (no AI Overview, titles or links)
  cloro-pages-top5-only raw/cloro, only the crawled page text of the top 5 organic links

Reader and grader: OPENAI_API_KEY, READER_MODEL, GRADER_MODEL. A model name that
starts with "gemini" uses GEMINI_API_KEY and the Gemini OpenAI-compatible endpoint.
With --search-only, no LLM is called: the run measures latency only.

Usage (from the repo root):
  python3 benchmark.py --providers cloro,serpapi [--n 1000] [--workers 4] [--search-only]
  python3 benchmark.py --summary --out <run folder>

Output, in outputs/search-benchmark-<dataset>-<date>/ (or --out):
results/<provider>.jsonl (one line per question; with --search-only,
results/<provider>.search-only.jsonl), raw/<provider>/<id>.json (the raw
search response, for the leak review) and data/simpleqa_verified.csv.
A re-run with the same --out skips (provider, question) pairs that are done.
"""
import argparse
import concurrent.futures as cf
import csv
import glob
import json
import os
import random
import re
import statistics
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = HERE
OUT = None  # outputs/search-benchmark-<dataset>-<date>, or --out
AS_OF = date.today()  # the date in the reader prompt and the FreshQA filter, or --as-of
DATASET_URLS = {
    "simpleqa": "https://huggingface.co/datasets/google/simpleqa-verified/resolve/main/simpleqa_verified.csv",
    "verticalrtk": "https://raw.githubusercontent.com/TakoData/VerticalRTK/f3f8628/datasets/fast/verticalrtk_fast.jsonl",
    "freshqa": "https://docs.google.com/spreadsheets/d/1_8mi-yuK30mvoDJu1KQXD6ODem7MKMcIgVAwDSzJkjM/export?format=csv",
    "frames": "https://huggingface.co/datasets/google/frames-benchmark/resolve/main/test.tsv",
    # The parquet files need pyarrow, so the rows come from the Hugging Face rows API.
    "sealqa": "https://datasets-server.huggingface.co/rows?dataset=vtllms/sealqa&split=test",
    "finsearchcomp": "https://huggingface.co/datasets/ByteSeedXpert/FinSearchComp/resolve/main/finsearchcomp_data.json",
    "obnews": "https://huggingface.co/datasets/openbenchmarks/OB-News-Websearch/resolve/main/data/eval.jsonl",
}
GRADER_TEMPLATE = open(os.path.join(HERE, "grader_template.txt")).read().strip()
READER_MODEL = os.environ.get("READER_MODEL", "gpt-5.6-luna")
GRADER_MODEL = os.environ.get("GRADER_MODEL", "gpt-5.6-sol")
NUM_RESULTS = 10
MAX_CONTEXT_CHARS = 30000  # same cap for every provider
MAX_CONTEXT = MAX_CONTEXT_CHARS  # or --max-context-chars
TIMEOUT_S = 120

READER_PROMPT = """Answer the question using only the search results below.
Give only the short answer (a name, number, date or phrase), with no explanation.
If the results do not contain the answer, reply exactly: NOT FOUND

Question: {question}

Search results:
{context}"""

# VerticalRTK and FreshQA ask about "current" and "this year" facts, so the
# reader gets the date. FreshQA also has false-premise questions, where the
# correct answer says that the premise is false. The SimpleQA prompt is not changed.
DATED_PREFIX = "Today's date is {today}.\n"
FALSE_PREMISE_LINE = "If the question rests on a false premise, say so in one short sentence.\n"


class Timed:
    """Collects the duration of each HTTP attempt for one question."""

    def __init__(self):
        self.ok_s = 0.0  # sum of the successful attempts (a user waits this long)
        self.calls = 0

    def http(self, url, body=None, headers=None):
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json", **(headers or {})})
        for attempt in range(3):
            self.calls += 1
            t0 = time.perf_counter()
            try:
                with urllib.request.urlopen(req, timeout=TIMEOUT_S) as r:
                    payload = r.read()
                self.ok_s += time.perf_counter() - t0
                return json.loads(payload)
            except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError):
                if attempt == 2:
                    raise
                time.sleep(5 * (attempt + 1))


def block(title, url, text):
    return f"{title or ''}\n{url or ''}\n{text or ''}".strip()


# Each search function returns (raw_response, list_of_text_blocks, aio_present).


def cloro_parts(d, aio=True, extras=True, max_organic=NUM_RESULTS, page1_only=False, snippets=True, aio_last=False, titles=True, links=True):
    """Text blocks from a cloro response. The defaults give the published cloro format."""
    r = d.get("result") or {}
    aio = aio and ((r.get("aioverview") or {}).get("text") or (r.get("aioverview") or {}).get("markdown"))
    parts = ["[AI Overview]\n" + aio] if aio else []
    kg = r.get("knowledgeGraph") or {}
    if extras and (kg.get("description") or kg.get("attributes")):
        attrs = "; ".join(f"{a.get('key')}: {a.get('value')}" for a in kg.get("attributes") or [])
        parts.append("[Knowledge graph]\n" + " ".join(filter(None, [kg.get("title"), kg.get("description"), attrs])))
    organic = [o for o in r.get("organicResults") or [] if not page1_only or o.get("page", 1) == 1]
    parts += [block(o.get("title") if titles else None, o.get("link") if links else None, o.get("snippet") if snippets else None) for o in organic[:max_organic]]
    if extras:
        parts += [block(p.get("question"), None, p.get("answer") or p.get("snippet")) for p in r.get("peopleAlsoAsk") or [] if p.get("answer") or p.get("snippet")]
    if aio and aio_last:
        parts = parts[1:] + parts[:1]
    return parts, bool(aio)


def search_cloro(t, q, with_aio=True, pages=1):
    body = {"query": q, "country": "US"}
    if with_aio:
        body["include"] = {"aioverview": {"markdown": True}}
    if pages > 1:
        body["pages"] = pages
    d = t.http("https://api.cloro.dev/v1/monitor/google", body, {"Authorization": f"Bearer {os.environ['CLORO_API_KEY']}"})
    return (d, *cloro_parts(d, aio=with_aio, max_organic=NUM_RESULTS * pages))


def serpapi_aio_text(aio):
    lines = []
    for b in aio.get("text_blocks") or []:
        if b.get("snippet"):
            lines.append(b["snippet"])
        for item in b.get("list") or []:
            lines.append("- " + " ".join(filter(None, [item.get("title"), item.get("snippet")])))
    return "\n".join(lines)


def search_serpapi(t, q):
    key = os.environ["SERPAPI_KEY"]
    params = {"engine": "google", "q": q, "gl": "us", "hl": "en", "no_cache": "true", "api_key": key}
    d = t.http("https://serpapi.com/search?" + urllib.parse.urlencode(params))
    aio = d.get("ai_overview") or {}
    if aio.get("page_token") and not aio.get("text_blocks"):
        # Google loads some AI Overviews in a second request. A user also waits for it.
        extra = t.http("https://serpapi.com/search?" + urllib.parse.urlencode(
            {"engine": "google_ai_overview", "page_token": aio["page_token"], "api_key": key}))
        aio = extra.get("ai_overview") or {}
        d["_ai_overview_followup"] = extra
    aio_text = serpapi_aio_text(aio)
    parts = ["[AI Overview]\n" + aio_text] if aio_text else []
    ab = d.get("answer_box") or {}
    if ab.get("answer") or ab.get("snippet"):
        parts.append("[Answer box]\n" + " ".join(filter(None, [ab.get("title"), ab.get("answer"), ab.get("snippet")])))
    kg = d.get("knowledge_graph") or {}
    if kg.get("description"):
        parts.append("[Knowledge graph]\n" + " ".join(filter(None, [kg.get("title"), kg.get("description")])))
    parts += [block(o.get("title"), o.get("link"), o.get("snippet")) for o in (d.get("organic_results") or [])[:NUM_RESULTS]]
    parts += [block(p.get("question"), None, p.get("snippet")) for p in d.get("related_questions") or [] if p.get("snippet")]
    return d, parts, bool(aio_text)


def search_tavily(t, q):
    d = t.http(
        "https://api.tavily.com/search",
        {"query": q, "search_depth": "basic", "max_results": NUM_RESULTS},
        {"Authorization": f"Bearer {os.environ['TAVILY_API_KEY']}"},
    )
    return d, [block(r.get("title"), r.get("url"), r.get("content")) for r in d.get("results") or []], False


def search_exa(t, q):
    d = t.http(
        "https://api.exa.ai/search",
        {"query": q, "type": "auto", "numResults": NUM_RESULTS, "contents": {"highlights": True}},
        {"x-api-key": os.environ["EXA_API_KEY"]},
    )
    return d, [block(r.get("title"), r.get("url"), "\n".join(r.get("highlights") or [])) for r in d.get("results") or []], False


def search_parallel(t, q):
    d = t.http(
        "https://api.parallel.ai/v1/search",
        {"objective": q, "search_queries": [q], "advanced_settings": {"max_results": NUM_RESULTS}},
        {"x-api-key": os.environ["PARALLEL_API_KEY"]},
    )
    return d, [block(r.get("title"), r.get("url"), "\n".join(r.get("excerpts") or [])) for r in d.get("results") or []], False


def search_brave(t, q):
    params = {"q": q, "count": NUM_RESULTS, "extra_snippets": "true"}
    d = t.http(
        "https://api.search.brave.com/res/v1/web/search?" + urllib.parse.urlencode(params),
        headers={"X-Subscription-Token": os.environ["BRAVE_API_KEY"], "Accept": "application/json"},
    )
    results = (d.get("web") or {}).get("results") or []
    return d, [block(r.get("title"), r.get("url"), "\n".join([r.get("description") or ""] + (r.get("extra_snippets") or []))) for r in results], False


PROVIDERS = {
    "cloro": search_cloro,
    "cloro-noaio": lambda t, q: search_cloro(t, q, with_aio=False),
    "cloro-2p": lambda t, q: search_cloro(t, q, pages=2),
    "serpapi": search_serpapi,
    "tavily": search_tavily,
    "exa": search_exa,
    "parallel": search_parallel,
    "brave": search_brave,
}

PAGE_CHARS = 20000  # the most characters of one crawled page that the reader gets


def cloro_crawl_parts(d, share):
    """Organic results with no AI Overview, plus the crawled page text of the top share of the
    page-1 organic links (crawl_pages.py saves the pages). A page that was not fetched adds nothing."""
    import hashlib
    organic = [o for o in (d.get("result") or {}).get("organicResults") or [] if o.get("page", 1) == 1][:NUM_RESULTS]
    keep = -(-len(organic) * share // 1)  # round up: 9 results give 5 for the top half
    parts = []
    for k, o in enumerate(organic):
        text = o.get("snippet")
        path = os.path.join(OUT, "pages", hashlib.sha1((o.get("link") or "").encode()).hexdigest() + ".json")
        if k < keep and os.path.exists(path):
            md = json.load(open(path)).get("markdown")
            if md:
                text = f"{text or ''}\n[Page text]\n{md[:PAGE_CHARS]}"
        parts.append(block(o.get("title"), o.get("link"), text))
    return parts, False


def cloro_pages_only(d, top):
    """Only the crawled page text of the top organic links (no AI Overview, titles, URLs or descriptions)."""
    import hashlib
    organic = [o for o in (d.get("result") or {}).get("organicResults") or [] if o.get("page", 1) == 1][:top]
    parts = []
    for o in organic:
        path = os.path.join(OUT, "pages", hashlib.sha1((o.get("link") or "").encode()).hexdigest() + ".json")
        md = json.load(open(path)).get("markdown") if os.path.exists(path) else None
        if md:
            parts.append(md[:PAGE_CHARS])
    return parts, False


# Read-only variants: name -> (provider whose saved raw response is read, function raw -> (parts, aio_present)).
READ_ONLY = {
    "cloro-reread": ("cloro", cloro_parts),
    "cloro-drop-aio": ("cloro", lambda d: cloro_parts(d, aio=False)),
    "cloro-organic": ("cloro", lambda d: cloro_parts(d, aio=False, extras=False)),
    "cloro-json": ("cloro", lambda d: ([json.dumps(d.get("result") or {}, ensure_ascii=False)], bool((d.get("result") or {}).get("aioverview")))),
    "cloro-2p-page1": ("cloro-2p", lambda d: cloro_parts(d, page1_only=True)),
    "cloro-top5": ("cloro", lambda d: cloro_parts(d, max_organic=5)),
    "cloro-aio-only": ("cloro", lambda d: cloro_parts(d, extras=False, max_organic=0)),
    "cloro-aio-last": ("cloro", lambda d: cloro_parts(d, aio_last=True)),
    "cloro-no-snippet": ("cloro", lambda d: cloro_parts(d, snippets=False)),
    "cloro-no-url": ("cloro", lambda d: cloro_parts(d, links=False)),
    "cloro-no-title": ("cloro", lambda d: cloro_parts(d, titles=False)),
    "cloro-minimal": ("cloro", lambda d: cloro_parts(d, extras=False, titles=False, links=False)),
    "cloro-crawl-top-half": ("cloro", lambda d: cloro_crawl_parts(d, 0.5)),
    "cloro-crawl-all": ("cloro", lambda d: cloro_crawl_parts(d, 1)),
    "cloro-desc-only": ("cloro", lambda d: cloro_parts(d, aio=False, extras=False, titles=False, links=False)),
    "cloro-pages-top5-only": ("cloro", lambda d: cloro_pages_only(d, 5)),
}


def llm(model, prompt):
    # On a rate limit (429), wait longer before the next try. A failed LLM call makes the
    # next pass search again, which costs a second search call.
    for k in range(5):
        try:
            # Gemini models go to the OpenAI-compatible Gemini endpoint.
            url, key = (("https://generativelanguage.googleapis.com/v1beta/openai/chat/completions", os.environ.get("GEMINI_API_KEY"))
                        if model.startswith("gemini") else ("https://api.openai.com/v1/chat/completions", os.environ.get("OPENAI_API_KEY")))
            d = Timed().http(url, {"model": model, "messages": [{"role": "user", "content": prompt}]}, {"Authorization": f"Bearer {key}"})
            break
        except urllib.error.HTTPError as e:
            if e.code != 429 or k == 4:
                raise
            time.sleep(30 * (k + 1))
    return d["choices"][0]["message"]["content"].strip(), (d.get("usage") or {}).get("prompt_tokens")


def grade(question, target, predicted):
    out, _ = llm(GRADER_MODEL, GRADER_TEMPLATE.format(question=question, target=target, predicted_answer=predicted))
    m = re.search(r"(A|B|C)", out)
    return {"A": "CORRECT", "B": "INCORRECT", "C": "NOT_ATTEMPTED"}[m.group(0) if m else "C"]


def run_one(provider, row, search_only, reader_prompt):
    rec = {"id": row["original_index"], "provider": provider, "problem": row["problem"], "gold": row["answer"], "topic": row["topic"]}
    if provider in READ_ONLY:
        source, to_parts = READ_ONLY[provider]
        path = os.path.join(OUT, "raw", source, f"{row['original_index']}.json")
        if not os.path.exists(path):
            rec.update(search_ok=False, http_calls=0, error=f"no saved response {path}", grade="ERROR")
            return rec
        parts, aio_present = to_parts(json.load(open(path)))
        rec.update(search_ok=True, search_latency_s=None, http_calls=0, aio_present=aio_present, n_blocks=len(parts))
    else:
        t = Timed()
        try:
            raw, parts, aio_present = PROVIDERS[provider](t, row["problem"])
        except Exception as e:
            rec.update(search_ok=False, http_calls=t.calls, error=repr(e), grade="ERROR")
            return rec
        rec.update(search_ok=True, search_latency_s=round(t.ok_s, 3), http_calls=t.calls, aio_present=aio_present, n_blocks=len(parts))
        raw_dir = os.path.join(OUT, "raw", provider)
        os.makedirs(raw_dir, exist_ok=True)
        with open(os.path.join(raw_dir, f"{row['original_index']}.json"), "w") as f:
            json.dump(raw, f, ensure_ascii=False)
    if search_only:
        return rec
    context = "\n\n".join(f"[{i}] {p}" for i, p in enumerate(parts, 1))[:MAX_CONTEXT]
    try:
        answer, prompt_tokens = llm(READER_MODEL, reader_prompt.format(question=row["problem"], context=context))
        rec.update(answer=answer, grade=grade(row["problem"], row["answer"], answer), context_chars=len(context), reader_prompt_tokens=prompt_tokens, error=None)
    except Exception as e:  # an LLM failure is ours, not the provider's
        rec.update(answer=None, grade="LLM_ERROR", error=repr(e))
    return rec


def pct(xs, p):
    return xs[min(len(xs) - 1, int(len(xs) * p))]


def summarize():
    print("| Provider | n | Accuracy | Acc. given attempted | Search errors | Latency p50 | p90 | p99 | AI Overview |")
    print("|---|---|---|---|---|---|---|---|---|")
    for path in sorted(glob.glob(os.path.join(OUT, "results", "*.jsonl"))):
        rows = list({r["id"]: r for r in map(json.loads, open(path))}.values())
        name = os.path.basename(path)[:-6]
        n = len(rows)
        graded = [r for r in rows if r.get("grade") in ("CORRECT", "INCORRECT", "NOT_ATTEMPTED", "ERROR")]
        c = sum(r["grade"] == "CORRECT" for r in graded)
        i = sum(r["grade"] == "INCORRECT" for r in graded)
        acc = f"{c / len(graded):.1%}" if graded and (c + i) else "-"
        acc_att = f"{c / (c + i):.1%}" if c + i else "-"
        lat = sorted(r["search_latency_s"] for r in rows if r.get("search_latency_s") is not None)
        errs = sum(not r.get("search_ok") for r in rows)
        aio = sum(bool(r.get("aio_present")) for r in rows)
        l50, l90, l99 = (f"{pct(lat, p):.2f}s" for p in (0.5, 0.9, 0.99)) if lat else ("-",) * 3
        print(f"| {name} | {n} | {acc} | {acc_att} | {errs} | {l50} | {l90} | {l99} | {aio}/{n} |")


def fetch_sealqa(path):
    """Save Seal-Hard as JSON, with a seal0 flag on the rows that are also in Seal-0."""
    def rows(config):
        out = []
        while True:
            url = f"{DATASET_URLS['sealqa']}&config={config}&offset={len(out)}&length=100"
            page = json.load(urllib.request.urlopen(url, timeout=TIMEOUT_S))["rows"]
            out += [r["row"] for r in page]
            if len(page) < 100:
                return out
    seal0 = {r["question"] for r in rows("seal_0")}
    keep = ("question", "answer", "freshness", "question_types", "effective_year", "topic")
    json.dump([{**{k: r[k] for k in keep}, "seal0": r["question"] in seal0} for r in rows("seal_hard")], open(path, "w"), ensure_ascii=False)


def load_questions(name, n, seed):
    """Return rows with the keys original_index, problem, answer, topic."""
    url = DATASET_URLS[name]
    base = {"freshqa": "freshqa.csv", "sealqa": "sealqa.json"}.get(name) or os.path.basename(urllib.parse.urlparse(url).path)
    dataset = os.path.join(OUT, "data", f"{name}-{base}" if base in ("test.tsv", "eval.jsonl") else base)
    if not os.path.exists(dataset):
        os.makedirs(os.path.dirname(dataset), exist_ok=True)
        if name == "sealqa":
            fetch_sealqa(dataset)
        else:
            urllib.request.urlretrieve(url, dataset)
    if name == "simpleqa":
        rows = list(csv.DictReader(open(dataset)))
    elif name == "verticalrtk":
        rows = [
            {"original_index": x["id"], "problem": x["query"], "answer": x["answer"], "topic": x["vertical"]}
            for x in map(json.loads, open(dataset))
            if not re.search(r"\d{4}-\d\d-\d\dT|captured|forecast", x["as_of"])
        ]
    elif name == "frames":
        rows = [{"original_index": r[""], "problem": r["Prompt"], "answer": r["Answer"], "topic": r["reasoning_types"]}
                for r in csv.DictReader(open(dataset), delimiter="\t")]
    elif name == "sealqa":
        rows = [{"original_index": str(i), "problem": r["question"], "answer": r["answer"],
                 "topic": f"{r['freshness']}{' seal-0' if r['seal0'] else ''}"} for i, r in enumerate(json.load(open(dataset)))]
    elif name == "finsearchcomp":
        rows = [{"original_index": r["prompt_id"], "problem": r["prompt"], "answer": r["response_reference"], "topic": r["label"]}
                for r in json.load(open(dataset)) if r["label"] == "Simple_Historical_Lookup(Global)"]
    elif name == "obnews":
        rows = [{"original_index": str(i), "problem": r["question"], "answer": r["answer"], "topic": "company-news"}
                for i, r in enumerate(map(json.loads, open(dataset)))]
    else:  # freshqa: two banner lines before the header
        def reviewed_by(r):
            m = re.fullmatch(r"(\d\d)/(\d\d)/(\d{4})", r["next_review"])
            return m and date(int(m[3]), int(m[1]), int(m[2])) <= AS_OF
        rows = [
            {"original_index": r["id"], "problem": r["question"],
             "answer": " OR ".join(r[f"answer_{i}"].strip() for i in range(10) if r[f"answer_{i}"].strip()),
             "topic": f"{r['fact_type']}{' false-premise' if r['false_premise'] == 'TRUE' else ''}"}
            for r in csv.DictReader(open(dataset).readlines()[2:])
            if r["split"] == "TEST" and r["fact_type"] != "fast-changing" and not reviewed_by(r)
        ]
    random.Random(seed).shuffle(rows)
    return rows[:n]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--providers", help="comma-separated: " + ",".join([*PROVIDERS, *READ_ONLY]))
    ap.add_argument("--dataset", choices=list(DATASET_URLS), default="simpleqa")
    ap.add_argument("--n", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--search-only", action="store_true", help="measure latency only, no LLM calls")
    ap.add_argument("--summary", action="store_true", help="print the results table and exit")
    ap.add_argument("--out", help="run folder (default: outputs/search-benchmark-<dataset>-<today>)")
    ap.add_argument("--max-context-chars", type=int, default=MAX_CONTEXT_CHARS,
                    help=f"cap on the reader context (default {MAX_CONTEXT_CHARS}, the same for every provider)")
    ap.add_argument("--as-of", type=date.fromisoformat, default=date.today(),
                    help="date for the reader prompt and the FreshQA filter (default: today). Set it to the date of an earlier run to read its saved responses again with the same questions")
    args = ap.parse_args()
    global OUT, AS_OF, MAX_CONTEXT
    AS_OF = args.as_of
    MAX_CONTEXT = args.max_context_chars
    OUT = os.path.abspath(args.out) if args.out else os.path.join(REPO, "outputs", f"search-benchmark-{args.dataset}-{date.today()}")
    reader_prompt = READER_PROMPT
    if args.dataset != "simpleqa":
        reader_prompt = DATED_PREFIX.format(today=AS_OF) + (FALSE_PREMISE_LINE if args.dataset == "freshqa" else "") + READER_PROMPT
    if args.summary:
        return summarize()
    providers = args.providers.split(",") if args.providers else []
    if not providers or any(p not in PROVIDERS and p not in READ_ONLY for p in providers):
        ap.error("--providers must name one or more of: " + ",".join([*PROVIDERS, *READ_ONLY]))

    os.makedirs(os.path.join(OUT, "results"), exist_ok=True)
    done, files = {}, {}
    for p in providers:
        path = os.path.join(OUT, "results", f"{p}{'.search-only' if args.search_only else ''}.jsonl")
        # A row with a search or LLM error runs again; summarize() keeps the last row per id.
        done[p] = {r["id"] for r in map(json.loads, open(path)) if r.get("grade") not in ("ERROR", "LLM_ERROR")} if os.path.exists(path) else set()
        files[p] = open(path, "a")
    # Interleave: question 1 on every provider, then question 2, and so on.
    tasks = [(p, row) for row in load_questions(args.dataset, args.n, args.seed) for p in providers if row["original_index"] not in done[p]]
    print(f"{len(tasks)} calls to run", file=sys.stderr)

    with cf.ThreadPoolExecutor(args.workers) as ex:
        for k, rec in enumerate(ex.map(lambda t: run_one(t[0], t[1], args.search_only, reader_prompt), tasks), 1):
            files[rec["provider"]].write(json.dumps(rec, ensure_ascii=False) + "\n")
            files[rec["provider"]].flush()
            if k % 25 == 0:
                print(f"{k}/{len(tasks)}", file=sys.stderr)
    summarize()


if __name__ == "__main__":
    main()
