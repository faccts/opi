from typing import Literal

from pydantic import field_validator

from opi.input.blocks import (
    Block,
    InputFilePath,
    IntGroup,
    NumList,
)

__all__ = ("BlockMdci",)


class BlockMdci(Block):
    """Class to model %mdci block in ORCA"""

    _name: str = "mdci"
    citype: Literal["cisd", "ccsd"] | None = None
    dosingles: bool | None = None
    dotriples: int | None = None
    usedavcis: bool | None = None
    doeom: bool | None = None
    doip: bool | None = None
    doea: bool | None = None
    doalpha: bool | None = None
    dobeta: bool | None = None
    dress3es: bool | None = None
    dress3ed: bool | None = None
    doaox3e: bool | None = None
    docosxeom: bool | None = None
    dosteom: bool | None = None
    dosimpledens: bool | None = None
    addl2term: bool | None = None
    updatel1: bool | None = None
    addddterm: bool | None = None
    dotransient: bool | None = None
    dotriplet: bool | None = None
    dotdm: bool | None = None
    doleft: bool | None = None
    dorootwise: bool | None = None
    nrootsperbatch: int | None = None
    dosolv: bool | None = None
    cvsep: bool | None = None
    docvs: bool | None = None
    xesfwhm: float | None = None
    xesnpoints: int | None = None
    xesnormalize: bool | None = None
    multicoreorb: bool | None = None
    rijcosxcis: bool | None = None
    docisnatpt: bool | None = None
    ccsd2: bool | None = None
    steomact: bool | None = None
    coretrans: bool | None = None
    acthresh: float | None = None
    steomsoc: bool | None = None
    donto: bool | None = None
    dorijcosx: bool | None = None
    recon2ed: bool | None = None
    dlpnosteom: bool | None = None
    cc2: bool | None = None
    dodyson: bool | None = None
    dlpnoeom: bool | None = None
    adc2: bool | None = None
    docd: bool | None = None
    dtol: float | None = None
    oorb: int | None = None
    vorb: int | None = None
    dorecan: bool | None = None
    invtol: float | None = None
    ipsthrs: float | None = None
    easthrs: float | None = None
    othresh: float | None = None
    vthresh: float | None = None
    docisnat: bool | None = None
    dostoresteom: bool | None = None
    dlpnoactspace: bool | None = None
    directdresssteom: bool | None = None
    dosteomnattransorb: bool | None = None
    doeommp2: bool | None = None
    dolpnoeom: bool | None = None
    dolpnosteom: bool | None = None
    docore: bool | None = None
    ndav: int | None = None
    nactip: int | None = None
    nactea: int | None = None
    nactip_a: int | None = None
    nactea_a: int | None = None
    nactip_b: int | None = None
    nactea_b: int | None = None
    corehole: int | None = None
    checkeachroot: bool | None = None
    roothoming: bool | None = None
    followcis: bool | None = None
    dolanczos: bool | None = None
    doolsen: bool | None = None
    usecisupdate: bool | None = None
    steomguess: bool | None = None
    useeomopts: bool | None = None
    useeomoptd: bool | None = None
    ninits: int | None = None
    localize: bool | None = None
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
    locrandom: bool | None = None
    locnattempts: int | None = None
    loctol: float | None = None
    loctolled: float | None = None
    loctolrel: float | None = None
    locmaxiter: int | None = None
    locmaxiterled: int | None = None
    dodidplot: bool | None = None
    covalpol: bool | None = None
    adld: bool | None = None
    adld_mulliken: bool | None = None
    adld_loewdin: bool | None = None
    adld_hirshfeld: bool | None = None
    adld_printspin: bool | None = None
    lmoread: bool | None = None
    lmorefprint: bool | None = None
    domdoi: bool | None = None
    domdoi_cc: bool | None = None
    led: int | None = None
    pnoextrapolation: int | None = None
    doledhf: bool | None = None
    brueckner: bool | None = None
    dof12: bool | None = None
    dof12ri: bool | None = None
    f12: bool | None = None
    dof12vt: bool | None = None
    coreopt: bool | None = None
    zsimple: bool | None = None
    useqros: bool | None = None
    userhfints: bool | None = None
    useseparatealphabeta: bool | None = None
    natorbiters: int | None = None
    donatorbs: bool | None = None
    pno: Literal["none", "diagonal", "diag", "full", "f12", "peo", "f12peo"] | None = None
    pnonorm: Literal["iepanorm", "mp2norm"] | None = None
    nrmp2pairs_trip: int | None = None
    paooverlapthresh: float | None = None
    usefulllmp2guess: int | None = None
    lmp2maxiter: int | None = None
    lmp2tole: float | None = None
    lmp2tolr: float | None = None
    lmp2fcut: float | None = None
    lmp2scaletcutpno: float | None = None
    singles_multilevel_mode: int | None = None
    maxdeloc: float | None = None
    overlapt: float | None = None
    pnoselection: int | None = None
    pnosel: (
        Literal["occupationnumber", "occnum", "occnum_en_enorder", "energy", "occnum_en"] | None
    ) = None
    pnooper: Literal["default", "fock", "psfock"] | None = None
    pnof12corr: bool | None = None
    pnof12coupling: bool | None = None
    pnodens: Literal["spinfree", "alphabeta"] | None = None
    pnosigmaopt: int | None = None
    pnosigma: int | None = None
    density: Literal["none", "linearized", "unrelaxed", "orbopt"] | None = None
    enforce_ccsd_density: bool | None = None
    triples_lin_dens: bool | None = None
    kcopt: (
        Literal[
            "kc_ao",
            "kc_mo",
            "kc_mo_ip",
            "kc_mo_ap",
            "kc_ri",
            "kc_ri2",
            "kc_aox",
            "kc_aox_gen",
            "kc_locaox",
            "kc_aoblas",
            "kc_cosx",
            "kc_ripno",
        ]
        | None
    ) = None
    gridx: int | None = None
    usexgrid: bool | None = None
    xcorrection: int | None = None
    intaccx: float | None = None
    tcutint: float | None = None
    tcutpairs: float | None = None
    tcutpno: float | None = None
    tcuten: float | None = None
    tcutmkn: float | None = None
    tcuttno: float | None = None
    ntcuttno: int | None = None
    tcuttnostep: float | None = None
    tcutpairsinter: float | None = None
    tcutpnointer: float | None = None
    tcutmkninter: float | None = None
    notriplesfragments: int | None = None
    fragtscaletcutpno_ss: float | None = None
    fragtscaletcutpno_sd: float | None = None
    fragtscaletcutpno_core: float | None = None
    fragtscaletcutpairs_somo: float | None = None
    fragtscaletcutpairs_core: float | None = None
    tcutdoaux: float | None = None
    tcutdo: float | None = None
    tcutpnosingles: float | None = None
    tcutdelocinter: float | None = None
    tcutprescr: float | None = None
    tcutosv: float | None = None
    tcutdoij: float | None = None
    tcutc: float | None = None
    tcutcmo: float | None = None
    tcutcpao: float | None = None
    tcutdopre: float | None = None
    tscalemp2pairs: float | None = None
    tcutpno_scale: float | None = None
    tscalemknstrong: float | None = None
    tscaledostrong: float | None = None
    tscalemknweak: float | None = None
    tscaledoweak: float | None = None
    pairpairtermstype: int | None = None
    tscaletcutpairs_somo: float | None = None
    tscaletcutpairs_core: float | None = None
    tscaletcutpnosingles: float | None = None
    tcompletenesspnoocc: float | None = None
    tcompletenesspnooccsingles: float | None = None
    doumpinnevpno: bool | None = None
    tcutgso: float | None = None
    tnat: float | None = None
    tfrac: float | None = None
    usescs: bool | None = None
    pt: float | None = None
    ps: float | None = None
    dopertnatorbs: int | None = None
    nroots: int | None = None
    nrootscisnat: int | None = None
    excitations: (
        Literal[
            "it",
            "ia",
            "ta",
            "ijtu",
            "ijta",
            "ijab",
            "ituv",
            "itua",
            "itau",
            "itab",
            "tuvw",
            "tuva",
            "tuab",
        ]
        | None
    ) = None
    trafotype: (
        Literal["trafo_ri", "trafo_jk", "trafo_jandk", "trafo_full", "trafo_ricosx"] | None
    ) = None
    printlevel: int | None = None
    tprint: float | None = None
    maxiter: int | None = None
    maxcore: int | None = None
    stol: float | None = None
    otol: float | None = None
    precondopt: int | None = None
    maxdiis: int | None = None
    diisstartiter: int | None = None
    levelshift: float | None = None
    pccsdab: float | None = None
    pccsdcd: float | None = None
    pccsdef: float | None = None
    tnoscales: float | None = None
    tnoscalew: float | None = None
    tcutweak: float | None = None
    tcutweakguess: float | None = None
    tcutiter: float | None = None
    tritole: float | None = None
    datatype: Literal["double", "float"] | None = None
    storagetype: Literal["shared"] | None = None
    compression: Literal["uncompressed", "compressed"] | None = None
    incore: Literal["nothing", "all"] | None = None
    iroot: int | None = None
    tddftguess: bool | None = None
    dodipolelength: bool | None = None
    dodipolevelocity: bool | None = None
    dohighermoments: bool | None = None
    dofullsemiclassical: bool | None = None
    decomposefosclength: bool | None = None
    decomposefoscvelocity: bool | None = None
    domcd: bool | None = None
    mcdgridtype: int | None = None
    lebedevintegrationpoints: int | None = None
    npointspsi: int | None = None
    npointsphi: int | None = None
    npointstheta: int | None = None
    ewin: NumList | None = None
    ipeashift: NumList | None = None
    cvsorb: NumList | None = None
    skiporb: NumList | None = None
    xeserange: NumList | None = None
    lmoinp: InputFilePath | None = None
    normalpnofraginter: IntGroup | None = None
    normalpnofragmentinteraction: IntGroup | None = None
    tightpnofraginter: IntGroup | None = None
    loosepnofraginter: IntGroup | None = None
    hffragmentinteraction: IntGroup | None = None
    mp2fraginter: IntGroup | None = None
    covalent: IntGroup | None = None

    @field_validator(
        "normalpnofraginter",
        "normalpnofragmentinteraction",
        "tightpnofraginter",
        "loosepnofraginter",
        "hffragmentinteraction",
        "mp2fraginter",
        "covalent",
        mode="before",
    )
    @classmethod
    def fraginteraction_init(cls, inp: list[int] | str | IntGroup) -> IntGroup:
        """
        Parameters
        ----------
        inp : list[int] | str | IntGroup
        """
        if isinstance(inp, IntGroup):
            return inp
        else:
            return IntGroup.init(inp)

    @field_validator("lmoinp", mode="before")
    @classmethod
    def filepath_init(cls, path: str | InputFilePath) -> InputFilePath:
        """
        Parameters
        ----------
        path : str | InputFilePath
        """
        if isinstance(path, str):
            return InputFilePath.from_string(path)
        else:
            return path
