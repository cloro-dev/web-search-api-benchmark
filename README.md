# Web Search API Benchmark 2026: Tavily vs Exa vs Parallel vs Brave vs SerpApi vs Perplexity vs Firecrawl vs You.com vs Keenable vs cloro

Parallel, Perplexity, Exa, Keenable and cloro are the most accurate web
search APIs for AI agents on short factual questions in this benchmark of 2,182
questions, and the order changes with the question type: SerpApi and cloro
lead on recent events, and cloro scores highest on multi-hop questions.

Accuracy by question type, one search per question, with the 95% interval in
brackets:

| Search API | Short factual: SimpleQA Verified (1,000) | Recent events: FreshQA (358) | Multi-hop: FRAMES (824) |
|---|---|---|---|
| Parallel | 97.8% (96.7-98.5) | 82.1% (77.8-85.7) | 65.7% (62.3-68.8) |
| Perplexity Search API\* | 97.5% (96.3-98.3) | 84.1% (79.9-87.5) | 62.9% (59.5-66.1) |
| Exa | 97.3% (96.1-98.1) | 82.7% (78.4-86.2) | 63.8% (60.5-67.0) |
| Keenable‡ | 97.2% (96.0-98.1) | 83.2% (79.0-86.8) | 56.9% (53.5-60.3) |
| cloro | 97.1% (95.9-98.0) | 88.0% (84.2-91.0) | 80.2% (77.4-82.8) |
| SerpApi | 95.0% (93.5-96.2) | 88.3% (84.5-91.2) | 78.2% (75.2-80.8) |
| Brave Search API | 93.0% (91.2-94.4) | 84.6% (80.5-88.0) | 53.9% (50.5-57.3) |
| You.com† | 93.0% (91.2-94.4) | 84.6% (80.5-88.0) | 51.2% (47.8-54.6) |
| Tavily | 91.7% (89.8-93.3) | 81.3% (76.9-85.0) | 48.2% (44.8-51.6) |
| Firecrawl | 91.7% (89.8-93.3) | 79.9% (75.4-83.7) | 43.4% (40.1-46.9) |

\* Perplexity's searches exclude huggingface.co and kaggle.com, which host
copies of the benchmark datasets. In its first run, without the filter, its
results held the answer from a dataset page on 471 of 1,000 SimpleQA Verified
questions. The other APIs return such a page on a smaller share of questions
and run without the filter; each report has the leak check. The first
Perplexity run is in [its report](runs/perplexity-firecrawl-2026-11/report.md),
and the filtered run in [this report](runs/perplexity-rerun-2026-11/report.md).

† You.com rejects queries longer than 50 words (HTTP 422): 42 FRAMES
questions and 1 SimpleQA Verified question. They count as not attempted.
Without them You.com scores 54.0% on FRAMES. See the
[You.com report](runs/youcom-2026-11/report.md).

‡ Keenable's searches also exclude huggingface.co and kaggle.com. Without the
filter, its results held a dataset page on 206 of 824 FRAMES questions, and
it scored 88.3% on those and 59.1% on the others. Its scores without the
filter are 97.7%, 83.5% and 66.4%. See the
[Keenable report](runs/keenable-2026-11/report.md).

An open benchmark of ten web search APIs for AI agents and RAG pipelines:
accuracy, cost per 1,000 searches and latency of cloro, SerpApi, Tavily, Exa,
Parallel, Brave Search API, Perplexity Search API, Firecrawl, You.com and
Keenable, on SimpleQA
Verified (1,000 questions), FreshQA (358 questions) and FRAMES (824 multi-hop
questions). Every provider got one search per question, the same reader model
and the same grader, Gemini (`gemini-pro-latest`), in November 2026. The code,
the settings and every graded answer are in this repo.

## Summary

- **Most accurate on SimpleQA Verified:** Parallel 97.8%, Perplexity 97.5%,
  Exa 97.3%, Keenable 97.2% and cloro 97.1%. The five are within the margin
  of error of each other. SerpApi scored 95.0%, Brave and You.com 93.0%, and Tavily and
  Firecrawl 91.7%.
- **Most accurate on FreshQA (questions whose answer changes over time):**
  SerpApi 88.3% and cloro 88.0%, then Brave and You.com 84.6%, Perplexity
  84.1%, Keenable 83.2%, Exa 82.7%, Parallel 82.1%, Tavily 81.3% and
  Firecrawl 79.9%.
- **Most accurate on FRAMES (multi-hop questions that need several
  sources):** cloro 80.2%, then SerpApi 78.2%, Parallel 65.7%, Exa 63.8%, Perplexity 62.9%,
  Keenable 56.9%, Brave 53.9%, You.com 51.2%, Tavily 48.2% and Firecrawl 43.4%.
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
search APIs in this benchmark were Parallel (97.8%), Perplexity (97.5%), Exa
(97.3%), Keenable (97.2%) and cloro (97.1%). A paired test on the same
questions finds no significant difference between them (cloro against
Parallel p = 0.30, against Perplexity p = 0.60, against Exa p = 0.87, against
Keenable p = 1.0). Each of the five was significantly
more accurate than SerpApi (95.0%), Brave Search API (93.0%), You.com
(93.0%), Tavily (91.7%) and Firecrawl (91.7%). Each API got one search per question, and the same
model answered from its results.

Which API is "most accurate" depends on the question type. On questions about
recent events (FreshQA), SerpApi and cloro lead. On multi-hop questions
(FRAMES), cloro scores highest (80.2%), and Parallel, Exa, Perplexity,
Keenable, Brave, You.com, Tavily and Firecrawl answer "not found" on 148 to
326 of 824 questions.

## Results table

Accuracy with the 95% Wilson interval, one search per question. Cost is the
list price per 1,000 searches on the plan that covers 100,000 searches a
month. Latency is the p50
of the search request alone, on SimpleQA Verified.

| Search API | SimpleQA Verified (1,000) | FreshQA (358) | FRAMES (824) | $ per 1,000 searches | p50 latency |
|---|---|---|---|---|---|
| Parallel | 97.8% (96.7-98.5) | 82.1% (77.8-85.7) | 65.7% (62.3-68.8) | $5.00 | 2.99 s |
| Perplexity Search API\* | 97.5% (96.3-98.3) | 84.1% (79.9-87.5) | 62.9% (59.5-66.1) | $5.00 | 0.34 s |
| Exa | 97.3% (96.1-98.1) | 82.7% (78.4-86.2) | 63.8% (60.5-67.0) | $7.00 | 0.74 s |
| Keenable‡ | 97.2% (96.0-98.1) | 83.2% (79.0-86.8) | 56.9% (53.5-60.3) | $4.00 | 0.27 s |
| cloro | 97.1% (95.9-98.0) | 88.0% (84.2-91.0) | 80.2% (77.4-82.8) | $1.92 | 7.96 s |
| SerpApi | 95.0% (93.5-96.2) | 88.3% (84.5-91.2) | 78.2% (75.2-80.8) | $7.25 | 8.20 s |
| Brave Search API | 93.0% (91.2-94.4) | 84.6% (80.5-88.0) | 53.9% (50.5-57.3) | $5.00 | 1.21 s |
| You.com† | 93.0% (91.2-94.4) | 84.6% (80.5-88.0) | 51.2% (47.8-54.6) | $5.00 | 0.83 s |
| Tavily | 91.7% (89.8-93.3) | 81.3% (76.9-85.0) | 48.2% (44.8-51.6) | $5.00 | 2.00 s |
| Firecrawl | 91.7% (89.8-93.3) | 79.9% (75.4-83.7) | 43.4% (40.1-46.9) | $3.49 | 0.93 s |

\* and ‡ With huggingface.co and kaggle.com excluded. † Queries over 50
words count as not attempted. See the notes under the first table.

The full reports, with the paired tests, the leak check, the questions with
possibly wrong gold answers and the run costs, are in [`runs/`](runs):
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
with a false premise), SerpApi (88.3%) and cloro (88.0%) were the most accurate
web search APIs, with no difference between them (paired p = 1.0). cloro was
significantly more accurate than Firecrawl (79.9%, p = 0.0001), Tavily
(81.3%, p = 0.0004), Exa (82.7%, p = 0.0009), Parallel (82.1%, p = 0.0011),
Keenable (83.2%, p = 0.0095) and Perplexity (84.1%, p = 0.020). The gaps to Brave Search API (84.6%,
p = 0.065) and You.com (84.6%, p = 0.088) were not significant.

## Which search API is the most accurate on multi-hop questions?

On FRAMES, 824 questions that need facts from two or more Wikipedia pages,
cloro (80.2%) and SerpApi (78.2%) were the most accurate web search APIs. The
paired test finds no significant difference between them (cloro 53 wins to
36, p = 0.089). Both were ahead of Parallel (65.7%), Exa (63.8%), Perplexity
(62.9%), Keenable (56.9%), Brave Search API (53.9%), You.com (51.2%), Tavily
(48.2%) and Firecrawl (43.4%), each at p < 0.001. With one search, Parallel,
Exa, Perplexity, Keenable, Brave, You.com, Tavily and Firecrawl answered "not
found" on 148 to 326 questions. Given an answer, cloro, SerpApi and Parallel
were correct 80.5% to 81.2% of the time and the other seven 71.9% to 77.8%, so most of the gap comes from how many questions
one results page can answer at all. FRAMES is usually run with an agent that
searches many times; this run measures one search.

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
cloro costs $1.98 per 1,000 correct SimpleQA answers ($1.92 / 97.1%),
against $3.81 for Firecrawl, $4.12 for Keenable, $5.11 for Parallel, $5.13 for Perplexity, $5.38
for Brave and You.com, $5.45 for Tavily, $7.19 for Exa and $15.03 for SerpApi (1.97
searches a question). On FreshQA, cloro and SerpApi have the same accuracy,
and cloro costs 73% less per search. These figures use the price past the
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
| Exa vs Tavily | Exa, 72 wins to 16 (p < 0.0001) | no difference (p = 0.56) | Exa, 198 to 69 (p < 0.0001) |
| Brave vs Tavily | no difference (p = 0.25) | no difference (p = 0.081) | Brave, 148 to 101 (p = 0.0035) |
| Exa vs Parallel | no difference (p = 0.36) | no difference (p = 0.86) | no difference (p = 0.32) |
| Exa vs Brave | Exa, 55 to 12 (p < 0.0001) | no difference (p = 0.30) | Exa, 139 to 57 (p < 0.0001) |
| Parallel vs Tavily | Parallel, 73 to 12 (p < 0.0001) | no difference (p = 0.77) | Parallel, 211 to 67 (p < 0.0001) |
| Firecrawl vs Tavily | no difference (p = 1.0) | no difference (p = 0.56) | Tavily, 136 to 97 (p = 0.013) |
| cloro vs SerpApi | cloro, 31 to 10 (p = 0.0015) | no difference (p = 1.0) | no difference (p = 0.089) |
| cloro vs Tavily | cloro, 73 to 19 (p < 0.0001) | cloro, 34 to 10 (p = 0.0004) | cloro, 296 to 32 (p < 0.0001) |
| cloro vs Brave | cloro, 52 to 11 (p < 0.0001) | no difference (p = 0.065) | cloro, 250 to 33 (p < 0.0001) |
| cloro vs Exa | no difference (p = 0.87) | cloro, 25 to 6 (p = 0.0009) | cloro, 179 to 44 (p < 0.0001) |
| cloro vs Parallel | no difference (p = 0.30) | cloro, 30 to 9 (p = 0.0011) | cloro, 170 to 50 (p < 0.0001) |
| cloro vs Perplexity | no difference (p = 0.60) | cloro, 23 to 9 (p = 0.020) | cloro, 197 to 54 (p < 0.0001) |
| cloro vs Firecrawl | cloro, 68 to 14 (p < 0.0001) | cloro, 41 to 12 (p = 0.0001) | cloro, 320 to 17 (p < 0.0001) |
| cloro vs You.com | cloro, 57 to 16 (p < 0.0001) | no difference (p = 0.088) | cloro, 271 to 32 (p < 0.0001) |
| You.com vs Brave | no difference (p = 1.0) | no difference (p = 1.0) | no difference (p = 0.088) |
| You.com vs Tavily | no difference (p = 0.27) | no difference (p = 0.088) | no difference (p = 0.13) |
| cloro vs Keenable | no difference (p = 1.0) | cloro, 28 to 11 (p = 0.0095) | cloro, 241 to 49 (p < 0.0001) |
| Keenable vs Exa | no difference (p = 1.0) | no difference (p = 0.86) | Exa, 147 to 90 (p = 0.0003) |
| Keenable vs Perplexity | no difference (p = 0.66) | no difference (p = 0.74) | Perplexity, 139 to 90 (p = 0.0015) |
| Keenable vs Brave | Keenable, 55 to 13 (p < 0.0001) | no difference (p = 0.51) | no difference (p = 0.12) |

### Tavily vs Exa: which is more accurate?

Exa was more accurate than Tavily on SimpleQA Verified (97.3% against 91.7%)
and on FRAMES (63.8% against 48.2%), and the two tied on FreshQA (82.7%
against 81.3%). Exa was also faster (0.74 s p50 against 2.00 s) and cost more
($7 against $5 per 1,000 searches).

### What is the best SerpApi alternative?

In this benchmark cloro beat SerpApi on SimpleQA Verified and matched it on
FreshQA and FRAMES, at about a quarter of the price per search: 97.1% against
95.0% on SimpleQA Verified (paired p = 0.0015), 88.0% against 88.3% on FreshQA
(no difference) and 80.2% against 78.2% on FRAMES (no significant difference,
p = 0.089), at $1.92 against $7.25 per 1,000 searches, and SerpApi needed a
second search on most questions. Both are slow: cloro's p50 latency was
7.96 s and SerpApi's 8.20 s.

## Which search API is best for a RAG pipeline?

This benchmark is a small RAG pipeline: one search, the top 10 results into
the context window, one LLM answer grounded only on those results. For
factual questions, Parallel, Exa, Perplexity, Keenable and cloro gave the most correct answers. For
time-sensitive questions, SerpApi and cloro did. For multi-hop questions, cloro did. For the lowest cost per
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
grader gave the same results. The tables, the preliminary FreshQA numbers and
the commands are in the
[sensitivity report](runs/sensitivity-2026-11/report.md).

## How the benchmark works

Every provider got the same setup:

1. **One search per question.** The query is the question text, unchanged.
   There is no query rewrite, no second search and no page fetch.
2. **10 results,** in the provider's default search mode.
3. **The same reader.** One LLM reads at most 30,000 characters of search
   results and gives a short answer from those results only, or "NOT FOUND".
   For FreshQA and FRAMES the prompt gives today's date, and for FreshQA it
   asks the reader to point out a false premise.
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

## Limitations

- **cloro runs this benchmark and sells one of the tested APIs.** That is why
  the code, the prompts, the settings and the graded answers are public. If a
  setting is not fair to a provider, change it and run it again.
- **The reader can answer from its own memory.** The prompt forbids it, and
  the same reader is used for every provider, so the effect is the same for
  all of them.
- **Some pages copy benchmark answers.** Every API returned a page of a
  benchmark dataset on some questions. On SimpleQA Verified the first six
  APIs did so on 23 to 117 questions each, Firecrawl on 81, You.com on 120,
  Keenable, without its filter, on 101 and Perplexity, without its filter,
  on 500. On FRAMES, Keenable did so on 206 of 824 questions without its
  filter, and on 46 with it, through Hugging Face mirrors. Without the flagged questions the order of the
  first six does not change. Each report has the leak check.
- **Gold answers go stale.** On 30 FreshQA questions most APIs disagree with
  an answer key that may be out of date. Without them the order does not
  change.
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

The reader and the grader default to Gemini (`gemini-pro-latest`). The
published runs used a different reader model: to run them again, set
`READER_MODEL=gpt-5.6-luna` and `OPENAI_API_KEY`. A run with another reader is
not comparable with the tables above. Every published grade is a Gemini
grade: do not grade with another model. A new API in the tables uses the
`gpt-5.6-luna` reader; on FRAMES the Gemini reader scored You.com 21.4%
against 50.0% on the same results (see the
[You.com report](runs/youcom-2026-11/report.md)).

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

In November 2026. The first six APIs ran SimpleQA Verified on November 4 and
5, FreshQA on November 5 and FRAMES on November 10 and 11. Perplexity and
Firecrawl ran on November 18, and Gemini graded every answer on the same day.
You.com ran on November 18 and 19, and Keenable on November 20, both graded
by Gemini. Prices were read on November 5, on November 18 for Perplexity,
Firecrawl and You.com, and on November 20 for Keenable.

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
