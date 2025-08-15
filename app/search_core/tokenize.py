from typing import Iterator, Tuple


def tokenize_with_offsets(s: str) -> Iterator[Tuple[str, int, int]]:
    buf = []
    start = None
    for i, ch in enumerate(s):
        if ch.isalnum():
            if start is None:
                start = i
            buf.append(ch)
        elif buf:
            tok = "".join(buf)
            yield tok, start, i
            buf, start = [], None
    if buf:
        yield "".join(buf), start, len(s)
