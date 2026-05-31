# Agent operating rules

Every rule below has a trigger. If the trigger does not fire, the rule does not
belong in this file.

## Rules

1. **Read project context before the first diff.** Trigger: first turn in a fresh
   session, new clone, context compaction, or a request touching the pipeline,
   ffmpeg/sampling, models, large-file/temp handling, the tag output, or any
   README/description capability claim. Action: read `CLAUDE.md`, then
   `docs/context/INDEX.md`, then the full linked files whose summaries match.

2. **Before editing a pipeline stage, read that stage's module.** Trigger: about to
   change sampling, captioning, keyword extraction, ranking, or normalization.
   Action: read the module in `tagstream/` (and `cli.py` for how it is wired) first;
   the stages pass plain Python lists between each other and a wrong shape breaks the
   next stage silently.

3. **Only claim what the code does.** Trigger: editing the README, the GitHub
   description, help text, or any user-facing copy. Action: do not assert "visual
   verification," supported input formats, or tag-quality guarantees unless the code
   does them and a test/run shows it. Today ranking is caption-text similarity, not
   image↔keyword verification — describe it that way.

4. **External binary + model assumptions must be explicit.** Trigger: touching
   `sampler.py` (ffmpeg) or any model load (BLIP / sentence-transformers / KeyBERT).
   Action: handle the missing/failed case with a clear message (ffmpeg not on PATH,
   model download failure, unsupported device). A raw `CalledProcessError` or import
   crash is not acceptable UX for a CLI.

5. **Be resource-safe on large inputs.** Trigger: changing frame sampling, temp
   files, or anything that scales with video length/size (≥1 GB, many frames).
   Action: clean up temp dirs (or stream), avoid loading whole videos into memory,
   and confirm behaviour on a genuinely large/long clip when the change could affect
   disk or memory.

6. **Protect the output contract.** Trigger: changing keyword extraction, ranking,
   normalization, or the CLI output. Action: preserve "up to `--top` unique,
   normalized, rank-ordered tags, comma-separated." Add/keep a test for dedup, count,
   and normalization (`normalize_tags`, `singularize`, `normalize_token`).

7. **Test the deterministic glue, not the models.** Trigger: adding or changing
   tests. Action: assert on sampler command/arg construction, keyword
   normalization/dedup, tag normalization/singularization, and output format/count.
   Do NOT assert exact captions/embeddings/tags — they vary by model version and
   device. Stub or mock the model classes where needed.

8. **Reproducible setup.** Trigger: adding a dependency, changing the run/setup, or
   touching `requirements.txt` / `pyproject.toml`. Action: keep `requirements.txt`
   the source of truth, remove genuinely-unused deps (or document why they stay),
   and update the README quick-start so `venv` + `pip install -r requirements.txt`
   still reproduces a working run.

9. **Never commit heavy or generated artifacts / secrets.** Trigger: `git add`.
   Action: keep venvs, model caches, sample videos, generated `tags.csv`,
   `tagstream_frames_*` temp dirs, and any `.env` out of the repo (see `.gitignore`).

10. **Write a handoff note before stopping mid-task.** Trigger: context running low,
    switching machine, or pausing with a partial pipeline/large-file change. Action:
    leave a clear commit message or repo note with state, the command run, and the
    next verification step.

11. **If the same failure class appears twice, make the third impossible.** Trigger:
    a recurring bug class (ffmpeg/env, temp leakage, tag-format regressions, model
    download/device issues). Action: add a guard or test in the same change as the fix.

## Where rules live

Cross-cutting operating rules belong here. Project-specific facts and invariants
live in `CLAUDE.md`, `docs/context/INDEX.md`, and `docs/context/*.md`.

## Delete criteria

Remove a rule if it has no concrete trigger, only restates normal engineering,
is not actionable for the next agent, or conflicts with a stronger project rule.
