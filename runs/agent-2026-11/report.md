# Search APIs with an agent that searches many times, 2026-11

The other reports in this repo give one search per question. In these runs,
an agent searches up to 10 times per question and chooses each query from the
results that it saw. The questions are multi-step and multi-hop: FRAMES,
DeepSearchQA and BrowseComp.

> **Do not put these scores in one table with the one-search scores of this
> repo.** `claude-haiku-5-5` reads and grades in both, but here the agent
> searches up to 10 times, the questions are different, and the score is
> parity, not accuracy.

## Result

2,024 questions: all 824 FRAMES, all 900 DeepSearchQA and 300 BrowseComp (a
sample, seed 2026). An answer counts only if it is correct and the search
results support it. A DeepSearchQA answer is a list, and its score is F1.

**Parity** is the score of an API divided by the average score of Exa and
Parallel, times 100. The 95% range comes from a bootstrap over the questions,
with the same sample for every API.

| API | Parity (95% range) | Correct and supported | Correct | FRAMES (824) | DeepSearchQA (900) | BrowseComp (300) |
|---|---|---|---|---|---|---|
| Parallel | 103.0 (101.5-104.7) | 70.0 | 79.5 | 78.6 | 65.1 | 61.3 |
| Keenable | 102.3 (99.7-104.9) | 69.5 | 79.7 | 78.6 | 67.3 | 51.3 |
| Exa\* | 97.0 (95.3-98.6) | 65.9 | 77.2 | 79.0 | 60.2 | 47.0 |
| Perplexity | 93.2 (90.4-96.2) | 63.4 | 75.0 | 78.4 | 55.6 | 45.3 |
| **cloro** | **77.1 (74.3-80.0)** | **52.4** | **59.7** | **78.0** | **35.9** | **31.7** |
| Brave Search API | 69.9 (67.0-72.6) | 47.5 | 55.0 | 75.2 | 24.4 | 40.7 |
| Tavily | 69.0 (66.4-71.6) | 46.9 | 57.5 | 73.9 | 32.0 | 17.3 |
| Firecrawl | 65.8 (63.0-68.8) | 44.7 | 58.7 | 74.9 | 26.7 | 16.0 |
| You.com | 60.7 (57.9-63.3) | 41.3 | 50.7 | 71.5 | 19.6 | 23.3 |
| SerpApi (Google) | 54.9 (52.1-57.5) | 37.3 | 42.4 | 71.4 | 14.5 | 12.3 |
| cloro-noaio | 51.5 (49.0-54.2) | 35.0 | 38.9 | 68.3 | 12.7 | 10.7 |
| SerpApi Search Index | 45.1 (42.4-47.8) | 30.7 | 36.8 | 62.7 | 6.8 | 14.3 |

The set columns show answers that are correct and supported.

\* Exa got 12 results per search on 294 questions and 20 on the others. The
agent sees the top 10 in both cases, after the copies of the benchmarks are
removed.

The 948 questions that Haiku never answers in 3 tries without search
(`need_search` in the results files; 360 FRAMES, 308 DeepSearchQA, 280
BrowseComp):

| API | Parity (95% range) | Correct and supported | Correct | FRAMES (360) | DeepSearchQA (308) | BrowseComp (280) |
|---|---|---|---|---|---|---|
| Parallel | 105.5 (102.6-108.1) | 64.6 | 71.5 | 68.6 | 63.1 | 61.1 |
| Keenable | 102.9 (98.6-107.4) | 63.0 | 71.2 | 70.0 | 65.4 | 51.4 |
| Exa\* | 94.5 (91.9-97.5) | 57.9 | 68.0 | 67.2 | 57.4 | 46.4 |
| Perplexity | 93.0 (88.6-97.4) | 57.0 | 66.6 | 68.9 | 53.6 | 45.4 |
| **cloro** | **74.5 (70.0-79.0)** | **45.6** | **51.0** | **68.3** | **33.2** | **30.0** |
| Brave Search API | 72.7 (68.0-77.3) | 44.5 | 51.1 | 65.3 | 25.0 | 39.3 |
| Tavily | 63.1 (59.1-67.4) | 38.6 | 45.8 | 63.3 | 30.3 | 16.1 |
| Firecrawl | 62.2 (57.3-66.8) | 38.1 | 46.8 | 66.9 | 25.3 | 15.0 |
| You.com | 59.9 (55.5-64.2) | 36.7 | 44.5 | 61.4 | 20.6 | 22.5 |
| SerpApi (Google) | 51.3 (47.2-55.7) | 31.4 | 35.9 | 59.7 | 16.2 | 11.8 |
| cloro-noaio | 45.4 (41.3-49.6) | 27.8 | 30.5 | 55.8 | 11.9 | 9.3 |
| SerpApi Search Index | 40.1 (35.9-44.3) | 24.6 | 30.1 | 47.5 | 6.8 | 14.6 |

- **Parallel and Keenable are first.** The gap between them is 0.5 points
  (95% range -1.6 to 2.6), so it is not significant. Keenable is 3.6 points
  ahead of Exa (1.3 to 5.9), and Exa is 2.5 points ahead of Perplexity (0.4
  to 4.7).
- **cloro is fifth.** It is 11.0 points behind Perplexity (8.6 to 13.1). It is
  ahead of Brave by 4.9 points (2.8 to 7.1) and of Tavily by 5.5 points (3.4
  to 7.6). On the 948 questions that need search, cloro and Brave are level:
  1.1 points (-2.2 to 4.3).
- **On FRAMES, cloro is level with the four above it:** 78.0, against 79.0
  for Exa, 78.6 for Parallel and Keenable and 78.4 for Perplexity. No gap is
  significant.
- **The gap is on DeepSearchQA and BrowseComp.** On all questions, cloro is
  13.5 points behind Exa (11.1 to 15.8), 17.1 behind Keenable (14.7 to 19.4)
  and 17.6 behind Parallel (15.2 to 19.8).
- **The AI Overview gives cloro 17.4 points** (15.4 to 19.4). The difference
  is largest on DeepSearchQA (23.2 points) and BrowseComp (21.0 points).
- **SerpApi with one request is like cloro without the AI Overview.** Only 81
  of its 14,763 searches (0.5%) returned an AI Overview, because SerpApi
  loads most of them in a second request that this run does not make. Its
  score, 37.3, is 2.3 points above cloro-noaio and 15.1 points below cloro.
- **Without the AI Overview, each search gives little text.** The agent gets
  only the titles and the snippets of the organic results. It cannot open a
  page. The median text per search for cloro was 4,592 characters with the
  AI Overview and 2,435 without it.
- **On DeepSearchQA, many cloro answers are NOT FOUND:** 378 of 900 with the
  AI Overview, 699 of 900 without it. On FRAMES: 26 and 98 of 824.

## Searches and latency

The time of each search request, from the agent's search tool. It does not
include the wait for a free search slot or the pauses between tries.

| API | p50 / p90 per search | Searches | Per question: FRAMES | DeepSearchQA | BrowseComp |
|---|---|---|---|---|---|
| Parallel | 2.6 / 3.8 s | 9,273 | 2.84 | 5.56 | 6.44 |
| Keenable | 0.3 / 0.7 s | 8,246 | 2.55 | 4.61 | 6.66 |
| Exa | 0.5 / 1.1 s | 8,569 | 2.70 | 4.71 | 7.02 |
| Perplexity | 0.3 / 0.3 s | 8,622 | 2.51 | 4.94 | 7.01 |
| cloro | 13.6 / 28.4 s | 11,405 | 2.96 | 7.25 | 8.15 |
| Brave Search API | 1.3 / 1.6 s | 12,640 | 3.35 | 8.33 | 7.94 |
| Tavily | 2.4 / 4.2 s | 12,476 | 3.24 | 7.86 | 9.11 |
| Firecrawl | 3.7 / 6.6 s | 12,101 | 3.45 | 7.26 | 9.08 |
| You.com | 1.0 / 1.3 s | 12,663 | 3.25 | 8.29 | 8.39 |
| SerpApi (Google) | 1.2 / 6.0 s | 14,763 | 4.23 | 9.37 | 9.48 |
| cloro-noaio | 1.5 / 13.0 s | 15,146 | 4.58 | 9.47 | 9.50 |
| SerpApi Search Index | 1.3 / 2.1 s | 15,767 | 5.18 | 9.62 | 9.45 |

- **Keenable, Exa, Perplexity and Parallel needed the fewest searches.** The agent searches again
  when the results do not hold the answer.
- **cloro is the slowest, because of the AI Overview.** In the cloro run, the
  searches that returned an AI Overview took p50 14.0 s and p90 29.1 s. The
  860 searches without one took p50 1.5 s.

cloro per set:

| API | FRAMES, p50 / p90 | DeepSearchQA | BrowseComp |
|---|---|---|---|
| cloro | 8.6 / 21.6 s | 13.9 / 27.2 s | 16.2 / 44.0 s |
| cloro-noaio | 1.5 / 4.3 s | 1.5 / 13.7 s | 1.5 / 10.2 s |

- **The load did not change the latency.** The two runs overlapped from
  17:40 to 18:25 UTC. In that time, the DeepSearchQA searches of the cloro run
  took p50 14.9 s, against 14.2 s before.
- **The search limit changed during the cloro run:** 10, then 20, then 100
  searches at a time. The run took 332 minutes. The cloro-noaio run took 40
  minutes at 100.

## The run

- **Agent:** `claude-haiku-5-5` in Claude Code headless (`claude -p`) with
  one tool, `search`. Up to 10 searches per question, one at a time. It sees
  the top 10 results of each search, at most 30,000 characters. The prompt:

  > You answer hard questions with web search. Your own knowledge cannot be
  > trusted and does not count.
  > - Call search up to 10 times, one query at a time. Choose each query from
  >   the question and from what the search results show.
  > - Use ONLY information from the search results. Do NOT use any internal
  >   knowledge, not even to fill a gap or to complete a list.
  > - Each fact that the answer needs must be stated in the search results.
  >   You may combine facts from different results, count, calculate and
  >   compare.
  > - If the search results do not show the answer, reply NOT FOUND. Do not
  >   guess. If the question asks for a list, give only the items that the
  >   search results show.
  >
  > When done, reply with JSON only: {"answer": "<the short final answer,
  > list items separated by commas, or NOT FOUND>", "sources": ["<URLs of the
  > results that state the facts you used>"]}

- **Requests.** Each search sends the agent's query unchanged.
  - **cloro:** the same request as `cloro` and `cloro-noaio` in
    `benchmark.py`: `POST https://api.cloro.dev/v1/monitor/google` with
    `country: "US"`, and for `cloro` the AI Overview as markdown. Page 1
    only. The agent sees the AI Overview (for `cloro`), the knowledge graph,
    then the organic results (title, URL, snippet). Unlike `benchmark.py`,
    these runs do not give People Also Ask.
  - **Parallel:** `/v1/search` with the query as `objective` and as the one
    item of `search_queries`, `max_results: 12`. The agent sees the excerpts.
  - **Exa:** `/search` with `type: "auto"`, highlights, 12 or 20 results (see
    the note under the first table). The agent sees the highlights.
  - **Brave Search API:** `/res/v1/web/search` with `count: 20` and
    `extra_snippets`. The agent sees the description and the extra snippets.
  - **Tavily:** `/search` with `search_depth: "basic"` and `max_results: 20`.
    The agent sees the content.
  - **Keenable:** `/v1/search` with `max_results: 10`, huggingface.co and
    kaggle.com excluded. The agent sees the snippets.
  - **You.com:** `/v1/search` with `count: 10`. The agent sees the
    description and the snippets.
  - **Firecrawl:** `/v2/search` with `limit: 10`, no page scraping. The agent
    sees the description.
  - **Perplexity Search API:** `/search` with `max_results: 10`,
    huggingface.co and kaggle.com excluded. The agent sees the snippets.
  - **SerpApi (Google):** the `google` engine with `gl: us`, `hl: en`,
    `no_cache: true`, one request per search (no second request for the AI
    Overview, as in the one-search tables). The agent sees the AI Overview
    when the first response has it, the answer box, the knowledge graph, the
    organic results and the related questions.
  - **SerpApi Search Index:** the `search_index` engine (not SerpApi's Google
    engine in the other reports) with `num: 20`, `gl: us`, `hl: en`. The
    agent sees the snippets.
- **Copies of the benchmarks are removed** from the results: dataset pages
  (huggingface.co datasets and others), pages that hold the question word for
  word, and pages whose URL names BrowseComp or DeepSearchQA.
- **Grading:** Haiku grades FRAMES and BrowseComp with
  [`grader_template.txt`](../../grader_template.txt), the same template as the
  other reports. For DeepSearchQA, it counts the matched, missed and extra
  items, and the score is F1. For a correct answer, a second check reads all
  the pages that the agent saw. The answer counts only if the results state it.
- **Why Haiku can grade:** on 349 saved answers, Haiku agreed with
  `gemini-pro-latest` on 99.2% of BrowseComp, 97.3% of DeepSearchQA (score
  within 0.05) and 91.0% of FRAMES. On FRAMES it is stricter with answers that
  hedge.
- **Failed questions score 0:** 3 in the cloro run, 8 in cloro-noaio, 2 in
  Keenable, 1 in You.com, 3 in Firecrawl, and 0 in
  the other runs. In all but one, the agent gave an answer, but the grader's
  reply had no letter A, B or C. In the other (Firecrawl, ds677), the
  search results of the question were more than the model can read. Each
  failed question costs 0.05 points. 12 of 11,405 searches failed in the
  cloro run. In the other runs, a question with a failed search was run
  again, so no failed search is left.
- **Runs (UTC):** Parallel, Exa, Brave, Tavily and SerpApi Search Index on
  2026-11-23. cloro on 2026-11-27 from 14:35, cloro-noaio from 17:40,
  Keenable from 21:23. You.com and Firecrawl on 2026-11-28 from 00:49.
  Perplexity and SerpApi (Google) on 2026-11-28 from 05:31. The questions have fixed answers, so the days
  between the runs matter little.

## Files

`results/<api>.jsonl`, one line per question:

| Field | What |
|---|---|
| `id` | `frames-N`: row N of [`frames-test.tsv`](../frames-2026-11/data/frames-test.tsv). `dsN`: question N of DeepSearchQA. `bcN`: row N of OpenAI's `browse_comp_test_set.csv` |
| `set` | `frames`, `deepsearchqa` or `browsecomp` |
| `question`, `gold`, `answer`, `search_queries` | The question, the correct answer, the agent's answer and its queries. Not for BrowseComp |
| `correct`, `supported` | The score without and with the support check |
| `need_search` | True for the 948 questions that Haiku never answers without search |
| `searches`, `failed_searches`, `search_latency_s` | The searches of the agent and the time of each search |
| `error` | Why the question failed, or null |

The file names: `parallel`, `keenable`, `exa`, `cloro`, `brave`, `tavily`, `youcom`, `firecrawl`, `perplexity`, `serpapi`, `cloro-noaio`, `serpapi-index`.

**BrowseComp has only IDs and scores.** OpenAI asks that its questions and
answers do not appear online as plain text, so the files do not have the
question, the answer or the queries.

The agent harness is not in this repo.
