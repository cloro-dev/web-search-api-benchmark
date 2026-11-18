# One grader for every API, and Firecrawl on all three datasets (2026-11-18)

Two changes, made on 2026-11-18:

1. **Gemini grades every answer.** Before this, one model graded the first
   six APIs and Firecrawl's FRAMES run, and Gemini graded the Perplexity
   rerun. Gemini (`gemini-pro-latest`) now grades the saved answers of all
   eight APIs with the same grader prompt
   ([`grader_template.txt`](../../grader_template.txt)). No search ran again
   and the reader answers did not change. The first grade of each answer is
   kept in the `grade_first` field of `runs/<dataset>-2026-11/results/`.
2. **Firecrawl ran SimpleQA Verified and FreshQA.** Its first run covered
   FRAMES only. The new runs use the same questions, request, reader and
   `--as-of` dates as the other APIs, and Gemini as the grader.

Command for the regrade (one line per dataset):

```bash
python3 analysis/regrade.py <run folder with the results to grade> <out folder> gemini-pro-latest --workers 6
python3 analysis/regrade.py --summary <out folder>
```

## Grader agreement

| Dataset | Answers | Same grade | Cohen's kappa |
|---|---|---|---|
| SimpleQA Verified | 6,000 | 99.7% | 0.969 |
| FreshQA | 2,148 | 98.9% | 0.960 |
| FRAMES | 5,760 | 99.0% | 0.981 |

FRAMES has 5,760 answers, not 5,768: 8 Brave searches failed and have no
answer. Perplexity and Firecrawl's FreshQA answers had Gemini grades already
and are not in this table.

Change in accuracy per API (first grade to Gemini grade):

| API | SimpleQA Verified | FreshQA | FRAMES |
|---|---|---|---|
| cloro | 96.9% to 97.1% | 88.3% to 88.0% | 80.2% to 80.2% |
| SerpApi | 94.7% to 95.0% | 88.5% to 88.3% | 77.4% to 78.2% |
| Parallel | 97.8% to 97.8% | 82.7% to 82.1% | 65.3% to 65.7% |
| Exa | 97.3% to 97.3% | 83.0% to 82.7% | 64.0% to 63.8% |
| Brave | 93.1% to 93.0% | 84.9% to 84.6% | 53.9% to 53.9% |
| Tavily | 91.8% to 91.7% | 81.8% to 81.3% | 48.4% to 48.2% |
| Firecrawl | new: 91.7% | new: 79.9% | 43.4% to 43.4% |

No score moved by 1 point or more. One paired test changed its result:
on FRAMES, cloro against SerpApi was 58 wins to 35 (p = 0.022) with the
first grades and is 53 to 36 (p = 0.089) with the Gemini grades. cloro still
has the higher score (80.2% against 78.2%), but the difference is no longer
significant. Every other test in the README keeps its result.

## Firecrawl on SimpleQA Verified and FreshQA

`benchmark.py --providers firecrawl`, `/v2/search`, `limit=10`, no page
scraping, 1 request at a time (Firecrawl returned HTTP 429 at 4). FreshQA
with `--as-of 2026-11-05`.

| Dataset | Correct | Accuracy (95% interval) | Not attempted | p50 latency |
|---|---|---|---|---|
| SimpleQA Verified | 917/1,000 | 91.7% (89.8-93.3) | 31 | 0.93 s |
| FreshQA | 286/358 | 79.9% (75.4-83.7) | 30 | 3.61 s |

8 SimpleQA questions failed on a DNS error of the machine and ran again.

Paired tests, Firecrawl against each API ("wins" for the other API first):

| API | SimpleQA Verified | FreshQA |
|---|---|---|
| cloro | 68 to 14 (p < 0.0001) | 41 to 12 (p = 0.0001) |
| SerpApi | 69 to 36 (p = 0.0017) | 40 to 10 (p < 0.0001) |
| Parallel | 71 to 10 (p < 0.0001) | 33 to 25 (p = 0.36) |
| Exa | 69 to 13 (p < 0.0001) | 31 to 21 (p = 0.21) |
| Perplexity | 70 to 12 (p < 0.0001) | 35 to 20 (p = 0.058) |
| Brave | 61 to 48 (p = 0.25) | 30 to 13 (p = 0.014) |
| Tavily | 53 to 53 (p = 1.0) | 26 to 21 (p = 0.56) |

### Leak check

On SimpleQA Verified, 81 of Firecrawl's 1,000 responses contain a page of a
benchmark dataset (all on huggingface.co). On 71 of them the result text
holds the gold answer. Firecrawl answered 79 of the 81 correctly, and 838 of
the other 919 (91.2%). On FreshQA no response matched.

The other APIs return such pages too. On SimpleQA Verified the first six were
flagged on 23 to 117 questions each
([SimpleQA report](../simpleqa-2026-11/report.md)), and cloro's results held
the gold answer on 45 of its 78 flagged questions. Perplexity, without a
filter, was flagged on 500 questions and held the answer on 471. Perplexity
runs with huggingface.co and kaggle.com excluded for this reason. Firecrawl
is in the range of the first six and runs without the filter, as they do.

## Run cost

| Item | Amount |
|---|---|
| Firecrawl | about 2,750 credits (1,358 searches and 24 searches of a stopped run) |
| Reader calls | about 1,400 (Firecrawl answers) |
| Gemini grader calls | about 15,300 (13,908 regrades, 1,358 Firecrawl answers, retries) |
