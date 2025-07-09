from typing import Literal

from pydantic import field_validator

from opi.input.blocks import Block, InputFilePath, IntGroup

__all__ = ("AtomList", "BlockGoat")


class AtomList(IntGroup):
    """
    Class to model `uphillatoms`, `topobreak`, `reactiveatoms` attributes in `BlockGeom`.
    """

    def __str__(self) -> str:
        return super().__str__() + " end"


class BlockGoat(Block):
    """Class to model %goat block in ORCA"""

    _name: str = "goat"
    usegoat: bool | None = None
    fac: float | None = None
    gradcompmu: float | None = None
    gradcompsigma: float | None = None
    initemp: float | None = None
    mintemp: float | None = None
    tempmult: float | None = None
    convcrit: int | None = None
    templist: float | None = None
    maxgradruns: int | None = None
    maxiter: int | None = None
    maxstruc: int | None = None
    randomtype: int | None = None
    randomangle: float | None = None
    endiff: float | None = None
    rmsd: float | None = None
    rotconstdiff: float | None = None
    maxrotconstdiff: float | None = None
    enperatom: float | None = None
    maxenperatom: float | None = None
    freeze: bool | None = None
    freezebonds: bool | None = None
    freezeangles: bool | None = None
    freezecistrans: bool | None = None
    freezeamides: bool | None = None
    autofrag: bool | None = None
    updateinternals: bool | None = None
    maxoptiter: int | None = None
    minglobaliter: int | None = None
    maxglobaliter: int | None = None
    checktopo: bool | None = None
    maxtopodiff: int | None = None
    keeptoporeact: bool | None = None
    randommaxgradcomp: bool | None = None
    align: bool | None = None
    comparefull: bool | None = None
    explore: bool | None = None
    react: bool | None = None
    optts: bool | None = None
    diversity: bool | None = None
    autocoarsegrain: bool | None = None
    randomseed: bool | None = None
    maxcoresopt: int | None = None
    splitworkers: int | None = None
    autosplit: bool | None = None
    maxuphilliter: int | None = None
    uphilltrust: float | None = None
    uphillmaxrmsd: float | None = None
    keepdata: bool | None = None
    nworkers: int | None = None
    maxitermult: float | None = None
    rmsdmetric: int | None = None
    maxentropy: bool | None = None
    conftemp: float | None = None
    mindels: float | None = None
    rotdegen: int | None = None
    confdegen: int | None = None
    rmsdboost: float | None = None
    gradboostminstruc: int | None = None
    rejectprevious: bool | None = None
    reduceinternals: bool | None = None
    sortbytopo: bool | None = None
    pushfraguphill: bool | None = None
    gfnuphill: Literal["XTB0", "XTB1", "XTB2", "GFNFF"] | None = None
    printinternals: bool | None = None
    freeheteroatoms: bool | None = None
    freenonhatoms: bool | None = None
    freefragments: bool | None = None
    maxen: float | None = None
    bondfactor: float | None = None
    skipinitopt: bool | None = None
    writereactfile: bool | None = None
    maxcoordnumber: int | None = None
    fixcoordnumber: int | None = None
    workerrandomstart: bool | None = None
    autowall: bool | None = None
    restartfromfirst: bool | None = None
    uphillatoms: AtomList | None = None
    topobreak: AtomList | None = None
    reactiveatoms: AtomList | None = None
    ensemblefile: InputFilePath | None = None

    @field_validator("topobreak", "reactiveatoms", mode="before")
    @classmethod
    def atomlist_instantiate(cls, inp: str | list[int | tuple[int, int]]) -> AtomList:
        """
        Parameters
        ----------
        inp : str | list[int | tuple[int | int]]
        """
        return AtomList.init(inp)

    @field_validator("ensemblefile", mode="before")
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
