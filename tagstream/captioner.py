try:
    from transformers import BlipProcessor, BlipForConditionalGeneration
except ImportError as exc:
    BlipProcessor = None
    BlipForConditionalGeneration = None
    _transformers_import_error = exc

try:
    from PIL import Image
except ImportError as exc:
    Image = None
    _pil_import_error = exc

try:
    import torch
except ImportError as exc:
    torch = None
    _torch_import_error = exc

from typing import List

class Captioner:
    def __init__(self, model_name: str = "Salesforce/blip-image-captioning-base", device: str = "cpu"):
        if BlipProcessor is None or BlipForConditionalGeneration is None:
            raise ImportError(
                "TagStream requires the transformers package for image captioning. "
                "Install it using `pip install -r requirements.txt` or `pip install transformers`.") from _transformers_import_error
        if Image is None:
            raise ImportError(
                "TagStream requires Pillow for image loading. "
                "Install it using `pip install -r requirements.txt` or `pip install Pillow`.") from _pil_import_error
        if torch is None:
            raise ImportError(
                "TagStream requires PyTorch for model execution. "
                "Install it using `pip install -r requirements.txt` or `pip install torch`.") from _torch_import_error
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
