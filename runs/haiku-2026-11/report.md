# Rerun of all ten APIs with `claude-haiku-5-5` (2026-11-28)

Run: 2026-11-27 and 2026-11-28, `READER_MODEL=claude-haiku-5-5`,
`GRADER_MODEL=claude-haiku-5-5`, `--support-check`, seed 42, with the
`<provider>-reread` variants of [`benchmark.py`](../../benchmark.py). No
search ran again: Haiku read the saved search responses of the published
runs, with the strict reader prompt ("Use ONLY information from the search
results. Do NOT use any internal knowledge."). The questions and the
`--as-of` dates (FreshQA 2026-11-05, FRAMES 2026-11-10) are the same as in
the earlier runs. Claude ran on a subscription login, through Claude Code
headless (`claude -p`).

The README tables come from this run. The agent runs in
[`runs/agent-2026-11/`](../agent-2026-11/report.md) use the same model, so
from this run on one model reads and grades every published score. The
earlier reports in `runs/` keep the Gemini scores (`gemini-3.8-flash` read,
`gemini-pro-latest` graded) as history.

Two things changed from the [Gemini run](../rerun-2026-11/report.md):

- **The model.** Haiku reads, grades and checks support.
- **SerpApi gets one request per search.** SerpApi loads most Google AI
  Overviews in a second request (`engine=google_ai_overview`). No other API
  gets a second request, so this run reads only the first SerpApi response
  (`serpapi-single-reread`). See [SerpApi with one request](#serpapi-with-one-request).

## Result

Accuracy with the 95% Wilson interval. A failed search of the earlier run
counts as an error.

| Search API | SimpleQA Verified (1,000) | FreshQA (358) | FRAMES (824) |
|---|---|---|---|
| cloro | 96.5% (95.2-97.5) | 89.7% (86.1-92.4) | 79.1% (76.2-81.8) |
| Perplexity Search API\* | 95.7% (94.3-96.8) | 86.6% (82.7-89.7) | 43.7% (40.3-47.1) |
| Keenable\* | 95.4% (93.9-96.5) | 84.4% (80.2-87.8) | 34.1% (30.9-37.4) |
| Parallel | 95.0% (93.5-96.2) | 84.1% (79.9-87.5) | 43.6% (40.2-47.0) |
| Exa | 95.0% (93.5-96.2) | 89.1% (85.5-91.9) | 48.9% (45.5-52.3) |
| Brave Search API | 89.7% (87.7-91.4) | 87.2% (83.3-90.2) | 26.3% (23.4-29.4) |
| Tavily | 88.9% (86.8-90.7) | 81.3% (76.9-85.0) | 18.1% (15.6-20.9) |
| You.com† | 88.6% (86.5-90.4) | 86.3% (82.4-89.5) | 23.1% (20.3-26.1) |
| Firecrawl | 88.6% (86.5-90.4) | 80.4% (76.0-84.2) | 16.1% (13.8-18.8) |
| SerpApi | 38.9% (35.9-42.0) | 69.0% (64.0-73.6) | 7.9% (6.2-9.9) |

\* With huggingface.co and kaggle.com excluded, as in the earlier runs.

† You.com rejects queries longer than 50 words (HTTP 422), so it has no
results for 42 FRAMES questions and 1 SimpleQA Verified question. They
count as errors. Brave has no saved response for 8 FRAMES questions, which
also count as errors.

- **SimpleQA Verified:** cloro, Perplexity, Keenable, Parallel and Exa are
  within the margin of error of each other (paired p = 0.067 to 1.0). Each of
  the five is ahead of Brave, Tavily, You.com, Firecrawl and SerpApi
  (p < 0.0001).
- **FreshQA:** cloro scores highest. The gaps to Exa, Brave, Perplexity and
  You.com are not significant. cloro is ahead of Parallel, Keenable, Tavily,
  Firecrawl and SerpApi.
- **FRAMES:** cloro is ahead of every other API by 30 to 71 points
  (p < 0.0001).

## Correct and supported

After the grade, Haiku checks each correct answer against the search
results: do the results state the answer? This is the score of the agent
runs.

| Search API | SimpleQA Verified | FreshQA | FRAMES |
|---|---|---|---|
| cloro | 94.1% (92.5-95.4) | 79.9% (75.4-83.7) | 73.7% (70.6-76.6) |
| Perplexity Search API\* | 95.5% (94.0-96.6) | 79.1% (74.5-82.9) | 41.5% (38.2-44.9) |
| Keenable\* | 95.0% (93.5-96.2) | 74.3% (69.5-78.6) | 30.8% (27.8-34.1) |
| Parallel | 94.7% (93.1-95.9) | 77.7% (73.1-81.7) | 41.4% (38.1-44.8) |
| Exa | 94.9% (93.4-96.1) | 81.8% (77.5-85.5) | 47.5% (44.1-50.9) |
| Brave Search API | 89.5% (87.4-91.3) | 79.6% (75.1-83.5) | 24.6% (21.8-27.7) |
| Tavily | 88.2% (86.1-90.1) | 71.2% (66.3-75.7) | 16.5% (14.1-19.2) |
| You.com | 88.3% (86.2-90.1) | 78.5% (73.9-82.4) | 21.6% (18.9-24.5) |
| Firecrawl | 87.9% (85.7-89.8) | 67.0% (62.0-71.7) | 14.9% (12.7-17.5) |
| SerpApi | 38.3% (35.3-41.4) | 54.7% (49.6-59.8) | 7.3% (5.7-9.3) |

On this score cloro is fifth on SimpleQA Verified and second on FreshQA.
The gaps to the APIs above it are not significant: on SimpleQA Verified,
p = 0.13 (Perplexity) to 0.59 (Parallel); on FreshQA, p = 0.44 (Exa).

The support check rejects more of cloro's correct SimpleQA answers than of
the other top APIs:

| Search API | SimpleQA Verified | FreshQA | FRAMES |
|---|---|---|---|
| cloro | 2.5% (24 of 965) | 10.9% (35 of 321) | 6.9% (45 of 652) |
| Perplexity\* | 0.2% (2 of 957) | 8.7% (27 of 310) | 5.0% (18 of 360) |
| Keenable\* | 0.4% (4 of 954) | 11.9% (36 of 302) | 9.6% (27 of 281) |
| Parallel | 0.3% (3 of 950) | 7.6% (23 of 301) | 5.0% (18 of 359) |
| Exa | 0.1% (1 of 950) | 8.2% (26 of 319) | 3.0% (12 of 403) |
| Brave | 0.2% (2 of 897) | 8.7% (27 of 312) | 6.5% (14 of 217) |
| You.com | 0.3% (3 of 886) | 9.1% (28 of 309) | 6.3% (12 of 190) |
| Tavily | 0.8% (7 of 889) | 12.4% (36 of 291) | 8.7% (13 of 149) |
| Firecrawl | 0.8% (7 of 886) | 16.7% (48 of 288) | 7.5% (10 of 133) |
| SerpApi | 1.5% (6 of 389) | 20.6% (51 of 247) | 7.7% (5 of 65) |

The check is not stable when it rejects. We ran it again two times on every
rejected SimpleQA answer of the top five and on the same 30 accepted answers
of each (random seed 7):

| Answers | First recheck | Second recheck |
|---|---|---|
| cloro: rejected answers that were SUPPORTED | 9 of 24 | 13 of 24 |
| The other four: rejected answers that were SUPPORTED | 8 of 10 | 8 of 10 |
| Accepted answers that changed | 0 of 150 | 0 of 150 |

Only the second recheck saved each verdict:
[`checks/simpleqa-support-recheck.jsonl`](checks/simpleqa-support-recheck.jsonl).

So the supported score is a lower bound. In the second recheck, 11 of
cloro's 24 rejected answers were rejected again. We read three of cloro's
rejected answers, and in all three the AI Overview states the answer. The
published scores keep the verdicts of the first run.

## Change from the Gemini run

Accuracy, Gemini run -> Haiku run.

| Search API | SimpleQA Verified | FreshQA | FRAMES |
|---|---|---|---|
| cloro | 96.4% -> 96.5% | 88.5% -> 89.7% | 79.9% -> 79.1% |
| Exa | 95.8% -> 95.0% | 86.6% -> 89.1% | 49.9% -> 48.9% |
| Parallel | 96.2% -> 95.0% | 86.0% -> 84.1% | 45.6% -> 43.6% |
| Perplexity\* | 96.9% -> 95.7% | 86.0% -> 86.6% | 44.2% -> 43.7% |
| Keenable\* | 96.0% -> 95.4% | 84.4% -> 84.4% | 34.5% -> 34.1% |
| Brave | 90.5% -> 89.7% | 85.8% -> 87.2% | 25.8% -> 26.3% |
| You.com | 89.2% -> 88.6% | 84.9% -> 86.3% | 22.1% -> 23.1% |
| Tavily | 89.2% -> 88.9% | 82.7% -> 81.3% | 18.1% -> 18.1% |
| Firecrawl | 88.8% -> 88.6% | 80.2% -> 80.4% | 15.8% -> 16.1% |
| SerpApi | two requests -> one request: see below | | |

Every change is 2.5 points or less. On FreshQA two gaps become significant:
cloro is now ahead of Parallel (p = 0.00082, against p = 0.11 in the Gemini
run), and Exa is ahead of Parallel (p = 0.0021). On SimpleQA Verified the top
five stay within the margin of error of each other.

## SerpApi with one request

The first SerpApi response holds Google's organic results, and the AI
Overview only when Google shows it on the page itself. For most queries
SerpApi gives a token for a second request, which returns the AI Overview
and is billed as a second search. The earlier runs made that request. This
run does not, because every other API gets one request per search.

| Dataset | AI Overview in the first response | With the second request |
|---|---|---|
| SimpleQA Verified | 15 of 1,000 | 983 of 1,000 |
| FreshQA | 83 of 358 | 351 of 358 |
| FRAMES | 2 of 824 | 794 of 824 |

Without the AI Overview, the reader gets Google's short snippets: a median
of 2,380 characters per SimpleQA question, against 13,475 for Brave. The
reader then says it cannot answer 562 of 1,000 SimpleQA Verified questions
and 739 of 824 FRAMES questions. The raw responses with both requests are
kept, and `serpapi-reread` in `benchmark.py` reads them.

## FRAMES: not attempted and accuracy given an answer

| Search API | Not attempted (of 824) | Correct when it answers |
|---|---|---|
| cloro | 29 | 82.0% |
| Exa | 338 | 82.9% |
| Parallel | 397 | 84.1% |
| Perplexity\* | 377 | 80.5% |
| Keenable\* | 470 | 79.4% |
| Brave | 540 | 78.6% |
| You.com | 542 | 79.2% |
| Tavily | 631 | 77.2% |
| Firecrawl | 646 | 74.7% |
| SerpApi | 739 | 76.5% |

When they answer, all ten are correct 74.7% to 84.1% of the time. The gap comes
from how many questions one results page can answer at all.

## Head-to-head

Paired exact McNemar tests on the same questions. The numbers are the
questions that one API answered correctly and the other did not.

| Comparison | SimpleQA Verified | FreshQA | FRAMES |
|---|---|---|---|
| Exa vs Tavily | Exa, 88 to 27 (p < 0.0001) | Exa, 40 to 12 (p = 0.00013) | Exa, 288 to 34 (p < 0.0001) |
| Brave vs Tavily | no difference (p = 0.54) | Brave, 36 to 15 (p = 0.0046) | Brave, 134 to 66 (p < 0.0001) |
| Exa vs Parallel | no difference (p = 1.00) | Exa, 25 to 7 (p = 0.0021) | Exa, 136 to 92 (p = 0.0043) |
| Exa vs Brave | Exa, 81 to 28 (p < 0.0001) | no difference (p = 0.30) | Exa, 223 to 37 (p < 0.0001) |
| Parallel vs Tavily | Parallel, 88 to 27 (p < 0.0001) | no difference (p = 0.17) | Parallel, 251 to 41 (p < 0.0001) |
| Firecrawl vs Tavily | no difference (p = 0.86) | no difference (p = 0.80) | no difference (p = 0.21) |
| cloro vs SerpApi | cloro, 581 to 5 (p < 0.0001) | cloro, 83 to 9 (p < 0.0001) | cloro, 591 to 4 (p < 0.0001) |
| cloro vs Tavily | cloro, 98 to 22 (p < 0.0001) | cloro, 42 to 12 (p < 0.0001) | cloro, 518 to 15 (p < 0.0001) |
| cloro vs Brave | cloro, 88 to 20 (p < 0.0001) | no difference (p = 0.16) | cloro, 450 to 15 (p < 0.0001) |
| cloro vs Exa | no difference (p = 0.067) | no difference (p = 0.85) | cloro, 280 to 31 (p < 0.0001) |
| cloro vs Parallel | no difference (p = 0.077) | cloro, 27 to 7 (p = 0.00082) | cloro, 327 to 34 (p < 0.0001) |
| cloro vs Perplexity | no difference (p = 0.33) | no difference (p = 0.099) | cloro, 331 to 39 (p < 0.0001) |
| cloro vs Firecrawl | cloro, 95 to 16 (p < 0.0001) | cloro, 42 to 9 (p < 0.0001) | cloro, 527 to 8 (p < 0.0001) |
| cloro vs You.com | cloro, 94 to 15 (p < 0.0001) | no difference (p = 0.058) | cloro, 473 to 11 (p < 0.0001) |
| You.com vs Brave | no difference (p = 0.21) | no difference (p = 0.70) | Brave, 54 to 27 (p = 0.0036) |
| You.com vs Tavily | no difference (p = 0.87) | You.com, 32 to 14 (p = 0.011) | You.com, 112 to 71 (p = 0.003) |
| cloro vs Keenable | no difference (p = 0.17) | cloro, 28 to 9 (p = 0.0026) | cloro, 402 to 31 (p < 0.0001) |
| Keenable vs Exa | no difference (p = 0.68) | Exa, 30 to 13 (p = 0.014) | Exa, 196 to 74 (p < 0.0001) |
| Keenable vs Perplexity | no difference (p = 0.77) | no difference (p = 0.26) | Perplexity, 161 to 82 (p < 0.0001) |
| Keenable vs Brave | Keenable, 83 to 26 (p < 0.0001) | no difference (p = 0.11) | Keenable, 138 to 74 (p < 0.0001) |

## The grader

The grader prompt of simple-evals asks for a bare letter (A, B or C). With
that prompt, Haiku agreed with `gemini-pro-latest` on only 80% to 82% of 716
FreshQA answers, and it graded correct false-premise answers as wrong. Two
changes fixed it:

- The grader writes one short sentence, then the letter on the last line.
  On the same 716 answers, Haiku then agreed with Gemini on 98.6% (cloro)
  and 98.3% (Parallel) in a test run. The published grades come from a
  second run of the same prompt over all answers, and they agree with Gemini
  on 97.8% for both. Each grade is in
  [`checks/freshqa-grader-agreement.jsonl`](checks/freshqa-grader-agreement.jsonl).
- FreshQA questions get two rules (`FRESHQA_GRADER_RULES` in
  `benchmark.py`): a gold target with "OR" lists alternatives, and an answer
  that says a false premise is false is correct.

Part of the Haiku answers were first graded with the bare-letter prompt: all
FreshQA and FRAMES answers, the first 141 SimpleQA Verified questions of
each API, and all SimpleQA Verified answers of SerpApi with one request.
[`analysis/regrade.py`](../../analysis/regrade.py) graded them again with the
new prompt. The change by dataset, old prompt -> new prompt, over all APIs:

- FreshQA: 13.4 to 17.0 points higher for each API, same grade on 79.7% of
  3,938 answers.
- FRAMES: 0.7 to 2.5 points lower, same grade on 97.0% of 9,014 answers.
- SimpleQA Verified: same grade on 99.7% of 6,905 answers in
  the regraded files, and on 99.0% of the 1,000 SerpApi answers.

## Files

`<dataset>/<provider>-reread.jsonl`: one row per question, with the reader's
answer, the grade and `supported`. The SerpApi file is
`serpapi-single-reread.jsonl`. The raw search responses are those of the
earlier runs and are not in the repo.

`checks/freshqa-grader-agreement.jsonl`: the 716 FreshQA answers of cloro
and Parallel, with the grade of `gemini-pro-latest`, of Haiku with the bare
letter, of Haiku with one sentence first (and that sentence), and the
published grade.

`checks/simpleqa-support-recheck.jsonl`: the second recheck of the support
check. `first_check` is the published verdict, `second_check` the new one.
