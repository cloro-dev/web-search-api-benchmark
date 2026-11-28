# web-search-api-benchmark

## Models

- **`claude-haiku-5-5` reads, grades and checks support for every published
  score.** It is the default `READER_MODEL` and `GRADER_MODEL` in
  `benchmark.py`, and the agent of `runs/agent-2026-11/`. The one-search
  tables come from [the Haiku run](runs/haiku-2026-11/report.md) (2026-11-28).
  Do not use another model for a published score. When you add an API, read
  and grade its results with Haiku and `--support-check`.
- **Run Claude on a subscription login, never on an API key.**
  `benchmark.py` calls Claude Code headless (`claude -p`) with
  `CLAUDE_CODE_OAUTH_TOKEN` and removes the `ANTHROPIC_*` variables. The
  token is `CLAUDE_SUB_OAUTH_TOKEN` in Doppler `monitor/prd`.
- **Keep the strict reader prompt:** "Use ONLY information from the search
  results. Do NOT use any internal knowledge." Do not change the model or
  the prompt without a full rerun of all APIs, and say so in the README.
- **Keep the grader prompt that writes one sentence before the letter.** With
  the bare-letter prompt of simple-evals, Haiku agreed with
  `gemini-pro-latest` on only 80% to 82% of FreshQA answers. With one
  sentence first, it agreed on 98%. FreshQA also gets the rules in
  `FRESHQA_GRADER_RULES` ("OR" alternatives, false premises).
- **Do not mix Haiku scores with the Gemini scores** of the earlier runs
  (`gemini-3.8-flash` read and `gemini-pro-latest` graded until 2026-11-27).
  Those reports stay in `runs/` as history.

## The agent runs

- **`runs/agent-2026-11/` has its own tables.** There, Haiku searches up to
  10 times per question, with the harness of the internal `web-search-evals`
  repo. Do not put its scores in a table with one-search scores.
- **Publish only IDs and scores for BrowseComp.** OpenAI asks that its
  questions and answers do not appear online as plain text. This includes
  the agent's answers and search queries, which can hold the question or the
  answer.

## One request per search

- **Every API gets one request per search.** SerpApi loads most Google AI
  Overviews in a second request (`engine=google_ai_overview`). Do not make
  it: no other API gets a second request. The published SerpApi row is
  `serpapi-single-reread`, the saved first responses without the second one.
  Without it, SerpApi has an AI Overview on 15 of 1,000 SimpleQA Verified
  questions, against 983 with it (decided 2026-11-27).

## Dataset leaks

- **Run the leak check on every new API.** If its results hold the
  benchmark's own dataset pages (huggingface.co, kaggle.com) and its score on
  those questions is higher, add a `<api>-nodata` variant that excludes the
  two hosts, and publish that score. Give the unfiltered score in a note.
  Perplexity and Keenable use this filter. See
  [the Keenable report](runs/keenable-2026-11/report.md).

## Keys

All provider keys are in Doppler `marketing/dev`, with `GEMINI_API_KEY`
for the runs before 2026-11-28 and `OPENAI_API_KEY` for the `gpt-5.6-sol`
judge of `analysis/grounding.py`. Never put a key in the repo.

```bash
doppler run -p marketing -c dev -- python3 benchmark.py --providers <api> ...
```

Use the `--as-of` date of the earlier run of each dataset (FreshQA
2026-11-05, FRAMES 2026-11-10), or the FreshQA question set changes.
