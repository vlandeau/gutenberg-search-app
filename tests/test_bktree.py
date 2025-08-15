import sys
import pathlib

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from app.search_core.bktree import BKTree


def test_bktree_basic():
    vocab = ["hello", "world", "help", "test"]
    tree = BKTree(vocab)

    results = tree.search("hello", 0)
    assert ("hello", 0) in results

    results = tree.search("helo", 1)
    distances = {term: dist for term, dist in results}
    assert distances.get("hello") == 1


def test_bktree_fuzzy_search():
    vocab = ["baskerville", "basket", "basic", "mask"]
    tree = BKTree(vocab)

    results = tree.search("baskervile", 1)
    distances = {term: dist for term, dist in results}
    assert distances.get("baskerville") == 1


def test_bktree_no_matches():
    vocab = ["hello", "world"]
    tree = BKTree(vocab)

    results = tree.search("xyz", 1)
    assert len(results) == 0


def test_bktree_empty():
    tree = BKTree([])
    results = tree.search("test", 1)
    assert len(results) == 0


if __name__ == "__main__":
    test_bktree_basic()
    test_bktree_fuzzy_search()
    test_bktree_no_matches()
    test_bktree_empty()
    print("All BKTree tests passed!")
