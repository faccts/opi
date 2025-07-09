from typing import Literal

from pydantic import field_validator

from opi.input.blocks import Block, NumList

__all__ = ("BlockCasscf",)


class BlockCasscf(Block):
    """Class to model %casscf block in ORCA"""

    _name: str = "casscf"
    nel: int | None = None
    norb: int | None = None
    mult: int | NumList | None = None
    irrep: int | NumList | None = None
    nroots: int | NumList | None = None
    bweight: float | NumList | None = None
    weights: float | None = None
    hessroot: int | None = None
    iroot: int | None = None
    jroot: int | None = None
    imult: int | None = None
    followiroot: bool | None = None
    followirootno: bool | None = None
    followirootmix: bool | None = None
    followiroottdens: bool | None = None
    orbstep: (
        Literal[
            "diis",
            "kdiis",
            "soscf",
            "superci",
            "superci_pt",
            "superci_ptno",
            "nr",
            "trah",
        ]
        | None
    ) = None
    cistep: (
        Literal[
            "csfci",
            "accci",
            "cipsi",
            "ice",
            "dmrgci",
            "qmcci",
            "molmpsci",
            "mccas",
            "detci",
            "treecsf",
        ]
        | None
    ) = None
    trafostep: Literal["exact", "rimo", "ri"] | None = None
    switchconv: float | None = None
    switchiter: int | None = None
    switchstep: int | None = None
    parametrization: Literal["cayley", "expk"] | None = None
    etol: float | None = None
    gtol: float | None = None
    printlevel: int | None = None
    printgstate: int | None = None
    printndo: int | None = None
    printwf: int | None = None
    actorbs: int | None = None
    actconstraints: Literal["unchanged", "canonorbs", "locorbs", "natorbs"] | None = None
    locmet: Literal["pipekmezey", "pm", "fosterboys", "fb", "iaoibo", "iaoboys", "ahfb"] | None = (
        None
    )
    nevpt2: int | None = None
    ptmethod: (
        Literal[
            "sc",
            "fic",
            "pc",
            "dlpno",
            "dlpno_nevpt2",
            "fic_nevpt2",
            "sc_nevpt2",
            "fic_caspt2",
            "fic_caspt2k",
            "fic_caspt2s",
        ]
        | None
    ) = None
    freezeactive: float | None = None
    dthresh: float | None = None
    buildhessian: int | None = None
    resethessian: int | None = None
    maxdampiter: int | None = None
    gradscaling: float | None = None
    convrate: float | None = None
    freezeie: float | None = None
    freezegrad: float | None = None
    superdiis: bool | None = None
    maxiter: int | None = None
    maxmicroiter: int | None = None
    maxdiis: int | None = None
    diisthresh: float | None = None
    resetfreq: int | None = None
    switchdens: float | None = None
    doipea: bool | None = None
    donto: bool | None = None
    ntothresh: float | None = None
    nntostates: int | None = None
    ntostates: int | None = None
    dondo: bool | None = None
    nndostates: int | None = None
    ndostates: int | None = None
    dotransdens: bool | None = None
    inistateenerrange: float | None = None
    docd: bool | None = None
    dodipolelength: bool | None = None
    dodipolevelocity: bool | None = None
    dohighermoments: bool | None = None
    dofullsemiclassical: bool | None = None
    decomposefosclength: bool | None = None
    decomposefoscvelocity: bool | None = None
    dotransient: int | None = None
    cas_ewin: NumList | None = None

    @field_validator("mult", "irrep", "nroots", "bweight", mode="before")
    @classmethod
    def numlist_fromlist(cls, inp: int | list[int] | NumList) -> int | NumList:
        """
        Parameters
        ----------
        inp : int | list[int] | NumList
        """
        if isinstance(inp, list):
            return NumList(inp)
        else:
            return inp

    @field_validator("cas_ewin", mode="before")
    @classmethod
    def qcas_ewin_init(cls, inp: list[float] | NumList) -> NumList:
        """
        Parameters
        ----------
        inp : list[float] | NumList
        """
        if isinstance(inp, list):
            return NumList(inp)
        else:
            return inp
