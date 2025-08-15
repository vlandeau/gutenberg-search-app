from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class Book:
    id: str
    title: str
    author: str | None
    language: str | None
    content: str


Postings = Dict[str, Dict[str, List[int]]]
