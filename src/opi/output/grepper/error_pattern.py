# patterns.py
from dataclasses import dataclass
from typing import Callable


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
    extractor: Callable[[str], str] | None = None


# > extractor functions for more elaborate error messages
def _extract_keyword(line: str) -> str:
    # e.g. parse "Unknown keyword: BLYPP" from the matched line
    return f"Unknown/duplicate keyword: {line.split()[-1].strip()}"
