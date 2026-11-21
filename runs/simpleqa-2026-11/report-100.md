# SimpleQA Verified, 100 questions, 6 search APIs

> **Earlier reader.** The scores in this report come from the earlier reader,
> `gpt-5.6-luna`, with the earlier reader prompt. The published scores use
> `gemini-3.8-flash` with a prompt that allows only the search results: see the
> [rerun report](../rerun-2026-11/report.md) and the
> [reader test](../reader-test-2026-11/report.md). The search responses, the
> latencies and the counts that do not depend on the reader stay valid.

Run: 2026-11-04, `benchmark.py`, seed 42, first 100
questions, `--workers 4`, from one laptop in one time window. Reader
`gpt-5.6-luna`, grader `gpt-5.6-sol`. One search per question.

## Result

cloro is not slower than SerpApi by much, but it is the slowest provider in
the table. Its accuracy is in the top group, together with Exa and Parallel.
At 100 questions, the top four accuracy scores are not different by more than
the noise.

| Provider | Accuracy | 95% interval | Latency p50 | p90 | p99 | Reader tokens per question |
|---|---|---|---|---|---|---|
| Exa | 100% | 96.3-100 | 0.87 s | 2.39 s | 6.33 s | 2,991 |
| cloro | 99% | 94.6-99.8 | 11.80 s | 39.76 s | 113.02 s | 843 |
| Parallel | 98% | 93.0-99.4 | 3.11 s | 4.09 s | 5.53 s | 2,934 |
| SerpApi | 96% | 90.2-98.4 | 9.06 s | 31.68 s | 93.13 s | 803 |
| Brave | 94% | 87.5-97.2 | 1.20 s | 1.37 s | 2.31 s | 3,436 |
| Tavily | 91% | 83.8-95.2 | 2.26 s | 3.12 s | 6.75 s | 3,022 |

Search errors: 0 for every provider. No provider ran out of credits.

## Notes

- **cloro's one miss** (id 2313): the answer "Over 1,200" for a gold range of
  1,199 to 1,226. The grader marked it NOT_ATTEMPTED.
- **Latency comes from the AI Overview.** cloro and SerpApi wait for Google's
  AI Overview. SerpApi needed a second request for it on 95 of 100 questions.
  The latency includes that second request. In the earlier 5-question test,
  cloro without the AI Overview took about 3 to 4.5 s.
- **cloro's tail is the worst**: p99 113 s. The mean is 20.99 s, against
  14.43 s for SerpApi.
- **Google results are short.** The reader needed about 800 tokens per
  question from cloro or SerpApi, against about 3,000 from the others. That is
  a smaller LLM bill per answer.
- **Possible leaks.** 15 of 100 questions have at least one raw response that
  names SimpleQA, simple-evals, a Hugging Face dataset or a Kaggle benchmark.
  This is a text match, not a review. Without those 15, the order does not
  change: Exa 85/85, cloro 84/85, Parallel 84/85, SerpApi 83/85, Brave 81/85,
  Tavily 76/85.

## cloro without the AI Overview

Provider `cloro-noaio`: the same 100 questions, the same reader and grader.
The request has no `include`, so cloro does not wait for the AI Overview, and
the response has only organic results, People Also Ask and related searches.
This run was alone and later in the day, not interleaved with the other
providers, so its latency is less comparable than the rows above.

| Provider | Accuracy | 95% interval | Latency p50 | p90 | p99 | Reader tokens per question |
|---|---|---|---|---|---|---|
| cloro (with AI Overview) | 99% | 94.6-99.8 | 11.80 s | 39.76 s | 113.02 s | 843 |
| cloro-noaio | 89% | 81.4-93.7 | 3.56 s | 6.64 s | 25.61 s | 743 |

- 89 correct, 7 incorrect, 4 not attempted. All 11 misses were correct in the
  run with the AI Overview.
- Without the AI Overview, cloro is the least accurate row in the table
  (Tavily 91%, Brave 94%). It is also slower than Exa, Brave, Tavily and
  Parallel at p50 and p90.
- Thus the AI Overview is where Google's accuracy comes from on SimpleQA. The
  trade is about 10 points of accuracy for about 8 s at p50.
- Cost: 100 calls, about 500 credits (3 base, 2 sync surcharge; estimated).

## Cost of this run

| API | Calls | Cost |
|---|---|---|
| cloro | 100 Google calls with AI Overview, sync | about 700 credits (3 base, 2 AI Overview, 2 sync surcharge per call; the REST response has no credits field, so this is not measured) |
| SerpApi | 195 searches (100 plus 95 AI Overview requests) | SerpApi account dashboard |
| Tavily | 100 basic searches | 100 of 1,000 free monthly credits |
| Exa | 100 | $0.70 (sum of `costDollars`) |
| Parallel | 100 | Not found in the response; check the dashboard |
| Brave | 100 | Not found |
| OpenAI | 600 reader + 600 grader calls | 1,402,896 reader prompt tokens; grader tokens not recorded |

## Before you publish

- Run all 1,000 questions. At 100, the top four are inside each other's intervals.
- Review the 15 flagged questions by hand.
- Decide on latency. The row without the AI Overview (89%) does not help
  the accuracy story. Show the trade-off, or show accuracy only.
