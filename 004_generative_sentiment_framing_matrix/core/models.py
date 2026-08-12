from dataclasses import dataclass, field
from typing import List, Dict

# -- Neumorphic Dark Theme (Lavender & Charcoal) -------------------------------
THEME = {
    "bg":        "#1a1a1a", # Charcoal
    "surface":   "#222222",
    "shadow_l":  "#2b2b2b", # Light shadow
    "shadow_d":  "#0f0f0f", # Dark shadow
    "lavender":  "#b39ddb", # Primary Accent
    "text":      "#e0e0e0",
    "muted":     "#888888",
}

@dataclass
class SentimentResult:
    score: float # -1.0 to 1.0
    label: str   # POS, NEG, NEU
    framing: str # e.g., "Premium Leader", "Cheap Alternative", "Technical Authority"
    confidence: float

@dataclass
class MatrixPoint:
    brand: str
    sentiment: float
    authority: float
    framing_index: int
    text_sample: str

@dataclass
class SimulationResult:
    temperature: float
    response: str
    sentiment_shift: float
