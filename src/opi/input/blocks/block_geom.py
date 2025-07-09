import re
from typing import Annotated, Literal

from pydantic import (
    Field,
    conlist,
    field_validator,
    model_validator,
)

from opi.input.blocks import (
    Block,
    InputFilePath,
    NumList,
)
from opi.input.blocks.fragment import FragList, Fragment, Frags
from opi.input.blocks.geom_wrapper import GeomWrapper, GeomWrapperBox
from opi.utils.element import Element
from opi.utils.misc import FLOAT_REGEX

__all__ = (
    "BlockGeom",
    "ConnectFragments",
    "Constraint",
    "Constraints",
    "FragConstraint",
    "Hybrid",
    "Modify",
    "ModifyInternal",
    "Potential",
    "Scan",
    "TSMode",
)


class Hybrid(GeomWrapper):
    """
    Class to model `hybrid` attribute in `BlockGeom`

    Attributes
    ----------
    list: `NumList`
    """

    list: NumList


class Potential(GeomWrapper):
    """
    Class to model `potential` attribute in `BlockGeom`

    Attributes
    ----------
    mode: "C"

    atom1: int
        Specify first atom
    atom2: int
        Specify second atom
    value: float
        Define value
    """

    mode: Literal["C"] = "C"
    atom1: Annotated[int, Field(ge=0)]
    atom2: Annotated[int, Field(ge=0)]
    value: float


class Constraint(GeomWrapper):
    """
    Class to model a singular constraint for the `constraints` attribute in `BlockGeom`

    Attributes
    ----------
    mode: {"A","B","C","D"}
        Define mode of constraint
    atom1: int | "*"
        Specify the first atom ( can also be *)
    atom2: int | "*"
        Specify the second atom ( can also be *)
    atom3: int | "*"
        Specify the third atom ( can also be *)
    atom4: int | "*"
        Specify the fourth atom ( can also be *)
    value: float
        Specify value of the constraint
    """

    mode: Literal["A", "B", "C", "D"]
    atom1: Annotated[int, Field(ge=0)] | Literal["*"]
    atom2: Annotated[int, Field(ge=0)] | Literal["*"] | None = None
    atom3: Annotated[int, Field(ge=0)] | Literal["*"] | None = None
    atom4: Annotated[int, Field(ge=0)] | Literal["*"] | None = None
    value: float | None = None

    @model_validator(mode="after")
    def validate_attributes(self) -> "Constraint":
        super().validate_mode(self)
        # Mode C should only have atom1, all others must be None
        if self.mode == "C":
            if any(x is not None for x in [self.atom2, self.atom3, self.atom4, self.value]):
                raise ValueError("Wrong format for mode C")

        return self

    @classmethod
    def from_string(cls, string: str) -> "Constraint":
        """
        Parameters
        ----------
        string : str
        """
        re_constraint = re.compile(
            rf"""
                ({{)?\s*                           # Optional opening brace with optional whitespace
                (?P<mode>[ABCD])\s+                # Mode: A, B, or D (case insensitive)
                (?P<atom1>\d+|\*)\s+               # atom1: digit or *
                (?P<atom2>\d+|\*)\s*               # atom2: digit or *    
                ((?P<atom3>\d+|\*)\s+)?          # Optional atom3
                ((?P<atom4>\d+|\*)\s+)?          # Optional atom4
                (?P<value>{FLOAT_REGEX})?         # Optional float value (must include decimal)
                \s*[C]\s*                          # Ending C or c
                (}})?                               # Optional closing brace
                """,
            re.VERBOSE,
        )
        match = re_constraint.match(string.upper().strip())
        if not match:
            raise ValueError("String not valid")

        groups = match.groupdict()
        return cls(**groups)

    def __str__(self) -> str:
        return (
            f"{{ {' '.join(str(val) for key, val in self.__dict__.items() if val is not None)} C }}"
        )


class Constraints(GeomWrapperBox):
    """
    Class to model the `constraints` attribute in `BlockGeom`

    Attributes
    -----------
    constraints: list[`Constraint`]
        list of constraints of type `Constraint`
    """

    constraints: conlist(Constraint)  # type:ignore

    def __str__(self) -> str:
        s = "\n     " + "\n     ".join(str(c) for c in self.constraints) + "\n    end"

        return s


class Scan(GeomWrapper):
    """
    Class to model the `scan` attribute in `BlockGeom`

    Attributes
    ----------
    mode: {"A","B","D"}
        Defines mode for modification
    atom1: int
        Specify first atom
    atom2: int
        Specify second atom
    atom3: int
        Specify optional third atom
    atom4: int
        Specify optional fourth atom
    startvalue: float
        Define start value
    endvalue: float
        Define end value
    steps: int
        Define number of steps
    valuelist: list[float]
        Define the values

    """

    mode: Literal["A", "B", "D"]
    atom1: Annotated[int, Field(ge=0)]
    atom2: Annotated[int, Field(ge=0)]
    atom3: Annotated[int, Field(ge=0)] | None = None
    atom4: Annotated[int, Field(ge=0)] | None = None
    startvalue: float | None = None
    endvalue: float | None = None
    steps: Annotated[int, Field(ge=0)] | None = None
    valuelist: conlist(float) | None = None  # type:ignore

    @model_validator(mode="after")
    def validate_attributes(self) -> "Scan":
        super().validate_mode(self)

        if (
            not all(x is not None for x in [self.startvalue, self.endvalue, self.steps])
            and not self.valuelist
        ):
            raise ValueError("Data missing")

        return self

    @classmethod
    def from_string(cls, string: str) -> "Scan":
        """
        Parameters
        ----------
        string : str
        """
        re_scan = re.compile(
            rf"""
           (?P<mode>[ABD])                                                        # Mode
           \s+(?P<atom1>\d+)                                                      # atom1
           \s+(?P<atom2>\d+)                                                      # atom2
           (\s+(?P<atom3>\d+))?                                                   # optional atom3
           (\s+(?P<atom4>\d+))?                                                   # optional atom4
           ((                                                                     # optional block
              \s*=\s*(?P<startvalue>{FLOAT_REGEX})\s*,                           # startvalue (must be float)
              \s*(?P<endvalue>{FLOAT_REGEX})\s*,                                 # endvalue (must be float)
              \s*(?P<steps>\d+)                                                   # steps
           )|                   
           \s*(?P<valuelist>\[\s*({FLOAT_REGEX})(\s+{FLOAT_REGEX})*]))         # optional valuelist
           """,
            re.VERBOSE,
        )
        match = re_scan.match(string.upper().strip())
        if not match:
            raise ValueError("String not valid")

        groups = match.groupdict()
        return cls(**groups)

    def __str__(self) -> str:
        if all(x is not None for x in [self.startvalue, self.endvalue, self.steps]):
            return (
                f"{' '.join(str(getattr(self, field)) for field in ['mode', 'atom1', 'atom2', 'atom3', 'atom4'] if getattr(self, field) is not None)} "
                + f"= {self.startvalue}, {self.endvalue}, {self.steps} end"
            )
        else:
            return f"{' '.join(str(val) for key, val in self.__dict__.items() if val is not None)}"


class TSMode(GeomWrapper):
    """
    Class to model the `tsmode` attribute in `BlockGeom`.

    Attributes
    ----------
    mode: {"A","B","D","M"}
        Defines mode for modification
    x: int
        choose mode to follow uphill in TS optimization
    atom1: int
        Specify first atom
    atom2: int
        Specify second atom
    atom3: int
        Specify third atom
    atom4: int
        Specify fourth atom
    """

    mode: Literal["A", "B", "D", "M"] = "M"
    x: Annotated[int, Field(ge=0)] | None = None  # choose mode to follow uphill in TS optimization
    atom1: Annotated[int, Field(ge=0)] | None = None
    atom2: Annotated[int, Field(ge=0)] | None = None
    atom3: Annotated[int, Field(ge=0)] | None = None
    atom4: Annotated[int, Field(ge=0)] | None = None

    @model_validator(mode="after")
    def validate_attributes(self) -> "TSMode":
        super().validate_mode(self)

        if self.mode == "M":
            if not self.x:
                raise ValueError("Wrong format for mode M")

        return self

    def __str__(self) -> str:
        if self.mode == "M":
            return f"{{ {self.mode} {self.x} }}"
        else:
            atoms = [str(self.atom1), str(self.atom2)]
            if self.atom3 is not None:
                atoms.append(str(self.atom3))
            if self.atom4 is not None:
                atoms.append(str(self.atom4))

            return f"{{ {self.mode} {' '.join(atoms)} }} end"

    @classmethod
    def from_string(cls, string: str) -> "TSMode":
        """
        Creates an object of `TSMode` from a string

        Parameters
        ----------
        string : str
        """
        re_tsmode1 = re.compile(
            r"""
                \{?\s*                               # Optional opening brace with optional whitespace
                (?P<mode>[ABD])\s+                   # Mode: A, B, or D (case insensitive)
                (?P<atom1>\d+)\s+                    # atom1: digit 
                (?P<atom2>\d+)\s+                    # atom2: digit     
                (\s+(?P<atom3>\d+))?                 # Optional atom3
                (\s+(?P<atom4>\d+))?                 # Optional atom4
                }?                                  # Optional closing brace
                """,
            re.VERBOSE,
        )
        re_tsmode2 = re.compile(
            r"""
                \{?\s*                             # Optional opening brace with optional whitespace
                (?P<mode>[Mm])\s+                  # Mode: M (case insensitive)
                (?P<x>\d+)?\s+                     # x: digit
                }?                                 # Optional closing brace
                """,
            re.VERBOSE,
        )
        match = re_tsmode1.match(string.upper().strip())
        if not match:
            match = re_tsmode2.match(string)
            if not match:
                raise ValueError("String not valid")

        groups = match.groupdict()
        return cls(**groups)


class Modify(GeomWrapper):
    """
    Class to model individual modifications for `ModifyInternal` class.

    Attributes
    ----------
    mode: {"A","B","D"}
        Defines mode for modification
    atom1: int
        Specify first atom
    atom2: int
        Specify second atom
    atom3: int
        Specify third atom
    atom4: int
        Specify fourth atom

    """

    mode: Literal["A", "B", "D"]
    atom1: Annotated[int, Field(ge=0)]
    atom2: Annotated[int, Field(ge=0)]
    atom3: Annotated[int, Field(ge=0)] | None = None
    atom4: Annotated[int, Field(ge=0)] | None = None
    action: Literal["A", "R"]

    @model_validator(mode="after")
    def validate_attributes(self) -> "Modify":
        super().validate_mode(self)

        return self

    @classmethod
    def from_string(cls, string: str) -> "Modify":
        """
        Parameters
        ----------
        string : str
        """
        re_modify = re.compile(
            r"""
                \{?\s*                             # Optional opening brace with optional whitespace
                (?P<mode>[ABD])\s+              # Mode: A, B, or D (case insensitive)
                (?P<atom1>\d+)\s+                  # atom1: digit 
                (?P<atom2>\d+)\s*                  # atom2: digit     
                (?P<atom3>\d+)?\s*                 # Optional atom3
                (?P<atom4>\d+)?\s*                 # Optional atom4
                (?P<action>[AR])                 # Action 
                }?                                 # Optional closing brace
                """,
            re.VERBOSE,
        )

        match = re_modify.match(string.upper().strip())

        if not match:
            raise ValueError("String not valid")

        groups = match.groupdict()
        return cls(**groups)

    def __str__(self) -> str:
        return (
            f"{{ {' '.join(str(val) for key, val in self.__dict__.items() if val is not None)} }}"
        )


class ModifyInternal(GeomWrapperBox):
    """
    Class used to model the `modify_internal` attribute in `BlockGeom`

    Attributes
    ----------
    modifications: list[`Modify`]
        List of modifications of type `Modify`
    """

    modifications: conlist(Modify)  # type:ignore

    def __str__(self) -> str:
        s = "\n     " + "\n     ".join(str(c) for c in self.modifications) + "\n    end"

        return s


class FragConstraint(GeomWrapper):
    """
    Class to model individual constraints for the `ConnectFragment` class

    Attributes
    ----------
    fragment1: int
        Define first fragment
    fragment2: int
        Define second fragment
    action: {"C", "O"}
        Define action
    atom1: int
        Specify first atom
    atom2: int
        Specify second atrom
    """

    fragment1: Annotated[int, Field(gt=0)]
    fragment2: Annotated[int, Field(gt=0)]
    action: Literal["C", "O"]
    atom1: Annotated[int, Field(ge=0)] | None = None
    atom2: Annotated[int, Field(ge=0)] | None = None

    def __str__(self) -> str:
        return (
            f"{{ {' '.join(str(val) for key, val in self.__dict__.items() if val is not None)} }}"
        )

    @classmethod
    def from_string(cls, string: str) -> "FragConstraint":
        """
        Parameters
        ----------
        string : str
        """
        re_modify = re.compile(
            r"""
                \{?\s*                             # Optional opening brace with optional whitespace
                (?P<fragment1>\d+)\s+              # Fragment1: int
                (?P<fragment2>\d+)\s+              # Fragment2: int 
                (?P<action>[CO])\s*              # action: "c" or "o"   
                (?P<atom1>\d+)?\s*                 # atom1: int
                (?P<atom2>\d+)?\s*                 # atom2: int
                }?                                 # Optional closing brace
                """,
            re.VERBOSE,
        )

        match = re_modify.match(string.upper().strip())

        if not match:
            raise ValueError("String not valid")

        groups = match.groupdict()
        return cls(**groups)


class ConnectFragments(GeomWrapperBox):
    """
    Class used to model the `connectfragments` attribute in `BlockGeom`

    Attributes
    ----------
    constraints: list[FragConstraint]
        list of constraints of type `FragConstraint`
    """

    constraints: conlist(FragConstraint)  # type:ignore

    def __str__(self) -> str:
        s = "\n     " + "\n     ".join(str(c) for c in self.constraints) + "\n    end"

        return s


class BlockGeom(Block):
    """Class to model %geom block in ORCA"""

    _name: str = "geom"
    maxiter: int | None = None
    projecttr: bool | None = None
    maxstep: float | None = None
    trust: float | None = None
    bmatderiv: bool | None = None
    updatefromcart: bool | None = None
    cartfallback: bool | None = None
    maxnsteptrial: int | None = None
    largeinternals: bool | None = None
    interpolate: bool | None = None
    shake: int | None = None
    shakermsd: float | None = None
    coordsys: Literal["cartesian", "redundant"] | None = None
    update: (
        Literal[
            "noupdate",
            "bfgs",
            "dfp",
            "bofill",
            "powell",
            "sr1",
            "fs",
            "flowpsb",
            "lbfgs",
            "l-bfgs",
        ]
        | None
    ) = None
    nstepsinresethess: int | None = None
    nresethess: int | None = None
    resethessmethod: int | None = None
    maxrmsdresethess: float | None = None
    printinternals: bool | None = None
    step: Literal["qn", "rfo", "gmf", "prfo"] | None = None
    inhess: (
        Literal[
            "unit",
            "lindh",
            "model",
            "almloef",
            "schlegel",
            "swart",
            "read",
            "xtb0",
            "xtb1",
            "xtb2",
            "gfnff",
            "gfn-ff",
        ]
        | None
    ) = None
    tole: float | None = None
    tolrmsg: float | None = None
    tolmaxg: float | None = None
    tolrmsd: float | None = None
    tolmaxd: float | None = None
    tolesc: float | None = None
    enforcestrictconvergence: bool | None = None
    usesoscf: bool | None = None
    reduceprint: bool | None = None
    optguess: Literal["patom", "pmodel", "hueckel", "oneelec", "moread"] | None = None
    convergence: Literal["loose", "normal", "tight"] | None = None
    fullscan: bool | None = None
    refinetsguess: bool | None = None
    simul_scan: bool | None = None
    optimizehydrogens: bool | None = None
    freezehydrogens: bool | None = None
    invertconstraints: bool | None = None
    ts_search: Literal["ef"] | None = None
    numhess: bool | None = None
    numhess_centraldiff: bool | None = None
    calc_hess: bool | None = None
    recalc_hess: int | None = None
    read_temp_hess: bool | None = None
    reconvcharge: int | None = None
    ts_active_atoms_factor: float | None = None
    hess_modification: Literal["shift_diag", "ev_reverse"] | None = None
    hess_minev: float | None = None
    scalepcdamp: float | None = None
    scalepccenter: float | None = None
    doscaleembeddingcharges: bool | None = None
    scaleembeddingpc: int | None = None
    scaleembeddingpc_a: float | None = None
    scaleembeddingpc_b: float | None = None
    addextrabonds: bool | None = None
    addextrabonds_maxlength: int | None = None
    addextrabonds_maxdist: float | None = None
    reduceredints: bool | None = None
    printinternalhess: bool | None = None
    printtsactiveatoms: bool | None = None
    thr_printtsactiveatoms: float | None = None
    hess2projectint: bool | None = None
    hess2projectintbonds: bool | None = None
    hess2projectintangles: bool | None = None
    hess2projectintdihedrals: bool | None = None
    hess2projectintimpropers: bool | None = None
    usespherepot: bool | None = None
    useboxpot: bool | None = None
    useellipsepot: bool | None = None
    boxpot: float | None = None
    spherepot: float | None = None
    ellipsepot: float | None = None
    wallexponent: float | None = None
    followmode: int | None = None
    fmkeepref: bool | None = None
    fmminoverlap: float | None = None
    rigidbody: bool | None = None
    check_topo: bool | None = None
    inhessname: InputFilePath | None = None
    inhessname2: InputFilePath | None = None
    optelement: Element | None = None
    hybridhess: Hybrid | None = None
    hybridhess_core: Hybrid | None = None
    ts_active_atoms: Hybrid | None = None
    ts_active_atoms2: Hybrid | None = None
    constraints: Constraints | None = None
    potentials: Potential | None = None
    scan: Scan | None = None
    ts_mode: TSMode | None = None
    modify_internal: ModifyInternal | None = None
    connectfragments: ConnectFragments | None = None
    constrainfragments: FragList | None = None
    rigidfrags: FragList | None = None
    relaxfrags: FragList | None = None
    relaxhfrags: FragList | None = None
    ghostfrags: FragList | None = None
    frags: Frags | None = None

    @field_validator("constraints", mode="before")
    @classmethod
    def constraint_str(cls, strings: list[str] | str) -> Constraints:
        """
        Creates Constraints object by parsing a given string or list of strings

        Parameters
        ----------
        strings : list[str] | str
        """
        try:
            if isinstance(strings, list):
                constraints = [Constraint.from_string(s) for s in strings]
            else:
                constraints = [Constraint.from_string(strings)]
        except Exception as e:
            raise ValueError(f"Failed to parse constraints: {e}")

        return Constraints(constraints=constraints)

    @field_validator("scan", mode="before")
    @classmethod
    def scan_str(cls, string: str) -> Scan:
        """
        Creates Scan object by parsing given string

        Parameters
        ----------
        string : str
        """
        return Scan.from_string(string)

    @field_validator("ts_mode", mode="before")
    @classmethod
    def tsmode_str(cls, string: str) -> TSMode:
        """
        Creates TSMode object by parsing given string

        Parameters
        ----------
        string : str
        """
        return TSMode.from_string(string)

    @field_validator("modify_internal", mode="before")
    @classmethod
    def modify_str(cls, strings: list[str] | str) -> ModifyInternal:
        """
        Creates ModifyInternal object by parsing given string or list of strings

        Parameters
        ----------
        strings : list[str] | str
        """
        try:
            if isinstance(strings, list):
                modifications = [Modify.from_string(s) for s in strings]
            else:
                modifications = [Modify.from_string(strings)]
        except Exception as e:
            raise ValueError(f"Failed to parse modifications: {e}")

        return ModifyInternal(modifications=modifications)

    @field_validator("connectfragments", mode="before")
    @classmethod
    def fragment_str(cls, strings: list[str] | str) -> ConnectFragments:
        """
        Creates ConnectFragments object by parsing given string or list of strings

        Parameters
        ----------
        strings : list[str] | str
        """
        try:
            if isinstance(strings, list):
                fragconstraints = [FragConstraint.from_string(s) for s in strings]
            else:
                fragconstraints = [FragConstraint.from_string(strings)]
        except Exception as e:
            raise ValueError(f"Failed to parse constraints: {e}")

        return ConnectFragments(constraints=fragconstraints)

    @field_validator(
        "rigidfrags",
        "relaxfrags",
        "relaxhfrags",
        "ghostfrags",
        "constrainfragments",
        mode="before",
    )
    @classmethod
    def frags_from_list(cls, frags: list[int]) -> FragList:
        """
        Initializes FragList object given a list of integers

        Parameters
        ----------
        frags : list[int]
        """
        return FragList.init(frags)

    @field_validator("frags", mode="before")
    @classmethod
    def frags_str(cls, strings: list[str] | str) -> Frags:
        """
        Parameters
        ----------
        strings : list[str] | str
        """
        try:
            if isinstance(strings, list):
                frags = [Fragment.from_string(s) for s in strings]
            else:
                frags = [Fragment.from_string(strings)]
        except Exception as e:
            raise ValueError(f"Failed to parse constraints: {e}")

        return Frags(frags=frags)

    @field_validator("inhessname", "inhessname2", mode="before")
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
