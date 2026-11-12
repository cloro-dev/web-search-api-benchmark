# Sensitivity tests: which parts of a search result give the accuracy

Run: 2026-11-10 and 2026-11-11, `benchmark.py`, seed 42. Reader
`gpt-5.6-luna`, grader `gpt-5.6-sol`, unless a section says otherwise. One
search per question. Linear: OPE-213.

## Question

The published runs give each search API one format of its results. For cloro,
that format is the AI Overview, then 10 organic results with title, link and
snippet. These tests change one part of that format at a time, and keep the
search results the same, to find which parts make the reader answer correctly.

## Result

- **The AI Overview gives most of the accuracy.** Without it, accuracy fell
  from 99% to 86% on 100 SimpleQA Verified questions (13 lost, 0 gained,
  p < 0.001). The preliminary FreshQA run and a second reader model show the
  same drop.
- **The snippets give most of the rest.** The AI Overview and the snippets
  alone scored 99% with 37% fewer reader tokens. Titles and links added
  tokens and no accuracy.
- **More results and more text did not add accuracy.** The top 5 results, a
  second results page, the full JSON response and the text of the result
  pages all scored the same as the default format or lower.
- **The checks of the setup pass.** A second reader and a second grader give
  the same results, and a reread of the same results changes the score by 3
  points at most.

On 100 questions, a change is significant only at about 6 points or more.

## Setup

- **Questions.** The first 100 SimpleQA Verified questions in the seed-42
  order, the same 100 as [`runs/simpleqa-2026-11/report-100.md`](../simpleqa-2026-11/report-100.md).
  The FreshQA tests use a partial run, stopped on 2026-11-10. Its numbers are
  preliminary.
- **Same search results.** Most variants make no search call. They read the
  saved raw cloro responses of the published run and change only the text
  given to the reader. The variants are defined in `PROVIDERS` in
  [`benchmark.py`](../../benchmark.py). `cloro-2p` is a new call that asks
  for two result pages, and `cloro-2p-page1` reads only page 1 of the same
  response.
- **Base.** `cloro-reread` is the default cloro format, read again on the
  same day as the variants. It scored the same as the published run (99%,
  0 questions changed).
- **Page text.** [`crawl_pages.py`](../../crawl_pages.py) fetched the page-1
  organic links on 2026-11-10, only where robots.txt allowed the user agent
  `benchmark-crawler/1.0`, and extracted the main text as markdown with
  trafilatura, up to 20,000 characters per page. The 30,000-character context
  cap was lifted for these variants. The page text is not in this repo,
  because it belongs to the sites. `crawl_pages.py` fetches it again.
- **Test.** Exact two-sided McNemar test on the paired questions, with
  [`analysis/sensitivity.py`](../../analysis/sensitivity.py). "Reader tokens"
  is the mean `reader_prompt_tokens` of the result file.

## Variants

| Variant | Text given to the reader |
|---|---|
| `cloro-reread` | Default format: AI Overview, then 10 organic results with title, link and snippet |
| `cloro-drop-aio` | Default format without the AI Overview |
| `cloro-organic` | The 10 organic results only (same text as `cloro-drop-aio`, separate read) |
| `cloro-aio-only` | The AI Overview only |
| `cloro-aio-last` | Default format with the AI Overview after the organic results |
| `cloro-top5` | Default format with the top 5 organic results |
| `cloro-no-snippet` | Default format without the snippets |
| `cloro-no-url` | Default format without the links |
| `cloro-no-title` | Default format without the titles |
| `cloro-minimal` | The AI Overview and the snippets only |
| `cloro-desc-only` | The snippets only |
| `cloro-json` | The full JSON response |
| `cloro-2p`, `cloro-2p-page1` | Two result pages (up to 20 organic results), and page 1 of the same response |
| `cloro-crawl-top-half` | The organic results without the AI Overview, plus the page text of the top half of the links |
| `cloro-crawl-all` | The same, with the page text of all page-1 links |
| `cloro-pages-top5-only` | The page text of the top 5 links only |

## SimpleQA Verified, 100 questions

| Base | Variant | Base correct | Variant correct | Only base correct | Only variant correct | p | Reader tokens (base / variant) |
|---|---|---|---|---|---|---|---|
| cloro (published) | cloro-reread | 99 | 99 | 0 | 0 | 1.00 | 843 / 843 |
| cloro-reread | cloro-drop-aio | 99 | 86 | 13 | 0 | <0.001 | 843 / 747 |
| cloro-drop-aio | cloro-organic | 86 | 89 | 0 | 3 | 0.25 | 747 / 747 |
| cloro-reread | cloro-aio-only | 99 | 95 | 4 | 0 | 0.13 | 843 / 174 |
| cloro-reread | cloro-aio-last | 99 | 99 | 0 | 0 | 1.00 | 843 / 843 |
| cloro-reread | cloro-top5 | 99 | 99 | 0 | 0 | 1.00 | 843 / 549 |
| cloro-reread | cloro-no-snippet | 99 | 96 | 3 | 0 | 0.25 | 843 / 515 |
| cloro-reread | cloro-no-url | 99 | 99 | 0 | 0 | 1.00 | 843 / 623 |
| cloro-reread | cloro-no-title | 99 | 100 | 0 | 1 | 1.00 | 843 / 748 |
| cloro-reread | cloro-minimal | 99 | 99 | 0 | 0 | 1.00 | 843 / 528 |
| cloro-reread | cloro-json | 99 | 99 | 0 | 0 | 1.00 | 843 / 4,605 |
| cloro-2p-page1 | cloro-2p | 98 | 98 | 0 | 0 | 1.00 | 808 / 1,502 |
| cloro-drop-aio | cloro-crawl-top-half | 86 | 91 | 0 | 5 | 0.06 | 747 / 6,239 |
| cloro-reread | cloro-crawl-top-half | 99 | 91 | 8 | 0 | 0.008 | 843 / 6,239 |
| cloro-crawl-top-half | cloro-crawl-all | 91 | 91 | 0 | 0 | 1.00 | 6,239 / 9,733 |
| cloro-aio-only | cloro-desc-only | 95 | 86 | 13 | 4 | 0.049 | 174 / 432 |
| cloro-aio-only | cloro-pages-top5-only | 95 | 84 | 14 | 3 | 0.013 | 174 / 5,871 |
| cloro-desc-only | cloro-pages-top5-only | 86 | 84 | 7 | 5 | 0.77 | 432 / 5,871 |

Reproduce:

```bash
python3 analysis/sensitivity.py runs/sensitivity-2026-11/simpleqa --extra runs/simpleqa-2026-11 \
  cloro:cloro-reread cloro-reread:cloro-drop-aio cloro-reread:cloro-minimal
```

### The AI Overview

The AI Overview is the largest single effect. Without it, 13 questions that
were correct became wrong or "not found", and no question went the other way.
On its own, the AI Overview scored 95%, more than the snippets alone (86%,
p = 0.049) or the text of the top 5 pages alone (84%, p = 0.013), at 174
reader tokens. With the snippets added, it scored 99%. The organic results
never made a question wrong that the AI Overview alone answered correctly.

Without the AI Overview, a cloro search costs 3 credits instead of 5.

### The organic fields

Of the organic fields, only the snippet changed the score. Without snippets,
3 questions became wrong answers (p = 0.25, not significant on 100
questions). Without links or without titles, no question was lost. The
minimal format, the AI Overview and the snippets, scored 99% with 37% fewer
reader tokens than the default format.

### More results and page text

The top 5 results scored the same as the top 10 with 35% fewer reader tokens.
A second results page scored the same as page 1 of the same response. The
full JSON response scored the same at 5.5 times the reader tokens. The
position of the AI Overview did not change the score.

Without the AI Overview, the page text of the top half of the links raised
accuracy from 86% to 91% (p = 0.06), at 8 times the reader tokens. The page
text of all page-1 links scored the same 91%. Both stayed 8 points below the
default format (p = 0.008). The reader got 2.9 pages of the top 4.8 links on
average for the top half, and 4.9 pages of 8.8 links for all links.

| Crawl result, all page-1 links of the 100 questions | Links | Share |
|---|---|---|
| Text extracted | 489 | 56% |
| Disallowed by robots.txt (Facebook 121, Instagram 37, Reddit 14) | 189 | 22% |
| Fetch error (121 of them HTTP 403) | 149 | 17% |
| No text found | 50 | 6% |
| Total | 877 | 100% |

Five of the 100 questions fetched a page on Hugging Face that holds a copy of
SimpleQA. Without those 5 questions, the gain from the page text is 82/95 to
86/95 (p = 0.13).

## FreshQA, preliminary

A partial FreshQA run, stopped on 2026-11-10. The number of questions differs
per comparison.

| Base | Variant | n | Base | Variant | Only base correct | Only variant correct | p |
|---|---|---|---|---|---|---|---|
| cloro (published) | cloro-reread | 261 | 89.7% | 90.4% | 4 | 6 | 0.75 |
| cloro-reread | cloro-drop-aio | 243 | 90.5% | 80.2% | 29 | 4 | <0.001 |
| cloro-reread | cloro-json | 241 | 91.7% | 90.9% | 6 | 4 | 0.75 |
| cloro (published) | cloro-2p | 168 | 89.3% | 89.9% | 2 | 3 | 1.00 |

```bash
python3 analysis/sensitivity.py runs/sensitivity-2026-11/freshqa-preliminary --extra runs/freshqa-2026-11 \
  cloro-reread:cloro-drop-aio
```

## A second reader: `gemini-3.8-flash`

The same 100 saved SimpleQA responses, read by `gemini-3.8-flash` and graded by
`gpt-5.6-sol`.

| Variant | GPT reader | Gemini reader |
|---|---|---|
| Default format (`cloro-reread`) | 99% | 98% |
| No AI Overview | 86% | 83% |
| Full JSON | 99% | 98% |
| Top 5 organic | 99% | 98% |
| AI Overview only | 95% | 95% |

With the Gemini reader, removing the AI Overview cost 15 points (15 lost,
0 gained, p < 0.001), and the other variants changed by 3 points or less.
Without the AI Overview, Gemini declined to answer more often and GPT guessed
more often: Gemini had 17 not attempted and 0 wrong answers, GPT had 8 not
attempted and 6 wrong.

```bash
python3 analysis/sensitivity.py runs/sensitivity-2026-11/simpleqa-gemini-reader cloro-reread:cloro-drop-aio
```

## A second grader: `gemini-3.1-pro-preview`

The 6,100 saved answers of the published SimpleQA run (1,000 questions for
each of the six APIs, plus 100 cloro answers without the AI Overview) were
graded again by `gemini-3.1-pro-preview`. The answers did not change.

| Search API | n | `gpt-5.6-sol` | `gemini-3.1-pro-preview` | Same grade |
|---|---|---|---|---|
| Parallel | 1,000 | 97.8% | 97.8% | 99.7% |
| Exa | 1,000 | 97.3% | 97.4% | 99.5% |
| cloro | 1,000 | 96.9% | 97.2% | 99.7% |
| SerpApi | 1,000 | 94.7% | 94.8% | 99.8% |
| Brave Search API | 1,000 | 93.1% | 93.1% | 100% |
| Tavily | 1,000 | 91.8% | 91.8% | 99.8% |
| cloro, no AI Overview | 100 | 89.0% | 88.0% | 99.0% |

The two graders gave the same grade on 99.7% of the answers (Cohen's kappa
0.972), and the order of the six APIs did not change. Most of the 16
disagreements are borderline, for example "12.27%" against a gold answer of
12.27.

The grades are in `simpleqa-regrade-gemini-pro/results/`, with the same ids
as `runs/simpleqa-2026-11/results/`.

## Not in this report

- **VerticalRTK.** The dataset was removed from the benchmark, so its
  sensitivity runs are not published.
- **Questions after the first 100.** Five variants also ran on part of the
  next questions. Those partial runs are not published.
- **The knowledge graph and People Also Ask.** These blocks were almost always
  empty in the saved responses (knowledge graph in 0 of 1,000 SimpleQA
  responses, People Also Ask answer text in 1), so their effect cannot be
  tested here.

## Files

| Folder | Content |
|---|---|
| `simpleqa/results/` | The SimpleQA variants, 100 questions each |
| `freshqa-preliminary/results/` | The partial FreshQA variants |
| `simpleqa-gemini-reader/results/` | The SimpleQA variants read by `gemini-3.8-flash` |
| `simpleqa-regrade-gemini-pro/results/` | The published SimpleQA answers graded by `gemini-3.1-pro-preview` |

A result file can have more than one line for an id when a row was run again.
The last line for an id is the one that counts, as in
`analysis/sensitivity.py`.
