from typing import List, Dict, Any
from .normalize import norm_text
from .trie import TitleTrie
from .bktree import BKTree
from .inverted_index import Postings
from .models import Book


class SearchEngine:
    def __init__(
        self,
        books: List[Book],
        title_trie: TitleTrie,
        vocab_tree: BKTree,
        postings: Postings,
    ):
        self.books = {b.id: b for b in books}
        self.title_trie = title_trie
        self.vocab_tree = vocab_tree
        self.postings = postings

    def autocomplete(self, q: str, limit: int = 10) -> List[str]:
        return self.title_trie.complete(norm_text(q), limit)

    def search_regex(
        self, pattern: str, case_insensitive: bool, per_book_limit: int = 20
    ) -> Dict[str, Any]:
        import re

        flags = re.IGNORECASE if case_insensitive else 0
        try:
            rx = re.compile(pattern, flags)
        except re.error:
            return {"error": "invalid_regex"}
        results = []
        for b in self.books.values():
            hits = []
            for m in rx.finditer(b.content):
                start, end = m.span()
                context = b.content[max(0, start - 60) : min(len(b.content), end + 60)]
                hits.append({"start": start, "end": end, "context": context})
                if len(hits) >= per_book_limit:
                    break
            if hits:
                results.append({"book_id": b.id, "title": b.title, "hits": hits})
        return {"results": results}

    def search_fuzzy(
        self, term: str, k: int = 1, per_token_docs: int = 5
    ) -> List[Dict[str, Any]]:
        q = norm_text(term)
        candidates = self.vocab_tree.search(q, k)
        out = []
        for tok, dist in sorted(candidates, key=lambda x: x[1]):
            docs = self.postings.get(tok, {})
            for book_id, positions in list(docs.items())[:per_token_docs]:
                out.append(
                    {
                        "token": tok,
                        "distance": dist,
                        "book_id": book_id,
                        "title": self.books[book_id].title,
                        "count": len(positions),
                    }
                )
        return out[:50]
