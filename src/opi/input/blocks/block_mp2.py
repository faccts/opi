from typing import Literal

from pydantic import field_validator

from opi.input.blocks import Block, InputString, NumList

__all__ = ("BlockMp2",)


class BlockMp2(Block):
    """Class to model %mp2 block in ORCA"""

    _name: str = "mp2"
    maxcore: int | None = None
    emin: float | None = None
    emax: float | None = None
    ri: bool | None = None
    f12: bool | None = None
    forcedirect: bool | None = None
    printlevel: int | None = None
    natorbs: bool | None = None
    natorb: bool | None = None
    donatorbs: bool | None = None
    donatorb: bool | None = None
    tnat: float | None = None
    doscs: bool | None = None
    pt: float | None = None
    ps: float | None = None
    doregmp2: bool | None = None
    regmp2type: int | None = None
    regmp2kappa: float | None = None
    regmp2sigma: float | None = None
    density: Literal["relaxed", "unrelaxed", "none"] | None = None
    usepertcanorbs: bool | None = None
    pertcan_ethresh: float | None = None
    pertcan_uthresh: float | None = None
    storetnmr: bool | None = None
    dijconvnmr: bool | None = None
    nmrstoret: bool | None = None
    nmrdijconv: bool | None = None
    eprstoret: bool | None = None
    eprdijconv: bool | None = None
    respstoret: bool | None = None
    respdijconv: bool | None = None
    kcopt: Literal["_aoblas", "_cosx"] | None = None
    orbopt: bool | None = None
    moopt: bool | None = None
    calcs2: bool | None = None
    maxorbiter: int | None = None
    mp2shift: float | None = None
    mp2solver: Literal["effectivefock", "cpscf"] | None = None
    gridx: int | None = None
    usexgrid: bool | None = None
    xcorrection: int | None = None
    intaccx: float | None = None
    kc_gridx: int | None = None
    kc_usexgrid: bool | None = None
    kc_xcorrection: int | None = None
    kc_intaccx: float | None = None
    dlpno: bool | None = None
    maxlociter: int | None = None
    maxpnoiter: int | None = None
    tole: float | None = None
    tolr: float | None = None
    loctol: float | None = None
    locdvdroots: int | None = None
    locdvdrootsfinal: int | None = None
    tcutpno: float | None = None
    tscalepno_core: float | None = None
    tscalepno_lshift: float | None = None
    tcutpno_range: float | None = None
    tcutdo: float | None = None
    tcutmkn: float | None = None
    fcut: float | None = None
    paooverlapthresh: float | None = None
    paosthresh_scale: float | None = None
    paosthresh_high: float | None = None
    tcutpre: float | None = None
    tcutdoij: float | None = None
    tcutdopre: float | None = None
    scaletcutc_mo: float | None = None
    tcutc: float | None = None
    maxdiis_pno: int | None = None
    diisstart_pno: int | None = None
    damp1_pno: float | None = None
    damp2_pno: float | None = None
    mp2shift_pno: float | None = None
    lagrconds: int | None = None
    zloc_tol: float | None = None
    zloc_maxiter: int | None = None
    zloc_maxdiis: int | None = None
    zloc_shift: float | None = None
    zloc_ethresh: float | None = None
    zloc_ethresh_core: float | None = None
    zloc_usedavidson: bool | None = None
    zloc_dvdroots: int | None = None
    zloc_dvdtole: float | None = None
    zloc_dvdtolr: float | None = None
    zloc_dvdniter: int | None = None
    zloc_dvdmaxdim: int | None = None
    storedlpnodata: bool | None = None
    locpopmethod: Literal["mulliken", "loewdin"] | None = None
    locmet: (
        Literal[
            "pipekmezey",
            "pm",
            "fosterboys",
            "fb",
            "iaoibo",
            "iaoboys",
            "newboys",
            "ahfb",
        ]
        | None
    ) = None
    locvirtopt: Literal["pao", "lmo"] | None = None
    dlpnograd_opt: Literal["auto", "ram", "disk", "buffered"] | None = None
    zloc_solver: Literal["dir", "jac", "cg"] | None = None
    ewin: NumList | None = None
    refbasename: InputString | None = None
    locguess: InputString | None = None

    @field_validator("refbasename", "locguess", mode="before")
    @classmethod
    def init_inputstring(cls, string: str | InputString) -> InputString:
        """
        Parameters
        ----------
        string : str | InputString
        """
        if isinstance(string, str):
            return InputString(string=string.strip())
        else:
            return string

    @field_validator("ewin", mode="before")
    @classmethod
    def numlist_fromlist(cls, inp: NumList | list[int | float]) -> NumList:
        """
        Parameters
        ----------
        inp : NumList | list[int | float]
        """
        if isinstance(inp, list):
            return NumList(inp)
        else:
            return inp
