from typing import Any, Literal, Self

from pydantic import BaseModel, field_validator

from opi.input.blocks import Block, InputFilePath, NumList

__all__ = ("DIIS", "Shift", "Damp", "SOSCF", "Trah", "Stab", "Rotate", "BlockScf")


class SubBlock(BaseModel):
    """
    Class to define a sub block within an input block
    """

    def __str__(self) -> str:
        s = " ".join(
            f"{key} {str(value)}" for key, value in self.__dict__.items() if value is not None
        )
        return s + " end"

    @classmethod
    def from_dict(cls, entries: dict[str, Any]) -> Self:
        """
        Parameters
        ----------
        entries : dict[str | Any]
        """
        filtered_data = {k: v for k, v in entries.items() if k in cls.model_fields.keys()}
        return cls.model_construct(**filtered_data)  # type:ignore


class DIIS(SubBlock):
    """
    Class to model `diis` attribute in `BlockScf`

    Attributes
    ----------
    start: float
    maxit: float
    maxeq: int
    bfac: float
    maxc: float
    """

    start: float | None = None
    maxit: int | None = None
    maxeq: int | None = None
    bfac: float | None = None
    maxc: float | None = None


class Shift(SubBlock):
    """
    Class to model `shift` attribute in `BlockScf`

    Attributes
    -----------
    shift: float
    erroff: float
    """

    shift: float | None = None
    erroff: float | None = None


class Damp(SubBlock):
    """
    Class to model `damp` attribute in `BlockScf`

    Attributes
    ----------
    fac: float
    erroff: float
    min: float
    max: float
    """

    fac: float | None = None
    erroff: float | None = None
    min: float | None = None
    max: float | None = None


class SOSCF(SubBlock):
    """
    Class to define `soscf` attribute in `BlockScf`

    Attributes
    ----------
    start: float
    maxit: float
    """

    start: float | None = None
    maxit: int | None = None


class Trah(SubBlock):
    """
    Class to model `trah` attribute in `BlockScf`

    Attributes
    ----------
    precond: {"diag", "full", "none"}
    preconmaxred: int
    """

    precond: Literal["diag", "full", "none"] | None = None
    preconmaxred: int | None = None


class Stab(SubBlock):
    """
    Class to model `stab` attribute in `BlockScf`

    Attributes
    ----------
    restartuhfifunstable: bool
    nroots: int
    maxdim: int
    maxiter: int
    nguess: int
    dtol: float
    rtol: float
    stablambda: float
    orbwin: NumList
    ewin: NumList
    """

    restartuhfifunstable: bool | None = None
    nroots: int | None = None
    maxdim: int | None = None
    maxiter: int | None = None
    nguess: int | None = None
    dtol: float | None = None
    rtol: float | None = None
    stablambda: float | None = None
    orbwin: NumList | None = None
    ewin: NumList | None = None

    @classmethod
    def from_dict(cls, entries: dict[str, Any]) -> "Stab":
        """
        Parameters
        ----------
        entries : dict[str | Any]
        """
        if "orbwin" in entries and entries["orbwin"] is not None:
            entries["orbwin"] = NumList(entries["orbwin"])
        if "ewin" in entries and entries["ewin"] is not None:
            entries["ewin"] = NumList(entries["ewin"])

            # Filter fields as before
        filtered_data = {k: v for k, v in entries.items() if k in cls.model_fields.keys()}
        return cls.model_construct(**filtered_data)

    @field_validator("orbwin", "ewin", mode="before")
    @classmethod
    def list_validator(cls, inp: list[int] | list[float]) -> NumList:
        """
        Parameters
        ----------
        inp : list[int] | list[float]
        """
        return NumList(inp)

    def __str__(self) -> str:
        s = " ".join(
            f"{str(key)} {str(value)}" for key, value in self.__dict__.items() if value is not None
        )
        s = s.replace("stablambda", "lambda")
        return s + " end"


class Rotate(BaseModel):
    """
    Class to model `rotate` attribute for `BlockScf`

    Attributes
    ------------
    rotate: list[int | float]
    """

    rotate: list[int | float]

    @field_validator("rotate")
    @classmethod
    def validate_rotate(cls, v: list[int | float]) -> list[int | float]:
        """
        Parameters
        ----------
        v : list[int | float]
        """
        # Check valid lengths (2, 3, or 5 elements)
        if len(v) not in (2, 3, 5):
            raise ValueError("Rotate must have either 2, 3, or 5 elements")

        # For all formats, first two elements must be integers
        if not isinstance(v[0], int):
            raise TypeError("First element must be an integer")
        if not isinstance(v[1], int):
            raise TypeError("Second element must be an integer")

        # If we have at least 3 elements, third must be of type float
        if len(v) >= 3 and not isinstance(v[2], float):
            raise TypeError("Third element must be a float")

        # If we have 5 elements, fourth and fifth must be integers
        if len(v) == 5:
            if not isinstance(v[3], int):
                raise TypeError("Fourth element must be an integer")
            if not isinstance(v[4], int):
                raise TypeError("Fifth element must be an integer")

        return v

    def __str__(self) -> str:
        return "{" + ", ".join(str(val) for val in self.rotate if val is not None) + "} end"


class BlockScf(Block):
    """Class to model %scf block in ORCA"""

    _name: str = "scf"
    maxiter: int | None = None
    scfmode: Literal["direct", "semidirect", "conventional"] | None = None
    directresetfreq: int | None = None
    keepints: bool | None = None
    readints: bool | None = None
    keepdensity: bool | None = None
    keepfock: bool | None = None
    fracocc: bool | None = None
    smeartemp: float | None = None
    smeartempmax: float | None = None
    smeartempmin: float | None = None
    doannealing: bool | None = None
    annealthresh: float | None = None
    reduceethresh: bool | None = None
    dryrun: bool | None = None
    calcguessen: bool | None = None
    keepall4intsinmem: bool | None = None
    autostart: bool | None = None
    convcheck: Literal["allchecks", "sloppycheck", "energycheck", "gradientcheck"] | None = None
    tole: float | None = None
    tolrmsp: float | None = None
    tolmaxp: float | None = None
    tolx: float | None = None
    tolg: float | None = None
    tolerr: float | None = None
    convergence: (
        Literal["sloppy", "loose", "medium", "strong", "tight", "verytight", "extreme"] | None
    ) = None
    sthresh: float | None = None
    diffsthresh: float | None = None
    eda: bool | None = None
    cnvdamp: bool | None = None
    cnvtrah: bool | None = None
    scflambda: float | None = None
    lambdamin: float | None = None
    lambdamax: float | None = None
    dampfac: float | None = None
    dampmin: float | None = None
    dampmax: float | None = None
    damperr: float | None = None
    cnvshift: bool | None = None
    lshift: float | None = None
    levelshift: float | None = None
    shifterr: float | None = None
    mingap: float | None = None
    minallowedgap: float | None = None
    cnvdiis: bool | None = None
    diisstart: float | None = None
    diismaxc: float | None = None
    diisbfac: float | None = None
    diismaxit: int | None = None
    diismaxeq: int | None = None
    cnvkdiis: bool | None = None
    kdiistransformation: Literal["kollmar", "cayley", "fullexp"] | None = None
    cnvsoscf: int | None = None
    soscfstart: float | None = None
    soscfmaxit: int | None = None
    soscfmaxstep: float | None = None
    soscfconvfactor: float | None = None
    robustsoscf: bool | None = None
    soscfconstrainedhessup: int | None = None
    deltascffromgs: bool | None = None
    soscfhessup: Literal["lbfgs", "lsr1", "lpowell", "lbofill"] | None = None
    soscfblockdiag: bool | None = None
    soscfconstraints: bool | None = None
    soscfwriteconstrainedgbw: bool | None = None
    soscfonlyconstrainedopt: bool | None = None
    autotrah: bool | None = None
    autotrahtol: float | None = None
    autotrahiter: int | None = None
    autotrahninter: int | None = None
    autotrahforcestartiter: int | None = None
    trahstart: float | None = None
    stabperform: bool | None = None
    stabrestartuhfifunstable: bool | None = None
    stabnroots: int | None = None
    stabmaxdim: int | None = None
    stabmaxiter: int | None = None
    stabmaxretries: int | None = None
    stabskip2ndstab: bool | None = None
    stabnguess: int | None = None
    stabdtol: float | None = None
    stabrtol: float | None = None
    stabotol: float | None = None
    stablambda: float | None = None
    thresh: float | None = None
    tcut: float | None = None
    tsize: float | None = None
    tcost: float | None = None
    fmopt: int | None = None
    apmethod: int | None = None
    guessmix: float | None = None
    finalms: float | None = None
    deltascf: bool | None = None
    domom: bool | None = None
    keepinitialref: bool | None = None
    pmom: bool | None = None
    averageocc: bool | None = None
    keeporbitals: bool | None = None
    doreortho: bool | None = None
    usegramschmidt: bool | None = None
    moinp: InputFilePath | None = None
    restartfile: InputFilePath | None = None
    cmatinp: InputFilePath | None = None
    ledorb: NumList | None = None
    staborbwin: NumList | None = None
    brokensym: NumList | None = None
    decompositionpath: NumList | None = None
    flipspin: NumList | None = None
    alphaconf: NumList | None = None
    betaconf: NumList | None = None
    setalpha: NumList | None = None
    setbeta: NumList | None = None
    removealpha: NumList | None = None
    removebeta: NumList | None = None
    ionizealpha: NumList | None = None
    ionizebeta: NumList | None = None
    efield: NumList | None = None
    qfield: NumList | None = None
    fgrad: NumList | None = None
    adip: NumList | None = None
    fermi: NumList | None = None
    aiso: NumList | None = None
    efieldorigin: (
        NumList | Literal["centerofmass", "centerofnuccharge", "centerofnuclearcharge"] | None
    ) = None
    diis: DIIS | None = None
    shift: Shift | None = None
    stab: Stab | None = None
    soscf: SOSCF | None = None
    damp: Damp | None = None
    trah: Trah | None = None
    rotate: Rotate | None = None
    ignoreconv: bool | None = None

    @field_validator(
        "staborbwin",
        "ledorb",
        "brokensym",
        "decompositionpath",
        "flipspin",
        "alphaconf",
        "betaconf",
        "setalpha",
        "setbeta",
        "removealpha",
        "removebeta",
        "ionizealpha",
        "ionizebeta",
        "efield",
        "qfield",
        "fgrad",
        "adip",
        "fermi",
        "aiso",
        "efieldorigin",
        mode="before",
    )
    def intlist_val(
        cls,
        input_list: list[int]
        | list[float]
        | NumList
        | Literal["centerofmass, centerofnuccharge, centerofnuclearcharge"],
    ) -> NumList | Literal["centerofmass, centerofnuccharge, centerofnuclearcharge"]:
        """
        Parameters
        ----------
        input_list : list[int] | list[float] | NumList | Literal["centerofmass, centerofnuccharge, centerofnuclearcharge"]
        """
        if isinstance(input_list, list):
            if any(isinstance(i, float) for i in input_list):
                input_list = [float(i) for i in input_list]
            return NumList(input_list)

        return input_list

    @field_validator("diis", mode="before")
    @classmethod
    def init_diis(cls, val: dict[str, Any] | DIIS) -> DIIS:
        """
        Parameters
        ----------
        val : dict[str | Any] | DIIS
        """
        if isinstance(val, dict):
            return DIIS.from_dict(val)
        else:
            return val

    @field_validator("shift", mode="before")
    @classmethod
    def init_shift(cls, val: dict[str, Any] | Shift) -> Shift:
        """
        Parameters
        ----------
        val : dict[str | Any] | Shift
        """
        if isinstance(val, dict):
            return Shift.from_dict(val)
        else:
            return val

    @field_validator("stab", mode="before")
    @classmethod
    def init_stab(cls, val: dict[str, Any] | Stab) -> Stab:
        """
        Parameters
        ----------
        val : dict[str | Any] | Stab
        """
        if isinstance(val, dict):
            return Stab.from_dict(val)
        else:
            return val

    @field_validator("soscf", mode="before")
    @classmethod
    def init_soscf(cls, val: dict[str, Any] | SOSCF) -> SOSCF:
        """
        Parameters
        ----------
        val : dict[str |Any] | SOSCF
        """
        if isinstance(val, dict):
            return SOSCF.from_dict(val)
        else:
            return val

    @field_validator("trah", mode="before")
    @classmethod
    def init_trah(cls, val: dict[str, Any] | Trah) -> Trah:
        """
        Parameters
        ----------
        val : dict[str | Any] | Trah
        """
        if isinstance(val, dict):
            return Trah.from_dict(val)
        else:
            return val

    @field_validator("rotate", mode="before")
    @classmethod
    def init_rotate(cls, val: list[int | float] | Rotate) -> Rotate:
        """
        Parameters
        ----------
        val : list[int | float] | Rotate
        """
        if isinstance(val, list):
            return Rotate(rotate=val)
        else:
            return val

    @field_validator("moinp", "restartfile", "cmatinp", mode="before")
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

    def format_orca(self) -> str:
        s = f"%{self.name}\n"
        for key, value in self.__dict__.items():
            if value is not None:
                if key == "aftercoord":
                    continue
                if key == "scflambda":
                    s += f"    lambda {str(value).lower()}\n"
                else:
                    s += f"    {key} {str(value).lower()}\n"
        s += "end"

        return s
