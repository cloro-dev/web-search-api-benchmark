# Keenable Search API, added on 2026-11-20

Run: 2026-11-20, `benchmark.py --providers keenable` and
`--providers keenable-nodata`, seed 42, `--workers 4`. The questions, the
reader (`gpt-5.6-luna`), the reader prompt and the `--as-of` dates (FRAMES
2026-11-10, FreshQA 2026-11-05) are the same as for the other nine APIs.
Gemini (`gemini-pro-latest`) graded every answer. The results are next to the
other APIs' results in `runs/<dataset>-2026-11/results/keenable.jsonl` and
`keenable-nodata.jsonl`.

- **Request:** `POST https://api.keenable.ai/v1/search` with `query` (the
  question text, unchanged) and `max_results=10`. No other parameters: the
  default mode (`pro`), no date or site filter, the default snippet length.
- **Reader input:** the title, URL and `snippet` of each result. The
  `description` field is deprecated and always empty, so the reader does not
  get it.
- **`keenable-nodata`:** the same request with
  `exclude_domains: ["huggingface.co", "kaggle.com"]`, the two hosts of the
  dataset copies. This is the filter of the
  [Perplexity rerun](../perplexity-rerun-2026-11/report.md).

**This run is not interleaved with the first six APIs.** It ran 10 to 16 days
after them. SimpleQA Verified and FRAMES have fixed answers, so the gap
matters little for them. On FreshQA, some answers can change in two weeks.

## Result

The published score is the `keenable-nodata` run, as for Perplexity.

| Dataset | Questions | Keenable, filtered | 95% interval | Not attempted | Keenable, no filter | 95% interval |
|---|---|---|---|---|---|---|
| SimpleQA Verified | 1,000 | 97.2% | 96.0-98.1 | 3 | 97.7% | 96.6-98.5 |
| FreshQA | 358 | 83.2% | 79.0-86.8 | 17 | 83.5% | 79.3-87.0 |
| FRAMES | 824 | 56.9% | 53.5-60.3 | 217 | 66.4% | 63.1-69.5 |

On SimpleQA Verified, Keenable is within the margin of error of Parallel
(97.8%), Perplexity (97.5%), Exa (97.3%) and cloro (97.1%). On FreshQA it
scored between Perplexity (84.1%) and Exa (82.7%). On FRAMES it scored
between Perplexity (62.9%) and Brave (53.9%).

The filter changed the FRAMES score by 9.5 points: the run without it
answered 111 questions correctly that the filtered run did not, and the
filtered run 33 that the other did not (p < 0.0001). On SimpleQA Verified
(9 to 4, p = 0.27) and FreshQA (11 to 10, p = 1.0) the difference is not
significant.

## Why the published score uses the filter

Without the filter, the Keenable results held a Hugging Face page of a
benchmark dataset, with the question and the answer, on 206 of 824 FRAMES
questions. The most frequent page was `huggingface.co/datasets/google/frames-benchmark`
(187 questions), often as the first result. On those 206 questions Keenable
scored 88.3% (182/206), and on the other 618 questions 59.1% (365/618). On
SimpleQA Verified it returned such a page on 101 of 1,000 questions (100/101
correct, against 97.6% on the others). On FreshQA it returned none.

You.com, the API added before Keenable, returned a dataset page on 99 FRAMES
questions and scored lower on them than on the others (46.5% against 51.9%).
For Keenable the dataset page raised the score, so the published score uses
the filter, as for Perplexity.

## Leak check

The patterns of the earlier reports: `simpleqa`, `simple-evals`,
`simple_qa`, `frames-benchmark`, `google/frames`, `framesbenchmark`,
`freshqa`, `huggingface.co/datasets` and `kaggle.com` in the raw response.

| Dataset | Flagged, no filter | Flagged, filtered | Accuracy on flagged, filtered | Accuracy without flagged, filtered | Most frequent hosts, filtered |
|---|---|---|---|---|---|
| SimpleQA Verified | 101 of 1,000 | 12 of 1,000 | 11/12 | 961/988, 97.3% | `d6108366.hf-mirror.com`, `hf.hahadalin.eu.org`, `hf-proxy-2dh.pages.dev` |
| FreshQA | 0 of 358 | 0 of 358 | - | 298/358, 83.2% | - |
| FRAMES | 206 of 824 | 46 of 824 | 44/46 | 425/778, 54.6% | `hf-proxy-2dh.pages.dev`, `d6108366.hf-mirror.com`, `cdn-avatars.qwak.ai` |

The filter does not remove the Hugging Face mirrors. They are on 46 FRAMES
questions, and Keenable answered 44 of them correctly. Without those 46
questions, the filtered FRAMES score is 54.6%. The Perplexity filtered run
had 52 flagged SimpleQA Verified questions and 1 flagged FRAMES question.

## Paired tests

Exact McNemar tests on the same questions, filtered run. "x to y" means
Keenable answered x questions correctly that the other API did not, and the
other API answered y that Keenable did not.

| Keenable against | SimpleQA Verified (1,000) | FreshQA (358) | FRAMES (824) |
|---|---|---|---|
| cloro | 19 to 18 (p = 1.0) | 11 to 28 (p = 0.0095) | 49 to 241 (p < 0.0001) |
| SerpApi | 38 to 16 (p = 0.0038) | 11 to 29 (p = 0.0064) | 59 to 234 (p < 0.0001) |
| Parallel | 10 to 16 (p = 0.33) | 21 to 17 (p = 0.63) | 79 to 151 (p < 0.0001) |
| Exa | 10 to 11 (p = 1.0) | 17 to 15 (p = 0.86) | 90 to 147 (p = 0.0003) |
| Perplexity\* | 9 to 12 (p = 0.66) | 16 to 19 (p = 0.74) | 90 to 139 (p = 0.0015) |
| Brave | 55 to 13 (p < 0.0001) | 16 to 21 (p = 0.51) | 131 to 106 (p = 0.12) |
| You.com | 58 to 16 (p < 0.0001) | 14 to 19 (p = 0.49) | 147 to 100 (p = 0.0033) |
| Tavily | 70 to 15 (p < 0.0001) | 26 to 19 (p = 0.37) | 174 to 102 (p < 0.0001) |
| Firecrawl | 67 to 12 (p < 0.0001) | 35 to 23 (p = 0.15) | 196 to 85 (p < 0.0001) |

\* The Perplexity run with huggingface.co and kaggle.com excluded.

## Latency

p50 search latency on SimpleQA Verified: 0.27 s (p90 0.38 s), the lowest of
the ten APIs. Perplexity took 0.34 s. This number comes from a
`--search-only` run of 1,000 questions, 4 requests at a time, with no other
benchmark running. The unfiltered request gave the same p50 (0.27 s, p90
0.36 s). In the graded runs the p50 was 0.27 s on SimpleQA Verified and
FreshQA, and 0.37 s on FRAMES.

The first pass of the unfiltered run had 18 rows with a local DNS error
(`gaierror`) on this machine, not an API error: 4 searches and 14 reader
calls. The filtered run had 8. They ran again, and every question has a
graded answer.

## Cost

Keenable gives every organization 100,000 free requests a month. The
allowance resets each month, and no card is needed for it (a signup from a
disposable or privacy mail domain gets 1,000 until a card is saved). Past the
allowance, pay as you go costs $4 per 1,000 requests, in the `pro` and the
`realtime` mode. "Dedicated capacity" is $1 per 1,000 requests at 100 or more
requests a second. Sources: [keenable.ai/pricing](https://keenable.ai/pricing)
and [docs.keenable.ai/credits.md](https://docs.keenable.ai/credits.md), read on
2026-11-20.

The README lists $4.00 per 1,000 searches, the price past the free
allowance. At 100,000 searches a month Keenable costs nothing. At 200,000 a
month it costs $400, $2.00 per 1,000 on average.

The runs used 4,364 searches plus about 20 test searches, all from the free
allowance. Reader: `gpt-5.6-luna`, 4,364 calls. Grader: `gemini-pro-latest`,
4,364 calls.

## Commands

```bash
export READER_MODEL=gpt-5.6-luna GRADER_MODEL=gemini-pro-latest
for p in keenable keenable-nodata; do
  python3 benchmark.py --providers $p --dataset simpleqa --out runs/simpleqa-2026-11
  python3 benchmark.py --providers $p --dataset freshqa --as-of 2026-11-05 --out runs/freshqa-2026-11
  python3 benchmark.py --providers $p --dataset frames --as-of 2026-11-10 --out runs/frames-2026-11
done
python3 benchmark.py --providers keenable,keenable-nodata --dataset simpleqa --search-only --out <scratch folder>
```
