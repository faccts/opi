from typing import Literal

from pydantic import field_validator

from opi.input.blocks import Block, InputFilePath

__all__ = ("BlockDocker",)


class BlockDocker(Block):
    """Class to model %docker block in ORCA"""

    _name: str = "docker"
    docklevel: Literal["screening", "normal", "quick", "complete"] | None = None
    evpes: Literal["gfnff", "gfn0xtb", "gfn1xtb", "gfn2xtb"] | None = None
    maxiter: int | None = None
    miniter: int | None = None
    printlevel: Literal["low", "normal", "high"] | None = None
    popdensity: float | None = None
    nopt: int | None = None
    cumulative: bool | None = None
    popsize: int | None = None
    fixhost: bool | None = None
    guestcharge: int | None = None
    guestmult: int | None = None
    nrepeatguest: int | None = None
    evoptlevel: Literal["sloppyopt", "looseopt", "normalopt"] | None = None
    randomseed: bool | None = None
    checkguesttopo: bool | None = None
    guest: InputFilePath | None = None

    @field_validator("guest", mode="before")
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
