from opi.input.simple_keywords.base import (
    ORCAKeyword,
    SimpleKeywordBox,
)

__all__ = ("Goat",)


class Goat(SimpleKeywordBox):
    """Enum to store all simple keywords of type Goat."""

    GOAT = ORCAKeyword("goat")
    """ORCAKeyword: GOAT Methods."""
    GOAT_COARSE = ORCAKeyword("goat-coarse")
    """ORCAKeyword: GOAT Methods."""
    GOAT_DIVERSITY = ORCAKeyword("goat-diversity")
    """ORCAKeyword: GOAT Methods."""
    GOAT_ENTROPY = ORCAKeyword("goat-entropy")
    """ORCAKeyword: GOAT Methods."""
    GOAT_EXPLORE = ORCAKeyword("goat-explore")
    """ORCAKeyword: GOAT Methods."""
    GOAT_REACT = ORCAKeyword("goat-react")
    """ORCAKeyword: GOAT Methods."""
    GOAT_TS = ORCAKeyword("goat-ts")
    """ORCAKeyword: GOAT Methods."""
