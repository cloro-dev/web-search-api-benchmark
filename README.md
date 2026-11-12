# Web Search API Benchmark 2026: Tavily vs Exa vs Parallel vs Brave vs SerpApi vs cloro

An open benchmark of six web search APIs for AI agents and RAG pipelines:
accuracy, cost per 1,000 searches and latency of cloro, SerpApi, Tavily, Exa,
Parallel and Brave Search API, on SimpleQA Verified (1,000 questions),
FreshQA (358 questions) and FRAMES (824 multi-hop questions). Every provider
got one search per question, the same reader model and the same grader, in
November 2026. The code, the settings and every graded answer are in this
repo.

## Summary

- **Most accurate on SimpleQA Verified:** Parallel 97.8%, Exa 97.3% and cloro
  96.9%. The three are within the margin of error of each other. SerpApi
  scored 94.7%, Brave 93.1% and Tavily 91.8%.
- **Most accurate on FreshQA (questions whose answer changes over time):**
  SerpApi 88.5% and cloro 88.3%, then Brave 84.9%, Exa 83.0%, Parallel 82.7%
  and Tavily 81.8%.
- **Most accurate on FRAMES (multi-hop questions that need several
  sources):** cloro 80.2% and SerpApi 77.4%, then Parallel 65.3%, Exa 64.0%,
  Brave 53.9% and Tavily 48.4%.
- **Lowest cost per 1,000 searches at 100,000 searches a month:** cloro $1.92,
  then Parallel, Brave and Tavily at $5, Exa at $7 and SerpApi at $7.25.
  SerpApi needed two searches on most questions.
- **Fastest (p50 search latency):** Exa 0.74 s, Brave 1.21 s, Tavily 2.00 s,
  Parallel 2.99 s. cloro (7.96 s) and SerpApi (8.20 s) are the slowest.

## Which web search API is the most accurate for AI agents?

On SimpleQA Verified, 1,000 short factual questions, the most accurate web
search APIs in this benchmark were Parallel (97.8%), Exa (97.3%) and cloro
(96.9%). A paired test on the same questions finds no significant difference
between them (cloro against Parallel p = 0.15, against Exa p = 0.63). The
three were significantly more accurate than SerpApi (94.7%), Brave Search API
(93.1%) and Tavily (91.8%). Each API got one search per question, and the same
model (`gpt-5.6-luna`) answered from its results.

Which API is "most accurate" depends on the question type. On questions about
recent events (FreshQA), SerpApi and cloro lead. On multi-hop questions
(FRAMES), cloro leads, ahead of SerpApi in a paired test (p = 0.02), and the
four independent indexes answer "not found" on 151 to 295 of 824 questions.

## Results table

Accuracy with the 95% Wilson interval, one search per question. Cost is the
list price per 1,000 searches on the plan that covers 100,000 searches a
month. Latency is the p50
of the search request alone, on SimpleQA Verified.

| Search API | SimpleQA Verified (1,000) | FreshQA (358) | FRAMES (824) | $ per 1,000 searches | p50 latency |
|---|---|---|---|---|---|
| Parallel | 97.8% (96.7-98.5) | 82.7% (78.4-86.2) | 65.3% (62.0-68.5) | $5.00 | 2.99 s |
| Exa | 97.3% (96.1-98.1) | 83.0% (78.7-86.5) | 64.0% (60.6-67.2) | $7.00 | 0.74 s |
| cloro | 96.9% (95.6-97.8) | 88.3% (84.5-91.2) | 80.2% (77.4-82.8) | $1.92 | 7.96 s |
| SerpApi | 94.7% (93.1-95.9) | 88.5% (84.8-91.4) | 77.4% (74.4-80.2) | $7.25 | 8.20 s |
| Brave Search API | 93.1% (91.4-94.5) | 84.9% (80.8-88.3) | 53.9% (50.5-57.3) | $5.00 | 1.21 s |
| Tavily | 91.8% (89.9-93.3) | 81.8% (77.5-85.5) | 48.4% (45.0-51.8) | $5.00 | 2.00 s |

The full reports, with the paired tests, the leak check, the questions with
possibly wrong gold answers and the run costs, are in [`runs/`](runs):
[SimpleQA Verified](runs/simpleqa-2026-11/report.md),
[FreshQA](runs/freshqa-2026-11/report.md),
[FRAMES](runs/frames-2026-11/report.md). The tests of which parts of a
search result give the accuracy are in the
[sensitivity report](runs/sensitivity-2026-11/report.md).

## Which search API is the most accurate on fresh, time-sensitive questions?

On FreshQA, 358 questions whose answers can change over time (a third of them
with a false premise), SerpApi (88.5%) and cloro (88.3%) were the most accurate
web search APIs, with no difference between them (paired p = 1.0). cloro was
significantly more accurate than Tavily (81.8%, p = 0.0004), Exa (83.0%,
p = 0.0009) and Parallel (82.7%, p = 0.0012). The gap to Brave Search API
(84.9%) was not significant (p = 0.065).

## Which search API is the most accurate on multi-hop questions?

On FRAMES, 824 questions that need facts from two or more Wikipedia pages,
cloro (80.2%) was the most accurate web search API, ahead of SerpApi (77.4%,
paired p = 0.022) and of Parallel (65.3%), Exa (64.0%), Brave Search API
(53.9%) and Tavily (48.4%), each at p < 0.001. With one search, Parallel, Exa,
Brave and Tavily answered "not found" on 151 to 295 questions. Given an
answer, five of the six APIs were correct 78% to 81% of the time, so the gap
comes from how many questions one results page can answer at all. FRAMES is
usually run with an agent that searches many times; this run measures one
search.

## How much does a web search API cost per 1,000 searches?

On each provider's cheapest self-serve plan that covers 100,000 searches a
month, the plan price divided by what the plan includes (list prices read on
November 5, 2026):

| Search API | $ per 1,000 searches | Plan and request | Free tier |
|---|---|---|---|
| cloro | $1.92 | Starter, $250 a month for 650,000 credits, 5 credits a search (async) | 500 credits a month (100 searches) |
| Parallel | $5.00 | Search API, pay as you go, default mode | 5,000 requests a month |
| Brave Search API | $5.00 | Search, $5 per 1,000 requests | $5 of credits a month (1,000 requests) |
| Tavily | $5.00 | Growth, $500 a month for 100,000 basic searches | 1,000 credits a month |
| Exa | $7.00 | Search (auto), pay as you go | $10 of credits a month |
| SerpApi | $7.25 | Searcher, $725 a month for 100,000 searches | 250 searches a month |

SerpApi bills a second search when part of the result loads separately. That
happened on 97% of SimpleQA questions and 75% of FreshQA questions, so a
SimpleQA question cost about 1.97 searches, $14.28 per 1,000 questions. A sync
cloro request costs 7 credits instead of 5, $2.69 per 1,000 searches. Exa's
price matches the `costDollars` field of its own responses
($0.007 a request with highlights). Prices change: check each provider's
pricing page before you buy.

## Which search API gives the most accuracy per dollar?

cloro had the lowest cost per correct answer on SimpleQA Verified and FreshQA.
cloro costs $1.98 per 1,000 correct SimpleQA answers ($1.92 / 96.9%),
against $5.11 for Parallel, $7.19 for Exa, $5.37 for Brave, $5.45 for Tavily
and $15.08 for SerpApi (1.97 searches a question). On FreshQA, cloro and
SerpApi have the same accuracy, and cloro costs 73% less per search.

## How fast is each web search API?

Exa was the fastest web search API in this benchmark, with a p50 search
latency of 0.74 s on SimpleQA Verified. Brave Search API took 1.21 s, Tavily
2.00 s and Parallel 2.99 s. cloro (7.96 s) and SerpApi (8.20 s) were the
slowest. These figures come from runs with no other benchmark at the same
time, 4 requests in parallel, from one machine.
Latency is the search request only, without the LLM. If you need answers in
under 3 seconds, cloro and SerpApi are not the right choice today.

## Head-to-head results

Paired exact McNemar tests on the same questions. "Wins" is the number of
questions one API answered correctly and the other did not.

| Comparison | SimpleQA Verified | FreshQA | FRAMES |
|---|---|---|---|
| Exa vs Tavily | Exa, 72 wins to 17 (p < 0.0001) | no difference (p = 0.67) | Exa, 197 to 69 (p < 0.0001) |
| Brave vs Tavily | no difference (p = 0.25) | no difference (p = 0.12) | Brave, 147 to 102 (p = 0.0052) |
| Exa vs Parallel | no difference (p = 0.38) | no difference (p = 1.0) | no difference (p = 0.48) |
| Exa vs Brave | Exa, 55 to 13 (p < 0.0001) | no difference (p = 0.32) | Exa, 139 to 56 (p < 0.0001) |
| Parallel vs Tavily | Parallel, 72 to 12 (p < 0.0001) | no difference (p = 0.77) | Parallel, 209 to 70 (p < 0.0001) |
| cloro vs SerpApi | cloro, 33 to 11 (p = 0.0013) | no difference (p = 1.0) | cloro, 58 to 35 (p = 0.022) |
| cloro vs Tavily | cloro, 70 to 19 (p < 0.0001) | cloro, 32 to 9 (p = 0.0004) | cloro, 297 to 35 (p < 0.0001) |
| cloro vs Brave | cloro, 50 to 12 (p < 0.0001) | no difference (p = 0.065) | cloro, 248 to 31 (p < 0.0001) |
| cloro vs Exa | no difference (p = 0.63) | cloro, 25 to 6 (p = 0.0009) | cloro, 179 to 45 (p < 0.0001) |
| cloro vs Parallel | no difference (p = 0.15) | cloro, 28 to 8 (p = 0.0012) | cloro, 172 to 49 (p < 0.0001) |

### Tavily vs Exa: which is more accurate?

Exa was more accurate than Tavily on SimpleQA Verified (97.3% against 91.8%)
and on FRAMES (64.0% against 48.4%), and the two tied on FreshQA (83.0%
against 81.8%). Exa was also faster (0.74 s p50 against 2.00 s) and cost more
($7 against $5 per 1,000 searches).

### What is the best SerpApi alternative?

In this benchmark cloro matched or beat SerpApi on every dataset at about a
quarter of the price per search: 96.9% against 94.7% on SimpleQA Verified
(paired p = 0.0013), 88.3%
against 88.5% on FreshQA (no difference) and 80.2% against 77.4% on FRAMES
(paired p = 0.022), at $1.92 against $7.25 per 1,000 searches, and
SerpApi needed a second search on most questions. Both are
slow: cloro's p50 latency was 7.96 s and SerpApi's 8.20 s.

## Which search API is best for a RAG pipeline?

This benchmark is a small RAG pipeline: one search, the top 10 results into
the context window, one LLM answer grounded only on those results. For
factual questions, Parallel, Exa and cloro gave the most correct answers. For
time-sensitive questions, SerpApi and cloro did. For multi-hop questions,
cloro did. For the lowest cost per
correct answer, cloro. For latency under 1 second, Exa. Run the harness on 50
to 100 of your own questions before you choose, because the order changed
between the three datasets.

## Which parts of a search result give the accuracy?

We kept cloro's saved responses for 100 SimpleQA Verified questions and
changed only what the reader could read. The AI Overview gave most of the
accuracy: 99% with it, 86% without it (13 questions lost, none gained,
p < 0.001). The snippets gave most of the rest: the AI Overview and the
snippets alone scored 99% with 37% fewer reader tokens. Titles, links, results
6 to 10, a second results page, the full JSON response and the text of the
result pages added tokens and no significant accuracy. A second reader model and a second
grader gave the same results. The tables, the preliminary FreshQA numbers and
the commands are in the
[sensitivity report](runs/sensitivity-2026-11/report.md).

## How the benchmark works

Every provider got the same setup:

1. **One search per question.** The query is the question text, unchanged.
   There is no query rewrite, no second search and no page fetch.
2. **10 results,** in the provider's default search mode.
3. **The same reader.** One LLM (`gpt-5.6-luna`) reads at most 30,000
   characters of search results and gives a short answer from those results
   only, or "NOT FOUND". For FreshQA and FRAMES the prompt gives today's
   date, and for FreshQA it asks the reader to point out a false premise.
4. **The same grader.** One LLM (`gpt-5.6-sol`) grades each answer CORRECT,
   INCORRECT or NOT_ATTEMPTED with the OpenAI simple-evals grader prompt
   ([`grader_template.txt`](grader_template.txt)), not changed.
5. **The same questions,** shuffled with seed 42.

| Search API | Request | Text given to the reader |
|---|---|---|
| cloro | Search endpoint, country US, 5 credits | Search results with titles, links, snippets and answer blocks |
| SerpApi | `engine=google`, `gl=us`, `hl=en`, `no_cache=true`, plus the follow-up request when part of the page loads separately | Answer blocks, knowledge graph, organic results, related questions |
| Tavily | `search_depth=basic` | title, url, content |
| Exa | `type=auto`, highlights | title, url, highlights |
| Parallel | default mode, objective and query = the question | title, url, excerpts |
| Brave Search API | `extra_snippets=true` | title, url, description, extra snippets |

The answer features that providers sell as separate options (Tavily
`include_answer`, Exa `summary`) are off, because they are not part of a
default search response.

Dropped rows: FreshQA uses the April 21, 2026 test split without fast-changing rows and rows past their review date, which
leaves 358.

Metrics: accuracy is correct answers over all questions, with a failed search
counted as not attempted. Latency is the time of the search request from the
first byte sent to the last byte received, the sum of both requests when a
provider needs two. All providers ran from the same machine in the same time
window, interleaved question by question, 4 requests at a time.

## Limitations

- **cloro runs this benchmark and sells one of the tested APIs.** That is why
  the code, the prompts, the settings and the graded answers are public. If a
  setting is not fair to a provider, change it and run it again.
- **The reader can answer from its own memory.** The prompt forbids it, and
  the same reader is used for every provider, so the effect is the same for
  all of them.
- **Some pages copy benchmark answers.** On SimpleQA, 193 of 1,000 questions
  had a search result that names the dataset. Without those questions the
  order of the providers does not change. Each report has the leak check.
- **Gold answers go stale.** On 30 FreshQA questions most APIs disagree with
  an answer key that may be out of date. Without them the order does not
  change.
- **One search per question measures the search API, not an agent.** A
  multi-step agent that searches many times can get a high score from a weak
  search API.

## Run the benchmark yourself

Python 3.10 or later, no packages to install. Set `OPENAI_API_KEY` and the
keys of the providers you want to test:

| Provider | Key |
|---|---|
| cloro | `CLORO_API_KEY` |
| SerpApi | `SERPAPI_KEY` |
| Tavily | `TAVILY_API_KEY` |
| Exa | `EXA_API_KEY` |
| Parallel | `PARALLEL_API_KEY` |
| Brave | `BRAVE_API_KEY` |

```bash
python3 benchmark.py --providers cloro,serpapi,tavily,exa,parallel,brave --n 1000 --workers 4
```

Run `--n 3` first to find a broken key before you spend the budget.

- `--dataset simpleqa|verticalrtk|freshqa|frames|sealqa|finsearchcomp|obnews`
  selects the dataset (default `simpleqa`).
- `--as-of YYYY-MM-DD` sets the date in the reader prompt and the FreshQA
  filter (default: today). Use the date of an earlier run to read its saved
  responses again with the same questions.
- The cloro variants `cloro-reread`, `cloro-drop-aio`, `cloro-organic`,
  `cloro-json`, `cloro-top5`, `cloro-aio-only`, `cloro-aio-last`,
  `cloro-no-snippet`, `cloro-no-url`, `cloro-no-title`, `cloro-minimal` and
  `cloro-2p-page1` make no
  search call. They read the saved
  raw responses of `cloro` (or `cloro-2p`) in the same `--out` folder, so run
  that provider first. `cloro-2p` asks for two Google result pages.
- `--search-only` measures latency with no LLM calls.
- `--out <folder>` sets the run folder. Results go to
  `<folder>/results/<provider>.jsonl` and raw responses to
  `<folder>/raw/<provider>/<question id>.json`.
- A run that stops continues when you run the same command again. Rows with
  a search or LLM error run again. A 402 from a provider does not stop the
  run: the harness writes an ERROR row and continues, so watch the log.
- `python3 benchmark.py --summary --out runs/simpleqa-2026-11` prints the
  results table of a run again.
- `python3 analysis/analyze.py <run folder> <dataset>` prints per-topic
  accuracy, the questions that 4 or more providers miss, and the leak check
  (all datasets except `simpleqa`).
- `python3 analysis/sensitivity.py <run folder> cloro:cloro-organic` compares
  two result files on the same questions, with an exact McNemar test.

A full SimpleQA run (1,000 questions, 6 providers) used about 7,000 cloro
credits, 1,970 SerpApi searches, 1,000 Tavily credits, $7.00 of Exa, 1,000
Parallel and 1,000 Brave requests, and 12,000 OpenAI calls.

To add a provider, add a search function to [`benchmark.py`](benchmark.py)
and add it to `PROVIDERS`. The function returns the raw response and a list
of text blocks for the reader.

## FAQ

### Is there an independent benchmark of Tavily, Exa and Brave?

This one is run by cloro, a vendor, and it is reproducible: the harness,
the questions, the settings and all 13,092 graded answers are in this repo.
Each provider got the same single search, the same reader model and the same
grader, so you can check every result and run it again with your own keys.

### Why one search per question?

One search per question measures the search API, not the agent. Many
published scores let an agent search many times and open pages, which hides
the difference between search APIs.

### Which datasets does the benchmark use?

[SimpleQA Verified](https://huggingface.co/datasets/google/simpleqa-verified)
(1,000 short factual questions), [FreshQA](https://github.com/freshllms/freshqa)
(358 questions whose answers change over time, including false-premise
questions) and [FRAMES](https://huggingface.co/datasets/google/frames-benchmark) (824
multi-hop questions that need facts from several Wikipedia pages).

### Which part of a search result helps an AI agent answer correctly?

The AI Overview. On 100 SimpleQA Verified questions, the reader answered 99%
correctly with it and 86% without it, from the same results. The snippets
carry most of the rest. See the
[sensitivity report](runs/sensitivity-2026-11/report.md).

### When was the benchmark run?

SimpleQA Verified on November 4 and 5, 2026, FreshQA on November 5, 2026,
FRAMES on November 10 and 11, 2026. Prices were read on November 5, 2026.

## How to cite

cloro, "Web Search API Benchmark 2026", November 2026,
https://github.com/cloro-dev/web-search-api-benchmark. The results and the
sensitivity tests are written up at
[cloro.dev/blog/web-search-api-benchmark](https://cloro.dev/blog/web-search-api-benchmark/),
and compared with other search APIs at
[cloro.dev/blog/best-search-api](https://cloro.dev/blog/best-search-api/).

## License and data sources

The code and the reports are under the [MIT License](LICENSE). The files in
`runs/*/results/` hold the question and answer text of three public datasets.
That text stays under the license of its source:

| Dataset | Source | License | Changes in this repo |
|---|---|---|---|
| SimpleQA Verified | [google/simpleqa-verified](https://huggingface.co/datasets/google/simpleqa-verified) | MIT | None |
| FreshQA | [freshllms/freshqa](https://github.com/freshllms/freshqa), version of April 21, 2026 | Apache-2.0 (repository) | Test split only, without the fast-changing questions and the questions past their review date |
| FRAMES | [google/frames-benchmark](https://huggingface.co/datasets/google/frames-benchmark), `test.tsv` | Apache-2.0 | None |

If you use these datasets, cite their authors as their pages ask: the
SimpleQA Verified technical report, the FreshLLMs paper (arXiv:2310.03214)
and the FRAMES paper (arXiv:2409.12941).
