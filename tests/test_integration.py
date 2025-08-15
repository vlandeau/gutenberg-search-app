import sys
import pathlib

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from app.search_core.models import Book
from app.search_core.trie import TitleTrie
from app.search_core.bktree import BKTree
from app.search_core.inverted_index import build_postings, build_vocab
from app.search_core.normalize import norm_text
from app.search_core.search import SearchEngine


def create_test_books():
    return [
        Book(
            id="test1",
            title="Pride and Prejudice",
            author="Jane Austen",
            language="en",
            content="It is a truth universally acknowledged, that a single man in possession of a good fortune, must be in want of a wife. However little known the feelings or views of such a man may be on his first entering a neighbourhood, this truth is so well established, that he is considered the rightful property of some one or other of the daughters.",
        ),
        Book(
            id="test2",
            title="The Hound of the Baskervilles",
            author="Arthur Conan Doyle",
            language="en",
            content="Mr. Sherlock Holmes, who was usually very late in the mornings, save upon those not infrequent occasions when he was up all night, was seated at the breakfast table. I stood upon the hearth-rug and picked up the stick which our visitor had left behind him the night before.",
        ),
    ]


def test_search_engine_integration():
    books = create_test_books()

    trie = TitleTrie()
    for b in books:
        trie.insert(norm_text(b.title), b.title)

    postings = build_postings(books)
    vocab = build_vocab(postings)
    bkt = BKTree(vocab)

    engine = SearchEngine(books, trie, bkt, postings)

    # Test autocomplete
    suggestions = engine.autocomplete("pri")
    assert "Pride and Prejudice" in suggestions

    # Test regex search
    regex_results = engine.search_regex(r"\bman\b", True)
    assert len(regex_results["results"]) > 0

    # Test fuzzy search
    fuzzy_results = engine.search_fuzzy("sherlok", k=1)
    assert len(fuzzy_results) > 0


def test_autocomplete_case_insensitive():
    books = create_test_books()

    trie = TitleTrie()
    for b in books:
        trie.insert(norm_text(b.title), b.title)

    postings = build_postings(books)
    vocab = build_vocab(postings)
    bkt = BKTree(vocab)

    engine = SearchEngine(books, trie, bkt, postings)

    suggestions_lower = engine.autocomplete("pride")
    suggestions_upper = engine.autocomplete("PRIDE")

    assert "Pride and Prejudice" in suggestions_lower
    assert "Pride and Prejudice" in suggestions_upper


if __name__ == "__main__":
    test_search_engine_integration()
    test_autocomplete_case_insensitive()
    print("All integration tests passed!")
