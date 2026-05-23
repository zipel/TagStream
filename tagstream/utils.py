import re

def singularize(word: str) -> str:
    if word.endswith("ies"):
        return word[:-3] + "y"
    if word.endswith("s") and not word.endswith("ss"):
        return word[:-1]
    return word

def normalize_tags(tags):
    seen = set()
    out = []
    for t in tags:
        t = t.strip().lower()
        t = re.sub(r"\s+", " ", t)
        t = singularize(t)
        if t and t not in seen:
            seen.add(t)
            out.append(t)
    return out
