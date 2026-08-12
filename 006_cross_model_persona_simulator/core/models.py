from dataclasses import dataclass, field
from typing import Dict, List

# -- A/B Testing Theme Constants (Burgundy & Warm Grey) ------------------------
COLORS = {
    "burgundy": "#800020",
    "warm_grey": "#B8B0A8",
    "bg": "#F5F5F5",
    "panel_a": "#922B3E", # Lighter Burgundy
    "panel_b": "#E0DCD9", # Lighter Grey
    "text": "#333333",
    "accent": "#5D6D7E",
}

@dataclass
class ModelResponse:
    model_name: str
    text: str
    empathy: float     # 0.0 - 1.0
    caution: float     # 0.0 - 1.0
    directness: float  # 0.0 - 1.0
    latency: float

@dataclass
class Persona:
    name: str
    description: str
    traits: List[str]
