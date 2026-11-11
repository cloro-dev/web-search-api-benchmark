# OPE-212: more benchmarks and cloro sensitivity runs

Status: phase 1 and phase 2 running since 2026-11-10. Linear: OPE-212.

## 1. What other search APIs benchmark on

Research done on 2026-11-10 from Google results (cloro) and the vendor pages.

| Benchmark | Size | Tests | Run as | Used by |
|---|---|---|---|---|
| SimpleQA (original) | 4,326 | short facts | one search | Tavily, Linkup, You.com, Tako, Firecrawl |
| SimpleQA Verified | 1,000 | short facts | one search or agent | Parallel, Tavily, us |
| FRAMES | 824 (Apache-2.0) | multi-hop, several sources | one search (You.com, Tako) or agent | Perplexity, You.com, Tako, Exa |
| SealQA (Seal-0, Seal-Hard) | about 111 and 254 | conflicting or noisy results | one search | Tavily, Exa, Linkup |
| FinSearchComp T1, T2, T3 | 635 in all | finance lookups (T1 live prices, T2 simple historical, T3 complex historical) | agent | Parallel, Linkup, You.com, Tako |
| VerticalRTK | 138 to 155 | recent business figures | one search | Tako, us |
| FreshQA | 358 (our filter) | answers that change | one search | us |
| Openbenchmarks company news (OB News Websearch) | 300 (100 public) | recent company facts | one search | independent board |
| BrowseComp | 1,266 | hard multi-hop browsing | agent loop | Perplexity, Parallel, Exa, Artificial Analysis |
| DeepSearchQA | 900 | deep research | agent loop | Perplexity, Parallel, Artificial Analysis |
| HLE (search subset) | 2,158 | expert questions | agent loop | Perplexity |
| WideSearch | 200 | collect a table of entities | agent loop | Perplexity, Parallel, Exa |

Google-results providers in other boards: Serper 82.2% SimpleQA (Tavily
repo), Serper Fast 83% (Linkup), "google_search" 50.1% SimpleQA and 60.0%
FRAMES (You.com repo), a RapidAPI Google endpoint 96.0% on company news and
the lowest multi-hop score (Openbenchmarks). cloro, SerpApi and Bright Data
are on no board.

The agent-loop benchmarks (BrowseComp, DeepSearchQA, HLE, WideSearch) need
a model that searches many times. With one search per question they score
near zero for every provider, so they are out of phase 1.

## 2. Phase 1: cloro sensitivity on SimpleQA

On 100 SimpleQA Verified questions: the first 100 of the seed-42 order,
the same 100 as the published `cloro-noaio` run. If a variant changes the
result, we do the same runs on more questions or on FreshQA and
VerticalRTK. The same reader, grader and
30,000-character cap as the published runs.

| Variant | What the reader gets | New cloro calls | Credits a search (async) | $ per 1,000 |
|---|---|---|---|---|
| A. Published | AI Overview, knowledge graph, organic, People Also Ask | none | 5 | $1.92 |
| A2. Reread (`cloro-reread`) | A, read again on the run day | none (from saved responses) | 5 | $1.92 |
| B. No AI Overview (`cloro-drop-aio`) | A without the AI Overview | none (from saved responses) | 3 | $1.15 |
| C. Organic only (`cloro-organic`) | titles, links, snippets of the organic results | none (from saved responses) | 3 | $1.15 |
| D. Full JSON (`cloro-json`) | the whole `result` object as JSON | none (from saved responses) | 5 | $1.92 |
| E. Page 1, new call (`cloro-2p-page1`) | A, from a new `pages: 2` call, page 1 only | 100 | 7 | $2.69 |
| F. Pages 1 and 2 (`cloro-2p`) | A with up to 20 organic results | same call as E | 7 | $2.69 |

Notes:

- B, C and D use the saved responses of the published SimpleQA run
  (`marketing/outputs/search-benchmark-simpleqa-2026-11-04/raw/cloro`), so
  they cost only LLM tokens and compare the same search results.
- B removes the block from a response that had an AI Overview. A request
  without the AI Overview can return a different page. The 100-question
  `cloro-noaio` run checks that.
- E and F come from the same new call, so the page-2 effect is not mixed
  with the change in results since November 4. E against A shows that drift.
- D: the saved responses are 10,700 characters at the median and 26,500 at
  most, so the whole object fits under the cap.
- The reader samples with the default temperature, so the same context can
  give a different answer. A2 against A measures that noise. B, C and D are
  compared with A2, because they are read on the same day.
- `--as-of 2026-11-04` keeps the question set of the published run. The
  reread gives the same context length as the published run on all 1,000
  questions (and on the 496 FreshQA and VerticalRTK questions).
- With 100 questions, a change is significant (p < 0.05) only when it is
  about 6 points or more: 6 questions flip one way and none flip back, or 8
  flip one way and 1 flips back. A smaller change needs more questions.
- Each comparison gets an exact McNemar test on the paired questions
  (`analysis/sensitivity.py`).

## 3. Phase 2: new single-search benchmarks, all six providers

| Dataset | Rows | License | Notes |
|---|---|---|---|
| FRAMES | 824 | Apache-2.0 | multi-hop; one search with the full question |
| SealQA Seal-Hard | 254 | Apache-2.0 | the 111 Seal-0 rows are a subset, marked in the topic |
| FinSearchComp T2 Global | 119 | CC-BY-4.0 | simple historical lookups; the Greater China rows are in Chinese and T1 needs live prices, so they are not used |
| OB News Websearch public set | 100 | no license given on the Hub | the board scores a private 300; the public 100 contain the gold answers |

1,297 questions in all. Same harness: one search, the same reader and
grader, the date of the run in the reader prompt. cloro runs as A only. The
saved responses let us add B, C and D later with no new search calls. The Openbenchmarks company-search set
(10 questions, set answers, agent loop) does not fit one search, so it is
not used.

## 4. Phase 3 (later, not planned in detail)

An agent loop with a fixed model and a search budget, for BrowseComp and
DeepSearchQA, as Artificial Analysis and the Exa harness do.

## 5. Cost (estimates)

| Phase | Search spend | LLM calls |
|---|---|---|
| 1 | about 700 cloro credits (E and F) | about 600 reader and 600 grader calls |
| 2 | about 6,500 cloro credits (1,297 calls); about 1,300 searches each on Parallel, Exa, Brave and Tavily; about 2,000 SerpApi calls (with AI Overview follow-ups) | about 7,800 reader and 7,800 grader calls |
