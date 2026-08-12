"""Attribution extractor + Semantic proximity engine."""
import re
from .models import Attribution
from datetime import datetime

# ── Attribution Extractor ─────────────────────────────────────────────────────
_URL_RE   = re.compile(r'https?://[^\s<>"\']+')
_DOM_RE   = re.compile(r'(?:https?://)?(?:www\.)?([^/\s\'"]+)')
_AUTH_RE  = [
    re.compile(r'(?:by|author:|written by|via)\s+([A-Z][a-z]+ [A-Z][a-z]+)', re.I),
    re.compile(r'([A-Z][a-z]+ [A-Z][a-z]+)\s+(?:reports?|writes?|says?)', re.I),
    re.compile(r'@([a-zA-Z0-9_]{3,20})'),
]
_TITLE_RE = [
    re.compile(r'"([^"]{10,100})"'),
    re.compile(r'\u201c([^\u201d]{10,100})\u201d'),
    re.compile(r'\[([^\]]{10,80})\]'),
]


class AttributionExtractor:
    def extract(self, text: str, provider: str, limit: int = 20) -> list[Attribution]:
        urls = list(dict.fromkeys(_URL_RE.findall(text)))  # deduplicate, preserve order

        authors = []
        for pat in _AUTH_RE:
            authors.extend(pat.findall(text))

        titles = []
        for pat in _TITLE_RE:
            titles.extend(pat.findall(text))

        results = []
        for i, url in enumerate(urls[:limit]):
            m = _DOM_RE.match(url)
            domain = m.group(1) if m else url
            results.append(Attribution(
                url=url,
                domain=domain,
                title=titles[i] if i < len(titles) else domain,
                author=authors[i] if i < len(authors) else "Unknown",
                mention_count=text.lower().count(domain.lower()),
                provider=provider,
            ))
        return results


# ── Semantic Proximity Engine ─────────────────────────────────────────────────
class SemanticEngine:
    _model = None
    _ready = False

    @classmethod
    def load(cls) -> bool:
        try:
            from sentence_transformers import SentenceTransformer
            cls._model = SentenceTransformer("all-MiniLM-L6-v2")
            cls._ready = True
        except Exception:
            cls._ready = False
        return cls._ready

    @classmethod
    def score(cls, query: str, response: str) -> float:
        if cls._ready and cls._model:
            try:
                from sentence_transformers import util
                eq = cls._model.encode(query, convert_to_tensor=True)
                er = cls._model.encode(response[:2000], convert_to_tensor=True)
                return float(max(0.0, min(1.0, util.cos_sim(eq, er).item())))
            except Exception:
                pass
        # Keyword-overlap fallback
        qw = set(query.lower().split())
        rw = set(response.lower().split())
        return min(len(qw & rw) / max(len(qw), 1) * 2, 1.0)
