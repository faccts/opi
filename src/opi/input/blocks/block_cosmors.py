from pydantic import field_validator

from opi.input.blocks import Block, InputFilePath
from opi.input.simple_keywords import SimpleKeyword, Solvent

__all__ = ("BlockCosmors",)


class BlockCosmors(Block):
    """Class to model %cosmors block in ORCA"""

    _name: str = "cosmors"
    orbs_vac: bool | None = None
    aeff: float | None = None
    lnalpha: float | None = None
    lnchb: float | None = None
    chbt: float | None = None
    sigmahb: float | None = None
    rav: float | None = None
    fcorr: float | None = None
    ravcorr: float | None = None
    astd: float | None = None
    zcoord: float | None = None
    dgsolv_eta: float | None = None
    dgsolv_omegaring: float | None = None
    temp: float | None = None
    dftfunc: SimpleKeyword | None = None
    dftbas: SimpleKeyword | None = None
    solvent: Solvent | None = None
    solventfilename: InputFilePath | None = None

    @field_validator("solventfilename", mode="before")
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
