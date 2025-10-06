from typing import Literal

from pydantic import field_validator

from opi.input.blocks import Block
from opi.input.blocks.util import InputFilePath

__all__ = ("BlockDocker",)


class BlockDocker(Block):
    """Class to model %docker block in ORCA"""

    _name: str = "docker"
    docklevel: Literal["screening", "normal", "quick", "complete"] | None = None
    """Literal: "screening", "normal", "quick", "complete". Defines docking strategy."""
    evpes: Literal["gfnff", "gfn0xtb", "gfn1xtb", "gfn2xtb"] | None = None
    """Literal: "cdp, "gfnff", "gfn0xtb", "gfn1xtb", "gfn2xtb". PES for evolution step"""
    maxiter: int | None = None
    """int: Maximum number of swarm iterations."""
    miniter: int | None = None
    """int: Minimum number of swarm iterations."""
    printlevel: Literal["low", "normal", "high"] | None = None
    """Literal: "low", "normal", "high". Define print level."""
    popdensity: float | None = None
    """float: Population density based on the HOST grid."""
    nopt: int | None = None
    """int: Fixed number of structure to be optimized."""
    opt: bool | None = None
    """bool: Whether optimizations should be performed."""
    cumulative: bool | None = None
    """bool: Add the contents of the "GUEST" file on top of each other?."""
    popsize: int | None = None
    """int: Fixed number of population size."""
    fixhost: bool | None = None
    """bool: Fix coordinates of the HOST during all steps?"""
    guestcharge: int | None = None
    """int: set the charge of the guest"""
    guestmult: int | None = None
    """int: set the multiplicity of the guest"""
    nrepeatguest: int | None = None
    """int: number of times to repeat the content of the guest file"""
    evoptlevel: Literal["sloppyopt", "looseopt", "normalopt"] | None = None
    """Literal: "sloppyopt", "looseopt", "normalopt". Optimization thresholds."""
    randomseed: bool | None = None
    """bool: Use a random seed. Runs will always be completely random."""
    checkguesttopo: bool | None = None
    """bool: Check the guest's topology and discard structures if topology changed during docking."""
    guest: InputFilePath | None = None
    """InputFilePath: Guest input file, e.g., "guest.xyz"."""

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
