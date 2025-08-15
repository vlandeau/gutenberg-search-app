import json
import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from search_core.trie import TitleTrie
from search_core.bktree import BKTree
from search_core.inverted_index import build_postings, build_vocab
from search_core.models import Book
from search_core.normalize import norm_text
from search_core.search import SearchEngine

data_dir = pathlib.Path(__file__).resolve().parents[1].parent / "data" / "built"
books_file = data_dir / "books.json"

if not books_file.exists():
    raise FileNotFoundError(
        f"Books index not found at {books_file}. Run the indexer first."
    )

books_data = json.loads(books_file.read_text())
books = [Book(**b) for b in books_data]

trie = TitleTrie()
for b in books:
    trie.insert(norm_text(b.title), b.title)

postings = build_postings(books)
vocab = build_vocab(postings)
bkt = BKTree(vocab)

engine = SearchEngine(books, trie, bkt, postings)
