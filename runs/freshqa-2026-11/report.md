# FreshQA, 358 questions, 6 search APIs

> **Earlier reader.** The scores in this report come from the earlier reader,
> `gpt-5.6-luna`, with the earlier reader prompt. The published scores use
> `gemini-3.8-flash` with a prompt that allows only the search results: see the
> [rerun report](../rerun-2026-11/report.md) and the
> [reader test](../reader-test-2026-11/report.md). The search responses, the
> latencies and the counts that do not depend on the reader stay valid.

> On 2026-11-18 Gemini (`gemini-pro-latest`) graded every answer again. The
> grades in `results/` are the Gemini grades, and the numbers below are the
> first grades. See the [regrade report](../regrade-gemini-2026-11/report.md).

Run: 2026-11-05, `benchmark.py --dataset freshqa`,
seed 42, all 358 kept TEST rows of FreshQA (April 21, 2026 version;
fast-changing rows and rows past `next_review` dropped), `--workers 4`.
Reader `gpt-5.6-luna`, grader `gpt-5.6-sol`. One search per question. The
reader prompt gives today's date and a false-premise line.

The run started at 00:27 CET. At 01:10 CET Brave hit its monthly spend cap
(HTTP 402) at 174 of 358 questions. The run continued at 07:18 CET after the
cap was raised, and it finished at 08:01 CET. The harness ran the 3 Brave
error rows again (ids 127, 175, 235). Thus every provider has 358 graded rows
and no error row.

## Result

cloro and SerpApi share the top accuracy, but cloro is much slower. cloro
answered 88.3% correct and SerpApi 88.5%. cloro's p50 latency is 17.48 s,
against 6.65 s for SerpApi, and it is the slowest provider at p50, p90 and
p99. On false-premise questions cloro is 3.4 points below SerpApi (84.7%
against 88.1%).

At 358 questions, all 6 providers are inside each other's 95% intervals.
The two Google providers are ahead by 3.4 to 6.7 points, but this run does
not show that difference with confidence.

| Provider | Accuracy | 95% interval | Latency p50 | p90 | p99 | Reader tokens per question |
|---|---|---|---|---|---|---|
| SerpApi | 88.5% | 84.8-91.4 | 6.65 s | 24.73 s | 70.91 s | 853 |
| cloro | 88.3% | 84.5-91.2 | 17.48 s | 45.36 s | 103.83 s | 873 |
| Brave | 84.9% | 80.8-88.3 | 1.30 s | 1.49 s | 1.71 s | 3,762 |
| Exa | 83.0% | 78.7-86.5 | 0.70 s | 2.53 s | 3.83 s | 3,531 |
| Parallel | 82.7% | 78.4-86.2 | 2.65 s | 3.79 s | 4.17 s | 2,703 |
| Tavily | 81.8% | 77.5-85.5 | 1.81 s | 2.65 s | 3.85 s | 2,878 |

| Provider | Correct | Incorrect | Not attempted | Accuracy given attempted | AI Overview present |
|---|---|---|---|---|---|
| SerpApi | 317 | 38 | 3 | 89.3% | 351/358 |
| cloro | 316 | 37 | 5 | 89.5% | 352/358 |
| Brave | 304 | 44 | 10 | 87.4% | - |
| Exa | 297 | 49 | 12 | 85.8% | - |
| Parallel | 296 | 47 | 15 | 86.3% | - |
| Tavily | 293 | 41 | 24 | 87.7% | - |

## Search errors

| Provider | Error rows in the final data | Error lines in the file | HTTP retries on successful rows |
|---|---|---|---|
| cloro | 0 | 0 | 0 |
| SerpApi | 0 | 0 | 4 |
| Tavily | 0 | 0 | 0 |
| Exa | 0 | 0 | 0 |
| Parallel | 0 | 0 | 0 |
| Brave | 0 | 3 | 0 |

- The 3 Brave error lines are ids 127, 175 and 235, each
  `HTTPError 402: 'Payment Required'` (3 attempts each). The resumed run
  replaced them with graded rows.

## Accuracy per fact type and premise

| Fact type | n | cloro | SerpApi | Tavily | Exa | Parallel | Brave |
|---|---|---|---|---|---|---|---|
| never-changing, valid premise | 125 | 121 (97%) | 121 (97%) | 118 (94%) | 121 (97%) | 121 (97%) | 122 (98%) |
| never-changing, false premise | 63 | 52 (83%) | 53 (84%) | 45 (71%) | 45 (71%) | 47 (75%) | 47 (75%) |
| slow-changing, valid premise | 115 | 95 (83%) | 92 (80%) | 85 (74%) | 89 (77%) | 87 (76%) | 89 (77%) |
| slow-changing, false premise | 55 | 48 (87%) | 51 (93%) | 45 (82%) | 42 (76%) | 41 (75%) | 46 (84%) |

| Set | n | cloro | SerpApi | Tavily | Exa | Parallel | Brave |
|---|---|---|---|---|---|---|---|
| False premise | 118 | 84.7% (77.2-90.1) | 88.1% (81.1-92.8) | 76.3% (67.8-83.0) | 73.7% (65.1-80.8) | 74.6% (66.0-81.6) | 78.8% (70.6-85.2) |
| Valid premise | 240 | 90.0% (85.6-93.2) | 88.8% (84.1-92.2) | 84.6% (79.5-88.6) | 87.5% (82.7-91.1) | 86.7% (81.8-90.4) | 87.9% (83.2-91.5) |
| Never-changing | 188 | 92.0% (87.3-95.1) | 92.6% (87.9-95.5) | 86.7% (81.1-90.8) | 88.3% (82.9-92.1) | 89.4% (84.1-93.0) | 89.9% (84.8-93.4) |
| Slow-changing | 170 | 84.1% (77.9-88.8) | 84.1% (77.9-88.8) | 76.5% (69.6-82.2) | 77.1% (70.2-82.7) | 75.3% (68.3-81.2) | 79.4% (72.7-84.8) |

- cloro is below SerpApi on false-premise questions (100 against 104 of
  118). It is above SerpApi on valid-premise questions (216 against 213 of
  240). Both differences are inside the intervals.
- The Google providers lead on false-premise questions: cloro and SerpApi
  are 6 to 14 points above the other four. The AI Overview often states that
  the premise is false.
- On never-changing questions with a valid premise, all 6 providers are
  between 94% and 98%.

## Possibly stale gold

30 of 358 questions have 4 or more providers graded INCORRECT. On 17 of them,
all 6 providers are INCORRECT. The FreshQA gold answers are from April 2026
or earlier, and the dataset had no update after that. The "Reading" column
is a first reading, not a verified one. Review these rows by hand before you
publish.

- 16 rows look like stale gold: the providers agree on a later event.
- 6 rows look like a false premise that the providers did not catch: the
  gold is probably correct.
- 8 rows are disputed: the correct answer depends on a definition or a
  source.

cloro is INCORRECT on 27 of the 30. It is CORRECT on 130, 60 and 74.
Without the 30 rows the order does not change:

| Provider | All 358 | Without the 30 | 95% interval without |
|---|---|---|---|
| SerpApi | 88.5% | 315/328 (96.0%) | 93.3-97.7 |
| cloro | 88.3% | 313/328 (95.4%) | 92.6-97.2 |
| Brave | 84.9% | 300/328 (91.5%) | 87.9-94.0 |
| Exa | 83.0% | 295/328 (89.9%) | 86.2-92.7 |
| Parallel | 82.7% | 294/328 (89.6%) | 85.9-92.5 |
| Tavily | 81.8% | 290/328 (88.4%) | 84.5-91.4 |

| Id | Type | Question | Gold | Common answer (providers) | Incorrect | Reading |
|---|---|---|---|---|---|---|
| 117 | never, false premise | What is the smallest cube number which can be expressed as the sum of two different positive cube numbers in two different ways? | None: by Fermat's Last Theorem, no cube is a sum of two positive cubes | 1729 (6) | 6 | Premise missed |
| 59 | never, false premise | When did Joe Biden announce his second presidential campaign in 2023? | His second campaign was in 2008 | April 25, 2023 (6) | 6 | Premise missed |
| 60 | never, false premise | Who won the FIFA Ballon d'Or last year? | No FIFA Ballon d'Or since 2015 | Ousmane Dembele (4) | 4 | Premise missed |
| 74 | never, false premise | When will IKEA celebrate its fiftieth anniversary? | It did in 1993 | October 2026 (3) | 4 | Premise missed |
| 92 | never, false premise | What date in 2026 did BTS release its 11th studio album? | BTS had released ten studio albums (April 2026) | March 20, 2026 (4) | 4 | Premise missed |
| 93 | never, false premise | Alphabet's market capitalization reached its highest-ever recorded value during what month in 2025? | The high was in February 2026, not 2025 | September 2025 (3) | 6 | Premise missed, or the high moved again |
| 131 | slow | What's the world record time for running a mile? | 3:43.13 | 3:42.66 (6) | 6 | Stale gold |
| 153 | slow | Which is the most recently launched NASA space telescope that observes in the visible and near-infrared? | Pandora | Nancy Grace Roman Space Telescope (6) | 6 | Stale gold |
| 156 | slow | How many vehicle models does Tesla offer? | 5 | 4 (4) | 5 | Stale gold |
| 162 | slow | How many LA metro rail stations are there? | 107 | 110 (3) or 115 (3) | 6 | Stale gold |
| 163 | slow | How many properties are there in the latest list of World Heritage in danger? | 53 | 58 (4) | 6 | Stale gold |
| 178 | slow | Who is the current Prime Minister of the United Kingdom? | Keir Starmer | Andy Burnham (6) | 6 | Stale gold |
| 179 | slow | Who is the most recent former Prime Minister of the United Kingdom? | Rishi Sunak | Keir Starmer (6) | 6 | Stale gold |
| 181 | slow | What is the most recent outbreak declared as a public health emergency of international concern by WHO? | Clade I mpox | Bundibugyo Ebola, DRC and Uganda (5) | 5 | Stale gold |
| 183 | slow | What is the name of the world's fastest supercomputer? | El Capitan | LineShine (6) | 6 | Stale gold |
| 203 | slow | Who was the most recent woman to become President of Peru? | Dina Boluarte | Keiko Fujimori (6) | 6 | Stale gold |
| 206 | slow | What club does Lewandowski play for? | Barcelona | Chicago Fire FC (6) | 6 | Stale gold |
| 210 | slow | How many total Nazca geoglyphs have been discovered so far? | 358 | 893 (4) | 6 | Stale gold |
| 228 | slow | How many presidents has Peru had in the last 5 years? | 4 | 6 (5) | 6 | Stale gold |
| 230 | slow | How many public health emergency of international concern declarations have been made by WHO in the last 5 years? | 2 | 3 (5) | 5 | Stale gold |
| 231 | slow | In what country was the current World's Strongest Man born? | South Africa | Canada (4) | 4 | Stale gold |
| 243 | slow | Who bought the most expensive 20th century artwork sold in a public sale? | Larry Gagosian (Warhol, $195.04 million) | Buyer not named (3) | 4 | Stale gold |
| 130 | slow | What is the top-ranked university in the US according to the US News Ranking? | Princeton | MIT (5) | 5 | Disputed (which US News list) |
| 140 | slow | Which is the oldest still-running university in the world? | University of Bologna | University of al-Qarawiyyin (6) | 6 | Disputed (definition of university) |
| 226 | slow | How many presidents of the United States have lost reelection? | 10 | 11 (4) | 4 | Disputed (count method) |
| 237 | slow | Which was the first country to detect a case of mpox in the most recent outbreak? | DR Congo | United Kingdom (4) | 5 | Disputed (which outbreak) |
| 42 | slow, false premise | Where will the FIFA World Cup be hosted next year? | There is no FIFA World Cup next year | Brazil (4) | 4 | Disputed (the 2027 Women's World Cup is in Brazil) |
| 295 | never | What time of day on August 15, 1947 did India become an independent nation? | 12:02 am | Midnight (6) | 6 | Disputed |
| 321 | never | How many public payphones are left in New York City? | None (the last public one was removed in 2022) | 4 (5) | 5 | Disputed (public or private payphones) |
| 367 | never | How many years did it take for the population of the world to reach 8 billion from 7 billion? | 10 years | 12 years (5) | 6 | Disputed (source dates) |

- The SKILL.md note about the Alphabet all-time-high row (93) is confirmed:
  all 6 providers miss it again.
- If you remove only the 16 likely stale rows, the 6 premise rows stay in
  the score. Those rows count against every provider except where it caught
  the premise (cloro on 60 and 74, Parallel and Brave on 92).

## Leak check of raw/

Method: the same text match as the SimpleQA analysis. A raw response is
flagged when it contains a dataset name (`freshqa`, `fresh_qa`, `fresh-qa`,
`freshllms`, `freshprompt`) or a dataset host (`huggingface.co/datasets`,
`kaggle.com`). This is a text match, not a review.

No raw response names FreshQA or FreshLLMs. 1 of 358 questions has a host
match: id 359 (Forbes Celebrity 100 athletes in 2020). Parallel returned the
Kaggle dataset "Forbes Celebrity 100 1999-2020". That is the source data for
the question, not a copy of FreshQA, so it is not a leak. Without this row
the order does not change.

## Cost of this run

The prediction uses the per-call estimates from the skill: cloro 7 credits,
SerpApi 2 searches, Exa about $0.007, 2 OpenAI calls per provider per
question. The actual values are from `http_calls` in the result files, the
raw responses and Exa's `costDollars`.

| API | Predicted | Actual |
|---|---|---|
| cloro | 358 calls, about 2,506 credits | 358 HTTP requests, no retries. About 2,506 credits (7 per call, not measured: the REST response has no credits field). |
| SerpApi | about 716 searches | 631 requests: 358 searches, 269 AI Overview follow-ups, 4 retries |
| Tavily | 358 credits | 358 requests, no retries |
| Exa | about $2.51 | $2.506 (sum of `costDollars`), 358 requests |
| Parallel | 358 searches | 358 requests. The cost is not in the response; check the dashboard. |
| Brave | 358 searches | 367 requests: 358 successful, 9 returned HTTP 402 (spend cap, 3 rows with 3 attempts each) |
| OpenAI | 4,296 calls | 2,148 reader and 2,148 grader calls. 5,227,237 reader prompt tokens. Grader tokens are not recorded. |

SerpApi needed fewer follow-ups than predicted: Google loaded the AI
Overview in a second request on 269 of 358 questions (75%), against 95 of
100 on SimpleQA.

## Latency under load

This run is less comparable on latency than the SimpleQA 100-question run.
It ran at the same time as the VerticalRTK run and the SimpleQA
1,000-question run. Each run had 4 workers, so about 12 requests were in
progress at one time across the 6 providers.

The SimpleQA 1,000 result files show the effect. Part of that run had no
other run active and part ran at the same time as this one (the time of
each call is from its raw file):

| Provider | SimpleQA p50, no other run (515 rows) | SimpleQA p50, during this run and VerticalRTK (375 rows) | FreshQA p50 |
|---|---|---|---|
| cloro | 10.97 s | 14.61 s | 17.48 s |
| SerpApi | 8.34 s | 7.04 s | 6.65 s |
| Tavily | 2.15 s | 1.77 s | 1.81 s |
| Exa | 0.72 s | 0.67 s | 0.70 s |
| Parallel | 3.06 s | 2.66 s | 2.65 s |
| Brave | 1.21 s | 1.19 s | 1.30 s |

- cloro is the only provider that became slower under the load: its SimpleQA
  p50 increased by about 33%. The rows with no other run are also from a
  different time of day (20:00 to 00:27 CET), so time of day can be a part
  of the change.
- cloro's FreshQA p50 (17.48 s) is 2.6 times SerpApi's (6.65 s) in the same
  run, with the AI Overview present on almost all questions for both.

## Before you publish

- Review the 30 possibly stale rows by hand. Correct the gold on the rows
  where the world changed, and keep the premise rows.
- At 358 questions the 6 providers are inside each other's intervals. Do
  not claim a rank from this run alone.
- Run cloro alone on FreshQA before you show its latency, to separate the
  load from cloro's own latency.
