from typing import Dict, List, Tuple, Iterable
from .levenshtein import distance_with_cutoff


class BKNode:
    def __init__(self, term: str) -> None:
        self.term = term
        self.children: Dict[int, BKNode] = {}


class BKTree:
    def __init__(self, terms: Iterable[str]) -> None:
        self.root: BKNode | None = None
        for t in terms:
            self.insert(t)

    def insert(self, term: str) -> None:
        if self.root is None:
            self.root = BKNode(term)
            return
        node = self.root
        while True:
            d = distance_with_cutoff(term, node.term, 4) or 9999
            child = node.children.get(d)
            if child is None:
                node.children[d] = BKNode(term)
                return
            node = child

    def search(self, query: str, k: int) -> List[Tuple[str, int]]:
        if self.root is None:
            return []
        out: List[Tuple[str, int]] = []
        stack = [self.root]
        while stack:
            node = stack.pop()
            d = distance_with_cutoff(query, node.term, k)
            if d is not None and d <= k:
                out.append((node.term, d))
            for ed, child in node.children.items():
                if d is None:
                    if abs(ed) <= k + 1:
                        stack.append(child)
                elif d - k <= ed <= d + k:
                    stack.append(child)
        return out
