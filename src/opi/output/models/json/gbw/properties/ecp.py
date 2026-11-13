from pydantic import Field, StrictFloat, StrictStr

from opi.output.models.base.get_item import GetItem
from opi.output.models.base.strict_types import StrictNonNegativeInt


class EcpShell(GetItem):
    """
    Contains one angular momentum channel of an effective core potential (ECP).

    The channel of the highest angular momentum (see `Ecp.lmax`) is the local part of the ECP,
    while all other channels hold the semi-local parts relative to it.

    Attributes
    ----------
    shell: StrictStr
        Angular momentum of the channel (e.g. "s", "p", ...)
    ecp: list[list[StrictFloat]]
        Primitives of the channel as three lists: exponents, coefficients, and the powers n of
        the radial prefactor r^(n-2).
    """

    shell: StrictStr | None = Field(default=None, serialization_alias="Shell")
    ecp: list[list[StrictFloat]] | None = Field(default=None, serialization_alias="ecp")


class Ecp(GetItem):
    """
    Contains the effective core potential (ECP) of an atom.

    Attributes
    ----------
    n_core: StrictNonNegativeInt
        Number of core electrons replaced by the ECP
    lmax: StrictStr
        Angular momentum of the local part of the ECP
    potential: list[EcpShell]
        Angular momentum channels of the ECP
    """

    n_core: StrictNonNegativeInt | None = Field(default=None, serialization_alias="N_core")
    lmax: StrictStr | None = Field(default=None, serialization_alias="lmax")
    potential: list[EcpShell] | None = Field(default=None, serialization_alias="potential")
