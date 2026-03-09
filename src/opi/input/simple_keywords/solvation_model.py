from opi.input.simple_keywords.base import (
    SimpleKeyword,
    SimpleKeywordBox,
)
from opi.input.simple_keywords.solvent import Solvent

__all__ = ("SolvationModel",)


class SolvationModelAndSolvent(SimpleKeyword):
    def __init__(self, model: str) -> None:
        super().__init__(model)

    def __call__(self, solvent: Solvent, /) -> SimpleKeyword:
        if not isinstance(solvent, Solvent):
            raise TypeError(f"Solvent '{solvent}' is not of Solvent type!")
        return SimpleKeyword(f"{self.keyword}({solvent})")


class SolvationModel(SimpleKeywordBox):
    """SolvationModel enum to store all valid Solvation Models for ORCA calculations"""

    CPCM = SolvationModelAndSolvent("CPCM")
    SMD = SolvationModelAndSolvent("SMD")
    COSMORS = SolvationModelAndSolvent("COSMORS")
