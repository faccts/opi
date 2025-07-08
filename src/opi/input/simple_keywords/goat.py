from opi.input.simple_keywords.base import (
    SimpleKeyword,
    SimpleKeywordBox,
)

__all__ = ("Goat",)


class Goat(SimpleKeywordBox):
    """Enum to store all simple keywords of type Goat."""

    GOAT = SimpleKeyword("goat")
    """SimpleKeyword: GOAT Methods."""
    GOAT_COARSE = SimpleKeyword("goat-coarse")
    """SimpleKeyword: GOAT Methods."""
    GOAT_DIVERSITY = SimpleKeyword("goat-diversity")
    """SimpleKeyword: GOAT Methods."""
    GOAT_ENTROPY = SimpleKeyword("goat-entropy")
    """SimpleKeyword: GOAT Methods."""
    GOAT_EXPLORE = SimpleKeyword("goat-explore")
    """SimpleKeyword: GOAT Methods."""
    GOAT_REACT = SimpleKeyword("goat-react")
    """SimpleKeyword: GOAT Methods."""
    GOAT_TS = SimpleKeyword("goat-ts")
    """SimpleKeyword: GOAT Methods."""
