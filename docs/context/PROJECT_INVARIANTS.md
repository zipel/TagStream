# TagStream Project Invariants

The correctness bar is not "the pipeline runs"; it is **honest, correct tag output**,
**surviving large real videos**, and **a clean reproducible run on a Mac**.

## Capability honesty (the load-bearing one)

- Only describe what the code actually does. The repo description claims keywords are
  "verified visually" — **this is not implemented.** `ranker.py` ranks candidates by
  cosine similarity to the **caption text**, not to the images. Until a real
  image↔keyword check exists (e.g. CLIP scoring frames against candidate tags), do
  not call it visual verification in the README, description, help text, or output.
- The same applies to supported input formats, languages, tag-quality, and
  performance claims: code + a run must back the claim, or it is "planned".

## Tag output contract

- Output is **up to `--top` (default 50) tags**, **unique**, **normalized**,
  **rank-ordered**, comma-separated, one line. Fewer than `--top` candidates → fewer
  tags (do not pad).
- Normalization (`utils.normalize_tags`) lowercases, collapses whitespace,
  singularizes, and dedups. Keyword normalization (`keywords.normalize_token`)
  lowercases and strips punctuation. Any change to these must keep dedup + count
  correct and be unit-tested.
- The singularizer is naive (`series`→`sery`, `analysis`→`analysi`). Improving it is
  welcome, but changes must be tested against real failure words, because mangled
  tags directly lower stock-platform acceptance.

## ffmpeg & external binaries

- `sampler.py` shells out to **ffmpeg** (`subprocess.run(..., check=True)`). ffmpeg is
  a hard runtime dependency (`brew install ffmpeg`). Any sampling code must detect a
  missing/failed ffmpeg and surface a clear, actionable error — never a bare
  `CalledProcessError` traceback to the end user.
- Keep the README, `requirements.txt`, and the code consistent about the sampling
  mechanism. (Today: README + code say ffmpeg; `opencv-python-headless` and
  `python-magic` are listed but unused — resolve, don't let it drift further.)

## Large files & resource safety

- Target inputs are **≥1 GB MP4s, 10–60 s clips**. Never load a whole video into
  memory; sample to disk and process frame paths (current design — preserve it).
- `sample_frames()` writes JPEGs to a `tempfile.mkdtemp()` dir and currently **never
  deletes it** — every run leaks frames into the system temp. Frame-producing code
  must clean up (context manager / explicit removal) or document a retention policy.
- Sampling rate scales frame count with clip length; defaults (0.5 fps) are tuned for
  10–60 s. Guard against pathological inputs (very long video × high fps) that would
  generate thousands of frames and exhaust disk or model time.

## Local models & determinism

- Captioning (BLIP) and ranking/keywords (sentence-transformers / KeyBERT) run
  **locally**; weights download from HuggingFace on first use (no API keys today). If
  a cloud vision/LLM API is ever added, its key goes in `.env` (gitignored) and must
  never be committed or logged.
- Model output is **not deterministic across versions/devices** (cpu/cuda/mps). Do
  not write tests that assert exact captions, embeddings, or tags. Pin model names in
  code; document the device flag behaviour.
- `captioner.batch_caption()` swallows per-frame exceptions into empty captions —
  acceptable for robustness, but it hides systematic failures. Prefer logging the
  count of failed frames over silent degradation.

## Reproducibility & setup

- `requirements.txt` is the source of truth for deps; the README quick-start
  (`venv` → `pip install -r requirements.txt` → `python cli.py ...`) must always
  reproduce a working run. Update it when setup changes.
- Never commit: `.venv/`, model caches, `*.pkl`, sample videos
  (`examples/sample_video.mp4`), generated `tags.csv`, `tagstream_frames_*` temp
  dirs, or `.env` (see `.gitignore`).

## Verification

- Run `pytest -q` after any logic change.
- For pipeline changes, run `cli.py` on a short real clip and check the tag count,
  dedup, and relevance.
- For ffmpeg / large-file / temp-cleanup / device changes, verify on a genuinely
  large or long video and note it in the commit.
