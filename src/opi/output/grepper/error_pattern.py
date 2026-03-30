# patterns.py
from dataclasses import dataclass
from typing import Callable

from opi.output.grepper.core import Grepper


@dataclass
class ErrorPattern:
    """
    Represents an error pattern in the ORCA output file.

    Attributes
    ----------
    grep_string: str
        The string that is searched in the output file.
    message: str
        A human-readable error message of the given error pattern.
    extractor: Callable | None, default = None
        Optional function for extracting more details from the matched line

    """

    grep_string: str
    message: str
    extractor: Callable[[str, Grepper], str] | None = None


# > extractor functions for more elaborate error messages


def _simple_keywords(grep_string: str, grepper: Grepper) -> str:
    """parse "Unknown keyword: BLYPP" from the matched line"""
    match = grepper.search(grep_string, case_sensitive=True, skip_lines=1)
    return f"Unknown/duplicate simple keyword(s): {match[0]}" if match else ""


def _unknown_block(grep_string: str, grepper: Grepper) -> str:
    """"""
    match = grepper.search(grep_string, case_sensitive=True, skip_lines=0)
    return f"Unknown block: {match[0].split()[-1]}" if match else ""

def _unknown_block_key(grep_string: str, grepper: Grepper) -> str:
    """parse "Unknown keyword: BLYPP" from the matched line"""
    match = grepper.search(grep_string, case_sensitive=True, skip_lines=1)
    return f"Unknown block key: {match[0].split(':')[-1]}" if match else ""

def _unknown_block_value(grep_string: str, grepper: Grepper) -> str:
    """"""
    match = grepper.search(grep_string, case_sensitive=True, skip_lines=1)
    return f"Unknown block value: {match[0].split(':')[-1]}" if match else ""
