import subprocess
import tempfile
import os
from pathlib import Path
from typing import List

def sample_frames(video_path: str, fps: float = 0.5) -> List[str]:
    # Extract frames using ffmpeg to a temporary directory.
    # Returns list of file paths to sampled images.

    tmpdir = tempfile.mkdtemp(prefix="tagstream_frames_")
    out_pattern = os.path.join(tmpdir, "frame_%05d.jpg")
    cmd = [
        "ffmpeg", "-hide_banner", "-loglevel", "error",
        "-i", video_path,
        "-vf", f"fps={fps}",
        "-q:v", "2",
        out_pattern
    ]
    subprocess.run(cmd, check=True)
    files = sorted(Path(tmpdir).glob("frame_*.jpg"))
    return [str(p) for p in files]
