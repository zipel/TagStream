# TagStream — Persona Review & Feature Plan

**Status:** proposal for discussion. Grounded in the committed code
(`cli.py` + `tagstream/{sampler,captioner,keywords,ranker,utils}.py`), not assumed.

## Where TagStream is today (from the code)

Linear, fully **local** pipeline:
`ffmpeg` frame sampling → **BLIP** captioning → **KeyBERT** keywords →
**sentence-transformers (MiniLM)** ranking → naive normalize → flat top-N
(default 50) comma-separated tags. One clip at a time. No scene/temporal
awareness, no metadata, no batch, no review step.

> **Note on "online" object detection:** the project description implies visual
> verification, but the committed code does **no network calls and no object
> detection** — ranking is caption-text↔keyword-text similarity, all on-device.
> If a newer online-detection version exists locally, it has not been pushed and
> should be, so it isn't lost.

## Expert persona reviews

**🎥 Videographer** — BLIP-base gives literal captions ("a man on a beach"); stock
buyers search **concept, mood, action, season, time-of-day, color** ("freedom",
"golden hour"). No subject specificity, shot type, or emotion. Tags are only as
rich as a weak caption.

**✂️ Editor** — No **batch** (one `--input`). No **scene/shot detection**, so a
multi-scene clip blends into one averaged tag bag. Output is a bare keyword CSV —
stock portals need a **title + description + category** and a **per-platform CSV
schema**, and tags should embed into the file (**XMP/IPTC**) to survive in
Premiere/MAM.

**🚁 Drone operator** — Zero aerial awareness (no "aerial/drone/bird's-eye",
top-down vs oblique, orbit/reveal). The MP4s carry **GPS/altitude/gimbal metadata**
that is ignored — free, accurate location tags.

**🎛️ UI/UX** — CLI-only and opaque; missing ffmpeg → raw traceback; no progress
(tqdm is a dep, unused); **no way to review/curate the 50 tags before they're
written**.

**🏗️ System architect** — The **"visual verification" claim is unimplemented**
(text-only ranking → can emit tags not actually visible). Also: temp-dir leak,
frame-by-frame (no GPU batching), not packaged (`python cli.py`, no entry point),
naive singularizer (`series`→`sery`), ~no tests.

## Decisions (captured 2026)

- **Audience:** personal footage-tagging tool first (productize later if ever).
- **Interface:** a **lightweight local GUI** (drag-drop, review/edit tag chips
  before export).
- **Models:** prefer **local/offline** — review confirmed a realistic local path
  (below); drop any online dependency.
- **Platforms:** target **all** of Adobe Stock, Shutterstock, Pond5, Getty/iStock.

## Local object-detection / verification — realistic on Apple Silicon (MPS)

| Local option | What it gives | Fit |
|---|---|---|
| **CLIP** (open-vocab) | Score any text tag against a frame ("is this visible?") + zero-shot tagging from a stock vocabulary | **Highest leverage** — visual verification **and** detection in one model |
| **YOLOv8 / YOLO11** (ultralytics) | Fast bounding-box detection of concrete subjects | Literal objects; runs on MPS/CPU |
| **OWL-ViT / Grounding DINO** | Open-vocabulary detection beyond fixed classes | When detection must exceed YOLO's classes; heavier |

**Recommendation:** go fully local — add **CLIP** (verification + zero-shot
concepts) and optionally **YOLO** for concrete objects. A top cloud API has a
higher accuracy ceiling, but local keeps footage **private, free, offline**, which
fits a personal tool. Local is genuinely realistic here.

## Phased feature plan

**Phase 1 — Local quality & trust (the engine behind everything)**
- **CLIP visual verification** — drop candidate tags not actually visible. Fixes the
  hallucination gap *and* makes the "verifies visually" claim true. Biggest single
  quality jump.
- **Scene-cut dedup** (PySceneDetect) so multi-scene clips aren't blended.
- Foundations: temp-dir cleanup, ffmpeg preflight + friendly error, progress bar,
  real glue tests (`normalize_tags`/dedup/output-count).
- *Open item:* CLIP-only vs CLIP+YOLO for this phase.

**Phase 2 — Local GUI (chosen interface)**
- A local **Gradio** (or FastAPI) app launched from the CLI: drag-drop clip(s) →
  sampled frame thumbnails → tags as **editable chips with per-tag CLIP
  confidence** → accept/reject/add → pick platform → export. Queue multiple clips
  for batch.

**Phase 3 — All-platform export**
- Per-platform **export profiles** (Adobe Stock, Shutterstock, Pond5, Getty/iStock):
  tag-count caps, CSV schema, **title + description + category** generation, and
  **XMP/IPTC embedding** (exiftool) so tags ride with the file.

**Phase 4 — Domain richness**
- **Aerial/drone pack** + read embedded **GPS → location tags**; shot-type &
  camera-move; a **color/mood/concept** layer via CLIP zero-shot against a curated
  stock vocabulary.

**Sequence:** 1 → 2 → 3 → 4. The GUI is only as good as the tags behind it, and
all-platform export (titles/descriptions/categories) leans on Phase 1's better
signal — so trust/quality first, then the GUI, then export breadth, then richness.

## Open items for the maintainer

1. Push the local online-detection version if it exists (so it isn't lost), or
   confirm the tool should stay fully local.
2. Phase 1 scope: CLIP-only vs CLIP + YOLO.
