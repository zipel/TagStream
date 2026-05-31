# Context Index

Read this index at the start of a session, then open the full files whose summaries
overlap the task. Summaries are pointers, not the rules.

## Operating method

- `../../CLAUDE.md` — project overview, session-start invariant, architecture,
  current project truth, hard rules, commands, commit standard.
- `../../AGENT_RULES.md` — trigger-based operating rules.
- `PROJECT_INVARIANTS.md` — TagStream-specific invariants: capability honesty,
  the tag output contract, ffmpeg/large-file/temp safety, local-model handling,
  determinism, and reproducibility.
- `METHOD.md` — the repo-local "agentic" invariant method this project adopts, and
  how it maps onto a CLI / local-ML tool (vs the web apps it came from).

## Code areas to pair with context

- Sampling / ffmpeg / large files: read `PROJECT_INVARIANTS.md` (ffmpeg + resource
  safety), then `tagstream/sampler.py` and `cli.py`.
- Captioning / models / device: read `PROJECT_INVARIANTS.md` (local models +
  determinism), then `tagstream/captioner.py` (BLIP) and `tagstream/ranker.py`
  (sentence-transformers).
- Keyword extraction / ranking / the tag output: read `PROJECT_INVARIANTS.md`
  (output contract), then `tagstream/keywords.py`, `tagstream/ranker.py`,
  `tagstream/utils.py`.
- README / description / user-facing copy: read `PROJECT_INVARIANTS.md` (capability
  honesty) and confirm the claim is backed by code + a run before writing it.
- Tests: read `AGENT_RULES.md` #7 — test the deterministic glue
  (`normalize_tags`, `singularize`, `normalize_token`, dedup, output count/format),
  not model outputs; stub the model classes.
