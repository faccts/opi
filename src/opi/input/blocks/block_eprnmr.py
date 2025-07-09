import re
from typing import Annotated, Literal

from pydantic import BaseModel, Field, field_validator

from opi.input.blocks import Block, InputFilePath, IntGroup, NumList
from opi.utils.element import Element

__all__ = ("NucleiFlag", "Nuclei", "NmrGroup", "NmrEquiv", "BlockEprnmr")


class NucleiFlag(BaseModel):
    """
    This class contains all flags for the `nuclei` parameter in `BlockEprnmr`.
    """

    ppp: float | None = None
    qqq: float | None = None
    iii: float | None = None
    ist: int | None = None
    ssgn: float | None = None
    aiso: bool = False
    adip: bool = False
    aorb: bool = False
    fgrad: bool = False
    rho: bool = False
    shift: bool = False
    ssdso: bool = False
    sspso: bool = False
    ssfc: bool = False
    sssd: bool = False
    ssall: bool = False

    def __str__(self) -> str:
        flags = []
        for key, value in self.__dict__.items():
            if value is not None:
                if isinstance(value, bool):
                    if value:
                        flags.append(key.lower())
                else:
                    flags.append(f"{key} = {str(value)}")

        return f"{', '.join(flags)}"

    @classmethod
    def from_string(cls, inp: str) -> "NucleiFlag":
        """
        Parameters
        ----------
        inp : str


        Returns
        -------
        NucleiFlag
        """
        instance = cls()
        strings = inp.split(",")
        for s in strings:
            s = s.strip()
            try:
                # flag = FlagEnum(inp)
                # return cls(flag=flag)
                # instance = cls()
                setattr(instance, s, True)
            except ValueError:
                try:
                    key, value = s.split("=")
                    key = key.strip()
                    value = value.strip()
                    typedvalue: int | float
                    if key == "ist":
                        typedvalue = int(value)
                    else:
                        typedvalue = float(value)

                    setattr(instance, key, typedvalue)
                except ValueError:
                    raise ValueError("Invalid string")

        return instance


class Nuclei(BaseModel):
    """
    Class to model `nuclei` attribute in `BlockEprnmr`

    Attributes
    ----------
    mode: "all" | NumList
        Defines for which atoms properties are calculated
    atom: Element
        Defines for atoms of which type properties are calculated
    flags: `NucleiFlag`
        Defines flags
    """

    mode: Literal["all"] | NumList = "all"
    atom: Element
    flags: NucleiFlag

    def __str__(self) -> str:
        flagstring = "{ " + str(self.flags) + " }"
        return f"= {str(self.mode)} {self.atom} {flagstring}"

    @classmethod
    def from_string(cls, string: str) -> "Nuclei":
        """
        Parameters
        ----------
        string : str
        """
        re_nuclei = re.compile(
            r"""
                (?P<mode> all|\d+(?:,\d+)*)\s+              # Mode: A, B, or D (case insensitive)
                (?P<atom>[\s\S]+?)\s+                       # atom: Member of Element enum
                \{?\s*                                      # Optional opening brace
                (?P<flags>[^}]+)                            # one or more flags, separated by comma  
                }?                                          # Optional closing brace
                """,
            re.VERBOSE,
        )
        res = re_nuclei.match(string.lower())
        if not res:
            raise ValueError("String not valid")

        groups = res.groupdict()
        return cls(**groups)

    @field_validator("atom", mode="before")
    @classmethod
    def get_element(cls, inp: str | Element) -> Element:
        """
        Parameters
        ----------
        inp : str | Element
        """
        if isinstance(inp, str):
            element = Element(inp.capitalize())
            if element is not None:
                return element
            else:
                raise ValueError("Invalid element")
        else:
            return inp

    @field_validator("flags", mode="before")
    @classmethod
    def init_flags(cls, inp: str | NucleiFlag) -> NucleiFlag:
        """
        Parameters
        ----------
        inp : str | list[NucleiFlag]

        Returns
        -------
        NucleiFlag
        """
        if isinstance(inp, str):
            return NucleiFlag.from_string(inp.strip())
        else:
            return inp

    @field_validator("mode", mode="before")
    @classmethod
    def init_mode(cls, inp: str | NumList | list[int] | list[float]) -> str | NumList:
        """
        Parameters
        ----------
        inp : str | NumList | list[int] | list[float]
        """
        if isinstance(inp, str):
            if inp == "all":
                return inp
            else:
                return NumList.from_string(inp)
        elif isinstance(inp, list):
            return NumList(inp)
        else:
            return inp


class NmrGroup(BaseModel):
    """
    Class to model a singular group of equivalent nuclei for the `nmrspecequiv` attribute in `BlockEprnmr`.

    Attributes
    ----------
    groupnumber: int
        Defines group number
    atoms: `IntGroup`
        Defines atoms that are grouped

    """

    groupnumber: Annotated[int, Field(gt=0)]
    atoms: IntGroup

    def __str__(self) -> str:
        return f"{self.groupnumber} {str(self.atoms)} end"

    @field_validator("atoms", mode="before")
    @classmethod
    def intgroup_init(cls, inp: str | list[int]) -> IntGroup:
        """
        Parameters
        ----------
        inp : str | list[int]
        """
        return IntGroup.init(inp)

    @classmethod
    def from_string(cls, inp: str) -> "NmrGroup":
        """
        Parameters
        ----------
        inp : str
        """
        re_group = re.compile(
            r"""
                        (?P<groupnumber>\d+)\s+              # Mode: A, B, or D (case insensitive)
                        \{\s*                                # Optional opening brace with optional whitespace
                        (?P<atoms>(\d+(?:\s\d+)*))           # atoms: space separated integers 
                        }\s*                                 # Optional closing brace
                        (end)?                               # Optional end
                        """,
            re.VERBOSE,
        )

        match = re_group.match(inp.upper().strip())

        if not match:
            raise ValueError("String not valid")

        groups = match.groupdict()
        return cls(**groups)


class NmrEquiv(BaseModel):
    """
    Class to model `nmrequiv` attribute in `BlockEprnmr`

    Attributes
    ----------
    groups: list[`NmrGroup`]
        List of groups of type NmrGroup that defines all groups of equivalent nuclei.

    """

    groups: list[NmrGroup]

    def __str__(self) -> str:
        s = "\n"
        for group in self.groups:
            s += f"      {str(group)}\n"
        s += "    end"
        return s

    @classmethod
    def from_string(cls, inp: str) -> "NmrEquiv":
        """
        Parameters
        ----------
        inp : str
        """
        parts = inp.split(",")
        groups = [NmrGroup.from_string(part) for part in parts]
        return NmrEquiv(groups=groups)


class BlockEprnmr(Block):
    """Class to model %eprnmr block in ORCA"""

    _name: str = "eprnmr"
    aftercoord: bool = True
    gtensor: int | None = None
    gtensor_dso_zeff: bool | None = None
    gtensor_1el2el: int | None = None
    hfcgaugecorrection_zeff: bool | None = None
    hfcgaugecorrection_angulargrid: int | None = None
    hfcgaugecorrection_prunegrid: int | None = None
    hfcgaugecorrection_intacc: float | None = None
    hfcgaugecorrection_bfcutoff: float | None = None
    hfcgaugecorrection_wcutoff: float | None = None
    hfcgaugecorrection_numeric: bool | None = None
    nmrshielding: int | None = None
    dtensor: Literal["ss", "so", "soc", "ssandso"] | None = None
    dsoc: Literal["qro", "pk", "cp", "pcp", "cvw"] | None = None
    dss: Literal["direct", "uno"] | None = None
    printlevel: int | None = None
    solver: Literal["cg", "diis", "pople"] | None = None
    tol: float | None = None
    maxiter: int | None = None
    maxdiis: int | None = None
    levelshift: float | None = None
    giao_1el: Literal["giao_1el_numeric", "giao_1el_analytic"] | None = None
    giao_2el: (
        Literal[
            "giao_2el_same_as_scf",
            "giao_2el_analytic",
            "giao_2el_rijk",
            "giao_2el_rijcosx",
            "giao_2el_rijonx",
            "giao_2el_cosjx",
            "giao_2el_cosjonx",
            "giao_2el_exactjcosx",
            "giao_2el_exactjrik",
        ]
        | None
    ) = None
    spinspinrthresh: float | None = None
    printreducedcoupling: bool | None = None
    printeuler: bool | None = None
    nmrspectrum: bool | None = None
    nmrref: float | None = None
    nmrspecfreq: float | None = None
    nmrcoal: float | None = None
    tau: Literal["ms", "gi", "dobson"] | None = None
    dospinadmixture: bool | None = None
    nuclei: Nuclei | None = None
    ewin: NumList | None = None
    zeff: NumList | None = None
    origin: (
        NumList
        | Literal[
            "centerofmass",
            "centerofnuccharge",
            "centerofnuclearcharge",
            "centerofelcharge",
            "centerofspindens",
            "centerofspindensity",
            "giao",
        ]
        | None
    ) = None
    locorbgbw: InputFilePath | None = None
    nmrshieldingfile: InputFilePath | None = None
    nmrcouplingfile: InputFilePath | None = None
    nmrspecequiv: NmrEquiv | None = None

    @field_validator("nuclei", mode="before")
    @classmethod
    def nuclei_fromstring(cls, inp: Nuclei | str) -> Nuclei:
        """
        Parameters
        ----------
        inp : Nuclei | str
        """
        if isinstance(inp, str):
            return Nuclei.from_string(inp)
        else:
            return inp

    @field_validator("origin", "ewin", "zeff", mode="before")
    @classmethod
    def numlist_from_list(cls, inp: NumList | str | list[int] | list[float]) -> NumList | str:
        """
        Parameters
        ----------
        inp : NumList | str | list[int] | list[float]
        """
        if isinstance(inp, list):
            return NumList(inp)
        else:
            return inp

    @field_validator("locorbgbw", "nmrshieldingfile", "nmrcouplingfile", mode="before")
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

    @field_validator("nmrspecequiv", mode="before")
    @classmethod
    def nmrequiv_fromstring(cls, inp: str | NmrEquiv) -> NmrEquiv:
        """
        Parameters
        ----------
        inp : str | NmrEquiv
        """
        if isinstance(inp, str):
            return NmrEquiv.from_string(inp)
        else:
            return inp
