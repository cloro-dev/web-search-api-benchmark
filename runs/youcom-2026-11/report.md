# You.com Web Search API, added on 2026-11-18

> **Earlier reader.** The scores in this report come from the earlier reader,
> `gpt-5.6-luna`, with the earlier reader prompt. The published scores use
> `gemini-3.8-flash` with a prompt that allows only the search results: see the
> [rerun report](../rerun-2026-11/report.md) and the
> [reader test](../reader-test-2026-11/report.md). The search responses, the
> latencies and the counts that do not depend on the reader stay valid.

Run: 2026-11-18 and 2026-11-19, `benchmark.py --providers youcom`, seed 42,
`--workers 4`. The questions, the reader (`gpt-5.6-luna`), the reader prompt
and the `--as-of` dates (FRAMES 2026-11-10, FreshQA 2026-11-05) are the same
as for the other eight APIs. Gemini (`gemini-pro-latest`) graded every answer.
The results are next to the other APIs' results in
`runs/<dataset>-2026-11/results/youcom.jsonl`.

- **Request:** `POST https://ydc-index.io/v1/search` with `query` (the
  question text, unchanged) and `count=10`. No other parameters: the default
  search mode, with no country, freshness or content extraction.
- **Reader input:** the title, URL, description and snippets of each web
  result.

**This run is not interleaved with the first six APIs.** It ran 8 to 14 days
after them. SimpleQA Verified and FRAMES have fixed answers, so the gap
matters little for them. On FreshQA, some answers can change in two weeks.

## Result

| Dataset | Questions | You.com | 95% interval | Not attempted | Search errors | p50 latency |
|---|---|---|---|---|---|---|
| SimpleQA Verified | 1,000 | 93.0% | 91.2-94.4 | 15 | 1 | 0.83 s |
| FreshQA | 358 | 84.6% | 80.5-88.0 | 16 | 0 | 0.82 s |
| FRAMES | 824 | 51.2% | 47.8-54.6 | 220 | 42 | 0.88 s |

You.com scored the same as Brave Search API on SimpleQA Verified (93.0%) and
FreshQA (84.6%). On FRAMES it scored between Brave (53.9%) and Tavily
(48.2%). Its p50 search latency, 0.83 s on SimpleQA Verified, is the third
lowest of the nine APIs, after Perplexity (0.34 s) and Exa (0.74 s).

## Queries longer than 50 words

The You.com API returns `HTTPError 422` for every query longer than 50 words.
All 43 failed queries have 51 to 130 words, and every query that has a
result has 50 words or fewer. Thus a retry does not help. These questions
count as not attempted, as Brave's 8 failed queries do in the
[FRAMES report](../frames-2026-11/report.md). Without them:

| Dataset | Questions over 50 words | Accuracy without them |
|---|---|---|
| SimpleQA Verified | 1 | 930/999, 93.1% |
| FRAMES | 42 | 422/782, 54.0% |

The order of the APIs does not change.

## Paired tests

Exact McNemar tests on the same questions. "x to y" means You.com answered x
questions correctly that the other API did not, and the other API answered y
that You.com did not.

| You.com against | SimpleQA Verified (1,000) | FreshQA (358) | FRAMES (824) |
|---|---|---|---|
| cloro | 16 to 57 (p < 0.0001) | 15 to 27 (p = 0.088) | 32 to 271 (p < 0.0001) |
| SerpApi | 36 to 56 (p = 0.047) | 15 to 28 (p = 0.066) | 33 to 255 (p < 0.0001) |
| Parallel | 10 to 58 (p < 0.0001) | 23 to 14 (p = 0.19) | 66 to 185 (p < 0.0001) |
| Exa | 15 to 58 (p < 0.0001) | 22 to 15 (p = 0.32) | 66 to 170 (p < 0.0001) |
| Perplexity\* | 13 to 58 (p < 0.0001) | 18 to 16 (p = 0.86) | 77 to 173 (p < 0.0001) |
| Brave | 19 to 19 (p = 1.0) | 13 to 13 (p = 1.0) | 65 to 87 (p = 0.088) |
| Tavily | 65 to 52 (p = 0.27) | 27 to 15 (p = 0.088) | 136 to 111 (p = 0.13) |
| Firecrawl | 60 to 47 (p = 0.25) | 34 to 17 (p = 0.024) | 145 to 81 (p < 0.0001) |

\* The Perplexity run with huggingface.co and kaggle.com excluded.

## Leak check

A question is flagged when the You.com raw response contains `simpleqa`,
`simple-evals`, `simple_qa`, `frames-benchmark`, `google/frames`,
`framesbenchmark`, `freshqa`, `huggingface.co/datasets` or `kaggle.com`, the
patterns of the earlier reports.

| Dataset | Flagged | Accuracy on flagged | Accuracy without flagged | Most frequent flagged URLs |
|---|---|---|---|---|
| SimpleQA Verified | 120 of 1,000 | 109/120, 90.8% | 821/880, 93.3% | `huggingface.co/datasets/SALT-NLP/...`, `huggingface.co/datasets/google/...` |
| FreshQA | 1 of 358 | 1/1 | 302/357, 84.6% | - |
| FRAMES | 99 of 824 | 46/99, 46.5% | 376/725, 51.9% | `huggingface.co/datasets/akseljoonas/...`, `huggingface.co/datasets/google/...` |

On the flagged questions You.com is less accurate than on the others, so the
dataset pages do not increase its score. The published score includes them,
as for the other APIs without a domain filter.

## Grader

Gemini graded every answer. The first 649 answers were graded by
`gpt-5.6-sol` during the run and then graded again by Gemini with
`analysis/regrade.py`. Their first grade is in the `grade_first` field. Gemini
gave the same grade on 638 of the 649.

## Reader check: Gemini as the reader

The You.com responses saved at that point in the run (676 questions) were
read again with Gemini (`gemini-pro-latest`) as the reader, with the
`youcom-reread` variant. No search ran again. On the questions that both
readers answered and Gemini graded:

| Dataset | Questions | `gpt-5.6-luna` reader | Gemini reader | Not attempted, luna to Gemini |
|---|---|---|---|---|
| SimpleQA Verified | 269 | 93.7% | 93.3% | 5 to 15 |
| FreshQA | 259 | 84.9% | 84.9% | 12 to 16 |
| FRAMES | 140 | 50.0% | 21.4% | 43 to 101 |

On FRAMES, the Gemini reader replies NOT FOUND when the answer needs a fact
from the results plus general knowledge. For example, the results give the
year in which Chile first won the Copa América, but not the name of the US
President in that year. Thus the published runs keep `gpt-5.6-luna` as the
reader, and the You.com score uses it too. The answers of this check are in
[`reader-check/`](reader-check).

```bash
READER_MODEL=gemini-pro-latest GRADER_MODEL=gemini-pro-latest \
  python3 benchmark.py --providers youcom-reread --dataset frames --as-of 2026-11-10 --out runs/frames-2026-11
```

## Cost

$5 per 1,000 searches, pay as you go
([pricing](https://you.com/pricing), read on 2026-11-18). New accounts get
$10 of free credit, about 2,000 searches. The run used the free credit and a
top-up for the last 130 FRAMES questions.

## Commands

```bash
export READER_MODEL=gpt-5.6-luna GRADER_MODEL=gemini-pro-latest
python3 benchmark.py --providers youcom --dataset simpleqa --out runs/simpleqa-2026-11
python3 benchmark.py --providers youcom --dataset freshqa --as-of 2026-11-05 --out runs/freshqa-2026-11
python3 benchmark.py --providers youcom --dataset frames --as-of 2026-11-10 --out runs/frames-2026-11
```
