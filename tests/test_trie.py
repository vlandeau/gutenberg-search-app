import sys
import pathlib

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from app.search_core.trie import TitleTrie
from app.search_core.normalize import norm_text


def test_trie_basic():
    trie = TitleTrie()
    trie.insert(norm_text("Pride and Prejudice"), "Pride and Prejudice")
    trie.insert(norm_text("Pride and Zombies"), "Pride and Zombies")

    results = trie.complete(norm_text("pride"))
    assert "Pride and Prejudice" in results
    assert "Pride and Zombies" in results


def test_trie_case_insensitive():
    trie = TitleTrie()
    trie.insert(norm_text("The Great Gatsby"), "The Great Gatsby")

    results = trie.complete(norm_text("the great"))
    assert "The Great Gatsby" in results

    results = trie.complete(norm_text("THE GREAT"))
    assert "The Great Gatsby" in results


def test_trie_accent_insensitive():
    trie = TitleTrie()
    trie.insert(norm_text("De la terre à la lune"), "De la terre à la lune")

    results = trie.complete(norm_text("de la terre a"))
    assert "De la terre à la lune" in results


def test_trie_no_matches():
    trie = TitleTrie()
    trie.insert(norm_text("Pride and Prejudice"), "Pride and Prejudice")

    results = trie.complete(norm_text("xyz"))
    assert len(results) == 0


if __name__ == "__main__":
    test_trie_basic()
    test_trie_case_insensitive()
    test_trie_accent_insensitive()
    test_trie_no_matches()
    print("All Trie tests passed!")
