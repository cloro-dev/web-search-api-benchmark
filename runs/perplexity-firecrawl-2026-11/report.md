# Perplexity Search API and Firecrawl, added on 2026-11-18

> **Earlier reader.** The scores in this report come from the earlier reader,
> `gpt-5.6-luna`, with the earlier reader prompt. The published scores use
> `gemini-3.8-flash` with a prompt that allows only the search results: see the
> [rerun report](../rerun-2026-11/report.md) and the
> [reader test](../reader-test-2026-11/report.md). The search responses, the
> latencies and the counts that do not depend on the reader stay valid.

> On 2026-11-18 Gemini (`gemini-pro-latest`) graded every answer again. The
> grades in `results/` are the Gemini grades, and the numbers below are the
> first grades. See the [regrade report](../regrade-gemini-2026-11/report.md).

Run: 2026-11-18, `benchmark.py --providers perplexity,firecrawl`, seed 42,
`--workers 4` (Firecrawl `--workers 1` after its rate limit). The questions,
the reader (`gpt-5.6-luna`), the grader (`gpt-5.6-sol`) and the reader prompt
are the same as in the six-API runs. `--as-of` is the date of each earlier
run: FRAMES 2026-11-10, FreshQA 2026-11-05. The results are next to the other
providers' results in `runs/<dataset>-2026-11/results/`.

- **Perplexity:** `POST https://api.perplexity.ai/search`, `max_results=10`,
  the default search type. All three datasets.
- **Firecrawl:** `POST https://api.firecrawl.dev/v2/search`, `limit=10`, no
  page scraping (the default). FRAMES only: the key's credits covered one
  dataset.

**This run is not interleaved with the six-API runs.** It ran 8 to 14 days
after them. SimpleQA Verified and FRAMES have fixed answers, so the gap
matters little for them. On FreshQA, some answers can change in two weeks.

## Result

Perplexity's raw score is inflated by leaked answers. Its Search API returned a
Hugging Face page of the benchmark dataset itself, with the question and the
gold answer, on 500 of 1,000 SimpleQA Verified questions and 411 of 824 FRAMES
questions. On those questions Perplexity scored 99.8% and 98.1%. On the
questions without a leak:

| Dataset | Questions | Perplexity | cloro | Parallel | Exa | SerpApi | Brave | Tavily | Firecrawl |
|---|---|---|---|---|---|---|---|---|---|
| SimpleQA Verified | 500 | 96.8% (94.9-98.0) | 96.4% | 97.2% | 96.6% | 94.0% | 94.0% | 91.2% | - |
| FreshQA | 355 | 84.5% (80.4-87.9) | 88.2% | 82.5% | 82.8% | 88.5% | 84.8% | 81.7% | - |
| FRAMES | 410 | 62.7% (57.9-67.2) | 77.3% | 63.9% | 66.1% | 75.4% | 54.6% | 48.8% | 45.4% |

On all questions, with the leaks:

| Dataset | Perplexity | Firecrawl |
|---|---|---|
| SimpleQA Verified (1,000) | 98.3% (97.3-98.9) | not run |
| FreshQA (358) | 84.6% (80.5-88.0) | not run |
| FRAMES (824) | 80.5% (77.6-83.0) | 43.4% (40.1-46.9) |

Firecrawl answered "not found" on 326 of 824 FRAMES questions. Perplexity
answered "not found" on 75 of the 410 FRAMES questions without a leak.

## Paired tests

Exact McNemar tests. "A, x to y" means A answered x questions correctly that
B did not, and B answered y that A did not.

| Comparison | SimpleQA, 500 without a leak | FreshQA, 355 | FRAMES, 410 without a leak |
|---|---|---|---|
| cloro vs Perplexity | 8 to 10 (p = 0.81) | 28 to 15 (p = 0.066) | 92 to 32 (p < 0.0001) |
| Parallel vs Perplexity | 8 to 6 (p = 0.79) | 16 to 23 (p = 0.34) | 58 to 53 (p = 0.70) |
| Exa vs Perplexity | 7 to 8 (p = 1.0) | 18 to 24 (p = 0.44) | 56 to 42 (p = 0.19) |
| SerpApi vs Perplexity | 7 to 21 (p = 0.013) | 27 to 13 (p = 0.038) | 85 to 33 (p < 0.0001) |
| Brave vs Perplexity | 6 to 20 (p = 0.0094) | 17 to 16 (p = 1.0) | 37 to 70 (p = 0.0018) |
| Tavily vs Perplexity | 7 to 35 (p < 0.0001) | 19 to 29 (p = 0.19) | 35 to 92 (p < 0.0001) |

Firecrawl on all 824 FRAMES questions: cloro 321 to 18 (p < 0.0001), Brave
158 to 72 (p < 0.0001), Tavily 136 to 95 (p = 0.0084).

## Leak check

A question is flagged when the Perplexity or Firecrawl raw response contains
`simpleqa`, `simple-evals`, `simple_qa`, `frames-benchmark`, `google/frames`,
`framesbenchmark`, `freshqa`, `huggingface.co/datasets` or `kaggle.com`, the
patterns of the earlier reports.

| Dataset | Flagged | Most frequent flagged URLs |
|---|---|---|
| SimpleQA Verified | 500 of 1,000 | `huggingface.co/datasets/SALT-NLP/simpleqa-verified/viewer/...` and copies of it |
| FreshQA | 3 of 358 | - |
| FRAMES | 414 of 824 (411 by Perplexity, 23 by Firecrawl, some by both) | `huggingface.co/datasets/google/frames-benchmark/blob/main/test.tsv`, `huggingface.co/datasets/gviviano/frames-benchmark-predictions` |

Firecrawl's own responses flagged 23 FRAMES questions.

The six earlier providers had 23 to 117 flagged questions each on SimpleQA
Verified, and the order did not change without them. For Perplexity the leak
changes the FRAMES result from a tie with cloro to fourth place.

## Latency and context

| Provider | p50 search latency | Median reader prompt tokens |
|---|---|---|
| Perplexity | 0.34 s (SimpleQA), 0.34 s (FreshQA), 0.37 s (FRAMES) | 3,278 to 4,153 |
| Firecrawl | 3.62 s (FRAMES, one worker) | 1,083 |

Perplexity's results carry long page passages, about four times the reader
tokens of cloro.

## Price at 100,000 searches a month

List prices read on November 18, 2026.

| Search API | $ per 1,000 searches | Plan |
|---|---|---|
| Perplexity | $5.00 | Search API, $5 per 1,000 requests; no free tier found |
| Firecrawl | $3.49 | Standard, $99 a month for 100,000 credits, plus 100,000 extra credits at $5 per 2,000; a search costs 2 credits per 10 results. Billed yearly: $3.33 |

Sources: [docs.perplexity.ai/getting-started/pricing](https://docs.perplexity.ai/getting-started/pricing),
[firecrawl.dev/pricing](https://www.firecrawl.dev/pricing).

## Run cost

| Provider | Requests |
|---|---|
| Perplexity | about 2,190 billed searches, about $11 |
| Firecrawl | about 1,650 credits; HTTP 429 responses were not billed |

About 6,000 OpenAI calls (reader and grader).
