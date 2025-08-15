import sys
import pathlib

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from app.search_core.levenshtein import distance_with_cutoff


def test_levenshtein_basic():
    assert distance_with_cutoff("cat", "cat", 2) == 0
    assert distance_with_cutoff("cat", "bat", 2) == 1
    assert distance_with_cutoff("cat", "dog", 2) is None
    assert distance_with_cutoff("kitten", "sitting", 3) == 3


def test_levenshtein_cutoff():
    assert distance_with_cutoff("hello", "world", 2) is None
    assert distance_with_cutoff("hello", "helo", 2) == 1
    assert distance_with_cutoff("test", "taste", 2) == 2


def test_levenshtein_edge_cases():
    assert distance_with_cutoff("", "", 0) == 0
    assert distance_with_cutoff("", "a", 1) == 1
    assert distance_with_cutoff("a", "", 1) == 1
    assert distance_with_cutoff("", "abc", 2) is None


if __name__ == "__main__":
    test_levenshtein_basic()
    test_levenshtein_cutoff()
    test_levenshtein_edge_cases()
    print("All Levenshtein tests passed!")
