import unicodedata


def casefold(s: str) -> str:
    return s.casefold()


def strip_accents(s: str) -> str:
    nfkd = unicodedata.normalize("NFKD", s)
    return "".join(ch for ch in nfkd if not unicodedata.combining(ch))


def norm_text(s: str) -> str:
    return strip_accents(unicodedata.normalize("NFC", s)).casefold()
