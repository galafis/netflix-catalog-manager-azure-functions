"""Content catalog data models."""
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
import uuid


@dataclass
class Content:
    """Streaming content item."""
    title: str
    content_type: str  # movie, series, documentary
    genre: List[str]
    year: int
    rating: float
    duration_minutes: int
    description: str
    cast: List[str] = field(default_factory=list)
    director: str = ""
    language: str = "en"
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "content_type": self.content_type,
            "genre": self.genre,
            "year": self.year,
            "rating": self.rating,
            "duration_minutes": self.duration_minutes,
            "description": self.description,
            "cast": self.cast,
            "director": self.director,
            "language": self.language,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Content":
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})
