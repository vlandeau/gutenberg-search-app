from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class TrieNode:
    children: Dict[str, "TrieNode"] = field(default_factory=dict)
    terminal: bool = False
    titles: List[str] = field(default_factory=list)


class TitleTrie:
    def __init__(self) -> None:
        self.root = TrieNode()

    def insert(self, normalized_key: str, original_title: str) -> None:
        node = self.root
        for ch in normalized_key:
            node = node.children.setdefault(ch, TrieNode())
        node.terminal = True
        if original_title not in node.titles:
            node.titles.append(original_title)
            if len(node.titles) > 8:
                node.titles.pop(0)

    def complete(self, prefix: str, limit: int = 10) -> List[str]:
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return []
            node = node.children[ch]
        out: List[str] = []

        def dfs(n: TrieNode) -> None:
            nonlocal out
            if len(out) >= limit:
                return
            out.extend([t for t in n.titles if t not in out])
            if len(out) >= limit:
                return
            for child in n.children.values():
                dfs(child)

        dfs(node)
        return out[:limit]
