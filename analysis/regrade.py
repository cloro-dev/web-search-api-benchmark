"""Grade the saved answers of a run again with a different grader model.

Usage: regrade.py <run folder> <out folder> <grader model> [--workers 8] [--n N]
       regrade.py --summary <out folder>

Reads <run folder>/results/<provider>.jsonl and writes
<out folder>/results/<provider>.jsonl with the new grade in "grade" and the
first grade in "grade_first". The reader answers are not changed. A re-run
skips rows that already have a grade. Rows with no answer (search or reader
error) are copied with their grade.
"""
import concurrent.futures as cf
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import benchmark  # noqa: E402


def summary(out):
    """Agreement of the two graders and accuracy per provider under each grader."""
    grades = ("CORRECT", "INCORRECT", "NOT_ATTEMPTED")
    print("| Provider | n | Accuracy (first grader) | Accuracy (new grader) | Change | Same grade | Correct only with first | Correct only with new |")
    print("|---|---|---|---|---|---|---|---|")
    pairs = []
    for path in sorted(glob.glob(os.path.join(out, "results", "*.jsonl"))):
        rows = [r for r in {r["id"]: r for r in map(json.loads, open(path))}.values() if r["grade"] in grades and r["grade_first"] in grades]
        n = len(rows)
        a = sum(r["grade_first"] == "CORRECT" for r in rows)
        b = sum(r["grade"] == "CORRECT" for r in rows)
        same = sum(r["grade"] == r["grade_first"] for r in rows)
        only_a = sum(r["grade_first"] == "CORRECT" and r["grade"] != "CORRECT" for r in rows)
        only_b = sum(r["grade"] == "CORRECT" and r["grade_first"] != "CORRECT" for r in rows)
        pairs += [(r["grade_first"], r["grade"]) for r in rows]
        print(f"| {os.path.basename(path)[:-6]} | {n} | {a / n:.1%} | {b / n:.1%} | {(b - a) / n * 100:+.1f} pts | {same / n:.1%} | {only_a} | {only_b} |")
    n = len(pairs)
    po = sum(x == y for x, y in pairs) / n
    pe = sum((sum(x == g for x, _ in pairs) / n) * (sum(y == g for _, y in pairs) / n) for g in grades)
    print(f"\nAll answers: {n}, same grade {po:.1%}, Cohen's kappa {(po - pe) / (1 - pe):.3f}\n")
    print("| First grader \\ new grader | " + " | ".join(grades) + " |")
    print("|---|---|---|---|")
    for g in grades:
        print(f"| {g} | " + " | ".join(str(sum(x == g and y == h for x, y in pairs)) for h in grades) + " |")


def main():
    args = sys.argv[1:]
    if args[0] == "--summary":
        return summary(args[1])
    run, out, model = args[0], args[1], args[2]
    workers = int(args[args.index("--workers") + 1]) if "--workers" in args else 8
    n = int(args[args.index("--n") + 1]) if "--n" in args else None
    benchmark.GRADER_MODEL = model
    os.makedirs(os.path.join(out, "results"), exist_ok=True)
    for path in sorted(glob.glob(os.path.join(run, "results", "*.jsonl"))):
        rows = list({r["id"]: r for r in map(json.loads, open(path))}.values())[:n]
        dest = os.path.join(out, "results", os.path.basename(path))
        done = {r["id"] for r in map(json.loads, open(dest)) if r["grade"] != "LLM_ERROR"} if os.path.exists(dest) else set()
        todo = [r for r in rows if r["id"] not in done]

        def regrade(r):
            r = {**r, "grade_first": r.get("grade")}
            if r.get("answer") is None:
                return r
            try:
                r["grade"] = benchmark.grade(r["problem"], r["gold"], r["answer"])
            except Exception as e:
                r.update(grade="LLM_ERROR", error=repr(e))
            return r

        with open(dest, "a") as f, cf.ThreadPoolExecutor(workers) as ex:
            for r in ex.map(regrade, todo):
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(f"{os.path.basename(path)}: {len(todo)} graded", file=sys.stderr)


if __name__ == "__main__":
    main()
