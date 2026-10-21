from opi.input.simple_keywords.base import (
    ORCAKeyword,
    SimpleKeywordBox,
)

__all__ = ("Solvation",)


class Solvation(SimpleKeywordBox):
    """Enum to store all simple keywords of type Solvation."""

    DRACO = ORCAKeyword("draco")
    """ORCAKeyword: apply dynamic charge dependent scaling of the solvation radii."""
    ECRISM = ORCAKeyword("ecrism")
    """ORCAKeyword: Use ecrism solvation model."""
    SMD18 = ORCAKeyword("smd18")
    """ORCAKeyword: Use refinde SMD18 model with different radii for Br and I."""
