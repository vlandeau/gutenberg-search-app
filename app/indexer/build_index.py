import json
import pathlib
import re
import sys

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from search_core.models import Book

RAW = pathlib.Path(__file__).resolve().parents[1].parent / "data" / "raw"
OUT = pathlib.Path(__file__).resolve().parents[1].parent / "data" / "built"
OUT.mkdir(parents=True, exist_ok=True)


def load_txt(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def strip_gutenberg_boilerplate(s: str) -> str:
    start = re.search(r"\*\*\* START OF.+\*\*\*", s)
    end = re.search(r"\*\*\* END OF.+\*\*\*", s)
    if start and end:
        return s[start.end() : end.start()]
    return s


def main():
    picks = [
        ("austen_pride.txt", "Pride and Prejudice", "Jane Austen", "en"),
        (
            "doyle_baskervilles.txt",
            "The Hound of the Baskervilles",
            "Arthur Conan Doyle",
            "en",
        ),
        ("verne_terrealalune.txt", "De la terre à la lune", "Jules Verne", "fr"),
    ]
    books = []
    for fname, title, author, lang in picks:
        file_path = RAW / fname
        if file_path.exists():
            raw = strip_gutenberg_boilerplate(load_txt(file_path))
            book = Book(
                id=fname, title=title, author=author, language=lang, content=raw
            )
            books.append(
                {
                    "id": book.id,
                    "title": book.title,
                    "author": book.author,
                    "language": book.language,
                    "content": book.content,
                }
            )
        else:
            print(f"Warning: {file_path} not found, skipping")

    if books:
        (OUT / "books.json").write_text(
            json.dumps(books, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"Built index for {len(books)} books in {OUT / 'books.json'}")
    else:
        print("No books found to index")


if __name__ == "__main__":
    main()
