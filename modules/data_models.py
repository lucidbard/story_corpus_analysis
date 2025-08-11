from dataclasses import dataclass, asdict
from typing import List, Optional
from datetime import datetime
import json
from pathlib import Path

@dataclass
class Scene:
    scene_id: str
    book_id: str
    chapter_num: int
    scene_num: int
    text: str
    narrator: Optional[str] = None
    start_paragraph: Optional[int] = None
    end_paragraph: Optional[int] = None

@dataclass
class Goal:
    goal_id: str
    scene_id: str
    character: str
    goal_text: str
    motivation_type: str
    category: str
    evidence: str
    confidence: float

@dataclass
class ProcessingProgress:
    books_segmented: List[str]
    books_narrators_identified: List[str]
    books_goals_analyzed: List[str]
    last_updated: str
    total_books: int

    def save(self, filepath: Path):
        with open(filepath, 'w') as f:
            json.dump(asdict(self), f, indent=2)

    @classmethod
    def load(cls, filepath: Path):
        if filepath.exists():
            with open(filepath, 'r') as f:
                data = json.load(f)
            return cls(**data)
        return cls([], [], [], datetime.now().isoformat(), 0)
