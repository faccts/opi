from typing import Literal

from pydantic import BaseModel, field_validator
from pydantic_core.core_schema import ValidationInfo

from opi.input.blocks import Block
from opi.input.blocks.util import InputFilePath

__all__ = ("BlockMethod",)


class ExternalParam(BaseModel):
    """
    Class to model `extparamx', `extparamx` and `extparamxc` attributes in `BlockMethod`.

    Attributes
    -----------
    field_name: str
        Field name.

    parameters: dict[str, float]
        Dictionary of parameter values.

    """

    field_name: str | None = None
    parameters: dict[str, float]

    @classmethod
    def from_string(cls, field_name: str | None, strings: str | list[str]) -> "ExternalParam":
        """Create a `ExternalParam` instance from a string or list of strings such as:
        '_bt 0.00444' or ['_bt 0.00444', '_alpha 19.823391']"""
        params = {}
        if isinstance(strings, str):
            strings = [strings]
        for string in strings:
            # split string into parameter name and value
            paramname, value = string.rsplit(" ", maxsplit=1)
            params[paramname.strip()] = float(value.strip())

        return ExternalParam(field_name=field_name, parameters=params)

    def __str__(self) -> str:
        lines = []

        for i, (key, value) in enumerate(self.parameters.items()):
            if i == 0:
                # when formatting block input for orca, the first line will already include field name
                lines.append(f'"{key}" {value}')
            else:
                # lines after first line need to add the field name
                lines.append(f'    {self.field_name} "{key}" {value}')

        return "\n".join(lines)


class BlockMethod(Block):
    """Class to model %method block in ORCA"""

    _name: str = "Method"

    method: Literal["dft"] | None = None
    exchange: (
        Literal[
            "x_nox",
            "x_slater",
            "x_becke",
            "x_wb88",
            "x_g96",
            "x_pw91",
            "x_mpw",
            "x_pbe",
            "x_rpbe",
            "x_optx",
            "x_x",
            "x_tpss",
            "x_b97d",
            "x_b97becke",
            "x_scan",
            "x_rscan",
            "x_r2scan",
            "gga_x_mpw91",
        ]
        | None
    ) = None
    correlation: (
        Literal[
            "c_noc",
            "c_vwn5",
            "c_vwn3",
            "c_pwlda",
            "c_p86",
            "c_pw91",
            "c_pbe",
            "c_lyp",
            "c_tpss",
            "c_b97d",
            "c_b97becke",
            "c_scan",
            "c_rscan",
            "c_r2scan",
            "mgga_c_bc95",
        ]
        | None
    ) = None
    ldaopt: Literal["c_noc", "c_pwlda", "c_vwn5", "c_vwn3"] | None = None
    xalpha: float | None = None
    xbeta: float | None = None
    xkappa: float | None = None
    xmuepbe: float | None = None
    cbetapbe: float | None = None
    rangesepexx: bool | None = None
    rangesepmu: float | None = None
    rangesepscal: float | None = None
    scalhfx: float | None = None
    scaldfx: float | None = None
    scalggac: float | None = None
    scalldac: float | None = None
    extparamx: ExternalParam | None = None
    extparamc: ExternalParam | None = None
    extparamxc: ExternalParam | None = None

    # > Options DFT-D
    d3s6: float | None = None
    d3a1: float | None = None
    d3s8: float | None = None
    d3a2: float | None = None

    # > Options for Extopt
    ProgExt: InputFilePath | None = None  # Path to wrapper script
    Ext_Params: str | None = None  # Arbitrary optional command line arguments

    @field_validator("ProgExt", mode="before")
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

    @field_validator("extparamx", "extparamc", "extparamxc", mode="before")
    @classmethod
    def init_ext_param(
        cls, inp: str | list[str] | dict[str, float] | ExternalParam, info: ValidationInfo
    ) -> ExternalParam:
        """
        Allows user to input dict or list of strings for external parameter attributes, the initialization of `ExternalParam` is done internally.
        Also sets field name which is required for formatting of external parameters attributes.

        Parameters
        ----------
        inp: list[str]| dict[str, float]| ExternalParam

        info: ValidationInfo

        Returns
        -------
        ExternalParam
            ExternalParam instance
        """
        field_name = info.field_name
        if isinstance(inp, ExternalParam):
            if inp.field_name is None:
                inp.field_name = field_name
            return inp
        elif isinstance(inp, dict):
            return ExternalParam(field_name=field_name, parameters=inp)
        else:
            return ExternalParam.from_string(field_name, inp)

    @field_validator("method", "exchange", "correlation", "ldaopt", mode="before")
    @classmethod
    def string_tolower(cls, inp: str) -> str:
        """If input is a string, convert it to lowercase. This allows for case-insensitive validation.

        Examples
        --------
        BlockMethod(method='DFT')
        BlockMethod(method='dft')
        BlockMethod(method='dFT')

        All of these will be accepted if `dft` is valid literal.
        """
        return inp.lower()
