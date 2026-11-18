# Perplexity Search API rerun with a domain filter (2026-11-18)

Run: 2026-11-18, `benchmark.py --providers perplexity-nodata`, seed 42,
`--workers 4`, on all three datasets. `--as-of`: FRAMES 2026-11-10, FreshQA
2026-11-05, the dates of the six-API runs. The results are in
`runs/<dataset>-2026-11/results/perplexity-nodata.jsonl`.

## Why it ran again

In the first run ([report](../perplexity-firecrawl-2026-11/report.md)),
Perplexity's results held a Hugging Face page of the benchmark dataset, with
the question and the answer, on 500 SimpleQA Verified and 411 FRAMES
questions. Its scores were then given on the other questions only, so they
were on fewer questions than the scores of the other APIs.

## What changed

- **Domain filter.** `search_domain_filter: ["-huggingface.co", "-kaggle.com"]`
  on every request, the two hosts of the dataset copies. The other APIs ran
  without a filter.
- **Grader.** `gemini-pro-latest` through the Gemini OpenAI-compatible
  endpoint (`GRADER_MODEL=gemini-pro-latest`). The other APIs were graded by
  `gpt-5.6-sol`. The grader prompt is the same.
- **Reader, questions, number of results:** the same as for the other APIs.

## Result

| Dataset | Questions | Accuracy (95% interval) | Not attempted | p50 search latency |
|---|---|---|---|---|
| SimpleQA Verified | 1,000 | 97.5% (96.3-98.3) | 2 | 0.35 s |
| FreshQA | 358 | 84.1% (79.9-87.5) | 13 | 0.36 s |
| FRAMES | 824 | 62.9% (59.5-66.1) | 152 | 0.37 s |

The scores are within 0.7 points of the first run's scores on the questions
without a dataset page (96.8%, 84.5%, 62.7%).

## Leak check

The same patterns as the earlier reports. Flagged questions after the filter:
SimpleQA Verified 52 of 1,000 (most frequent hosts: cdn-avatars.qwak.ai,
fossies.org, hf-mirror.com, huggingface.co URLs inside page text,
anyeval.com), FreshQA 2 of 358 (github.com), FRAMES 1 of 824. The six earlier
providers had 23 to 117 flagged SimpleQA Verified questions each.

## Paired tests

Exact McNemar tests on the same questions. "A, x to y": A answered x questions
correctly that Perplexity did not, and Perplexity answered y that A did not.

| Comparison | SimpleQA Verified | FreshQA | FRAMES |
|---|---|---|---|
| cloro vs Perplexity | 13 to 19 (p = 0.38) | 24 to 9 (p = 0.014) | 199 to 56 (p < 0.0001) |
| SerpApi vs Perplexity | 11 to 39 (p < 0.0001) | 25 to 9 (p = 0.009) | 187 to 67 (p < 0.0001) |
| Parallel vs Perplexity | 14 to 11 (p = 0.69) | 12 to 17 (p = 0.46) | 122 to 102 (p = 0.20) |
| Exa vs Perplexity | 11 to 13 (p = 0.84) | 15 to 19 (p = 0.61) | 102 to 93 (p = 0.57) |
| Brave vs Perplexity | 10 to 54 (p < 0.0001) | 19 to 16 (p = 0.74) | 67 to 141 (p < 0.0001) |
| Tavily vs Perplexity | 13 to 70 (p < 0.0001) | 17 to 25 (p = 0.28) | 78 to 197 (p < 0.0001) |
| Firecrawl vs Perplexity | not run | not run | 58 to 218 (p < 0.0001) |

The two sides of each test have different graders, so a small difference can
come from the grader.

## Cost

Perplexity: 2,182 searches plus 8 test searches at $5 per 1,000, about $11.
Reader: `gpt-5.6-luna`, 2,182 calls. Grader: `gemini-pro-latest`, 2,182 calls.
