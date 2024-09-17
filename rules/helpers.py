import json
import re
from pathlib import Path
from typing import Iterable, Iterator

import jsonschema
import jsonschema.exceptions


def fix_number(number: int, force_plus_sign=False) -> str:
    """Convert an integer into a modifier style.  For example, 3 would be converted
    into '+3'.

    Args:
        number (int): The modifier to convert
        force_plus_sign (bool, optional): Force the use of a plus sign on zero modifiers. Defaults to False.

    Returns:
        str: The modifier styled as a string
    """
    if number == 0 and not force_plus_sign:
        return '0'
    return str(number) if number < 0 else f'+{number}'


def format_keywords(keywords: Iterable[str]) -> Iterator[str]:
    """Fixes capitalization issues with keywords such as '1d8' so that it matches the
    formatting of the source books

    Args:
        keywords (Iterable[str]): The keywords to process

    Yields:
        str: A keyword post-formatting
    """
    regex = re.compile(r'\s(?:\d+)?D(?:\d+)')
    for k in keywords:
        k = k.title()
        if match := regex.search(k):
            start, end = match.span(0)
            k = k[:start] + k[start:end].lower() + k[end:]
        yield k


class Validator:
    """Quick validator class to validate the character sheet information file

    Attributes:
        schema (dict | list): The schema information
        schema_file (Path): The schema file
    """

    schema: dict | list
    schema_file: Path

    def __init__(self) -> None:
        self.schema_file = Path("validation/schema.json")
        self.schema = json.load(self.schema_file.open())

    def validate(self, content: dict | list) -> None:
        """Validate the content against the schema

        Args:
            content (dict | list): The contents of the file

        Raises:
            jsonschema.exceptions.ValidationError: When the content does not validate against the schema
        """
        jsonschema.exceptions.ValidationError
        jsonschema.validate(content, self.schema)
