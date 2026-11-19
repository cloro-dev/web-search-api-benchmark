# web-search-api-benchmark

## Models

- **Gemini (`gemini-pro-latest`) grades every answer.** Do not grade with
  another model. Since 2026-11-18, all published grades are Gemini grades.
- **The reader of the published runs is `gpt-5.6-luna`.** When you add an API
  to the published tables, read its results with `gpt-5.6-luna`, so that its
  score compares with the other APIs. Change the reader only in a full rerun
  of all APIs, and say so in the README.
- **Why the reader stays:** on the same 140 You.com FRAMES results, the
  `gpt-5.6-luna` reader scored 50.0% and the Gemini reader 21.4%. The Gemini
  reader replies NOT FOUND when the answer needs a found fact plus general
  knowledge. On SimpleQA Verified and FreshQA the two readers gave the same
  score. See [the You.com report](runs/youcom-2026-11/report.md).

## Keys

All keys are in Doppler `marketing/dev`: the provider keys,
`OPENAI_API_KEY` for the reader and `GEMINI_API_KEY` for the grader. Never put
a key in the repo.

```bash
READER_MODEL=gpt-5.6-luna GRADER_MODEL=gemini-pro-latest \
  doppler run -p marketing -c dev -- python3 benchmark.py --providers <api> ...
```

Use the `--as-of` date of the earlier run of each dataset (FreshQA
2026-11-05, FRAMES 2026-11-10), or the FreshQA question set changes.
