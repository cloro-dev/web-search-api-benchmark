"""Paired comparison of result files on the same questions (OPE-212 sensitivity runs).

Usage: sensitivity.py <run folder> [--extra <results folder>] <a:b> [<a:b> ...]

Each <a:b> compares results/<b>.jsonl with results/<a>.jsonl on the ids in
both files. A name is looked up in the run folder first, then in the --extra
folder (for example the published results). The test is the exact two-sided
McNemar test on the discordant pairs. A question with a search, reader or
grader error in either file is left out of that comparison.
"""
import json
import math
import os
import statistics
import sys


def load(name, folders):
    for f in folders:
        path = os.path.join(f, "results", f"{name}.jsonl") if os.path.isdir(os.path.join(f, "results")) else os.path.join(f, f"{name}.jsonl")
        if os.path.exists(path):
            return {r["id"]: r for r in map(json.loads, open(path))}  # the last line per id wins
    sys.exit(f"no results for {name} in {folders}")


def mcnemar_p(b, c):
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n)


def wilson(c, n, z=1.96):
    p = c / n
    d = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return centre - half, centre + half


ERR = ("ERROR", "LLM_ERROR")


def ok(r):
    return r.get("grade") == "CORRECT"


def main():
    args = sys.argv[1:]
    folders = [args.pop(0)]
    if args and args[0] == "--extra":
        args.pop(0)
        folders.append(args.pop(0))
    print("| Base | Variant | n | Base correct | Variant correct | Change | Only base correct | Only variant correct | McNemar p | Variant 95% interval | Mean context chars (base / variant) | Questions left out for errors (base / variant) |")
    print("|" + "---|" * 12)
    for pair in args:
        a, b = pair.split(":")
        ra, rb = load(a, folders), load(b, folders)
        both = set(ra) & set(rb)
        # A search, reader or grader failure says nothing about the variant, so those questions are left out.
        ids = sorted(i for i in both if ra[i].get("grade") not in ERR and rb[i].get("grade") not in ERR)
        ca = sum(ok(ra[i]) for i in ids)
        cb = sum(ok(rb[i]) for i in ids)
        only_a = sum(ok(ra[i]) and not ok(rb[i]) for i in ids)
        only_b = sum(ok(rb[i]) and not ok(ra[i]) for i in ids)
        lo, hi = wilson(cb, len(ids))
        ctx = [statistics.mean([r[i].get("context_chars") or 0 for i in ids]) for r in (ra, rb)]
        err = [sum(r[i].get("grade") in ERR for i in both) for r in (ra, rb)]
        n = len(ids)
        print(f"| {a} | {b} | {n} | {ca} ({ca / n:.1%}) | {cb} ({cb / n:.1%}) | {(cb - ca) / n * 100:+.1f} pts | {only_a} | {only_b} | {mcnemar_p(only_a, only_b):.3f} | {lo * 100:.1f}-{hi * 100:.1f} | {ctx[0]:,.0f} / {ctx[1]:,.0f} | {err[0]} / {err[1]} |")


if __name__ == "__main__":
    main()
