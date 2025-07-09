from typing import Literal

from pydantic import field_validator

from opi.input.blocks import Block, InputFilePath
from opi.input.blocks.geom_wrapper import Internal, Internals

__all__ = ("BlockIrc",)


class BlockIrc(Block):
    """Class to model %irc block in ORCA"""

    _name: str = "irc"
    maxiter: int | None = None
    direction: Literal["both", "forward", "backward", "down"] | None = None
    inithess: Literal["read", "calc_anfreq", "calc_numfreq"] | None = None
    hessmode: int | None = None
    irc_centraldiff: bool | None = None
    init_displ: Literal["de", "length"] | None = None
    scale_init_displ: float | None = None
    de_init_displ: float | None = None
    scale_displ_sd: float | None = None
    scale_displ_sd_corr: float | None = None
    adapt_scale_displ: bool | None = None
    do_sd_corr: bool | None = None
    sd_parabolicfit: bool | None = None
    sd_corr_parabolicfit: bool | None = None
    interpolate_only: bool | None = None
    tolmaxg: float | None = None
    tolrmsg: float | None = None
    tolmaxd: float | None = None
    tolrmsd: float | None = None
    tole: float | None = None
    follow_coordtype: Literal["cartesian"] | None = None
    printlevel: int | None = None
    hess_filename: InputFilePath | None = None
    monitor_internals: Internals | None = None

    @field_validator("hess_filename", mode="before")
    @classmethod
    def path_from_string(cls, path: str | InputFilePath) -> InputFilePath:
        """
        Parameters
        ----------
        path : str | InputFilePath
        """
        if isinstance(path, str):
            return InputFilePath.from_string(path)

        return path

    @field_validator("monitor_internals", mode="before")
    @classmethod
    def internals_str(cls, strings: list[str] | str) -> Internals:
        """
        Parameters
        ----------
        strings : list[str] | str
        """
        try:
            if isinstance(strings, list):
                internals = [Internal.from_string(s) for s in strings]
            else:
                internals = [Internal.from_string(strings)]
        except Exception as e:
            raise ValueError(f"Failed to parse strings: {e}")

        return Internals(internals=internals)
