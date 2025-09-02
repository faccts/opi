from opi.input.simple_keywords.base import (
    SimpleKeyword,
    SimpleKeywordBox,
)

__all__ = ("Solvation",)


class Solvation(SimpleKeywordBox):
    """Enum to store all simple keywords of type Solvation."""

    DRACO = SimpleKeyword("draco")
    """SimpleKeyword: apply dynamic charge dependent scaling of the solvation radii."""
    ECRISM = SimpleKeyword("ecrism")
    """SimpleKeyword: Use ecrism solvation model."""
    SMD18 = SimpleKeyword("smd18")
    """SimpleKeyword: Use refinde SMD18 model with different radii for Br and I."""
