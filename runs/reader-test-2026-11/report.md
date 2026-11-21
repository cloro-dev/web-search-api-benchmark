# Reader test: which LLM reads the search results? (2026-11-21)

**Result:** the reader is now `gemini-3.8-flash`, with the prompt line "Use
ONLY information from the search results. Do NOT use any internal
knowledge." Of 11 readers, the GPT models scored highest on FRAMES because
they add facts from their own memory: with the strict prompt, 23%
(`gpt-5.6-luna`) and 27% (`gpt-4.1`) of their answers are not supported by
the search results. For `gemini-3.8-flash` it is 4%, the same as the more
expensive Gemini models, at a lower price. See
[Reader selection with the strict prompt](#reader-selection-with-the-strict-prompt).

The sections below are in the order of the tests.


Run: 2026-11-20 and 2026-11-21. Six other Gemini models ran on 2026-11-21
(see [Other Gemini models](#other-gemini-models)). The reader selection with
the strict prompt ran on 2026-11-21 (see
[Reader selection with the strict prompt](#reader-selection-with-the-strict-prompt)). `READER_MODEL=gemini-pro-latest`,
`GRADER_MODEL=gemini-pro-latest`, `--n 200`, seed 42, with the
`<provider>-reread` variants of [`benchmark.py`](../../benchmark.py). No
search ran again. The Gemini reader read the saved search responses of the
published runs, with the same reader prompt and the same `--as-of` dates
(FRAMES 2026-11-10, FreshQA 2026-11-05). Gemini graded every answer, as for
the published scores. Thus the reader is the only change.

The `<provider>-reread` variants rebuild the reader input from the saved
responses. On 200 FRAMES questions of each of the 12 variants, the input
had the same length as in the published run, 2,400 of 2,400.

## Scope

| Dataset | Questions | APIs |
|---|---|---|
| FRAMES | the first 200 of the published run | all ten |
| SimpleQA Verified | the first 200 of the published run | Perplexity\*, Firecrawl, You.com, Keenable\* |
| FreshQA | the first 200 of the published run | Perplexity\*, Firecrawl, You.com, Keenable\* |

\* The run with huggingface.co and kaggle.com excluded, the published run.

When this test ran, the saved SimpleQA Verified and FreshQA responses of the
first six APIs (cloro, SerpApi, Tavily, Exa, Parallel, Brave) were not
found. Thus those two datasets have four APIs only. The responses were found
later in the `marketing` repo (see the last section).

## Result

**On SimpleQA Verified and FreshQA, Gemini gives the same scores as
`gpt-5.6-luna`. On FRAMES, it gives scores 14 to 29 points lower for eight
of the ten APIs, and the same scores for cloro and SerpApi.** The order of
the APIs on FRAMES does not change, except that Parallel and Perplexity
change places.

"luna only to Gemini only" is the number of questions that only the luna
reader answered correctly, and the number that only the Gemini reader
answered correctly. The p value is from an exact McNemar test. "Not
attempted" includes the failed searches of the published run.

### FRAMES (200 questions)

| API | luna | Gemini | Change | Not attempted, luna to Gemini | luna only to Gemini only | p |
|---|---|---|---|---|---|---|
| cloro | 80.0% | 81.0% | +1.0 | 3 to 7 | 3 to 5 | 0.73 |
| SerpApi | 79.5% | 78.5% | -1.0 | 4 to 11 | 6 to 4 | 0.75 |
| Exa | 65.5% | 51.5% | -14.0 | 38 to 76 | 28 to 0 | < 0.0001 |
| Parallel | 65.0% | 45.0% | -20.0 | 40 to 92 | 43 to 3 | < 0.0001 |
| Perplexity\* | 61.0% | 47.0% | -14.0 | 36 to 89 | 31 to 3 | < 0.0001 |
| Keenable\* | 56.5% | 36.5% | -20.0 | 55 to 111 | 43 to 3 | < 0.0001 |
| Brave | 55.5% | 31.0% | -24.5 | 47 to 124 | 52 to 3 | < 0.0001 |
| You.com | 50.0% | 21.5% | -28.5 | 65 to 146 | 60 to 3 | < 0.0001 |
| Tavily | 44.5% | 19.5% | -25.0 | 76 to 153 | 51 to 1 | < 0.0001 |
| Firecrawl | 43.5% | 15.0% | -28.5 | 76 to 163 | 57 to 0 | < 0.0001 |
| All | 60.1% | 42.6% | -17.4 | | 374 to 25 | < 0.0001 |

Spearman rank correlation of the ten API scores: 0.99. In the published
FRAMES run, Parallel and Perplexity are not significantly different from
each other.

### SimpleQA Verified (200 questions)

| API | luna | Gemini | Not attempted, luna to Gemini | luna only to Gemini only | p |
|---|---|---|---|---|---|
| Perplexity\* | 98.5% | 98.5% | 0 to 0 | 1 to 1 | 1.0 |
| Keenable\* | 97.0% | 97.0% | 1 to 0 | 2 to 2 | 1.0 |
| You.com | 94.0% | 93.5% | 1 to 10 | 1 to 0 | 1.0 |
| Firecrawl | 91.0% | 90.0% | 4 to 14 | 3 to 1 | 0.62 |
| All (799) | 95.1% | 94.7% | | 7 to 4 | 0.55 |

### FreshQA (200 questions)

| API | luna | Gemini | Not attempted, luna to Gemini | luna only to Gemini only | p |
|---|---|---|---|---|---|
| You.com | 85.5% | 86.5% | 10 to 11 | 8 to 10 | 0.81 |
| Perplexity\* | 84.0% | 85.5% | 7 to 8 | 13 to 16 | 0.71 |
| Keenable\* | 87.0% | 83.5% | 7 to 13 | 12 to 5 | 0.14 |
| Firecrawl | 81.0% | 83.5% | 17 to 22 | 8 to 13 | 0.38 |
| All (800) | 84.4% | 84.8% | | 41 to 44 | 0.83 |

## Why the FRAMES scores go down

On 352 of the 374 FRAMES questions that only luna answered correctly, the
Gemini reader replied NOT FOUND. On the other 22 it gave a wrong answer.

On most of these questions, the answer is not in the search results. A
test: are all the words of the gold answer in the text that the reader got?

| Questions | Count | Gold answer in the results |
|---|---|---|
| Both readers correct | 828 | 651 (79%) |
| Only luna correct | 374 | 123 (33%) |
| Only Gemini correct | 25 | 15 (60%) |

The test is approximate: it misses an answer in other words ("12 years"
against "Twelve Years") and an answer that the reader must calculate. But
the difference between 79% and 33% is large. On most of the 374 questions,
luna adds facts from its own memory to the results, and the prompt does not
allow this ("Answer the question using only the search results below").
Examples, all with the answer not in the results:

| API | Question (shortened) | Gold | luna | Gemini |
|---|---|---|---|---|
| Firecrawl | Who wrote the first movie that Chris Columbus ever directed? | David Simkins | David Simkins | NOT FOUND |
| Tavily | Who was the Prime Minister of Canada in the year that the 1965 Best New Artist Grammy winner first appeared on US television? | Lester Pearson | Lester B. Pearson | NOT FOUND |
| Keenable | Two seasons after DeMar DeRozan was traded to the Spurs, who was the leading scorer of the fifth-place team in the West? | Luka Dončić | Luka Dončić | NOT FOUND |
| Tavily | What attraction in Walt Disney World opened exactly 50 years after the park opened? | Remy's Ratatouille Adventure | Remy's Ratatouille Adventure | NOT FOUND |

But Gemini also misses answers that are in the results. On the FRAMES
questions where the gold answer is in the results, Gemini scored lower too:

| Dataset | Gold answer in the results | Questions | luna | Gemini |
|---|---|---|---|---|
| FRAMES | yes | 952 | 81.3% | 70.0% |
| FRAMES | no | 1,038 | 41.2% | 18.0% |
| SimpleQA Verified | yes | 701 | 97.1% | 96.6% |
| SimpleQA Verified | no | 98 | 80.6% | 81.6% |
| FreshQA | yes | 420 | 92.4% | 90.0% |
| FreshQA | no | 380 | 75.5% | 78.9% |

This split is approximate too: a gold answer can be in the results while a
link of the multi-hop chain is not. A manual check of 6 random questions of
the 113 where the gold words are in the results, luna is correct and Gemini
replied NOT FOUND:

| API | Question (shortened) | Full chain in the results? |
|---|---|---|
| Tavily | Which MLB teams did the 1953 Schenectady Blue Jays manager play for? | No: the manager's name is there, his teams are not |
| You.com | Which John Carpenter film before 2015 is the longest? | No: no running times |
| Perplexity | Canadian PM in the year the 1965 Best New Artist first appeared on US TV | No: no result says the Beatles were on US TV in 1964 |
| Exa | Do zebras, giraffes or hippos wean the earliest? | No: only the giraffe's weaning age |
| Parallel | Youngest non-American winner of the Phoenix Open | No: the "Youngest winners" table is cut |
| Perplexity | Letters in the capitals of the 5 most populated countries | Yes: the five capitals are in one table, and Gemini did not count |

In 5 of the 6, luna added a fact from its memory and Gemini kept to the
prompt. In 1 of the 6, Gemini did not join facts that the results hold. The
sample is small, but most of the 81.3% against 70.0% gap is not a Gemini
failure.

Gemini gives fewer wrong answers. When it answers, it is correct more
often:

| Dataset | Reader | Correct | Wrong | Not attempted | Correct when it answers |
|---|---|---|---|---|---|
| FRAMES | luna | 1,202 | 358 | 430 | 77.1% |
| FRAMES | Gemini | 853 | 175 | 962 | 83.0% |
| SimpleQA Verified | luna | 760 | 33 | 6 | 95.8% |
| SimpleQA Verified | Gemini | 757 | 18 | 24 | 97.7% |
| FreshQA | luna | 675 | 84 | 41 | 88.9% |
| FreshQA | Gemini | 678 | 68 | 54 | 90.9% |

The failed searches of the published runs are not in these two tables.

cloro and SerpApi do not lose points because their results usually include
Google's AI Overview, which often gives the full answer. Thus the reader
does not have to add facts.

The [You.com report](../youcom-2026-11/report.md) said that the Gemini
reader replies NOT FOUND "when the answer needs a fact from the results plus
general knowledge". This test shows two causes: on most of the lost
questions, the missing fact is the answer itself, and luna adds it from
memory. On a small part, the facts are in the results and Gemini does not
join them.

## Other Gemini models

Six other Gemini models read the same saved FRAMES results of four APIs:
cloro (the control), and Parallel, Keenable\* and Firecrawl, the APIs with
large drops. 200 questions for each API, 800 for each model. Gemini
(`gemini-pro-latest`) graded every answer. `gemini-flash-latest` is not in
the table: on 2026-11-21 it gave its name as Gemini 3.8 Flash.

| Reader | cloro | Parallel | Keenable\* | Firecrawl | All 800 | Wrong | Not attempted | Correct when it answers | Correct, gold in results (392) | Correct, gold not in results (408) |
|---|---|---|---|---|---|---|---|---|---|---|
| `gpt-5.6-luna` (published) | 80.0% | 65.0% | 56.5% | 43.5% | 61.2% | 136 | 174 | 78.3% | 330 (84.2%) | 160 (39.2%) |
| `gemini-pro-latest` | 81.0% | 45.0% | 36.5% | 15.0% | 44.4% | 72 | 373 | 83.1% | 291 (74.2%) | 64 (15.7%) |
| `gemini-3.1-pro-preview` | 82.0% | 46.0% | 40.0% | 14.5% | 45.6% | 68 | 367 | 84.3% | 298 (76.0%) | 67 (16.4%) |
| `gemini-3.8-flash` | 80.0% | 45.0% | 37.5% | 15.0% | 44.4% | 65 | 380 | 84.5% | 290 (74.0%) | 65 (15.9%) |
| `gemini-4-argon` | 80.5% | 44.0% | 37.0% | 15.0% | 44.1% | 63 | 384 | 84.9% | 288 (73.5%) | 65 (15.9%) |
| `gemini-4-carbon` | 82.5% | 44.5% | 35.0% | 14.0% | 44.0% | 48 | 400 | 88.0% | 289 (73.7%) | 63 (15.4%) |
| `gemini-4-hydrogen` | 80.0% | 41.5% | 34.5% | 13.0% | 42.2% | 62 | 400 | 84.5% | 276 (70.4%) | 62 (15.2%) |
| `gemini-4-neon` | 82.0% | 46.0% | 38.0% | 15.5% | 45.4% | 50 | 387 | 87.9% | 293 (74.7%) | 70 (17.2%) |

All seven Gemini models scored 42.2% to 45.6%, against 61.2% for luna. They
all keep cloro's score and lose 19 to 30 points on the other three APIs.
The best, `gemini-3.1-pro-preview`, is 1.2 points above `gemini-pro-latest`
(13 to 3 questions, p = 0.02). Thus the gap to luna is not from one weak
Gemini model. All the Gemini models keep to "using only the search results"
in the same way: when the answer is not in the results, they answer
correctly on 15% to 17% of the questions, and luna on 39%.

## What other search API benchmarks use

Found on 2026-11-21. Rows marked "code" were read in the harness source.
The other rows come from the published pages.

| Source | Reader | Grader | Control for the reader's memory |
|---|---|---|---|
| Perplexity `search_evals` v0.1 (2025-09, code) | gpt-4.1, one search, 10 results | gpt-4.1, simple-evals prompt | Prompt: "Use ONLY information from the search results. Do NOT use any internal knowledge." One-search FRAMES score: 0.453 |
| Tavily `tavily-search-evals` (2025-06, code) | gpt-4.1 | gpt-4.1 | Prompt: "based solely on the provided list of documents" |
| You.com `web-search-api-evals` (2026-10, code) | gpt-5.6-luna | gpt-5.4-mini, simple-evals prompt | Prompt: "answer based only on information found in the results" |
| Artificial Analysis Search Index (2026) | GPT-5.6 Luna | the same model | A run with no search, and a leak filter |
| AIMultiple agentic search (2026-11) | gpt-5.6-luna | three judges, 2 of 3 must agree | None on the answer |
| Exa API 2.1 (2025-11) | GPT-5 mini | gpt-4o-mini | None |
| Google FRAMES paper (2024-09) | Gemini Pro 1.5 | Gemini Pro 1.5 | A run with no retrieval |

- The most frequent grader is gpt-4.1 with the simple-evals prompt.
- There is no common reader. In 2026, most harnesses use gpt-5.6-luna, and
  none of them checks whether the answer is in the results.
- The usual control for the reader's memory is a run with no search. No
  harness found checks whether the graded answer is in the search results.
- Perplexity's one-search FRAMES score with a strict results-only prompt,
  0.453, is near the 42% to 46% of the Gemini readers in this test.

## Reader selection with the strict prompt

The reader prompt now has the line of the Perplexity harness: "Use ONLY
information from the search results. Do NOT use any internal knowledge."
Eleven readers ran with it. The aim is the reader that answers from its
input only, not the reader with the highest score.

### Test 1: the results of another question

`cloro-other` gives each question the saved cloro results of a different
question. A reader that keeps to its input replies NOT FOUND.

All eleven readers replied NOT FOUND on all 200 FRAMES and all 200 SimpleQA
Verified questions: 0 answers each. With the strict prompt, no reader
answers from memory when the results are on a different subject. Thus this
test does not separate the readers.

### Test 2: real FRAMES results

100 FRAMES questions for each of cloro, Parallel, Keenable\* and Firecrawl,
400 for each reader. Two judges, `gpt-5.6-sol` and `gemini-pro-latest`, read
each answer (not NOT FOUND) with the search results and replied SUPPORTED
(the results alone give the answer, with simple reasoning) or NOT_SUPPORTED
(a fact that the answer needs is not in the results). The judges do not
check whether the answer is true. They agreed on 520 of 562 different
answers (92.5%).

| Reader | Correct | Correct, supported | Correct, not supported | Wrong | Wrong, not supported | Not found | Answers supported (both judges) | Supported, `gpt-5.6-sol` | Supported, `gemini-pro-latest` |
|---|---|---|---|---|---|---|---|---|---|
| `gemini-4-hydrogen` | 162 | 153 | 3 | 29 | 0 | 209 | 95.3% | 98.4% | 95.3% |
| `gemini-4-carbon` | 164 | 154 | 3 | 27 | 0 | 209 | 94.8% | 98.4% | 94.8% |
| `gemini-4-argon` | 171 | 154 | 8 | 29 | 0 | 200 | 91.5% | 96.0% | 91.5% |
| `gemini-4-neon` | 173 | 156 | 7 | 28 | 1 | 199 | 91.0% | 96.0% | 91.0% |
| `gemini-3.1-pro-preview` | 167 | 152 | 5 | 38 | 4 | 195 | 90.2% | 95.6% | 90.2% |
| `gemini-3.8-flash` | 171 | 152 | 6 | 28 | 1 | 201 | 89.9% | 96.5% | 89.9% |
| `gemini-pro-latest` | 168 | 151 | 6 | 39 | 2 | 193 | 89.9% | 95.7% | 90.3% |
| `gemini-3.5-flash-lite` | 147 | 134 | 5 | 41 | 2 | 212 | 88.8% | 94.7% | 90.4% |
| `gemini-3.1-flash-lite` | 170 | 142 | 17 | 69 | 27 | 161 | 74.5% | 80.3% | 75.7% |
| `gpt-5.6-luna` | 197 | 151 | 35 | 67 | 26 | 136 | 70.1% | 76.5% | 70.5% |
| `gpt-4.1` | 185 | 146 | 29 | 86 | 43 | 129 | 66.4% | 72.7% | 67.2% |

"Supported" and "not supported" count the answers where both judges agree.
The last two columns give each judge alone.

- **The strict prompt reduces luna's answers from memory, but does not stop
  them.** On the same 400 answers, luna scored 60.5% with the earlier prompt
  and 49.2% with the strict prompt. With the strict prompt, 61 of its 264
  answers are not supported by the results (35 correct, 26 wrong).
- **`gpt-4.1`, the reader of the Perplexity and Tavily harnesses, does the
  same:** 72 of 271 answers are not supported.
- **The Gemini models keep to the results.** 3 to 12 of their answers are
  not supported. `gemini-4-hydrogen` and `gemini-4-carbon` have the fewest:
  3 each, all correct answers, and no wrong answer that is not supported.
- **The Gemini models use the results as well as luna, except Flash-Lite.**
  Nine of the readers give 146 to 156 correct answers that the results
  support. luna's extra score comes from the answers that the results do not
  support. `gemini-3.5-flash-lite` gives 134: it keeps to the results but
  misses answers that they hold (19 to 1 against `gemini-3.8-flash`,
  p < 0.0001). `gemini-3.1-flash-lite` answers from memory, as luna does.
- **Price per 1M tokens, input and output (Google and OpenAI pricing pages,
  2026-11-21):** `gemini-3.1-flash-lite` $0.25 and $1.50,
  `gemini-3.5-flash-lite` $0.30 and $2.50, `gemini-3.8-flash` $0.75 and
  $3.75 ($1.50 and $7.50 from 2027-01-01), `gemini-4-hydrogen` $1.50 and
  $7.50, `gemini-4-carbon` and `gemini-4-argon` $2 and $10 ($4 and $20 from
  2026-12-01), `gemini-3.1-pro-preview` $2 and $12, `gemini-4-neon` $3 and
  $15, `gpt-5.6-luna` $0.20 and $1.20. The `-latest` names are not on the
  Google price list.
- **Both judges give the same order.** `gpt-5.6-sol`, an OpenAI model, finds
  76.5% of luna's answers supported and 98.4% of the answers of
  `gemini-4-hydrogen` and `gemini-4-carbon`.

## What this means for the benchmark

The reader must answer from the search results only. The benchmark
measures the search API, so an answer from the reader's memory is not a
result of the search API. The reader prompt says this ("Answer the question
using only the search results below").

- **Use a Gemini reader with the strict prompt.** With the strict prompt,
  23% of luna's answers and 27% of `gpt-4.1`'s answers on FRAMES are not
  supported by the search results. For the Gemini models it is 2% to 4%,
  except `gemini-3.1-flash-lite` (18%).
- **Chosen reader: `gemini-3.8-flash`.** It is the least expensive reader
  that keeps to the results and uses them fully. 7 of its 199 answers are
  not supported, against 3 of 191 for `gemini-4-carbon` (p = 0.34) and 8 of
  207 for `gemini-pro-latest` (p = 0.22 against carbon): not significant.
  Its correct answers that the results support are the same as those of
  `gemini-pro-latest` (3 to 2, p = 1.0) and `gemini-4-carbon` (1 to 3,
  p = 0.63). It costs about a third of `gemini-4-carbon`. Its name is a fixed
  version, not a `-latest` name that Google changes at each release.
- **luna does not do what the benchmark needs on FRAMES.** With the earlier
  prompt, on the questions where the answer is not in the results, luna is
  correct on 39% and the Gemini models on 15% to 17%. Most of luna's extra
  FRAMES score comes from its memory.
- **The Gemini models keep to the results.** Seven Gemini models gave
  42.2% to 45.6% on the same 800 FRAMES results. They give fewer wrong
  answers than luna. In the manual check, 1 of 6 NOT FOUND replies was a
  real error: the facts were in the results and Gemini did not join them.
- **On SimpleQA Verified and FreshQA, the reader does not change the
  scores.** The change is on FRAMES only.
- **The order of the APIs on FRAMES does not change, but the gaps do.**
  With Gemini, the gap between cloro and SerpApi and the other eight APIs is
  27.0 to 66.0 points instead of 14.0 to 36.5 on these 200 questions. cloro
  and SerpApi keep their scores because Google's AI Overview often gives the
  full answer.
- **cloro gains from the change and runs this benchmark.** A change of
  reader that makes cloro's lead larger needs this report next to it.
- **A change of reader needs a full rerun of all ten APIs, with no new
  searches.** The saved responses of all ten APIs on the three datasets are
  on disk: in `runs/` and `outputs/` of this repo, and the SimpleQA Verified
  (2026-11-04) and FreshQA (2026-11-05) responses of the first six APIs in
  `outputs/` of the `marketing` repo. They rebuild the published reader
  input exactly: 8,148 of 8,148 for those six APIs.

## Cost

`gemini-pro-latest`: 3,600 reader calls and 3,600 grader calls, plus 18
questions that ran again after an LLM error. The other six models: 4,800
reader calls and 4,800 grader calls. No search calls.

Reader selection (11 readers, strict prompt): 8,800 reader calls and 8,800
grader calls. Judges: 562 answers and 145 answers of the pairwise checks,
each read by `gpt-5.6-sol` and `gemini-pro-latest`.

## Commands

The test folders link `raw/<provider>` to the saved responses: for FRAMES,
`outputs/search-benchmark-frames-2026-11-10/raw/` (cloro, SerpApi, Tavily,
Exa, Parallel, Brave) and `runs/frames-2026-11/raw/` (the other four).

```bash
export READER_MODEL=gemini-pro-latest GRADER_MODEL=gemini-pro-latest
NEW=perplexity-nodata-reread,firecrawl-reread,youcom-reread,keenable-nodata-reread
ALL=cloro-reread,serpapi-reread,tavily-reread,exa-reread,parallel-reread,brave-reread,$NEW
python3 benchmark.py --n 200 --providers $ALL --dataset frames --as-of 2026-11-10 --out outputs/reader-test-2026-11/frames
python3 benchmark.py --n 200 --providers $NEW --dataset simpleqa --out outputs/reader-test-2026-11/simpleqa
python3 benchmark.py --n 200 --providers $NEW --dataset freshqa --as-of 2026-11-05 --out outputs/reader-test-2026-11/freshqa
```

Other Gemini models, on four APIs (the `raw/` links as above):

```bash
for m in gemini-3.1-pro-preview gemini-3.8-flash gemini-4-argon gemini-4-carbon gemini-4-hydrogen gemini-4-neon; do
  READER_MODEL=$m GRADER_MODEL=gemini-pro-latest python3 benchmark.py --n 200 \
    --providers cloro-reread,parallel-reread,keenable-nodata-reread,firecrawl-reread \
    --dataset frames --as-of 2026-11-10 --out outputs/reader-test-2026-11/models/$m/frames
done
```

Reader selection, with the strict prompt in `benchmark.py`. Each reader
folder links `frames/raw/<api>` as above, and `simpleqa/raw/cloro` to
`outputs/search-benchmark-simpleqa-2026-11-04/raw/cloro` of the `marketing`
repo:

```bash
export GRADER_MODEL=gemini-pro-latest
for m in gpt-5.6-luna gpt-4.1 gemini-pro-latest gemini-3.1-pro-preview gemini-3.8-flash \
         gemini-4-argon gemini-4-carbon gemini-4-hydrogen gemini-4-neon \
         gemini-3.5-flash-lite gemini-3.1-flash-lite; do
  READER_MODEL=$m python3 benchmark.py --n 200 --providers cloro-other --dataset frames --as-of 2026-11-10 --out outputs/reader-select-2026-11/$m/frames
  READER_MODEL=$m python3 benchmark.py --n 200 --providers cloro-other --dataset simpleqa --out outputs/reader-select-2026-11/$m/simpleqa
  READER_MODEL=$m python3 benchmark.py --n 100 --providers cloro-reread,parallel-reread,keenable-nodata-reread,firecrawl-reread \
    --dataset frames --as-of 2026-11-10 --out outputs/reader-select-2026-11/$m/frames
done
python3 analysis/grounding.py outputs/reader-select-2026-11 runs/reader-test-2026-11/selection/grounding.json
```

The Gemini answers are in [`results/`](results), those of the other models
in [`results/models/`](results/models), and the reader selection answers and
the judges' verdicts in [`selection/`](selection).
