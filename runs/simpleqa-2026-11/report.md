# SimpleQA Verified, 1,000 questions, 6 search APIs

> On 2026-11-18 Gemini (`gemini-pro-latest`) graded every answer again. The
> grades in `results/` are the Gemini grades, and the numbers below are the
> first grades. See the [regrade report](../regrade-gemini-2026-11/report.md).

Run: 2026-11-04 to 2026-11-05, `benchmark.py`, seed 42,
all 1,000 questions, `--workers 4`, from one laptop. Reader `gpt-5.6-luna`,
grader `gpt-5.6-sol`. One search per question. The calls are interleaved
across the 6 providers.

The run had four parts. The first 100 questions ran on 2026-11-04 from 20:05
to 20:31 CET (the 100-question run, `report-100.md`). Questions 101 to 696 ran
from 22:49 to 01:09 CET. At 01:10 Brave hit its monthly spend cap (HTTP 402)
and the run stopped. The cap was raised, and the run continued on 2026-11-05
from 07:18 to 08:25 CET. The resumed part ran the last 304 questions on all 6
providers and ran again the 2 Brave rows that had the 402 error.

All numbers below come from `results/*.jsonl` and the raw responses (not
in this repo, 171 MB), with the last row for each question id. The latency
split by period used the write time of each raw file.

## Result

cloro is not the most accurate provider, and it is the slowest. cloro is
third on accuracy (96.9%), behind Parallel (97.8%) and Exa (97.3%). The
difference is not significant: the intervals overlap, and a paired test on
the same questions gives p = 0.15 against Parallel and p = 0.63 against Exa.
cloro has the highest latency at p50, p90 and p99. Its p50 is 12.29 s,
against 7.62 s for SerpApi, the other Google provider, and under 3 s for the
other four.

cloro is more accurate than SerpApi (96.9% against 94.7%). On the same
questions, cloro was correct on 33 questions that SerpApi missed, and SerpApi
was correct on 11 that cloro missed (paired test p = 0.0013). cloro is also
more accurate than Brave and Tavily (p < 0.0001 for both).

| Provider | Accuracy | 95% interval | Latency p50 | p90 | p99 | Reader tokens per question |
|---|---|---|---|---|---|---|
| Parallel | 97.8% | 96.7-98.5 | 2.84 s | 3.92 s | 4.45 s | 2,966 |
| Exa | 97.3% | 96.1-98.1 | 0.72 s | 2.40 s | 4.45 s | 3,300 |
| cloro | 96.9% | 95.6-97.8 | 12.29 s | 40.12 s | 101.50 s | 836 |
| SerpApi | 94.7% | 93.1-95.9 | 7.62 s | 20.78 s | 77.89 s | 816 |
| Brave | 93.1% | 91.4-94.5 | 1.21 s | 1.39 s | 1.66 s | 3,272 |
| Tavily | 91.8% | 89.9-93.3 | 1.92 s | 3.08 s | 5.05 s | 3,239 |

The interval is the 95% Wilson interval. The latency in this table includes
all four parts of the run, with and without the other runs in parallel. See
"Latency under load" for the split.

| Provider | Correct | Incorrect | Not attempted | Accuracy given attempted | AI Overview present | Mean latency |
|---|---|---|---|---|---|---|
| Parallel | 978 | 20 | 2 | 98.0% | - | 2.96 s |
| Exa | 973 | 23 | 4 | 97.7% | - | 1.26 s |
| cloro | 969 | 29 | 2 | 97.1% | 986 | 21.06 s |
| SerpApi | 947 | 44 | 9 | 95.6% | 983 | 11.47 s |
| Brave | 931 | 50 | 19 | 94.9% | - | 1.22 s |
| Tavily | 918 | 44 | 38 | 95.4% | - | 1.96 s |

### Paired comparison with cloro

The same 1,000 questions went to each provider, so a paired test (exact
McNemar) is more sensitive than the overlap of the intervals.

| Provider | cloro correct, provider wrong | Provider correct, cloro wrong | p |
|---|---|---|---|
| Parallel | 11 | 20 | 0.15 |
| Exa | 17 | 21 | 0.63 |
| SerpApi | 33 | 11 | 0.0013 |
| Brave | 50 | 12 | < 0.0001 |
| Tavily | 70 | 19 | < 0.0001 |

The Wilson intervals do not overlap for these pairs: cloro and Tavily, cloro
and Brave, SerpApi and Exa, SerpApi and Parallel, Tavily and Exa, Tavily and
Parallel, Exa and Brave, Parallel and Brave. cloro and SerpApi overlap by
0.3 points (95.6 against 95.9), but the paired test separates them.

## Search errors

| Provider | Search errors in the final rows | Failed rows during the run | HTTP retries that then succeeded |
|---|---|---|---|
| cloro | 0 | 0 | 6 |
| SerpApi | 0 | 0 | 25 |
| Tavily | 0 | 0 | 0 |
| Exa | 0 | 0 | 0 |
| Parallel | 0 | 0 | 0 |
| Brave | 0 | 2 (ids 2914, 2939, HTTP 402 at 01:09) | 0 |

The 2 Brave rows ran again in the resumed part and got a search result. All 6
providers have 1,000 graded rows. No row has the grade ERROR or LLM_ERROR.
The Brave results file still contains the 2 old error rows. The summary uses
the last row for each id, so it ignores them.

## Possible leaks

193 of 1,000 questions have at least one raw response that contains
`simpleqa`, `simple-evals`, `simple_qa`, `huggingface.co/datasets` or
`kaggle.com`. This is a text match, not a review. Questions flagged by each
provider's own response: Brave 117, Parallel 87, cloro 79, SerpApi 46, Exa
37, Tavily 23.

With the 193 questions removed, the order does not change:

| Provider | Correct | Accuracy | 95% interval |
|---|---|---|---|
| Parallel | 787/807 | 97.5% | 96.2-98.4 |
| Exa | 784/807 | 97.1% | 95.8-98.1 |
| cloro | 780/807 | 96.7% | 95.2-97.7 |
| SerpApi | 764/807 | 94.7% | 92.9-96.0 |
| Brave | 756/807 | 93.7% | 91.8-95.2 |
| Tavily | 745/807 | 92.3% | 90.3-94.0 |

## Possible stale gold answers

On 11 questions, 4 or more of the 6 providers are INCORRECT. None of the 11
is in the leak list. cloro is INCORRECT on all 11. These are 11 of cloro's 29
incorrect answers. Review them by hand before you publish. Some are not stale
gold: on id 1740 the answers contain the gold name plus a second name, and
the grader marked them incorrect.

| Id | Question | Gold | Most common wrong answer | Providers wrong |
|---|---|---|---|---|
| 2279 | What day, month, and year did Panama decide to use DVB-T? | May 19, 2009 | 12 May 2009 (6) | 6 |
| 1239 | Who was the 18th Chief Minister of Karnataka? | H. D. Kumaraswamy | D. K. Shivakumar (6, one written "D.K. Shivakumar") | 6 |
| 2821 | What day, month, and year did Carrie Underwood reveal the track listing for her album "Storyteller"? | September 10, 2015 | September 9, 2015 (6, two date formats) | 6 |
| 1717 | How many people were killed when a tractor-trolley returning from a temple fell into a pond in Kanpur on October 2, 2022? | 27 | 26 people (5; cloro "26-27 people") | 6 |
| 744 | What is the maximum depth of the Mediterranean Sea in meters? | 5109 m (5057 to 5161 m accepted) | 5,267 meters (6) | 6 |
| 3584 | What day, month, and year did over 500,000 people gather at the Black Star Square in Ghana to welcome Bill and Hillary Clinton? | 23 March 1998 | 24 March 1998 (5, two date formats) | 5 |
| 2454 | What multiple-choice letter could be selected by the button surrounded by yellow on the original 2-XL Robot? | C | B (3; 2 answered A) | 5 |
| 2914 | What was John Graham Lough's cause of death? | Pneumonia | Bronchitis (5; Brave answered Pneumonia) | 5 |
| 3555 | Where was the first B.A.S.S. Bassmaster Tournament held? | Lake Mead | Beaver Lake, Arkansas (5; Tavily answered Lake Mead) | 5 |
| 940 | During which years was Otto Schlüter a professor of geography at the University of Halle? | 1911 to 1959 | 1911-1951 (3) | 4 |
| 1740 | Who did Richard Neutra design the Elkay Apartments for? | Louis Kievman | Louis Kievman and E. G. Larsen (3) | 4 |

With the 193 leak-flagged and the 11 stale-gold questions removed (796
questions), the order does not change: Parallel 786 (98.7%), Exa 783
(98.4%), cloro 780 (98.0%), SerpApi 764 (96.0%), Brave 754 (94.7%), Tavily
742 (93.2%).

## Latency under load

Other benchmark runs used the same machine and the same API keys during two
parts of this run:

- 00:25 to 01:10 CET: the VerticalRTK run (761 search calls) and the FreshQA
  run (1,042 search calls), so three runs in parallel.
- 07:18 to 08:01 CET: the resumed VerticalRTK run (61 calls, until 07:22)
  and the resumed FreshQA run (1,098 calls, until 08:01). From 08:01 to 08:25
  SimpleQA ran alone.

Before 00:25 SimpleQA ran alone, except for two smoke tests (36 calls) at
23:19 to 23:21.

p50 latency in seconds, by period (rows per provider in brackets):

| Period | Load | cloro | SerpApi | Tavily | Exa | Parallel | Brave |
|---|---|---|---|---|---|---|---|
| 11-04 20:05 to 20:31 (first 100) | alone | 11.80 | 9.06 | 2.26 | 0.87 | 3.11 | 1.20 |
| 11-04 22:49 to 11-05 00:24 (405) | alone | 10.61 | 8.23 | 2.13 | 0.71 | 3.06 | 1.22 |
| 11-05 00:25 to 01:09 (191) | 3 runs in parallel | 16.15 | 6.87 | 1.65 | 0.65 | 2.80 | 1.22 |
| 11-05 07:18 to 08:25, resumed (304) | parallel until 08:01 | 12.13 | 7.24 | 1.68 | 0.86 | 2.54 | 1.19 |
| of which 07:18 to 08:01 (194) | 2 runs in parallel | 13.12 | 7.06 | 1.81 | 0.86 | 2.56 | 1.18 |
| of which 08:01 to 08:25 (110) | alone | 10.98 | 7.39 | 1.36 | 0.84 | 2.49 | 1.22 |
| All rows that ran alone (615) | alone | 10.96 | 8.20 | 2.00 | 0.74 | 2.99 | 1.21 |

Some periods have up to 3 rows more or less for a provider, because the 4
workers do not finish a question on all providers at the same time, and
because of the 2 Brave rows that ran again.

What the split shows:

- **cloro gets slower under load. SerpApi does not.** cloro's p50 went from
  10.61 s (alone) to 16.15 s (three runs in parallel), an increase of 52%.
  In the same period SerpApi's p50 went down from 8.23 s to 6.87 s. In the
  resumed part the same pattern is smaller: cloro 13.12 s with the FreshQA
  run, 10.98 s alone. The other runs also call cloro, so cloro gets more
  concurrent requests from our account. This run cannot show if the cause is
  cloro, Google or the time of day.
- **The fairest period for publication is the one where SimpleQA ran alone**:
  all rows before 00:25 plus 08:01 to 08:25, 615 rows per provider. That
  matches the setup in `methodology.md` (one run, 4 workers). In it, cloro
  p50 is 10.96 s (p90 37.79 s, p99 101.40 s) and SerpApi p50 is 8.20 s (p90
  24.67 s, p99 80.94 s). cloro is still the slowest provider.

| Provider (alone, 615 rows) | p50 | p90 | p99 | Mean |
|---|---|---|---|---|
| cloro | 10.96 s | 37.79 s | 101.40 s | 20.19 s |
| SerpApi | 8.20 s | 24.67 s | 80.94 s | 12.37 s |
| Parallel | 2.99 s | 3.94 s | 4.55 s | 3.05 s |
| Tavily | 2.00 s | 3.17 s | 5.44 s | 2.11 s |
| Brave | 1.21 s | 1.38 s | 1.61 s | 1.22 s |
| Exa | 0.74 s | 2.43 s | 4.28 s | 1.27 s |

## Cost

### Resumed part (2026-11-05), predicted against actual

Remaining work before the resume: 304 questions on 5 providers and 307 on
Brave (1,827 search calls).

| API | Predicted | Actual |
|---|---|---|
| cloro | 304 calls, about 2,128 credits (7 per call) | 304 calls, 305 HTTP attempts (1 retry). The REST response has no credits field, so credits are not measured. Estimate: about 2,128 credits |
| SerpApi | about 600 searches (about 1.96 per question) | 604 searches (304 plus 300 AI Overview follow-ups), plus 9 retried requests (613 HTTP requests) |
| Tavily | 304 credits | 304 basic searches, 304 credits |
| Exa | about $2.13 | $2.128 (sum of `costDollars`) |
| Parallel | 304 searches | 304 searches. Cost not in the response; check the dashboard |
| Brave | about 307 searches | 307 searches (includes the 2 rows that ran again) |
| OpenAI | 3,654 calls, about 3.6 million reader prompt tokens | 3,654 calls (no LLM errors), 4,413,181 reader prompt tokens. Grader tokens are not recorded |

The OpenAI token prediction was 18% low. The correct estimate from the
per-question means (304 x 11,113 + 307 x 3,291) is about 4.39 million.

### Full run, 1,000 questions

| API | Calls | Cost |
|---|---|---|
| cloro | 1,000 calls with AI Overview, sync, 1,006 HTTP attempts | about 7,000 credits (estimate, not measured) |
| SerpApi | 1,970 searches (1,000 plus 970 AI Overview follow-ups), 1,995 HTTP requests | SerpApi account dashboard |
| Tavily | 1,000 basic searches | 1,000 credits |
| Exa | 1,000 | $7.00 (sum of `costDollars`) |
| Parallel | 1,000 | Not found in the response |
| Brave | 1,000 successful requests, plus 6 attempts that got HTTP 402 | Not found in the response |
| OpenAI | 6,000 reader and 6,000 grader calls on the final rows | 14,428,087 reader prompt tokens; grader tokens not recorded |

## Notes

- **The 100-question result did not hold for cloro.** At 100 questions cloro
  was 99%, second. At 1,000 it is 96.9%, third. On questions 101 to 1,000
  cloro got 870 of 900 (96.7%).
- **Google results are short.** The reader needed about 830 tokens per
  question from cloro or SerpApi, against 2,966 to 3,300 from the others.
- **The AI Overview is almost always there.** cloro returned one on 986 of
  1,000 questions, SerpApi on 983. SerpApi needed a second request for it on
  970.
- **Brave stopped the first run.** When Brave hit its spend cap, the harness
  retried each call 3 times, wrote an ERROR row and went on with the other
  providers. A 402 does not stop the harness. Watch the log for it.

## Before you publish

- Review the 11 stale-gold questions and the 193 leak-flagged questions by
  hand. Neither changes the order.
- Publish the latency from the rows that ran alone (615 per provider), or
  say in the table that the full-run latency includes periods with other
  runs in parallel.
- Say that cloro, Parallel and Exa are not different by more than the noise
  on this run, and that cloro is ahead of SerpApi, Brave and Tavily.
