from sentence_transformers import SentenceTransformer, util
from typing import List
import torch

class Ranker:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2", device: str = "cpu"):
        self.device = device
        self.text_model = SentenceTransformer(model_name, device=device)

    def _embed_texts(self, texts: List[str]):
        return self.text_model.encode(texts, convert_to_tensor=True, show_progress_bar=False)

    def rank_and_filter(self, captions: List[str], candidates: List[str], top_k: int = 50) -> List[str]:
        if not candidates:
            return []
        if not captions:
            return candidates[:top_k]

        candidate_emb = self._embed_texts(candidates)
        caption_emb = self._embed_texts(captions)
        similarity = util.cos_sim(candidate_emb, caption_emb)
        scores = similarity.max(dim=1).values.cpu().numpy()
        ranked = [c for _, c in sorted(zip(scores, candidates), reverse=True)]
        return ranked[:top_k]
