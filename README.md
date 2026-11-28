# Web Search API Benchmark 2026: Tavily vs Exa vs Parallel vs Brave vs SerpApi vs Perplexity vs Firecrawl vs You.com vs Keenable vs cloro

cloro, Perplexity, Keenable, Parallel and Exa are the most accurate web
search APIs for AI agents on short factual questions in this benchmark of
2,182 questions. The order changes with the question type: cloro scores
highest on recent events, and on multi-hop questions cloro leads the next API
by 30 points.

Accuracy by question type, one search per question, with the 95% interval in
brackets:

| Search API | Short factual: SimpleQA Verified (1,000) | Recent events: FreshQA (358) | Multi-hop: FRAMES (824) |
|---|---|---|---|
| cloro | 96.5% (95.2-97.5) | 89.7% (86.1-92.4) | 79.1% (76.2-81.8) |
| Perplexity Search API\* | 95.7% (94.3-96.8) | 86.6% (82.7-89.7) | 43.7% (40.3-47.1) |
| Keenable‡ | 95.4% (93.9-96.5) | 84.4% (80.2-87.8) | 34.1% (30.9-37.4) |
| Parallel | 95.0% (93.5-96.2) | 84.1% (79.9-87.5) | 43.6% (40.2-47.0) |
| Exa | 95.0% (93.5-96.2) | 89.1% (85.5-91.9) | 48.9% (45.5-52.3) |
| Brave Search API | 89.7% (87.7-91.4) | 87.2% (83.3-90.2) | 26.3% (23.4-29.4) |
| Tavily | 88.9% (86.8-90.7) | 81.3% (76.9-85.0) | 18.1% (15.6-20.9) |
| You.com† | 88.6% (86.5-90.4) | 86.3% (82.4-89.5) | 23.1% (20.3-26.1) |
| Firecrawl | 88.6% (86.5-90.4) | 80.4% (76.0-84.2) | 16.1% (13.8-18.8) |
| SerpApi§ | 38.9% (35.9-42.0) | 69.0% (64.0-73.6) | 7.9% (6.2-9.9) |

\* Perplexity's searches exclude huggingface.co and kaggle.com, which host
copies of the benchmark datasets. In its first run, without the filter, its
results held the answer from a dataset page on 471 of 1,000 SimpleQA Verified
questions. The other APIs return such a page on a smaller share of questions
and run without the filter; each report has the leak check. The first
Perplexity run is in [its report](runs/perplexity-firecrawl-2026-11/report.md),
and the filtered run in [this report](runs/perplexity-rerun-2026-11/report.md).

† You.com rejects queries longer than 50 words (HTTP 422): 42 FRAMES
questions and 1 SimpleQA Verified question. They count as errors. See the
[You.com report](runs/youcom-2026-11/report.md).

‡ Keenable's searches also exclude huggingface.co and kaggle.com. Without the
filter, its results held a dataset page on 206 of 824 FRAMES questions, and
with an earlier reader it scored 88.3% on those and 59.1% on the others. See
the [Keenable report](runs/keenable-2026-11/report.md).

§ Every API gets one request per search. SerpApi loads most Google AI
Overviews in a second request, which this benchmark does not make. Its first
response had an AI Overview on 15 of 1,000 SimpleQA Verified questions and 2
of 824 FRAMES questions. See
[SerpApi with one request](runs/haiku-2026-11/report.md#serpapi-with-one-request).

One model, `claude-haiku-5-5`, reads the search results and grades every
answer, with a prompt that forbids the reader's own knowledge. The
[Haiku report](runs/haiku-2026-11/report.md) has the scores, the change from
the earlier Gemini scores and the paired tests.

An open benchmark of ten web search APIs for AI agents and RAG pipelines:
accuracy, cost per 1,000 searches and latency of cloro, SerpApi, Tavily, Exa,
Parallel, Brave Search API, Perplexity Search API, Firecrawl, You.com and
Keenable, on SimpleQA Verified (1,000 questions), FreshQA (358 questions) and
FRAMES (824 multi-hop questions). Every provider got one search per question
and the same reader and grader, `claude-haiku-5-5`, in November 2026. A
second track lets an agent search up to 10 times per question. The code, the
settings and every graded answer are in this repo.

## Summary

- **Most accurate on SimpleQA Verified:** cloro 96.5%, Perplexity 95.7%,
  Keenable 95.4%, and Parallel and Exa 95.0%. The five are within the margin
  of error of each other. Brave scored 89.7%, Tavily 88.9%, You.com and
  Firecrawl 88.6%, and SerpApi 38.9% with one request.
- **Most accurate on FreshQA (questions whose answer changes over time):**
  cloro 89.7%, then Exa 89.1%, Brave 87.2%, Perplexity 86.6%, You.com 86.3%,
  Keenable 84.4%, Parallel 84.1%, Tavily 81.3%, Firecrawl 80.4% and SerpApi
  69.0%. The gaps from cloro to the next four are not significant.
- **Most accurate on FRAMES (multi-hop questions that need several
  sources):** cloro 79.1%, then Exa 48.9%, Perplexity 43.7%, Parallel
  43.6%, Keenable 34.1%, Brave 26.3%, You.com 23.1%, Tavily 18.1%,
  Firecrawl 16.1% and SerpApi 7.9%.
- **Most accurate for an agent that searches up to 10 times:** Parallel
  70.0% and Keenable 69.5% (correct and supported by the search results),
  then Exa 65.9% and Perplexity 63.4%. cloro was fifth with 52.4%, ahead of
  Brave 47.5%, Tavily 46.9%, Firecrawl 44.7%, You.com 41.3% and SerpApi
  37.3%. On the FRAMES questions, cloro was level with the four above it.
- **Lowest cost per 1,000 searches:** Keenable's free tier covers 100,000
  searches a month, so at that volume it costs nothing. Past the free tiers,
  cloro costs $1.92 on a plan for 100,000 searches a month, then Firecrawl
  $3.49, Keenable $4, Parallel, Brave, Tavily, Perplexity and You.com at $5,
  Exa at $7 and SerpApi at $7.25.
- **Fastest (p50 search latency):** Keenable 0.27 s, Perplexity 0.34 s, Exa
  0.74 s, You.com 0.83 s, Firecrawl 0.93 s, SerpApi 1.17 s
  (measured in the agent run), Brave 1.21 s, Tavily 2.00 s, Parallel 2.99 s.
  cloro (7.96 s) is the slowest.

## What is the most accurate web search API for AI agents?

On SimpleQA Verified, 1,000 short factual questions, the most accurate web
search APIs in this benchmark were cloro (96.5%), Perplexity (95.7%),
Keenable (95.4%), Parallel (95.0%) and Exa (95.0%). A paired test on the same
questions finds no significant difference between any two of them (p = 0.067
to 1.0). Each of the five was significantly more accurate than Brave Search
API (89.7%), Tavily (88.9%), You.com (88.6%), Firecrawl (88.6%) and SerpApi
(38.9%), each at p < 0.0001. Each API got one search per question, and the
same model answered from its results.

Which API is "most accurate" depends on the question type. On questions about
recent events (FreshQA), cloro scores highest, and four APIs are within the
margin of error of it. On multi-hop questions (FRAMES), cloro (79.1%) leads,
and the other nine answer "not found" on 338 to 739 of 824 questions. For an
agent that searches many times, the order is different again: see
[Which search API is the most accurate for an agent that searches many times?](#which-search-api-is-the-most-accurate-for-an-agent-that-searches-many-times)

## Results table

Accuracy with the 95% Wilson interval, one search per question. Cost is the
list price per 1,000 searches on the plan that covers 100,000 searches a
month. Latency is the p50 of the search request alone, on SimpleQA Verified.

| Search API | SimpleQA Verified (1,000) | FreshQA (358) | FRAMES (824) | $ per 1,000 searches | p50 latency |
|---|---|---|---|---|---|
| cloro | 96.5% (95.2-97.5) | 89.7% (86.1-92.4) | 79.1% (76.2-81.8) | $1.92 | 7.96 s |
| Perplexity Search API\* | 95.7% (94.3-96.8) | 86.6% (82.7-89.7) | 43.7% (40.3-47.1) | $5.00 | 0.34 s |
| Keenable‡ | 95.4% (93.9-96.5) | 84.4% (80.2-87.8) | 34.1% (30.9-37.4) | $4.00 | 0.27 s |
| Parallel | 95.0% (93.5-96.2) | 84.1% (79.9-87.5) | 43.6% (40.2-47.0) | $5.00 | 2.99 s |
| Exa | 95.0% (93.5-96.2) | 89.1% (85.5-91.9) | 48.9% (45.5-52.3) | $7.00 | 0.74 s |
| Brave Search API | 89.7% (87.7-91.4) | 87.2% (83.3-90.2) | 26.3% (23.4-29.4) | $5.00 | 1.21 s |
| Tavily | 88.9% (86.8-90.7) | 81.3% (76.9-85.0) | 18.1% (15.6-20.9) | $5.00 | 2.00 s |
| You.com† | 88.6% (86.5-90.4) | 86.3% (82.4-89.5) | 23.1% (20.3-26.1) | $5.00 | 0.83 s |
| Firecrawl | 88.6% (86.5-90.4) | 80.4% (76.0-84.2) | 16.1% (13.8-18.8) | $3.49 | 0.93 s |
| SerpApi§ | 38.9% (35.9-42.0) | 69.0% (64.0-73.6) | 7.9% (6.2-9.9) | $7.25 | 1.17 s¶ |

\*, †, ‡ and § See the notes under the first table.

¶ The SimpleQA Verified run timed the two SerpApi requests together (8.20 s
p50). The time of the first request alone was not saved. This figure is the
p50 of the 14,763 one-request SerpApi searches of the
[agent run](runs/agent-2026-11/report.md), with the agent's own queries and
40 questions at a time, so it is not measured in the same conditions as the
other rows.

The scores, the change from the Gemini scores, the support check and the
paired tests are in the [Haiku report](runs/haiku-2026-11/report.md). The
earlier reports, with the leak check, the questions with possibly wrong gold
answers, the run costs and the scores of the earlier readers, are in
[`runs/`](runs): [SimpleQA Verified](runs/simpleqa-2026-11/report.md),
[FreshQA](runs/freshqa-2026-11/report.md),
[FRAMES](runs/frames-2026-11/report.md), You.com and Keenable in their own
reports ([You.com](runs/youcom-2026-11/report.md),
[Keenable](runs/keenable-2026-11/report.md)), and the Gemini scores in the
[Gemini rerun report](runs/rerun-2026-11/report.md). The tests of which parts
of a search result give the accuracy are in the
[sensitivity report](runs/sensitivity-2026-11/report.md).

## Which search API is the most accurate on fresh, time-sensitive questions?

On FreshQA, 358 questions whose answers can change over time (a third of them
with a false premise), cloro (89.7%) scored highest. The gaps to Exa (89.1%,
p = 0.85), Brave Search API (87.2%, p = 0.16), Perplexity (86.6%, p = 0.099)
and You.com (86.3%, p = 0.058) are not significant. cloro was significantly
more accurate than Keenable (84.4%, p = 0.0026), Parallel (84.1%,
p = 0.00082), Tavily (81.3%), Firecrawl (80.4%) and SerpApi (69.0%), the
last three at p < 0.0001.

## Which search API is the most accurate on multi-hop questions?

On FRAMES, 824 questions that need facts from two or more Wikipedia pages,
cloro (79.1%) was the most accurate web search API. It was ahead of Exa
(48.9%), Perplexity (43.7%), Parallel (43.6%), Keenable (34.1%), Brave
Search API (26.3%), You.com (23.1%), Tavily (18.1%), Firecrawl (16.1%) and
SerpApi (7.9%), each at p < 0.0001. With one search, the other nine answered
"not found" on 338 to 739 of the 824 questions, against 29 for cloro. When
they answered, all ten were correct 74.7% to 84.1% of the time. So the gap
comes from how many questions one results page can answer at all. cloro's
results usually include Google's AI Overview, which often holds the full
answer. SerpApi returns the AI Overview only in a second request, so with one
request it has it on 2 of 824 questions. FRAMES is usually run with an agent
that searches many times; this run measures one search.

## Which search API is the most accurate for an agent that searches many times?

In separate runs, an agent (`claude-haiku-5-5`) searched up to 10 times per
question on 2,024 multi-step questions, with each of 12 search setups.
Parallel (70.0%) and Keenable (69.5%) were the most accurate, and the gap
between them is not significant. Exa (65.9%) and Perplexity (63.4%) came
next. cloro was fifth: 52.4% of its answers were correct and supported by
the search results, 11.0 points behind Perplexity and 4.9 points ahead of
Brave (47.5%). Both gaps are significant.

On the FRAMES questions, cloro (78.0%) was level with Exa (79.0%), Parallel
(78.6%), Keenable (78.6%) and Perplexity (78.4%): no gap is significant. On
DeepSearchQA and BrowseComp it was far behind them. Without the AI Overview,
cloro fell to 35.0%. SerpApi, with one request per search and so with few AI
Overviews, scored 37.3%. See the [agent report](runs/agent-2026-11/report.md).

| Search API | Parity | Correct and supported (2,024) | FRAMES (824) | DeepSearchQA (900) | BrowseComp (300) | p50 search latency |
|---|---|---|---|---|---|---|
| Parallel | 103.0 | 70.0 | 78.6 | 65.1 | 61.3 | 2.6 s |
| Keenable | 102.3 | 69.5 | 78.6 | 67.3 | 51.3 | 0.3 s |
| Exa | 97.0 | 65.9 | 79.0 | 60.2 | 47.0 | 0.5 s |
| Perplexity Search API | 93.2 | 63.4 | 78.4 | 55.6 | 45.3 | 0.3 s |
| cloro | 77.1 | 52.4 | 78.0 | 35.9 | 31.7 | 13.6 s |
| Brave Search API | 69.9 | 47.5 | 75.2 | 24.4 | 40.7 | 1.3 s |
| Tavily | 69.0 | 46.9 | 73.9 | 32.0 | 17.3 | 2.4 s |
| Firecrawl | 65.8 | 44.7 | 74.9 | 26.7 | 16.0 | 3.7 s |
| You.com | 60.7 | 41.3 | 71.5 | 19.6 | 23.3 | 1.0 s |
| SerpApi (one request) | 54.9 | 37.3 | 71.4 | 14.5 | 12.3 | 1.2 s |
| cloro, no AI Overview | 51.5 | 35.0 | 68.3 | 12.7 | 10.7 | 1.5 s |
| SerpApi Search Index | 45.1 | 30.7 | 62.7 | 6.8 | 14.3 | 1.3 s |

Parity is the score divided by the average of Exa and Parallel, times 100.
The FRAMES, DeepSearchQA and BrowseComp columns are the correct-and-supported
score on each set. The agent ran 40 questions at a time, so its latency is
higher than in the one-search runs. Do not put these scores in one table
with the one-search scores: the task is different.

## How much does a web search API cost per 1,000 searches?

Up to 100,000 searches a month, the cheapest web search API in this
benchmark is Keenable: its free tier covers that volume, so it costs nothing.
Past the free tiers, the cheapest is cloro, at $1.92 per 1,000 searches on a
plan for 100,000 searches a month, and Keenable costs $4. At 200,000 searches
a month Keenable costs $400, $2.00 per 1,000 on average. The table gives each
provider's cheapest self-serve plan that covers 100,000 searches a month, the
plan price divided by what the plan includes (list prices read on November 5,
2026):

| Search API | $ per 1,000 searches | Plan and request | Free tier |
|---|---|---|---|
| cloro | $1.92 | Starter, $250 a month for 650,000 credits, 5 credits a search (async) | 500 credits a month (100 searches) |
| Parallel | $5.00 | Search API, pay as you go, default mode | 5,000 requests a month |
| Brave Search API | $5.00 | Search, $5 per 1,000 requests | $5 of credits a month (1,000 requests) |
| Tavily | $5.00 | Growth, $500 a month for 100,000 basic searches | 1,000 credits a month |
| Exa | $7.00 | Search (auto), pay as you go | $10 of credits a month |
| SerpApi | $7.25 | Searcher, $725 a month for 100,000 searches | 250 searches a month |
| Perplexity Search API | $5.00 | $5 per 1,000 requests (read November 18) | Not found |
| Firecrawl | $3.49 | Standard, $99 a month for 100,000 credits plus 100,000 extra credits at $5 per 2,000; 2 credits a search (read November 18) | 1,000 credits a month (500 searches) |
| You.com | $5.00 | Web Search API, $5 per 1,000 calls, pay as you go (read November 18) | $10 of credit (about 2,000 searches) |
| Keenable | $4.00 | Pay as you go, $4 per 1,000 requests past the free allowance (read November 20) | 100,000 requests a month |

This benchmark makes one SerpApi request per search. SerpApi bills a second
search when the AI Overview loads separately. The earlier runs made that
request on 97% of SimpleQA questions, so a SimpleQA question cost about 1.97
searches, $14.28 per 1,000 questions. A sync
cloro request costs 7 credits instead of 5, $2.69 per 1,000 searches. Exa's
price matches the `costDollars` field of its own responses
($0.007 a request with highlights). Prices change: check each provider's
pricing page before you buy.

## Which web search APIs have a free tier?

Keenable has the largest free tier in this benchmark: 100,000 requests a
month, with no card. Of the six web search APIs of the first run, which all
have a free tier, Exa's monthly tier buys the most searches with the request
used here: $10 of credits a month, about 1,428 searches at $7 per 1,000. Of
the five that say whether they need a card, Parallel and Brave do.

| Search API | Free allowance | Refill | Searches with the benchmark's request | Card needed |
|---|---|---|---|---|
| Keenable | 100,000 requests (read November 20) | Monthly, on the day the organization was created | 100,000 | No (a signup from a disposable or privacy mail domain gets 1,000 until a card is saved) |
| Exa | $10 of credits, plus $10 once after onboarding | Resets to $10 on the 1st of each month | About 1,428 (`auto`, $7 per 1,000) | No |
| Parallel | $5 of credits with a card on file, up to 5,000 requests; up to $80 once at sign-up | Monthly ($5) | 1,000 in the default mode ($5 per 1,000) | Yes, for the $5 |
| Brave Search API | $5 of credits on the Search plan | Monthly | 1,000 ($5 per 1,000) | Yes, "to prevent abuse" |
| Tavily | 1,000 API credits | Monthly | 1,000 basic searches (1 credit each) | No |
| SerpApi | 250 searches, 50 an hour | Monthly | 250 | Not stated |
| Firecrawl | 1,000 credits (read November 18) | Monthly | 500 (2 credits a search) | No |
| You.com | $10 of credit (read November 18) | Not stated | About 2,000 ($5 per 1,000) | Not stated |
| cloro | 500 credits, 1 request at a time | Monthly | 100 at 5 credits (Google Search with the AI Overview); 166 Google searches without it, at 3 credits each | No |

Sources, all read on November 16, 2026:
[exa.ai/pricing](https://exa.ai/pricing),
[parallel.ai/pricing](https://parallel.ai/pricing),
[brave.com/search/api](https://brave.com/search/api/),
[tavily.com/pricing](https://www.tavily.com/pricing) and
[docs.tavily.com/documentation/api-credits](https://docs.tavily.com/documentation/api-credits),
[serpapi.com/pricing](https://serpapi.com/pricing),
[cloro.dev/pricing](https://cloro.dev/pricing/) and the
[cloro billing guide](https://cloro.dev/docs/guides/billing). A sync cloro
request adds 2 credits, so 500 credits make 71 sync searches with the AI
Overview. The Perplexity pricing page shows no free tier for the Search API
(read November 18, 2026). [you.com/pricing](https://you.com/pricing) gives
"$10 free credit = 2,000 searches" and does not say if the credit renews
(read November 18, 2026).
[keenable.ai/pricing](https://keenable.ai/pricing) and
[docs.keenable.ai/credits.md](https://docs.keenable.ai/credits.md) give the
Keenable allowance (read November 20, 2026).

A free tier answers "What is the cheapest web search API?" only up to these
volumes. Past them, the number to compare is the price per 1,000 searches in
[How much does a web search API cost per 1,000 searches?](#how-much-does-a-web-search-api-cost-per-1000-searches).

## Which search API gives the most accuracy per dollar?

cloro had the lowest cost per correct answer on SimpleQA Verified and FreshQA.
cloro costs $1.99 per 1,000 correct SimpleQA answers ($1.92 / 96.5%),
against $3.94 for Firecrawl, $4.19 for Keenable, $5.22 for Perplexity, $5.26
for Parallel, $5.57 for Brave, $5.62 for Tavily, $5.64 for You.com, $7.37
for Exa and $18.64 for SerpApi with one request. On FreshQA, cloro and Exa
are not significantly different, and cloro costs 73% less per search. These
figures use the price past the free tier. Inside Keenable's free tier,
100,000 searches a month, a correct answer from Keenable costs nothing.

## What is the fastest web search API?

Keenable was the fastest web search API in this benchmark, with a p50 search
latency of 0.27 s on SimpleQA Verified. Perplexity Search API took 0.34 s,
Exa 0.74 s, You.com 0.83 s, Firecrawl 0.93 s, Brave Search API 1.21 s, Tavily
2.00 s and Parallel 2.99 s. cloro (7.96 s) was the slowest. These figures
come from runs with no other benchmark at the same time, from one machine, 4
requests in parallel. Firecrawl ran 1 request at a time, because its rate
limit returned HTTP 429 at 4. The Keenable figure comes from a search-only run
with no other benchmark at the same time. Latency is the search request only,
without the LLM.

SerpApi's figure comes from another run. The SimpleQA Verified run made two
SerpApi requests per question and timed them together: 8.20 s p50. With one
request, the p50 was 1.17 s over 14,763 searches in the
[agent run](runs/agent-2026-11/report.md), where the queries come from the
agent and 40 questions ran at a time.

If you need answers in under 3 seconds, cloro is not the right choice today.

## Head-to-head results

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

### Tavily vs Exa: which is more accurate?

Exa was more accurate than Tavily on all three datasets: SimpleQA Verified
(95.0% against 88.9%), FreshQA (89.1% against 81.3%, p = 0.00013) and FRAMES
(48.9% against 18.1%). Exa was also faster (0.74 s p50 against 2.00 s) and
cost more ($7 against $5 per 1,000 searches).

### What is the best SerpApi alternative?

With one request per search, SerpApi has Google's organic results but almost
never the AI Overview, and it scored 38.9% on SimpleQA Verified, 69.0% on
FreshQA and 7.9% on FRAMES. cloro returns the AI Overview in the same request
and scored 96.5%, 89.7% and 79.1%, ahead of SerpApi on all three
(p < 0.0001), at $1.92 against $7.25 per 1,000 searches. If you need the
SerpApi AI Overview, you pay for a second search on most questions.

## Which search API is best for a RAG pipeline?

This benchmark is a small RAG pipeline: one search, the top 10 results into
the context window, one LLM answer grounded only on those results. For
factual questions, cloro, Perplexity, Keenable, Parallel and Exa gave the
most correct answers. For time-sensitive questions, cloro scored highest,
with Exa, Brave, Perplexity and You.com within the margin of error. For
multi-hop questions, cloro did. For the lowest cost per correct answer,
cloro. For latency under 1 second, Keenable, Perplexity, Exa or You.com. For
the most free searches, Keenable (100,000 a month). Run the harness on 50 to
100 of your own questions before you choose, because the order changed
between the three datasets.

## Which parts of a search result give the accuracy?

We kept cloro's saved responses for 100 SimpleQA Verified questions and
changed only what the reader could read. The AI Overview gave most of the
accuracy: 99% with it, 86% without it (13 questions lost, none gained,
p < 0.001). The snippets gave most of the rest: the AI Overview and the
snippets alone scored 99% with 37% fewer reader tokens. Titles, links, results
6 to 10, a second results page, the full JSON response and the text of the
result pages added tokens and no significant accuracy. A second reader model and a second
grader gave the same results. These tests ran with the earlier reader,
`gpt-5.6-luna`, before the strict prompt. The tables, the preliminary FreshQA
numbers and the commands are in the
[sensitivity report](runs/sensitivity-2026-11/report.md).

## How the benchmark works

Every provider got the same setup:

1. **One search per question.** The query is the question text, unchanged.
   There is no query rewrite, no second search and no page fetch.
2. **10 results,** in the provider's default search mode.
3. **The same reader.** `claude-haiku-5-5` reads at most 30,000 characters
   of search results and gives a short answer from those results only, or
   "NOT FOUND". The prompt says: "Use ONLY information from the search
   results. Do NOT use any internal knowledge." For FreshQA and FRAMES the
   prompt gives today's date, and for FreshQA it asks the reader to point out
   a false premise.
4. **The same grader.** `claude-haiku-5-5` grades each answer CORRECT,
   INCORRECT or NOT_ATTEMPTED with the simple-evals grader prompt
   ([`grader_template.txt`](grader_template.txt)), changed in one way: the
   grader writes one short sentence before the letter. FreshQA questions also
   get two rules: a gold target with "OR" lists alternatives, and an answer
   that says a false premise is false is correct. The
   [Haiku report](runs/haiku-2026-11/report.md#the-grader) says why.
5. **The support check.** Haiku then checks each correct answer against the
   search results. The README tables give accuracy; the Haiku report also
   gives the score of correct answers that the results support.
6. **The same questions,** shuffled with seed 42.

| Search API | Request | Text given to the reader |
|---|---|---|
| cloro | Search endpoint, country US, 5 credits | Search results with titles, links, snippets and answer blocks |
| SerpApi | `engine=google`, `gl=us`, `hl=en`, `no_cache=true`, one request (no `engine=google_ai_overview` follow-up) | AI Overview when it is in the first response, answer blocks, knowledge graph, organic results, related questions |
| Tavily | `search_depth=basic` | title, url, content |
| Exa | `type=auto`, highlights | title, url, highlights |
| Parallel | default mode, objective and query = the question | title, url, excerpts |
| Brave Search API | `extra_snippets=true` | title, url, description, extra snippets |
| Perplexity Search API | `/search`, `max_results=10`, huggingface.co and kaggle.com excluded | title, url, snippet |
| Firecrawl | `/v2/search`, `limit=10`, no page scraping | title, url, description |
| You.com | `/v1/search`, `count=10` | title, url, description, snippets |
| Keenable | `/v1/search`, `max_results=10`, default mode (`pro`), huggingface.co and kaggle.com excluded | title, url, snippet |

The answer features that providers sell as separate options (Tavily
`include_answer`, Exa `summary`) are off, because they are not part of a
default search response.

Dropped rows: FreshQA uses the April 21, 2026 test split without fast-changing rows and rows past their review date, which
leaves 358.

Metrics: accuracy is correct answers over all questions, with a failed search
counted as not attempted. Latency is the time of the search request from the
first byte sent to the last byte received. All providers ran from the same
machine. The first six ran
in the same time window, interleaved question by question, 4 requests at a
time. Perplexity, Firecrawl, You.com and Keenable ran later in November 2026.
On November 27 and 28, 2026, `claude-haiku-5-5` read the saved responses of
all ten APIs again, with no new searches, and graded them. The tables come
from that run.

## How the reader was chosen

The reader must answer from the search results only. An answer from its own
memory is not a result of the search API. So the prompt has the line "Use
ONLY information from the search results. Do NOT use any internal
knowledge.", and the reader must keep to that line.

We first gave 11 reader models the same saved search results for 400 FRAMES
questions. Two judges, `gpt-5.6-sol` and `gemini-pro-latest`, checked each
answer: do the search results alone support it?

| Reader | Answers not supported by the search results |
|---|---|
| `gpt-4.1` | 27% |
| `gpt-5.6-luna` (the first reader) | 23% |
| `gemini-3.1-flash-lite` | 18% |
| `gemini-3.8-flash` | 4% |
| Seven other Gemini models | 2% to 4% |

The GPT readers gave the most correct answers on FRAMES because they added
facts from memory. Changing from `gpt-5.6-luna` to `gemini-3.8-flash` lowered
the FRAMES scores of cloro and SerpApi by less than 2 points and those of the
other eight APIs by 14 to 30 points. cloro runs this benchmark and gains from
that change, so the [reader test](runs/reader-test-2026-11/report.md) has
every answer and both judges' verdicts.

`claude-haiku-5-5` replaced `gemini-3.8-flash` on 2026-11-28, so that the
one-search tables and the [agent runs](runs/agent-2026-11/report.md) use one
model. Haiku was not in the reader test. Its FRAMES scores are within 2.5
points of the `gemini-3.8-flash` scores for every API, where a reader that
adds facts from memory moved them by 14 to 30 points. The Haiku support check
finds 3.0% to 9.6% of the correct FRAMES answers of each API not supported by
its results.

## Limitations

- **cloro runs this benchmark and sells one of the tested APIs.** That is why
  the code, the prompts, the settings and the graded answers are public. If a
  setting is not fair to a provider, change it and run it again.
- **The reader can answer from its own memory.** The prompt forbids it.
  Haiku was not in the reader test, but its FRAMES scores are within 2.5
  points of those of `gemini-3.8-flash`, which kept to the results on 96% of
  its answers. A reader that adds facts from memory does not affect every API
  the same way. It lifts the APIs whose results hold part of the answer.
- **One model reads and grades.** Haiku grades answers that Haiku wrote. With
  the changed grader prompt, it agreed with `gemini-pro-latest` on 98.3% to
  98.6% of the FreshQA answers we compared.
- **The support check is noisy when it rejects.** On a second run, 17 of 34
  rejected SimpleQA answers of the top five APIs were SUPPORTED, and 0 of 150
  accepted answers changed. See the
  [Haiku report](runs/haiku-2026-11/report.md#correct-and-supported).
- **Some pages copy benchmark answers.** Every API returned a page of a
  benchmark dataset on some questions. On SimpleQA Verified the first six
  APIs did so on 23 to 117 questions each, Firecrawl on 81, You.com on 120,
  Keenable, without its filter, on 101 and Perplexity, without its filter,
  on 500. On FRAMES, Keenable did so on 206 of 824 questions without its
  filter, and on 46 with it, through Hugging Face mirrors. With the earlier
  reader, the order of the first six did not change without the flagged
  questions. Each report has the leak check.
- **Gold answers go stale.** On 30 FreshQA questions most APIs disagreed with
  an answer key that may be out of date (earlier reader). Without them the
  order did not change.
- **One search per question measures the search API, not an agent.** A
  multi-step agent that searches many times can get a high score from a weak
  search API. The [agent runs](runs/agent-2026-11/report.md) measure that
  case, and their order is different.
- **One request per search is a choice.** It keeps every API on the same
  footing, and it removes most of SerpApi's AI Overviews, which SerpApi loads
  in a second, billed request.

## Run the benchmark yourself

Python 3.10 or later, no packages to install. The reader and the grader run
on Claude Code headless (`claude -p`): install Claude Code and set
`CLAUDE_CODE_OAUTH_TOKEN` (from `claude setup-token`). Set the keys of the
providers you want to test:

| Provider | Key |
|---|---|
| cloro | `CLORO_API_KEY` |
| SerpApi | `SERPAPI_KEY` |
| Tavily | `TAVILY_API_KEY` |
| Exa | `EXA_API_KEY` |
| Parallel | `PARALLEL_API_KEY` |
| Brave | `BRAVE_API_KEY` |
| Perplexity | `PERPLEXITY_API_KEY` |
| Firecrawl | `FIRECRAWL_API_KEY` |
| You.com | `YDC_API_KEY` |
| Keenable | `KEENABLE_API_KEY` |

The reader and the grader default to `claude-haiku-5-5`, the model of the
published tables. A run with another reader is not comparable with the
tables: on FRAMES, a change of reader moved the scores of eight APIs by 14 to
30 points. `READER_MODEL` and `GRADER_MODEL` select another model: a
`gemini*` model uses `GEMINI_API_KEY`, and other models use the OpenAI API.
Add `--support-check` to check each correct answer against the search
results.

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
- `<provider>-reread` (for every API except cloro, which has `cloro-reread`)
  reads the saved raw responses of `<provider>` again in the published
  format, with no search call. `serpapi-single-reread` reads the saved
  SerpApi responses without the AI Overview follow-up. Use it to test another reader model on the
  same results, as in the [reader test](runs/reader-test-2026-11/report.md).
- `cloro-other` gives each question the saved cloro results of a different
  question. A reader that keeps to its input replies NOT FOUND. It tests the
  reader, not an API.
- `--search-only` measures latency with no LLM calls.
- `--out <folder>` sets the run folder. Results go to
  `<folder>/results/<provider>.jsonl` and raw responses to
  `<folder>/raw/<provider>/<question id>.json`.
- A run that stops continues when you run the same command again. Rows with
  a search or LLM error run again. A 402 from a provider does not stop the
  run: the harness writes an ERROR row and continues, so watch the log.
- `python3 benchmark.py --summary --out runs/simpleqa-2026-11` prints the
  results table of a run again.
- `python3 analysis/regrade.py <run folder> <out folder> <model>` grades the
  saved answers of a run again with another grader, with `--dataset freshqa`,
  `--support-check` and `--ids <file>`.
- `python3 analysis/analyze.py <run folder> <dataset>` prints per-topic
  accuracy, the questions that 4 or more providers miss, and the leak check
  (all datasets except `simpleqa`).
- `python3 analysis/sensitivity.py <run folder> cloro:cloro-organic` compares
  two result files on the same questions, with an exact McNemar test.

A full SimpleQA run (1,000 questions, 6 providers) used about 7,000 cloro
credits, 1,000 SerpApi searches with one request (1,970 with the follow-up),
1,000 Tavily credits, $7.00 of Exa, 1,000 Parallel and 1,000 Brave requests,
and 12,000 LLM calls.

To add a provider, add a search function to [`benchmark.py`](benchmark.py)
and add it to `PROVIDERS`. The function returns the raw response and a list
of text blocks for the reader.

## FAQ

### Is there an independent benchmark of Tavily, Exa and Brave?

This one is run by cloro, a vendor, and it is reproducible: the harness,
the questions, the settings and all 21,820 graded answers are in this repo.
Each provider got the same single search and the same reader and grader
(`claude-haiku-5-5`), so you can check every result and run it again with
your own keys.

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

### Which LLM should read the search results in a search API benchmark?

One that answers only from the search results. With a prompt that forbids
outside knowledge, `gpt-5.6-luna` and `gpt-4.1` still gave 23% and 27% of
their FRAMES answers from memory, and `gemini-3.8-flash` 4%. The published
tables use `claude-haiku-5-5`, whose FRAMES scores are within 2.5 points of
those of `gemini-3.8-flash`. A reader that
fills gaps from memory hides weak search results and shrinks the gaps
between APIs. See [How the reader was chosen](#how-the-reader-was-chosen).

### Which part of a search result helps an AI agent answer correctly?

The AI Overview. On 100 SimpleQA Verified questions, the reader answered 99%
correctly with it and 86% without it, from the same results. The snippets
carry most of the rest. See the
[sensitivity report](runs/sensitivity-2026-11/report.md).

### When was the benchmark run?

In November 2026. The first six APIs ran SimpleQA Verified on November 4 and
5, FreshQA on November 5 and FRAMES on November 10 and 11. Perplexity and
Firecrawl ran on November 18.
You.com ran on November 18 and 19, and Keenable on November 20. On
November 27 and 28, `claude-haiku-5-5` read and graded the saved responses
of all ten APIs again, and the tables come from that run. The agent runs ran
from November 23 to 28. Prices were read on
November 5, on November 18 for Perplexity, Firecrawl and You.com, and on
November 20 for Keenable.

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
