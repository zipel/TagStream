# TagStream

TagStream is a macOS command line tool that generates stock-style keyword tags from MP4 videos by sampling frames, captioning, extracting keywords, and ranking them.

## Quick start

Prerequisites:
- Python 3.10+
- ffmpeg (`brew install ffmpeg`)
- Optional: Apple Silicon PyTorch with MPS support or CUDA GPU

Create and activate a venv:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Usage:
```bash
python cli.py --input examples/sample_video.mp4 --sample-rate 0.5 --top 50 --out examples/tags.csv
```

Requirements:
- Python 3.10+
- `ffmpeg` installed and available on `PATH` (`brew install ffmpeg`)
- `torch`, `transformers`, `sentence-transformers`, and other packages from `requirements.txt`

Notes:
- The default sampling rate is `0.5` fps, which means one frame every 2 seconds.
- For a 30 fps video, this is appropriate for 10–60 second clips and avoids scanning every frame.
- Output is written as a comma-separated list of tags to `tags.csv` by default.

