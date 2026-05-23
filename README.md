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

