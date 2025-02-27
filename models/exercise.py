from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Exercise:
    name: str
    description: Optional[str] = None
    id: Optional[int] = None

@dataclass
class Session:
    exercise_id: int
    reps: int
    timestamp: datetime = datetime.now()
    id: Optional[int] = None