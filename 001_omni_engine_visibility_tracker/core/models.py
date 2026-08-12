"""Data models and theme constants for Omni-Engine Visibility Tracker."""
from dataclasses import dataclass, field, asdict
from datetime import datetime

# ── Cyber-Pentagon Color Palette ─────────────────────────────────────────────
C = {
    "bg0":       "#0a0e17",
    "bg1":       "#111827",
    "bg2":       "#141d2e",
    "bg3":       "#1a2540",
    "cyan":      "#00d4ff",
    "cyan_dim":  "#00aacc",
    "cyan_dark": "#003d4d",
    "text":      "#e2e8f0",
    "text2":     "#8892a4",
    "muted":     "#4a5568",
    "green":     "#00ff9d",
    "yellow":    "#ffb800",
    "red":       "#ff4b6e",
    "border":    "#1e3a5f",
    "sel":       "#0066aa",
    "purple":    "#7c3aed",
    "emerald":   "#16a34a",
}

PROVIDERS = {
    "gemini":     {"label": "◈ GEMINI",      "color": C["cyan"],    "model": "gemini-1.5-flash"},
    "perplexity": {"label": "◈ PERPLEXITY",  "color": C["purple"],  "model": "llama-3.1-sonar-large-128k-online"},
    "searchgpt":  {"label": "◈ SEARCHGPT",   "color": C["emerald"], "model": "gpt-4o-search-preview"},
}


@dataclass
class Attribution:
    url:           str
    domain:        str
    title:         str
    author:        str
    mention_count: int
    provider:      str
    timestamp:     str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self):
        return asdict(self)


@dataclass
class SearchResult:
    provider:      str
    query:         str
    response_text: str
    attributions:  list = field(default_factory=list)
    semantic_score: float = 0.0
    timestamp:     str = field(default_factory=lambda: datetime.now().isoformat())
    status:        str = "pending"   # "live" | "demo" | "error"

    def to_dict(self):
        return {
            "provider": self.provider,
            "query": self.query,
            "response_text": self.response_text,
            "attributions": [a.to_dict() if hasattr(a, "to_dict") else a for a in self.attributions],
            "semantic_score": self.semantic_score,
            "timestamp": self.timestamp,
            "status": self.status,
        }
