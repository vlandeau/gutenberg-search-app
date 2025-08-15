import pytest
from app.search_core.tokenize import tokenize_with_offsets

def test_basic_tokenization():
    s = "Hello, world!"
    tokens = list(tokenize_with_offsets(s))
    assert tokens == [
        ("Hello", 0, 5),
        ("world", 7, 12)
    ]

def test_empty_string():
    s = ""
    tokens = list(tokenize_with_offsets(s))
    assert tokens == []

def test_numbers_and_letters():
    s = "abc123 def456"
    tokens = list(tokenize_with_offsets(s))
    assert tokens == [
        ("abc123", 0, 6),
        ("def456", 7, 13)
    ]

def test_non_alnum_separators():
    s = "foo-bar_baz!qux"
    tokens = list(tokenize_with_offsets(s))
    assert tokens == [
        ("foo", 0, 3),
        ("bar", 4, 7),
        ("baz", 8, 11),
        ("qux", 12, 15)
    ]

def test_unicode_characters():
    s = "café naïve résumé"
    tokens = list(tokenize_with_offsets(s))
    assert tokens == [
        ("café", 0, 4),
        ("naïve", 5, 10),
        ("résumé", 11, 17)
    ]

def test_token_at_end():
    s = "test!"
    tokens = list(tokenize_with_offsets(s))
    assert tokens == [("test", 0, 4)]
