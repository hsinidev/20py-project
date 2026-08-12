from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

class Keyword(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    term: str = Field(index=True, unique=True)
    category: str = "General"
    ranks: List["RankHistory"] = Relationship(back_populates="keyword")

class RankHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    keyword_id: int = Field(foreign_key="keyword.id")
    position: int # Rank position (1-10)
    domain: str
    is_top_tier: bool = False
    timestamp: datetime = Field(default_factory=datetime.now)
    volatility: float = 0.0
    
    keyword: Optional[Keyword] = Relationship(back_populates="ranks")

class Proxy(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    address: str
    status: str = "Active"
    last_used: Optional[datetime] = None

# -- Trading-Floor Theme Constants ---------------------------------------------
COLORS = {
    "bg":           (10, 10, 10, 255),
    "green":        (0, 255, 127, 255),
    "red":          (255, 75, 110, 255),
    "grey":         (40, 40, 40, 255),
    "text":         (220, 220, 220, 255),
    "yellow":       (255, 184, 0, 255),
    "blue":         (0, 170, 255, 255),
}
