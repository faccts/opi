from opi.input.simple_keywords.base import (
    SimpleKeyword,
    SimpleKeywordBox,
)

__all__ = ("Goat",)


class Goat(SimpleKeywordBox):
    """Enum to store all simple keywords of type Goat.

    Attributes
    ----------
    GOAT : SimpleKeyword
        GOAT Methods
    GOAT_COARSE : SimpleKeyword
        GOAT Methods
    GOAT_DIVERSITY : SimpleKeyword
        GOAT Methods
    GOAT_ENTROPY : SimpleKeyword
        GOAT Methods
    GOAT_EXPLORE : SimpleKeyword
        GOAT Methods
    GOAT_REACT : SimpleKeyword
        GOAT Methods
    GOAT_TS : SimpleKeyword
        GOAT Methods
    """

    GOAT = SimpleKeyword("goat")
    GOAT_COARSE = SimpleKeyword("goat-coarse")
    GOAT_DIVERSITY = SimpleKeyword("goat-diversity")
    GOAT_ENTROPY = SimpleKeyword("goat-entropy")
    GOAT_EXPLORE = SimpleKeyword("goat-explore")
    GOAT_REACT = SimpleKeyword("goat-react")
    GOAT_TS = SimpleKeyword("goat-ts")
