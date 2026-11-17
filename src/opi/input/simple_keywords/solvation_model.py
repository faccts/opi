from opi.input.simple_keywords.base import (
    ORCAKeyword,
    SimpleKeywordBox,
)
from opi.input.simple_keywords.solvent import Solvent

__all__ = ("SolvationModel",)


class SolvationModelAndSolvent(ORCAKeyword):
    def __init__(self, model: str) -> None:
        super().__init__(model)

    def __call__(self, solvent: Solvent, /) -> ORCAKeyword:
        if not isinstance(solvent, Solvent | str):
            raise TypeError(f"Solvent '{solvent}' is not of valid type!")
        return ORCAKeyword(f"{self.keyword}({solvent})")


class SolvationModel(SimpleKeywordBox):
    """SolvationModel enum to store all valid Solvation Models for ORCA calculations"""

    CPCM = SolvationModelAndSolvent("CPCM")
    SMD = SolvationModelAndSolvent("SMD")
    COSMORS = SolvationModelAndSolvent("COSMORS")
