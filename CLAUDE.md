# web-search-api-benchmark

## Models

- **Gemini (`gemini-pro-latest`) grades every answer.** Do not grade with
  another model. Since 2026-11-18, all published grades are Gemini grades.
- **The reader is `gemini-3.8-flash`, with the strict reader prompt.** It is
  the default `READER_MODEL` in `benchmark.py`. Every published run uses this
  reader and the prompt line "Use ONLY information from the search results.
  Do NOT use any internal knowledge." When you add an API, read its results
  with this reader. Do not change the reader or the prompt without a full
  rerun of all APIs, and say so in the README.
- **Why this reader:** the reader must answer from the search results only,
  not from its own memory. With the strict prompt, judges found that 23% of
  the FRAMES answers of `gpt-5.6-luna` and 27% of `gpt-4.1` are not supported
  by the search results. For `gemini-3.8-flash` it is 4%, the same as the
  more expensive Gemini models, and it misses no more answers that the
  results hold. `gemini-3.5-flash-lite` misses more, and
  `gemini-3.1-flash-lite` answers from memory. See
  [the reader test](runs/reader-test-2026-11/report.md).
- **Use the fixed model name, not a `-latest` name.** Google changes the
  model behind a `-latest` name at each release.

## Dataset leaks

- **Run the leak check on every new API.** If its results hold the
  benchmark's own dataset pages (huggingface.co, kaggle.com) and its score on
  those questions is higher, add a `<api>-nodata` variant that excludes the
  two hosts, and publish that score. Give the unfiltered score in a note.
  Perplexity and Keenable use this filter. See
  [the Keenable report](runs/keenable-2026-11/report.md).

## Keys

All keys are in Doppler `marketing/dev`: the provider keys, `GEMINI_API_KEY`
for the reader and the grader, and `OPENAI_API_KEY` for the `gpt-5.6-sol`
judge of `analysis/grounding.py`. Never put a key in the repo.

```bash
doppler run -p marketing -c dev -- python3 benchmark.py --providers <api> ...
```

Use the `--as-of` date of the earlier run of each dataset (FreshQA
2026-11-05, FRAMES 2026-11-10), or the FreshQA question set changes.
