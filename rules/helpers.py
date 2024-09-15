import re
from typing import Iterable


def fix_number(number: int, force_plus_sign=False) -> str:
    if number == 0 and not force_plus_sign:
        return '0'
    return str(number) if number < 0 else f'+{number}'


def format_keywords(keywords: Iterable[str]) -> Iterable[str]:
    regex = re.compile(r'\s(?:\d+)?D(?:\d+)')
    for k in keywords:
        k = k.title()
        if match := regex.search(k):
            start, end = match.span(0)
            k = k[:start] + k[start:end].lower() + k[end:]
        yield k
