from typing import Literal

from pydantic import field_validator

from opi.input.blocks import Block, InputFilePath

__all__ = ("BlockSolvator",)


class BlockSolvator(Block):
    """Class to model %solvator block in ORCA"""

    _name: str = "solvator"
    nsolv: int | None = None
    randomsolv: bool | None = None
    droplet: bool | None = None
    radius: float | None = None
    fixsolute: bool | None = None
    clustermode: Literal["stochastic", "docking"] | None = None
    wallfac: float | None = None
    printlevel: Literal["low", "normal", "high"] | None = None
    vacuumsearch: bool | None = None
    useeeqcharges: bool | None = None
    solvatorfile: InputFilePath | None = None

    @field_validator("solvatorfile", mode="before")
    @classmethod
    def path_from_string(cls, path: str | InputFilePath) -> InputFilePath:
        """
        Parameters
        ----------
        path : str | InputFilePath
        """
        if isinstance(path, str):
            return InputFilePath.from_string(path)
        else:
            return path
