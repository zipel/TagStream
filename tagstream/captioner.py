from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
from typing import List
import torch

class Captioner:
def init(self, model_name: str = "Salesforce/blip-image-captioning-base", device: str = "cpu"):
self.device = device
self.processor = BlipProcessor.from_pretrained(model_name)
self.model = BlipForConditionalGeneration.from_pretrained(model_name).to(device)

def caption(self, image_path: str) -> str:
image = Image.open(image_path).convert("RGB")
inputs = self.processor(images=image, return_tensors="pt").to(self.device)
out = self.model.generate(**inputs, max_length=40)
caption = self.processor.decode(out[0], skip_special_tokens=True)
return caption

def batch_caption(self, image_paths: List[str]) -> List[str]:
captions = []
for p in image_paths:
try:
captions.append(self.caption(p))
except Exception:
captions.append("")
return captions
