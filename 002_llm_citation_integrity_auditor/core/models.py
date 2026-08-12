"""Data models and theme constants for Citation Integrity Auditor."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

# -- Medical-Laboratory Theme (Fluent Design) ----------------------------------
THEME = {
    "bg":          "#f8fafc", # Soft Clinical White
    "card":        "#ffffff",
    "emerald":     "#10b981", # Primary Action
    "emerald_dim": "#d1fae5",
    "slate":       "#64748b", # Muted Text
    "navy":        "#0f172a", # Header Text
    "border":      "#e2e8f0",
    "red":         "#ef4444", # Hallucination Alert
    "yellow":      "#f59e0b", # Partial Grounding
}

class GroundingLevel(Enum):
    VERIFIED = "Verified"
    PARTIAL = "Partial"
    HALLUCINATION = "Hallucination"
    UNCERTAIN = "Uncertain"

@dataclass
class Citation:
    url: str
    index: int
    source_text: str = ""
    status: str = "Pending"

@dataclass
class Claim:
    text: str
    citations: list[Citation] = field(default_factory=list)
    grounding_score: float = 0.0
    status: GroundingLevel = GroundingLevel.UNCERTAIN
    diff_html: str = "" # To store the interactive diff view

@dataclass
class AuditResult:
    query: str
    llm_response: str
    overall_score: float
    claims: list[Claim]
    timestamp: datetime = field(default_factory=datetime.now)
    developer: str = "HSINI MOHAMED"
