"""Sentence splitting shared by train.py (job postings) and handler.py (CVs)."""
import re


def sentences(text, limit=400):
    text = re.sub(r"(?<![.!?:;。！？])[ \t]*\r?\n[ \t]*(?=[a-z(])", " ", text[:60000])  # re-join wrapped lines
    parts = re.split(r"(?<=[.!?。！？])\s+|[\r\n]+|\s*[•·▪●]\s*", text)
    out = []
    for p in (p.strip(" -*\t") for p in parts):
        while len(p) > 300:  # keep chunks close to the short task descriptions the model was trained on
            cut = p.rfind(" ", 0, 300); cut = cut if cut > 100 else 300
            out.append(p[:cut]); p = p[cut:].strip()
        if len(p) >= 15:
            out.append(p)
    return out[:limit]


def term_regex(term):
    """Same rule as collector/build_dataset.py: whole word, case-insensitive, trailing * = prefix."""
    body = re.escape(term.rstrip("*"))
    return re.compile(r"(?<![a-z0-9])" + body + ("" if term.endswith("*") else r"(?![a-z0-9])"), re.I)
