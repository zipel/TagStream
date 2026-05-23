#!/usr/bin/env python3
import argparse
from tagstream.sampler import sample_frames
from tagstream.captioner import Captioner
from tagstream.keywords import extract_keywords_from_captions
from tagstream.ranker import Ranker
from tagstream.utils import normalize_tags

def main():
parser = argparse.ArgumentParser(description="TagStream CLI")
parser.add_argument("--input", required=True, help="Input MP4 file")
parser.add_argument("--sample-rate", type=float, default=0.5, help="Frames per second to sample (e.g., 0.5 = 1 frame every 2s)")
parser.add_argument("--top", type=int, default=50, help="Number of tags to output")
parser.add_argument("--out", default="tags.csv", help="Output CSV file")
parser.add_argument("--device", default="cpu", help="Device for models: cpu or cuda or mps")
args = parser.parse_args()

print(f"Sampling frames from {args.input} at {args.sample_rate} fps...")
frames = sample_frames(args.input, fps=args.sample_rate)
print(f"Sampled {len(frames)} frames")

captioner = Captioner(device=args.device)
captions = captioner.batch_caption(frames)
print("Generated captions for sampled frames")

candidates = extract_keywords_from_captions(captions)
print(f"Extracted {len(candidates)} unique candidate keywords")

ranker = Ranker(device=args.device)
tags = ranker.rank_and_filter(frames, candidates, top_k=args.top)
tags = normalize_tags(tags)

tags = tags[:args.top]
line = ",".join(tags)
with open(args.out, "w") as f:
f.write(line + "\n")
print(f"Wrote {len(tags)} tags to {args.out}")

if name == "main":
main()
