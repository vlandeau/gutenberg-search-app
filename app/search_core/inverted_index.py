from collections import defaultdict
from typing import Dict, List
from .tokenize import tokenize_with_offsets
from .normalize import norm_text
from .models import Book, Postings


def build_postings(books: List[Book]) -> Postings:
    postings: Postings = defaultdict(lambda: defaultdict(list))
    for b in books:
        norm = norm_text(b.content)
        for tok, start, _ in tokenize_with_offsets(norm):
            postings[tok][b.id].append(start)
    return postings


def build_vocab(postings: Postings) -> set[str]:
    return set(postings.keys())
