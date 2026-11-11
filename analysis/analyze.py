"""Analyse one benchmark run folder. Usage: analyze.py <run folder> <verticalrtk|freshqa|frames|sealqa|finsearchcomp|obnews>"""
import glob, json, math, os, re, statistics, sys
from collections import defaultdict, Counter

OUT, DS = sys.argv[1], sys.argv[2]
PROVS = ["cloro", "serpapi", "tavily", "exa", "parallel", "brave"]
NAMES = {"cloro": "cloro", "serpapi": "SerpApi", "tavily": "Tavily", "exa": "Exa", "parallel": "Parallel", "brave": "Brave"}
# Same text-match approach as the SimpleQA analysis: dataset names plus dataset hosts.
LEAK = {
    "verticalrtk": ["verticalrtk", "vertical-rtk", "vertical_rtk", "takodata", "trytako"],
    "freshqa": ["freshqa", "fresh_qa", "fresh-qa", "freshllms", "freshprompt"],
    "frames": ["frames-benchmark", "frames benchmark", "google/frames"],
    "sealqa": ["sealqa", "seal-qa", "seal_qa", "seal-0", "vtllms"],
    "finsearchcomp": ["finsearchcomp", "byteseedxpert"],
    "obnews": ["openbenchmarks", "ob-news"],
}[DS] + ["huggingface.co/datasets", "kaggle.com"]


def wilson(c, n, z=1.96):
    if n == 0:
        return (0, 0)
    p = c / n
    d = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (centre - half, centre + half)


def pct(xs, p):
    return xs[min(len(xs) - 1, int(len(xs) * p))]


allrows, rows = {}, {}
for p in PROVS:
    path = os.path.join(OUT, "results", f"{p}.jsonl")
    lines = [json.loads(l) for l in open(path)] if os.path.exists(path) else []
    allrows[p] = lines
    rows[p] = {r["id"]: r for r in lines}

ids = sorted(set().union(*[set(rows[p]) for p in PROVS]))
q = {}
for p in PROVS:
    for i, r in rows[p].items():
        q.setdefault(i, {"problem": r["problem"], "gold": r["gold"], "topic": r["topic"]})


def acc_row(p, keep):
    rs = [r for i, r in rows[p].items() if i in keep]
    n = len(rs)
    c = sum(r.get("grade") == "CORRECT" for r in rs)
    return c, n


# stale gold: 4+ providers INCORRECT
stale = [i for i in ids if sum(rows[p].get(i, {}).get("grade") == "INCORRECT" for p in PROVS) >= 4]
# leak
leak = {}
for i in ids:
    hits = []
    for p in PROVS:
        f = os.path.join(OUT, "raw", p, f"{i}.json")
        if os.path.exists(f):
            t = open(f, encoding="utf-8", errors="ignore").read().lower()
            k = [w for w in LEAK if w in t]
            if k:
                hits.append(f"{NAMES[p]} ({', '.join(k)})")
    if hits:
        leak[i] = hits

res = {}
print(f"# {DS}: {len(ids)} ids\n")
print("## Main table\n")
print("| Provider | n | Correct | Incorrect | Not attempted | Search errors | LLM errors | Accuracy | 95% interval | Acc. given attempted | p50 | p90 | p99 | Mean | AI Overview | Mean reader tokens | HTTP calls (deduped) | HTTP calls (all lines) |")
print("|" + "---|" * 18)
for p in PROVS:
    rs = list(rows[p].values())
    n = len(rs)
    g = Counter(r.get("grade") for r in rs)
    c, i_, na = g["CORRECT"], g["INCORRECT"], g["NOT_ATTEMPTED"]
    serr = sum(not r.get("search_ok") for r in rs)
    lerr = g["LLM_ERROR"]
    lo, hi = wilson(c, n)
    lat = sorted(r["search_latency_s"] for r in rs if r.get("search_ok"))
    toks = [r["reader_prompt_tokens"] for r in rs if r.get("reader_prompt_tokens")]
    aio = sum(bool(r.get("aio_present")) for r in rs)
    hc = sum(r.get("http_calls", 0) for r in rs)
    hca = sum(r.get("http_calls", 0) for r in allrows[p])
    res[p] = dict(n=n, c=c, i=i_, na=na, serr=serr, lerr=lerr, acc=c / n if n else 0, lo=lo, hi=hi,
                  att=c / (c + i_) if c + i_ else 0, p50=pct(lat, .5), p90=pct(lat, .9), p99=pct(lat, .99),
                  mean=statistics.mean(lat), aio=aio, tok=statistics.mean(toks) if toks else 0, hc=hc, hca=hca)
    R = res[p]
    print(f"| {NAMES[p]} | {n} | {c} | {i_} | {na} | {serr} | {lerr} | {R['acc']:.1%} | {lo*100:.1f}-{hi*100:.1f} | {R['att']:.1%} | {R['p50']:.2f} s | {R['p90']:.2f} s | {R['p99']:.2f} s | {R['mean']:.2f} s | {aio}/{n} | {R['tok']:,.0f} | {hc} | {hca} |")

print("\n## Error texts\n")
for p in PROVS:
    for r in rows[p].values():
        if r.get("error"):
            print(f"- {NAMES[p]} {r['id']} {r.get('grade')}: {r['error'][:200]}")
for p in PROVS:
    e = [r for r in allrows[p] if r.get("error")]
    if e:
        print(f"- {NAMES[p]}: {len(e)} error lines in the file (before dedupe)")

print("\n## Overlapping 95% intervals\n")
order = sorted(PROVS, key=lambda p: -res[p]["acc"])
ov, nov = [], []
for a in range(len(order)):
    for b in range(a + 1, len(order)):
        x, y = res[order[a]], res[order[b]]
        (ov if x["lo"] <= y["hi"] and y["lo"] <= x["hi"] else nov).append(f"{NAMES[order[a]]}-{NAMES[order[b]]}")
print("Overlap:", ", ".join(ov))
print("\nNo overlap:", ", ".join(nov))

topics = sorted({q[i]["topic"] for i in ids})
print("\n## Accuracy per topic\n")
print("| Topic | n | " + " | ".join(NAMES[p] for p in PROVS) + " |")
print("|" + "---|" * (2 + len(PROVS)))
for t in topics:
    keep = {i for i in ids if q[i]["topic"] == t}
    cells = []
    for p in PROVS:
        c, n = acc_row(p, keep)
        cells.append(f"{c}/{n} ({c/n:.0%})" if n else "-")
    print(f"| {t} | {len(keep)} | " + " | ".join(cells) + " |")
if DS == "freshqa":
    print("\n## False premise vs valid premise\n")
    print("| Set | n | " + " | ".join(NAMES[p] for p in PROVS) + " |")
    print("|" + "---|" * (2 + len(PROVS)))
    for label, f in [("false premise", lambda t: "false-premise" in t), ("valid premise", lambda t: "false-premise" not in t),
                     ("never-changing (all)", lambda t: t.startswith("never")), ("slow-changing (all)", lambda t: t.startswith("slow"))]:
        keep = {i for i in ids if f(q[i]["topic"])}
        cells = []
        for p in PROVS:
            c, n = acc_row(p, keep)
            lo, hi = wilson(c, n)
            cells.append(f"{c}/{n} ({c/n:.1%}, {lo*100:.1f}-{hi*100:.1f})" if n else "-")
        print(f"| {label} | {len(keep)} | " + " | ".join(cells) + " |")


def excl_table(title, excl):
    keep = set(ids) - set(excl)
    print(f"\n## {title} ({len(excl)} excluded, {len(keep)} kept)\n")
    print("| Provider | All | Without | 95% interval without |")
    print("|---|---|---|---|")
    for p in order:
        c, n = acc_row(p, keep)
        lo, hi = wilson(c, n)
        print(f"| {NAMES[p]} | {res[p]['acc']:.1%} | {c}/{n} ({c/n:.1%}) | {lo*100:.1f}-{hi*100:.1f} |")


excl_table("Accuracy without possibly stale gold", stale)
print("\n### Stale-gold list\n")
for i in stale:
    inc = [NAMES[p] for p in PROVS if rows[p].get(i, {}).get("grade") == "INCORRECT"]
    print(f"- **{i}** [{q[i]['topic']}] ({len(inc)} incorrect: {', '.join(inc)})")
    print(f"  - Q: {q[i]['problem'].strip()}")
    print(f"  - Gold: {q[i]['gold']}")
    norm = Counter(re.sub(r"[^a-z0-9.%$ ]", "", (rows[p].get(i, {}).get("answer") or "").lower()).strip()
                   for p in PROVS if rows[p].get(i, {}).get("grade") == "INCORRECT")
    print(f"  - Most common incorrect answer (normalised): {norm.most_common(1)[0][0]!r} x{norm.most_common(1)[0][1]}")
    for p in PROVS:
        r = rows[p].get(i, {})
        a = (r.get("answer") or "").replace("\n", " ")[:160]
        print(f"  - {NAMES[p]} ({r.get('grade')}): {a}")

excl_table("Accuracy without leak-flagged ids", list(leak))
print("\n### Leak list\n")
for i, h in leak.items():
    print(f"- {i}: {'; '.join(h)}. Q: {q[i]['problem'].strip()[:120]}")

# costs
exa = 0.0
for f in glob.glob(os.path.join(OUT, "raw", "exa", "*.json")):
    exa += (json.load(open(f)).get("costDollars") or {}).get("total") or 0
fu = sum("_ai_overview_followup" in json.load(open(f)) for f in glob.glob(os.path.join(OUT, "raw", "serpapi", "*.json")))
llm_lines = sum(1 for p in PROVS for r in allrows[p] if r.get("search_ok"))
print("\n## Cost actuals\n")
print(f"- cloro calls (all lines http_calls): {res['cloro']['hca']}, est credits x7 = {res['cloro']['hca']*7}")
print(f"- SerpApi http calls all lines: {res['serpapi']['hca']}; AI Overview followups in raw: {fu}")
for p in ["tavily", "parallel", "brave", "exa"]:
    print(f"- {NAMES[p]} http calls all lines: {res[p]['hca']}")
print(f"- Exa costDollars sum (raw files): ${exa:.3f}")
print(f"- Rows with search_ok (each = 1 reader + 1 grader call attempt, all lines): {llm_lines}")
fu_all = {p: sum(1 for f in glob.glob(os.path.join(OUT, "raw", p, "*.json"))) for p in PROVS}
print(f"- Raw files per provider: {fu_all}")
print(f"- Error lines (all lines) per provider: { {p: sum(1 for r in allrows[p] if r.get('grade') in ('ERROR', 'LLM_ERROR')) for p in PROVS} }")
print(f"- http_calls on error lines per provider: { {p: sum(r.get('http_calls', 0) for r in allrows[p] if r.get('grade') in ('ERROR', 'LLM_ERROR')) for p in PROVS} }")
print(f"- http_calls on ok lines minus ok lines (retries; SerpApi also AI Overview follow-ups) per provider: { {p: sum(r.get('http_calls', 0) - 1 for r in allrows[p] if r.get('search_ok')) for p in PROVS} }")
print(f"- LLM calls made (2 per search_ok line): {2 * llm_lines}")
print(f"- Reader prompt tokens, sum over deduped rows: {sum(r.get('reader_prompt_tokens') or 0 for p in PROVS for r in rows[p].values()):,}")
json.dump({"res": res, "stale": stale, "leak": leak}, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"res-{DS}.json"), "w"), indent=1, default=str)
