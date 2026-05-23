from keybert import KeyBERT
from typing import List
import re

_kw_model = KeyBERT(model="all-MiniLM-L6-v2")

def normalize_token(tok: str) -> str:
tok = tok.lower().strip()
tok = re.sub(r"[^\w\s-]", "", tok)
return tok

def extract_keywords_from_captions(captions: List[str], top_n_per_caption: int = 8) -> List[str]:
candidates = []
for cap in captions:
if not cap:
continue
kws = _kw_model.extract_keywords(cap, keyphrase_ngram_range=(1,2), stop_words="english", top_n=top_n_per_caption)
for kw, score in kws:
candidates.append(normalize_token(kw))
seen = set()
uniq = []
for c in candidates:
if c not in seen:
seen.add(c)
uniq.append(c)
return uniq
