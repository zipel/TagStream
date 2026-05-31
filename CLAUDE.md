# TagStream

A macOS command-line Python tool that turns an MP4 video into stock-style keyword tags:
sample frames → caption each frame → extract candidate keywords → rank/filter →
normalize → write the top-N (default 50) as a comma-separated list.

The product's value is the **quality and correctness of the final tag list**, the
ability to handle **large videos (≥1 GB, 10–60 s clips)** without falling over, and
running cleanly **from a Mac terminal / VS Code**. Treat those three as product
requirements, not polish.

## INVARIANT — session-start context is in `docs/context/`

This rule fires on the first turn of every session, after context compaction, or
whenever the task touches: the pipeline stages, ffmpeg/frame sampling, model
loading (BLIP / sentence-transformers / KeyBERT), large-file or temp-dir handling,
the tag output contract, performance/device (cpu/cuda/mps), or any user-facing /
README capability claim.

Before making a diff:

1. Read the user's message and list the topics it touches.
2. Open `docs/context/INDEX.md`.
3. For every index entry whose summary overlaps the task, read the full linked
   file. The index is a pointer, not the rule.
4. If the task touches a pipeline stage, read that stage's module in `tagstream/`
   before changing it.

## Architecture

- **CLI** entry: `cli.py` (argparse). Pipeline is linear:
  1. `tagstream/sampler.py` — `sample_frames()` shells out to **ffmpeg** to extract
     JPEG frames at `--sample-rate` fps into a temp dir; returns file paths.
  2. `tagstream/captioner.py` — `Captioner` (BLIP `Salesforce/blip-image-captioning-base`
     via `transformers`) captions each frame.
  3. `tagstream/keywords.py` — `extract_keywords_from_captions()` (KeyBERT) →
     unique normalized candidate keywords.
  4. `tagstream/ranker.py` — `Ranker` (sentence-transformers `all-MiniLM-L6-v2`)
     ranks candidates by cosine similarity **to the caption text**.
  5. `tagstream/utils.py` — `normalize_tags()` (lowercase, collapse whitespace,
     naive singularize, dedup). `cli.py` truncates to `--top`.
- **Models run locally** (downloaded from HuggingFace on first use). There are **no
  cloud API keys** in the current pipeline.
- Python 3.10+, `venv`, deps in `requirements.txt`. Device: `cpu` / `cuda` / `mps`.
- Tests in `tests/` (pytest-style). macOS is the target; ffmpeg via `brew install ffmpeg`.

## Current project truth

- Early scaffold. The pipeline runs end-to-end but several parts are thin.
- **"Visual verification" is NOT implemented.** The project description says keywords
  are "verified visually," but `ranker.py` ranks candidates by similarity to the
  **caption text**, not to the **images**. The frames are never compared to the
  keywords. Do not describe the tool as doing visual verification until a real
  image↔keyword check (e.g. CLIP) exists.
- `sampler.py` **does not clean up its temp frame dir** (`tempfile.mkdtemp`). On a
  ≥1 GB / long video this leaks JPEGs into the system temp each run.
- `captioner.batch_caption()` **silently swallows per-frame errors** (appends `""`),
  so a broken frame degrades tag quality invisibly. It also captions one frame at a
  time (not truly batched).
- Possible dependency drift: `requirements.txt` lists `opencv-python-headless` and
  `python-magic`, but the code samples with ffmpeg and does not validate file type.
  Confirm intent before relying on either.
- `normalize_tags()` singularization is naive (`series`→`sery`, etc.) — a real
  correctness risk for the final stock tags.
- `tests/test_sampler.py` is a placeholder (`assert True`). There is effectively no
  test coverage yet.

## Hard rules

- **Never claim a capability the code doesn't have** — especially "visual
  verification," supported formats, or tag-quality guarantees — in the README,
  description, or output. If it isn't in the code + exercised, call it planned.
- **ffmpeg is a required external binary.** Code that samples frames must fail with a
  clear, actionable message if ffmpeg is missing (not a raw `CalledProcessError`).
- **Be disk-safe on large inputs.** Anything that writes frames/temp files must clean
  up after itself (or stream), and must not load a whole ≥1 GB video into memory.
- **The output contract is load-bearing:** up to `--top` (default 50) **unique,
  normalized** tags, comma-separated. Don't break dedup, ordering-by-rank, or the count.
- **Never commit** virtualenvs, model caches, sample videos, generated `tags.csv`,
  or `tagstream_frames_*` temp dirs (see `.gitignore`). No secrets.
- **Test the deterministic glue, not model outputs.** Model captions/embeddings vary
  by version/device; assert on sampler arg-building, keyword normalization/dedup,
  `normalize_tags`/`singularize`, and the output format/count — not exact tags.

## Common commands

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python cli.py --input examples/sample_video.mp4 --sample-rate 0.5 --top 50 --out examples/tags.csv
pytest -q
```

## Commit standard

Before committing code changes:

1. Run `pytest -q`.
2. For pipeline changes, run `cli.py` on a short sample clip when feasible and
   eyeball the tag output (count, dedup, relevance).
3. For ffmpeg / large-file / device / model changes, state the verification command
   in the commit body (and whether it was run on a real large file).
4. If a high-risk path (large-file/temp cleanup, ffmpeg-missing handling) is left
   unverified, say so plainly.
