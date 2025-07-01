from opi.input.simple_keywords.base import (
    SimpleKeyword,
    SimpleKeywordBox,
)

__all__ = ("Solvation",)


class Solvation(SimpleKeywordBox):
    """Enum to store all simple keywords of type Solvation.

    Attributes
    ----------
    DRACO : SimpleKeyword
        apply dynamic charge dependent scaling of the solvation radii
    ECRISM : SimpleKeyword
        Use ecrism solvation model
    SMD18 : SimpleKeyword
        Use refinde SMD18 model with different radii for Br and I
    """

    DRACO = SimpleKeyword("draco")
    ECRISM = SimpleKeyword("ecrism")
    SMD18 = SimpleKeyword("smd18")
