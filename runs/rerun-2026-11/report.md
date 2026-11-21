# Rerun of all ten APIs with the `gemini-3.8-flash` reader (2026-11-21)

Run: 2026-11-21, `READER_MODEL=gemini-3.8-flash`, `GRADER_MODEL=gemini-pro-latest`,
seed 42, `--workers 6`, with the `<provider>-reread` variants of
[`benchmark.py`](../../benchmark.py). No search ran again: the reader read the
saved search responses of the published runs, with the strict reader prompt
("Use ONLY information from the search results. Do NOT use any internal
knowledge."). The questions and the `--as-of` dates (FreshQA 2026-11-05,
FRAMES 2026-11-10) are the same as in the earlier runs. The
[reader test](../reader-test-2026-11/report.md) says why the reader changed.

The README tables come from this run. The earlier reports in `runs/` keep the
scores of the earlier reader, `gpt-5.6-luna`, with the earlier prompt.

## Result

Accuracy with the 95% Wilson interval. A failed search of the earlier run
counts as not attempted.

| Search API | SimpleQA Verified (1,000) | FreshQA (358) | FRAMES (824) |
|---|---|---|---|
| cloro | 96.4% (95.1-97.4) | 88.5% (84.8-91.4) | 79.9% (77.0-82.5) |
| SerpApi | 93.9% (92.2-95.2) | 86.9% (83.0-90.0) | 76.8% (73.8-79.6) |
| Exa | 95.8% (94.4-96.9) | 86.6% (82.7-89.7) | 49.9% (46.5-53.3) |
| Parallel | 96.2% (94.8-97.2) | 86.0% (82.1-89.2) | 45.6% (42.3-49.0) |
| Perplexity Search API\* | 96.9% (95.6-97.8) | 86.0% (82.1-89.2) | 44.2% (40.8-47.6) |
| Keenable\* | 96.0% (94.6-97.0) | 84.4% (80.2-87.8) | 34.5% (31.3-37.8) |
| Brave Search API | 90.5% (88.5-92.2) | 85.8% (81.8-89.0) | 25.8% (23.0-28.9) |
| You.com | 89.2% (87.1-91.0) | 84.9% (80.8-88.3) | 22.1% (19.4-25.0) |
| Tavily | 89.2% (87.1-91.0) | 82.7% (78.4-86.2) | 18.1% (15.6-20.9) |
| Firecrawl | 88.8% (86.7-90.6) | 80.2% (75.7-84.0) | 15.8% (13.4-18.4) |

\* With huggingface.co and kaggle.com excluded, as in the earlier runs.

## Change from the earlier reader

| Search API | SimpleQA Verified | FreshQA | FRAMES |
|---|---|---|---|
| cloro | 97.1% -> 96.4% | 88.0% -> 88.5% | 80.2% -> 79.9% |
| SerpApi | 95.0% -> 93.9% | 88.3% -> 86.9% | 78.2% -> 76.8% |
| Exa | 97.3% -> 95.8% | 82.7% -> 86.6% | 63.8% -> 49.9% |
| Parallel | 97.8% -> 96.2% | 82.1% -> 86.0% | 65.7% -> 45.6% |
| Perplexity\* | 97.5% -> 96.9% | 84.1% -> 86.0% | 62.9% -> 44.2% |
| Keenable\* | 97.2% -> 96.0% | 83.2% -> 84.4% | 56.9% -> 34.5% |
| Brave | 93.0% -> 90.5% | 84.6% -> 85.8% | 53.9% -> 25.8% |
| You.com | 93.0% -> 89.2% | 84.6% -> 84.9% | 51.2% -> 22.1% |
| Tavily | 91.7% -> 89.2% | 81.3% -> 82.7% | 48.2% -> 18.1% |
| Firecrawl | 91.7% -> 88.8% | 79.9% -> 80.2% | 43.4% -> 15.8% |

- **FRAMES:** cloro and SerpApi lose 0.3 and 1.4 points, the other eight 14 to
  30 points. The results of cloro and SerpApi usually include Google's AI
  Overview, which often gives the full answer, so the reader has nothing to
  add from memory.
- **SimpleQA Verified:** every API loses 0.6 to 3.8 points.
- **FreshQA:** most APIs gain up to 3.9 points, and SerpApi loses 1.4.

## FRAMES: not attempted and accuracy given an answer

| Search API | Not attempted (of 824) | Correct when it answers |
|---|---|---|
| cloro | 28 | 82.7% |
| SerpApi | 62 | 83.1% |
| Exa | 372 | 90.9% |
| Parallel | 411 | 91.0% |
| Perplexity\* | 412 | 88.3% |
| Keenable\* | 501 | 87.9% |
| Brave | 588 | 90.3% |
| You.com | 622 | 90.1% |
| Tavily | 654 | 87.6% |
| Firecrawl | 673 | 86.1% |

You.com rejects queries longer than 50 words (HTTP 422), and Brave failed 8
searches in the earlier run: those 50 FRAMES questions count as not
attempted. Without its failed searches, You.com scores 182/782 (23.3%) on
FRAMES and 892/999 (89.3%) on SimpleQA Verified.

## Paired tests

Exact McNemar tests on the same questions. Every pair of the ten APIs on each
dataset, with the counts, is in the commands below. The ones that the README
uses:

| Comparison | SimpleQA Verified | FreshQA | FRAMES |
|---|---|---|---|
| cloro vs SerpApi | cloro, 38 to 13 (p = 0.0006) | no difference (p = 0.29) | cloro, 68 to 43 (p = 0.022) |
| cloro vs Exa | no difference (p = 0.46) | no difference (p = 0.28) | cloro, 280 to 33 (p < 0.0001) |
| cloro vs Parallel | no difference (p = 0.88) | no difference (p = 0.11) | cloro, 310 to 28 (p < 0.0001) |
| cloro vs Perplexity | no difference (p = 0.51) | no difference (p = 0.14) | cloro, 333 to 39 (p < 0.0001) |
| cloro vs Keenable | no difference (p = 0.64) | cloro, 26 to 11 (p = 0.020) | cloro, 404 to 30 (p < 0.0001) |
| cloro vs Brave | cloro, 77 to 18 (p < 0.0001) | no difference (p = 0.087) | cloro, 457 to 12 (p < 0.0001) |
| cloro vs You.com | cloro, 88 to 16 (p < 0.0001) | cloro, 21 to 8 (p = 0.024) | cloro, 483 to 7 (p < 0.0001) |
| cloro vs Tavily | cloro, 88 to 16 (p < 0.0001) | cloro, 29 to 8 (p = 0.0008) | cloro, 521 to 12 (p < 0.0001) |
| cloro vs Firecrawl | cloro, 93 to 17 (p < 0.0001) | cloro, 40 to 10 (p < 0.0001) | cloro, 535 to 7 (p < 0.0001) |
| Exa vs Tavily | Exa, 81 to 15 (p < 0.0001) | Exa, 28 to 14 (p = 0.044) | Exa, 285 to 23 (p < 0.0001) |
| Exa vs Parallel | no difference (p = 0.63) | no difference (p = 0.81) | Exa, 120 to 85 (p = 0.017) |
| Exa vs Brave | Exa, 72 to 19 (p < 0.0001) | no difference (p = 0.66) | Exa, 218 to 20 (p < 0.0001) |
| Parallel vs Tavily | Parallel, 87 to 17 (p < 0.0001) | no difference (p = 0.058) | Parallel, 265 to 38 (p < 0.0001) |
| Brave vs Tavily | no difference (p = 0.29) | no difference (p = 0.099) | Brave, 125 to 61 (p < 0.0001) |
| Firecrawl vs Tavily | no difference (p = 0.78) | no difference (p = 0.21) | no difference (p = 0.13) |
| You.com vs Brave | no difference (p = 0.060) | no difference (p = 0.58) | Brave, 45 to 14 (p < 0.0001) |
| You.com vs Tavily | no difference (p = 1.0) | no difference (p = 0.22) | You.com, 99 to 66 (p = 0.012) |
| Keenable vs Exa | no difference (p = 0.86) | no difference (p = 0.15) | Exa, 191 to 64 (p < 0.0001) |
| Keenable vs Perplexity | no difference (p = 0.15) | no difference (p = 0.29) | Perplexity, 156 to 76 (p < 0.0001) |
| Keenable vs Brave | Keenable, 74 to 19 (p < 0.0001) | no difference (p = 0.46) | Keenable, 136 to 65 (p < 0.0001) |

On SimpleQA Verified, Perplexity, cloro, Parallel, Keenable and Exa are not
significantly different from each other (p = 0.071 to 0.88), and each of them
is significantly more accurate than SerpApi (p = 0.00023 to 0.037), Brave,
You.com, Tavily and Firecrawl (p < 0.0001 each).

## Content filter

Gemini's content filter blocked 4 reader calls on SimpleQA Verified (Exa
questions 799 and 3763, Tavily and You.com question 608), with the reason
`PROHIBITED_CONTENT` in all three passes. They count as not attempted, and
`benchmark.py` now writes a blocked call as NOT FOUND.

## Cost

21,820 reader calls to `gemini-3.8-flash` and 21,820 grader calls to
`gemini-pro-latest`, plus the calls that ran again after an error. No search
calls.

## Commands

The run folders link `raw/<api>` to the saved responses: for the first six
APIs, the SimpleQA Verified (2026-11-04) and FreshQA (2026-11-05) runs in
`outputs/` of the `marketing` repo and the FRAMES run in
`outputs/search-benchmark-frames-2026-11-10/` of this repo; for the other
four, `runs/<dataset>-2026-11/raw/`.

```bash
P=cloro-reread,serpapi-reread,tavily-reread,exa-reread,parallel-reread,brave-reread,perplexity-nodata-reread,firecrawl-reread,youcom-reread,keenable-nodata-reread
python3 benchmark.py --n 1000 --providers $P --dataset simpleqa --out outputs/rerun-2026-11/simpleqa
python3 benchmark.py --n 1000 --providers $P --dataset freshqa --as-of 2026-11-05 --out outputs/rerun-2026-11/freshqa
python3 benchmark.py --n 1000 --providers $P --dataset frames --as-of 2026-11-10 --out outputs/rerun-2026-11/frames
python3 analysis/sensitivity.py outputs/rerun-2026-11/frames cloro-reread:serpapi-reread
```
