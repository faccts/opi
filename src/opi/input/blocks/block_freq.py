from pathlib import Path

from pydantic import FilePath, field_validator

from opi.input.blocks import Block, IntGroup

__all__ = ("HessList", "BlockFreq")


class HessList(IntGroup):
    """
    Class to model `hybrid_hess` and `partial_hess` attributes in `BlockFreq`
    """

    def __str__(self) -> str:
        return super().__str__() + " end"


class BlockFreq(Block):
    """Class to model %freq block in ORCA"""

    _name: str = "freq"
    numfreq: bool | None = None
    anfreq: bool | None = None
    dovcd: bool | None = None
    centraldiff: bool | None = None
    restart: bool | None = None  # Restart numerical frequency calculation?
    increment: float | None = None  # Sets the increment in numerical freq
    quasirrho: bool | None = None  # Use quasi RRHO?
    cutofffreq: float | None = None  # cutoff value for low freqs
    qrrhoreffreq: float | None = None  # QRRHO reference frequency
    scalfreq: float | None = None
    transinvar: bool | None = None  # Make sure the hessian is translational invariant
    projecttr: bool | None = None  # Project our translation and rotation in the hessian?
    finitediff: bool | None = None
    accuracy: int | None = None
    hessgridx: int | None = None
    dryrun: bool | None = None
    nearir: bool | None = None
    xtbvpt2: bool | None = None
    delq: float | None = None
    temp: float | None = None
    pressure: float | None = None
    hybrid_hess: HessList | None = None
    partial_hess: HessList | None = None
    inhessname: FilePath | None = None

    @field_validator("inhessname")
    @classmethod
    def check_inhessname(cls, path: FilePath | str) -> FilePath:
        """
        Parameters
        ----------
        path : FilePath | str
        """
        file_path = Path(path) if isinstance(path, str) else path
        return file_path

    @field_validator("hybrid_hess", "partial_hess", mode="before")
    @classmethod
    def hessian_list(cls, ints: list[int]) -> HessList:
        """
        Parameters
        ----------
        ints : list[int]
        """
        return HessList.init(ints)
