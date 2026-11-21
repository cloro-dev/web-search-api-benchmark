# Web Search API Benchmark 2026: Tavily vs Exa vs Parallel vs Brave vs SerpApi vs Perplexity vs Firecrawl vs You.com vs Keenable vs cloro

Perplexity, cloro, Parallel, Keenable and Exa are the most accurate web
search APIs for AI agents on short factual questions in this benchmark of 2,182
questions, and the order changes with the question type: cloro scores highest
on recent events, and cloro and SerpApi lead on multi-hop questions by 27 to
64 points.

Accuracy by question type, one search per question, with the 95% interval in
brackets:

| Search API | Short factual: SimpleQA Verified (1,000) | Recent events: FreshQA (358) | Multi-hop: FRAMES (824) |
|---|---|---|---|
| Perplexity Search API\* | 96.9% (95.6-97.8) | 86.0% (82.1-89.2) | 44.2% (40.8-47.6) |
| cloro | 96.4% (95.1-97.4) | 88.5% (84.8-91.4) | 79.9% (77.0-82.5) |
| Parallel | 96.2% (94.8-97.2) | 86.0% (82.1-89.2) | 45.6% (42.3-49.0) |
| Keenable‡ | 96.0% (94.6-97.0) | 84.4% (80.2-87.8) | 34.5% (31.3-37.8) |
| Exa | 95.8% (94.4-96.9) | 86.6% (82.7-89.7) | 49.9% (46.5-53.3) |
| SerpApi | 93.9% (92.2-95.2) | 86.9% (83.0-90.0) | 76.8% (73.8-79.6) |
| Brave Search API | 90.5% (88.5-92.2) | 85.8% (81.8-89.0) | 25.8% (23.0-28.9) |
| You.com† | 89.2% (87.1-91.0) | 84.9% (80.8-88.3) | 22.1% (19.4-25.0) |
| Tavily | 89.2% (87.1-91.0) | 82.7% (78.4-86.2) | 18.1% (15.6-20.9) |
| Firecrawl | 88.8% (86.7-90.6) | 80.2% (75.7-84.0) | 15.8% (13.4-18.4) |

\* Perplexity's searches exclude huggingface.co and kaggle.com, which host
copies of the benchmark datasets. In its first run, without the filter, its
results held the answer from a dataset page on 471 of 1,000 SimpleQA Verified
questions. The other APIs return such a page on a smaller share of questions
and run without the filter; each report has the leak check. The first
Perplexity run is in [its report](runs/perplexity-firecrawl-2026-11/report.md),
and the filtered run in [this report](runs/perplexity-rerun-2026-11/report.md).

† You.com rejects queries longer than 50 words (HTTP 422): 42 FRAMES
questions and 1 SimpleQA Verified question. They count as not attempted.
Without them You.com scores 23.3% on FRAMES. See the
[You.com report](runs/youcom-2026-11/report.md).

‡ Keenable's searches also exclude huggingface.co and kaggle.com. Without the
filter, its results held a dataset page on 206 of 824 FRAMES questions, and
with the earlier reader it scored 88.3% on those and 59.1% on the others. See
the [Keenable report](runs/keenable-2026-11/report.md).

All scores come from the reader `gemini-3.8-flash` with a prompt that forbids
the reader's own knowledge. [How the reader was chosen](#how-the-reader-was-chosen)
says why, and the [rerun report](runs/rerun-2026-11/report.md) has the change
from the earlier reader.

An open benchmark of ten web search APIs for AI agents and RAG pipelines:
accuracy, cost per 1,000 searches and latency of cloro, SerpApi, Tavily, Exa,
Parallel, Brave Search API, Perplexity Search API, Firecrawl, You.com and
Keenable, on SimpleQA
Verified (1,000 questions), FreshQA (358 questions) and FRAMES (824 multi-hop
questions). Every provider got one search per question, the same reader,
`gemini-3.8-flash`, and the same grader, `gemini-pro-latest`, in November 2026. The code,
the settings and every graded answer are in this repo.

## Summary

- **Most accurate on SimpleQA Verified:** Perplexity 96.9%, cloro 96.4%,
  Parallel 96.2%, Keenable 96.0% and Exa 95.8%. The five are within the
  margin of error of each other. SerpApi scored 93.9%, Brave 90.5%, You.com
  and Tavily 89.2%, and Firecrawl 88.8%.
- **Most accurate on FreshQA (questions whose answer changes over time):**
  cloro 88.5%, then SerpApi 86.9%, Exa 86.6%, Parallel and Perplexity 86.0%,
  Brave 85.8%, You.com 84.9%, Keenable 84.4%, Tavily 82.7% and Firecrawl
  80.2%. The gaps from cloro to the next five are not significant.
- **Most accurate on FRAMES (multi-hop questions that need several
  sources):** cloro 79.9%, then SerpApi 76.8%, Exa 49.9%, Parallel 45.6%,
  Perplexity 44.2%, Keenable 34.5%, Brave 25.8%, You.com 22.1%, Tavily 18.1%
  and Firecrawl 15.8%.
- **Lowest cost per 1,000 searches:** Keenable's free tier covers 100,000
  searches a month, so at that volume it costs nothing. Past the free tiers,
  cloro costs $1.92 on a plan for 100,000 searches a month, then Firecrawl
  $3.49, Keenable $4, Parallel, Brave, Tavily, Perplexity and You.com at $5,
  Exa at $7 and SerpApi at $7.25. SerpApi needed two searches on most
  questions.
- **Fastest (p50 search latency):** Keenable 0.27 s, Perplexity 0.34 s, Exa
  0.74 s, You.com 0.83 s, Firecrawl 0.93 s, Brave 1.21 s, Tavily 2.00 s,
  Parallel 2.99 s. cloro (7.96 s) and SerpApi (8.20 s) are the slowest.

## What is the most accurate web search API for AI agents?

On SimpleQA Verified, 1,000 short factual questions, the most accurate web
search APIs in this benchmark were Perplexity (96.9%), cloro (96.4%),
Parallel (96.2%), Keenable (96.0%) and Exa (95.8%). A paired test on the same
questions finds no significant difference between any two of them (p = 0.071
to 0.88). Each of the five was significantly more accurate than SerpApi
(93.9%, p = 0.00023 to 0.037), Brave Search API (90.5%), You.com (89.2%),
Tavily (89.2%) and Firecrawl (88.8%), each at p < 0.0001. Each API got one
search per question, and the same model answered from its results.

Which API is "most accurate" depends on the question type. On questions about
recent events (FreshQA), cloro scores highest, and five APIs are within the
margin of error of it. On multi-hop questions (FRAMES), cloro (79.9%) and
SerpApi (76.8%) lead, and Exa, Parallel, Perplexity, Keenable, Brave,
You.com, Tavily and Firecrawl answer "not found" on 372 to 673 of 824
questions.

## Results table

Accuracy with the 95% Wilson interval, one search per question. Cost is the
list price per 1,000 searches on the plan that covers 100,000 searches a
month. Latency is the p50
of the search request alone, on SimpleQA Verified.

| Search API | SimpleQA Verified (1,000) | FreshQA (358) | FRAMES (824) | $ per 1,000 searches | p50 latency |
|---|---|---|---|---|---|
| Perplexity Search API\* | 96.9% (95.6-97.8) | 86.0% (82.1-89.2) | 44.2% (40.8-47.6) | $5.00 | 0.34 s |
| cloro | 96.4% (95.1-97.4) | 88.5% (84.8-91.4) | 79.9% (77.0-82.5) | $1.92 | 7.96 s |
| Parallel | 96.2% (94.8-97.2) | 86.0% (82.1-89.2) | 45.6% (42.3-49.0) | $5.00 | 2.99 s |
| Keenable‡ | 96.0% (94.6-97.0) | 84.4% (80.2-87.8) | 34.5% (31.3-37.8) | $4.00 | 0.27 s |
| Exa | 95.8% (94.4-96.9) | 86.6% (82.7-89.7) | 49.9% (46.5-53.3) | $7.00 | 0.74 s |
| SerpApi | 93.9% (92.2-95.2) | 86.9% (83.0-90.0) | 76.8% (73.8-79.6) | $7.25 | 8.20 s |
| Brave Search API | 90.5% (88.5-92.2) | 85.8% (81.8-89.0) | 25.8% (23.0-28.9) | $5.00 | 1.21 s |
| You.com† | 89.2% (87.1-91.0) | 84.9% (80.8-88.3) | 22.1% (19.4-25.0) | $5.00 | 0.83 s |
| Tavily | 89.2% (87.1-91.0) | 82.7% (78.4-86.2) | 18.1% (15.6-20.9) | $5.00 | 2.00 s |
| Firecrawl | 88.8% (86.7-90.6) | 80.2% (75.7-84.0) | 15.8% (13.4-18.4) | $3.49 | 0.93 s |

\* and ‡ With huggingface.co and kaggle.com excluded. † Queries over 50
words count as not attempted. See the notes under the first table.

The scores, the change from the earlier reader and the paired tests are in
the [rerun report](runs/rerun-2026-11/report.md). The earlier reports, with
the leak check, the questions with possibly wrong gold answers, the run costs
and the scores of the earlier reader, are in [`runs/`](runs):
[SimpleQA Verified](runs/simpleqa-2026-11/report.md),
[FreshQA](runs/freshqa-2026-11/report.md),
[FRAMES](runs/frames-2026-11/report.md), and You.com and Keenable in their own
reports ([You.com](runs/youcom-2026-11/report.md),
[Keenable](runs/keenable-2026-11/report.md)). The Gemini grades and the Firecrawl
runs on SimpleQA Verified and FreshQA are in the
[regrade report](runs/regrade-gemini-2026-11/report.md). The tests of which parts of a
search result give the accuracy are in the
[sensitivity report](runs/sensitivity-2026-11/report.md).

## Which search API is the most accurate on fresh, time-sensitive questions?

On FreshQA, 358 questions whose answers can change over time (a third of them
with a false premise), cloro (88.5%) scored highest. The gaps to SerpApi
(86.9%, p = 0.29), Exa (86.6%, p = 0.28), Parallel (86.0%, p = 0.11),
Perplexity (86.0%, p = 0.14) and Brave Search API (85.8%, p = 0.087) are not
significant. cloro was significantly more accurate than You.com (84.9%,
p = 0.024), Keenable (84.4%, p = 0.020), Tavily (82.7%, p = 0.0008) and
Firecrawl (80.2%, p < 0.0001).

## Which search API is the most accurate on multi-hop questions?

On FRAMES, 824 questions that need facts from two or more Wikipedia pages,
cloro (79.9%) and SerpApi (76.8%) were the most accurate web search APIs, and
cloro was ahead of SerpApi in the paired test (68 wins to 43, p = 0.022).
Both were ahead of Exa (49.9%), Parallel (45.6%), Perplexity (44.2%),
Keenable (34.5%), Brave Search API (25.8%), You.com (22.1%), Tavily (18.1%)
and Firecrawl (15.8%), each at p < 0.0001. With one search, those eight
answered "not found" on 372 to 673 of the 824 questions, against 28 for cloro
and 62 for SerpApi. When they answered, the eight were correct 86.1% to 91.0%
of the time, and cloro and SerpApi 82.7% and 83.1%. So the gap comes from how
many questions one results page can answer at all. The results of cloro and
SerpApi usually include Google's AI Overview, which often holds the full
answer. FRAMES is usually run with an agent that searches many times; this
run measures one search.

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

SerpApi bills a second search when part of the result loads separately. That
happened on 97% of SimpleQA questions and 75% of FreshQA questions, so a
SimpleQA question cost about 1.97 searches, $14.28 per 1,000 questions. A sync
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
| SerpApi | 250 searches, 50 an hour | Monthly | 250 (a SimpleQA question took about 1.97 searches) | Not stated |
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
cloro costs $1.99 per 1,000 correct SimpleQA answers ($1.92 / 96.4%),
against $3.93 for Firecrawl, $4.17 for Keenable, $5.16 for Perplexity, $5.20
for Parallel, $5.52 for Brave, $5.61 for You.com and Tavily, $7.31 for Exa
and $15.21 for SerpApi (1.97 searches a question). On FreshQA, cloro and
SerpApi are not significantly different, and cloro costs 73% less per search. These figures use the price past the
free tier. Inside Keenable's free tier, 100,000 searches a month, a correct
answer from Keenable costs nothing.

## What is the fastest web search API?

Keenable was the fastest web search API in this benchmark, with a p50 search
latency of 0.27 s on SimpleQA Verified. Perplexity Search API took 0.34 s,
Exa 0.74 s, You.com 0.83 s, Firecrawl 0.93 s, Brave Search API 1.21 s, Tavily 2.00 s and Parallel 2.99 s.
cloro (7.96 s) and SerpApi (8.20 s) were the slowest. These figures come from
runs with no other benchmark at the same time, from one machine, 4 requests in
parallel. Firecrawl ran 1 request at a time, because its rate limit returned
HTTP 429 at 4. The Keenable figure comes from a search-only run with no
other benchmark at the same time.
Latency is the search request only, without the LLM. If you need answers in
under 3 seconds, cloro and SerpApi are not the right choice today.

## Head-to-head results

Paired exact McNemar tests on the same questions. "Wins" is the number of
questions one API answered correctly and the other did not.

| Comparison | SimpleQA Verified | FreshQA | FRAMES |
|---|---|---|---|
| Exa vs Tavily | Exa, 81 wins to 15 (p < 0.0001) | Exa, 28 to 14 (p = 0.044) | Exa, 285 to 23 (p < 0.0001) |
| Brave vs Tavily | no difference (p = 0.29) | no difference (p = 0.099) | Brave, 125 to 61 (p < 0.0001) |
| Exa vs Parallel | no difference (p = 0.63) | no difference (p = 0.81) | Exa, 120 to 85 (p = 0.017) |
| Exa vs Brave | Exa, 72 to 19 (p < 0.0001) | no difference (p = 0.66) | Exa, 218 to 20 (p < 0.0001) |
| Parallel vs Tavily | Parallel, 87 to 17 (p < 0.0001) | no difference (p = 0.058) | Parallel, 265 to 38 (p < 0.0001) |
| Firecrawl vs Tavily | no difference (p = 0.78) | no difference (p = 0.21) | no difference (p = 0.13) |
| cloro vs SerpApi | cloro, 38 to 13 (p = 0.0006) | no difference (p = 0.29) | cloro, 68 to 43 (p = 0.022) |
| cloro vs Tavily | cloro, 88 to 16 (p < 0.0001) | cloro, 29 to 8 (p = 0.0008) | cloro, 521 to 12 (p < 0.0001) |
| cloro vs Brave | cloro, 77 to 18 (p < 0.0001) | no difference (p = 0.087) | cloro, 457 to 12 (p < 0.0001) |
| cloro vs Exa | no difference (p = 0.46) | no difference (p = 0.28) | cloro, 280 to 33 (p < 0.0001) |
| cloro vs Parallel | no difference (p = 0.88) | no difference (p = 0.11) | cloro, 310 to 28 (p < 0.0001) |
| cloro vs Perplexity | no difference (p = 0.51) | no difference (p = 0.14) | cloro, 333 to 39 (p < 0.0001) |
| cloro vs Firecrawl | cloro, 93 to 17 (p < 0.0001) | cloro, 40 to 10 (p < 0.0001) | cloro, 535 to 7 (p < 0.0001) |
| cloro vs You.com | cloro, 88 to 16 (p < 0.0001) | cloro, 21 to 8 (p = 0.024) | cloro, 483 to 7 (p < 0.0001) |
| You.com vs Brave | no difference (p = 0.060) | no difference (p = 0.58) | Brave, 45 to 14 (p < 0.0001) |
| You.com vs Tavily | no difference (p = 1.0) | no difference (p = 0.22) | You.com, 99 to 66 (p = 0.012) |
| cloro vs Keenable | no difference (p = 0.64) | cloro, 26 to 11 (p = 0.020) | cloro, 404 to 30 (p < 0.0001) |
| Keenable vs Exa | no difference (p = 0.86) | no difference (p = 0.15) | Exa, 191 to 64 (p < 0.0001) |
| Keenable vs Perplexity | no difference (p = 0.15) | no difference (p = 0.29) | Perplexity, 156 to 76 (p < 0.0001) |
| Keenable vs Brave | Keenable, 74 to 19 (p < 0.0001) | no difference (p = 0.46) | Keenable, 136 to 65 (p < 0.0001) |

### Tavily vs Exa: which is more accurate?

Exa was more accurate than Tavily on all three datasets: SimpleQA Verified
(95.8% against 89.2%), FreshQA (86.6% against 82.7%, p = 0.044) and FRAMES
(49.9% against 18.1%). Exa was also faster (0.74 s p50 against 2.00 s) and
cost more ($7 against $5 per 1,000 searches).

### What is the best SerpApi alternative?

In this benchmark cloro beat SerpApi on SimpleQA Verified and FRAMES and
matched it on FreshQA, at about a quarter of the price per search: 96.4%
against 93.9% on SimpleQA Verified (paired p = 0.0006), 88.5% against 86.9%
on FreshQA (no significant difference, p = 0.29) and 79.9% against 76.8% on
FRAMES (p = 0.022), at $1.92 against $7.25 per 1,000 searches, and SerpApi
needed a second search on most questions. Both are slow: cloro's p50 latency was
7.96 s and SerpApi's 8.20 s.

## Which search API is best for a RAG pipeline?

This benchmark is a small RAG pipeline: one search, the top 10 results into
the context window, one LLM answer grounded only on those results. For
factual questions, Perplexity, cloro, Parallel, Keenable and Exa gave the
most correct answers. For time-sensitive questions, cloro scored highest,
with SerpApi, Exa, Parallel, Perplexity and Brave within the margin of error.
For multi-hop questions, cloro and SerpApi did. For the lowest cost per
correct answer, cloro. For latency under 1 second, Keenable, Perplexity, Exa or You.com. For the
most free searches, Keenable (100,000 a month). Run the harness on 50
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
grader gave the same results. These tests ran with the earlier reader,
`gpt-5.6-luna`, before the strict prompt. The tables, the preliminary FreshQA
numbers and the commands are in the
[sensitivity report](runs/sensitivity-2026-11/report.md).

## How the benchmark works

Every provider got the same setup:

1. **One search per question.** The query is the question text, unchanged.
   There is no query rewrite, no second search and no page fetch.
2. **10 results,** in the provider's default search mode.
3. **The same reader.** `gemini-3.8-flash` reads at most 30,000 characters
   of search results and gives a short answer from those results only, or
   "NOT FOUND". The prompt says: "Use ONLY information from the search
   results. Do NOT use any internal knowledge." For FreshQA and FRAMES the
   prompt gives today's date, and for FreshQA it asks the reader to point out
   a false premise.
4. **The same grader.** Gemini (`gemini-pro-latest`) grades each answer
   CORRECT, INCORRECT or NOT_ATTEMPTED with the simple-evals grader prompt
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
first byte sent to the last byte received, the sum of both requests when a
provider needs two. All providers ran from the same machine. The first six ran
in the same time window, interleaved question by question, 4 requests at a
time. Perplexity, Firecrawl, You.com and Keenable ran later in November 2026.
On November 21, 2026, `gemini-3.8-flash` read the saved responses of all ten
APIs again, with no new searches. The tables come from that run.

## How the reader was chosen

The reader must answer from the search results only. An answer from its own
memory is not a result of the search API. So the prompt has the line "Use
ONLY information from the search results. Do NOT use any internal
knowledge.", and the reader is the model that keeps to that line best.

We gave 11 reader models the same saved search results for 400 FRAMES
questions. Two judges, `gpt-5.6-sol` and `gemini-pro-latest`, checked each
answer: do the search results alone support it?

| Reader | Answers not supported by the search results |
|---|---|
| `gpt-4.1` | 27% |
| `gpt-5.6-luna` (the earlier reader) | 23% |
| `gemini-3.1-flash-lite` | 18% |
| `gemini-3.8-flash` | 4% |
| Seven other Gemini models | 2% to 4% |

The GPT readers gave the most correct answers on FRAMES because they added
facts from memory. `gemini-3.8-flash` is the least expensive reader that
keeps to the results and uses them fully. The change lowered the FRAMES
scores of cloro and SerpApi by less than 2 points and those of the other
eight APIs by 14 to 30 points. cloro runs this benchmark and gains from the
change, so the [reader test](runs/reader-test-2026-11/report.md) has every
answer and both judges' verdicts.

## Limitations

- **cloro runs this benchmark and sells one of the tested APIs.** That is why
  the code, the prompts, the settings and the graded answers are public. If a
  setting is not fair to a provider, change it and run it again.
- **The reader can answer from its own memory.** The prompt forbids it, and
  `gemini-3.8-flash` keeps to that: 4% of its FRAMES answers in the reader
  test were not supported by the search results. A reader that adds facts
  from memory does not affect every API the same way. It lifts the APIs whose
  results hold part of the answer.
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
  search API.

## Run the benchmark yourself

Python 3.10 or later, no packages to install. Set `GEMINI_API_KEY` and the
keys of the providers you want to test:

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

The reader defaults to `gemini-3.8-flash` and the grader to
`gemini-pro-latest`, the models of the published tables. A run with another
reader is not comparable with the tables: on FRAMES, the reader changed the
scores of eight APIs by 14 to 30 points. Every published grade is a Gemini
grade: do not grade with another model.

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
  format, with no search call. Use it to test another reader model on the
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
- `python3 analysis/analyze.py <run folder> <dataset>` prints per-topic
  accuracy, the questions that 4 or more providers miss, and the leak check
  (all datasets except `simpleqa`).
- `python3 analysis/sensitivity.py <run folder> cloro:cloro-organic` compares
  two result files on the same questions, with an exact McNemar test.

A full SimpleQA run (1,000 questions, 6 providers) used about 7,000 cloro
credits, 1,970 SerpApi searches, 1,000 Tavily credits, $7.00 of Exa, 1,000
Parallel and 1,000 Brave requests, and 12,000 LLM calls.

To add a provider, add a search function to [`benchmark.py`](benchmark.py)
and add it to `PROVIDERS`. The function returns the raw response and a list
of text blocks for the reader.

## FAQ

### Is there an independent benchmark of Tavily, Exa and Brave?

This one is run by cloro, a vendor, and it is reproducible: the harness,
the questions, the settings and all 21,820 graded answers are in this repo.
Each provider got the same single search, the same reader (`gemini-3.8-flash`)
and the same grader, so you can check every result and run it again with your
own keys.

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
their FRAMES answers from memory, and `gemini-3.8-flash` 4%. A reader that
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
Firecrawl ran on November 18, and Gemini graded every answer on the same day.
You.com ran on November 18 and 19, and Keenable on November 20, both graded
by Gemini. On November 21, `gemini-3.8-flash` read the saved responses of
all ten APIs again, and the tables come from that run. Prices were read on
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
