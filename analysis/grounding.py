"""Is each reader answer supported by the search results alone?

Usage: grounding.py <selection folder> <judged.json>

The selection folder has <reader>/frames/results/<api>-reread.jsonl and
<reader>/frames/raw/<api>/ (the saved search responses). Two judges read each
answer (not NOT FOUND) with the search results and reply SUPPORTED or
NOT_SUPPORTED. The same answer to the same question is judged once, and the
verdicts are kept in judged.json, so a second run calls no judge. The script
prints, per reader, how many answers both judges call supported.
"""
import collections
import concurrent.futures as cf
import importlib.util
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("b", os.path.join(HERE, "..", "benchmark.py"))
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)

B, CACHE = sys.argv[1], sys.argv[2]
APIS = ["cloro", "parallel", "keenable-nodata", "firecrawl"]
READERS = sorted(d for d in os.listdir(B) if os.path.isdir(os.path.join(B, d, "frames", "results")))
JUDGES = ["gpt-5.6-sol", "gemini-pro-latest"]
PROMPT = """You check whether an answer comes from the search results below.
Answer SUPPORTED if a careful reader can get the answer from the search results alone,
by reading them and by simple reasoning on them (combining facts from two or more results,
counting, arithmetic, dates). Answer NOT_SUPPORTED if a fact that the answer needs is
not in the search results. Do not judge whether the answer is true.
Reply with one word: SUPPORTED or NOT_SUPPORTED.

Question: {q}
Answer: {a}

Search results:
{ctx}"""


def load(path):
    return {json.loads(l)["id"]: json.loads(l) for l in open(path)}


def norm(a):
    return re.sub(r"\s+", " ", (a or "").strip().lower())


data = {m: {p: load(f"{B}/{m}/frames/results/{p}-reread.jsonl") for p in APIS} for m in READERS}
done = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
ctxs, todo = {}, {}
for p in APIS:
    src, fn = b.READ_ONLY[p + "-reread"]
    for m in READERS:
        for i, r in data[m][p].items():
            key = f"{p}|{i}|{norm(r.get('answer'))}"
            if r["grade"] not in ("CORRECT", "INCORRECT") or key in done or key in todo:
                continue
            if (p, i) not in ctxs:
                parts, _ = fn(json.load(open(f"{B}/{m}/frames/raw/{src}/{i}.json")))
                ctxs[(p, i)] = "\n\n".join(f"[{k}] {t}" for k, t in enumerate(parts, 1))[:b.MAX_CONTEXT]
            todo[key] = (r["problem"], r["answer"], (p, i))


def judge(item):
    key, (q, a, pi) = item
    out = {}
    for j in JUDGES:
        t, _ = b.llm(j, PROMPT.format(q=q, a=a, ctx=ctxs[pi]))
        out[j] = "NOT_SUPPORTED" if "NOT_SUPPORTED" in t.upper() else "SUPPORTED" if "SUPPORTED" in t.upper() else "?"
    return key, out


with cf.ThreadPoolExecutor(12) as ex:
    for k, out in ex.map(judge, todo.items()):
        done[k] = out
json.dump(done, open(CACHE, "w"), indent=1, ensure_ascii=False)

agree = sum(v[JUDGES[0]] == v[JUDGES[1]] for v in done.values())
print(f"{len(done)} answers judged, judges agree on {agree} ({100 * agree / max(len(done), 1):.1f}%)")
print("| Reader | Correct | Correct, supported | Correct, not supported | Wrong | Wrong, not supported | Not found | Answers supported |")
print("|---|---|---|---|---|---|---|---|")
for m in READERS:
    c = collections.Counter()
    for p in APIS:
        for i, r in data[m][p].items():
            if r["grade"] == "NOT_ATTEMPTED":
                c["nf"] += 1
            elif r["grade"] in ("CORRECT", "INCORRECT"):
                v = done[f"{p}|{i}|{norm(r['answer'])}"]
                s = "S" if all(v[j] == "SUPPORTED" for j in JUDGES) else "U" if all(v[j] == "NOT_SUPPORTED" for j in JUDGES) else "D"
                c[(r["grade"], s)] += 1
    cor = sum(v for k, v in c.items() if k[0] == "CORRECT")
    wro = sum(v for k, v in c.items() if k[0] == "INCORRECT")
    sup = c[("CORRECT", "S")] + c[("INCORRECT", "S")]
    print(f"| {m} | {cor} | {c[('CORRECT', 'S')]} | {c[('CORRECT', 'U')]} | {wro} | {c[('INCORRECT', 'U')]} "
          f"| {c['nf']} | {sup}/{cor + wro} ({100 * sup / max(cor + wro, 1):.1f}%) |")
