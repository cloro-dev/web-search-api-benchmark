# FRAMES, 824 questions, 6 search APIs

Run: 2026-11-10 to 2026-11-11, `benchmark.py --dataset frames`, seed 42, all
824 questions of [google/frames-benchmark](https://huggingface.co/datasets/google/frames-benchmark)
(`test.tsv`, Apache-2.0), `--workers 6`. Reader `gpt-5.6-luna`, grader
`gpt-5.6-sol`. One search per question, with the full question text as the
query. The reader prompt gives the date of the run.

FRAMES questions need facts from 2 to 15 Wikipedia pages ("multi-hop"). The
FRAMES paper and most vendors run it with an agent that searches many times.
This run gives each API one search, so it measures how much of the answer one
results page holds.

## Result

cloro is the most accurate API on FRAMES: 80.2%, against 77.4% for SerpApi
and 48.4% to 65.3% for the other four. The 95% intervals of cloro and SerpApi
overlap, but on the same questions cloro answered 58 questions that SerpApi
missed and SerpApi 35 that cloro missed (exact McNemar test, p = 0.02). cloro
is ahead of Parallel, Exa, Brave and Tavily by 15 to 32 points (p < 0.001
for each).

The two Google APIs answer almost every question. Parallel, Exa, Brave and
Tavily reply "not found" on 151 to 295 questions: their 10 results do not
hold all the facts of a multi-hop question. The AI Overview was present on
813 of 824 cloro searches.

cloro is the slowest API at p50 and p99.

| Provider | Accuracy | 95% interval | Latency p50 | p90 | p99 | Reader tokens per question |
|---|---|---|---|---|---|---|
| cloro | 80.2% | 77.4-82.8 | 15.08 s | 48.49 s | 105.53 s | 901 |
| SerpApi | 77.4% | 74.4-80.2 | 22.74 s | 36.65 s | 49.92 s | 864 |
| Parallel | 65.3% | 62.0-68.5 | 3.12 s | 4.09 s | 6.03 s | 2,873 |
| Exa | 64.0% | 60.6-67.2 | 1.69 s | 3.23 s | 6.34 s | 5,216 |
| Brave | 53.9% | 50.5-57.3 | 1.37 s | 1.61 s | 3.29 s | 3,865 |
| Tavily | 48.4% | 45.0-51.8 | 2.52 s | 3.52 s | 6.59 s | 3,192 |

| Provider | Correct | Incorrect | Not attempted | Search errors | Accuracy given attempted | AI Overview present |
|---|---|---|---|---|---|---|
| cloro | 661 | 152 | 11 | 0 | 81.3% | 813/824 |
| SerpApi | 638 | 158 | 28 | 0 | 80.2% | 794/824 |
| Parallel | 538 | 130 | 156 | 0 | 80.5% | - |
| Exa | 527 | 146 | 151 | 0 | 78.3% | - |
| Brave | 444 | 160 | 212 | 8 | 73.5% | - |
| Tavily | 399 | 130 | 295 | 0 | 75.4% | - |

Accuracy given attempted is close for five of the six APIs (78% to 81%). The
difference in accuracy comes from how many questions each API can answer at
all.

## Paired tests against cloro

| Provider | Only cloro correct | Only the provider correct | Exact McNemar p |
|---|---|---|---|
| SerpApi | 58 | 35 | 0.022 |
| Parallel | 172 | 49 | < 0.001 |
| Exa | 179 | 45 | < 0.001 |
| Brave | 248 | 31 | < 0.001 |
| Tavily | 297 | 35 | < 0.001 |

## Accuracy per reasoning type

A question can have more than one type, so the rows overlap.

| Reasoning type | n | cloro | SerpApi | Parallel | Exa | Brave | Tavily |
|---|---|---|---|---|---|---|---|
| Multiple constraints | 549 | 81% | 78% | 67% | 63% | 54% | 50% |
| Numerical reasoning | 293 | 71% | 71% | 62% | 58% | 50% | 41% |
| Tabular reasoning | 236 | 78% | 75% | 62% | 60% | 47% | 44% |
| Temporal reasoning | 278 | 78% | 76% | 62% | 58% | 50% | 48% |
| Post processing | 107 | 76% | 71% | 64% | 59% | 44% | 37% |

The per-topic table with every combination of types is in
`analysis/analyze.py` output (`python3 analysis/analyze.py <run folder> frames`).

## Search errors

| Provider | Error rows in the final data | Error lines in the file |
|---|---|---|
| cloro | 0 | 69 |
| SerpApi | 0 | 14 |
| Tavily | 0 | 7 |
| Exa | 0 | 9 |
| Parallel | 0 | 7 |
| Brave | 8 | 23 |

- cloro: 52 lines are `HTTPError 503: 'Service Temporarily Unavailable'`,
  2 are timeouts and 1 is a DNS error. The harness ran these questions again
  and every one has a graded row. The rest of the error lines on every
  provider are reader or grader errors (OpenAI `429`) or DNS errors on our
  side; those questions also ran again.
- Brave: 8 questions return `HTTPError 422: 'Unprocessable Entity'` on every
  attempt. All 8 are longer than 400 characters (78 to 130 words). Brave
  rejects these queries, so they count as not attempted. Without them Brave
  scores 444/816 (54.4%), and the order does not change.
- SerpApi needed a second request (AI Overview follow-up) on 805 of 824
  questions.

## Possibly stale or hard gold

80 of 824 questions have 4 or more providers graded INCORRECT. FRAMES answers
come from Wikipedia in 2024, so some can be out of date, and some questions
are hard for every API. These rows are not reviewed by hand. Without them the
order does not change:

| Provider | All 824 | Without the 80 | 95% interval without |
|---|---|---|---|
| cloro | 80.2% | 648/744 (87.1%) | 84.5-89.3 |
| SerpApi | 77.4% | 627/744 (84.3%) | 81.5-86.7 |
| Parallel | 65.3% | 525/744 (70.6%) | 67.2-73.7 |
| Exa | 64.0% | 518/744 (69.6%) | 66.2-72.8 |
| Brave | 53.9% | 440/744 (59.1%) | 55.6-62.6 |
| Tavily | 48.4% | 390/744 (52.4%) | 48.8-56.0 |

## Leak check

178 of 824 questions have a search result, from any provider, that contains
`frames-benchmark`, `google/frames`, `framesbenchmark`,
`huggingface.co/datasets` or `kaggle.com`. Most hits are a link to a Hugging
Face dataset page, not the answer itself. Without these questions the order
does not change:

| Provider | All 824 | Without the 178 | 95% interval without |
|---|---|---|---|
| cloro | 80.2% | 518/646 (80.2%) | 76.9-83.1 |
| SerpApi | 77.4% | 503/646 (77.9%) | 74.5-80.9 |
| Parallel | 65.3% | 414/646 (64.1%) | 60.3-67.7 |
| Exa | 64.0% | 421/646 (65.2%) | 61.4-68.7 |
| Brave | 53.9% | 356/646 (55.1%) | 51.3-58.9 |
| Tavily | 48.4% | 321/646 (49.7%) | 45.8-53.5 |

## Run cost

| Provider | HTTP requests (all lines) |
|---|---|
| cloro | 1,017 |
| SerpApi | 1,662 (805 AI Overview follow-ups) |
| Tavily | 839 |
| Exa | 839 ($5.77 in `costDollars`) |
| Parallel | 832 |
| Brave | 872 |

About 10,000 OpenAI calls (reader and grader) and 13.9 million reader prompt
tokens.
