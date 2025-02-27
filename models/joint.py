from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Joint:
    name: str
    points: List[int]
    id: Optional[int] = None