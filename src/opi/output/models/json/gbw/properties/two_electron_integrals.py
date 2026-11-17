from pydantic import Field

from opi.output.models.base.get_item import GetItem
from opi.output.models.base.strict_types import StrictNonNegativeFloat, StrictNonNegativeInt
from opi.output.models.json.gbw.properties.molecular_two_electron_integral import (
    MOTwoElectronIntegral,
)
from opi.output.models.json.gbw.properties.two_electron_integral_element import (
    TwoElectronIntegralElement,
)


class TwoElectronIntegrals(GetItem):
    """
    This class contains information about the two electron integrals.

    Attributes
    ----------
    orbwin : list[StrictNonNegativeInt]
        Orbital window
    thresh : StrictNonNegativeFloat
        Threshold for neglecting integrals
    ao_pqrs: list[list[TwoElectronIntegralElement]]
        Atomic orbital basis two electron integrals in Coulomb order
    ao_prqs : list[list[TwoElectronIntegralElement]]
        Atomic orbital basis two electron integrals in Exchange order
    mo_ijkl : MOTwoElectronIntegral
        Molecular orbital basis two electron integrals in Coulomb order, 0-external
    mo_ijka : MOTwoElectronIntegral
        Molecular orbital basis two electron integrals in Coulomb order, 1-external
    mo_ijab : MOTwoElectronIntegral
        Molecular orbital basis two electron integrals in Coulomb order, 2-external
    mo_iabc : MOTwoElectronIntegral
        Molecular orbital basis two electron integrals in Coulomb order, 3-external
    mo_abcd : MOTwoElectronIntegral
        Molecular orbital basis two electron integrals in Coulomb order, 4-external
    mo_pqrs : MOTwoElectronIntegral
        Molecular orbital basis two electron integrals in Coulomb order, all
    mo_ikjl : MOTwoElectronIntegral
        Molecular orbital basis two electron integrals in Exchange order, 0-external
    mo_ikja : MOTwoElectronIntegral
        Molecular orbital basis two electron integrals in Exchange order, 1-external
    mo_iajb : MOTwoElectronIntegral
        Molecular orbital basis two electron integrals in Exchange order, 2-external
    mo_ibac : MOTwoElectronIntegral
        Molecular orbital basis two electron integrals in Exchange order, 3-external
    mo_acbd : MOTwoElectronIntegral
        Molecular orbital basis two electron integrals in Exchange order, 4-external
    mo_prqs : MOTwoElectronIntegral
        Molecular orbital basis two electron integrals in Exchange order, all
    """

    orbwin: list[StrictNonNegativeInt] | None = Field(default=None, serialization_alias="OrbWin")
    thresh: StrictNonNegativeFloat | None = Field(default=None, serialization_alias="Thresh")
    ao_pqrs: list[list[TwoElectronIntegralElement]] | None = Field(
        default=None, serialization_alias="AO_PQRS"
    )
    ao_prqs: list[list[TwoElectronIntegralElement]] | None = Field(
        default=None, serialization_alias="AO_PRQS"
    )
    mo_ijkl: MOTwoElectronIntegral | None = Field(default=None, serialization_alias="MO_IJKL")
    mo_ijka: MOTwoElectronIntegral | None = Field(default=None, serialization_alias="MO_IJKA")
    mo_ijab: MOTwoElectronIntegral | None = Field(default=None, serialization_alias="MO_IJAB")
    mo_iabc: MOTwoElectronIntegral | None = Field(default=None, serialization_alias="MO_IABC")
    mo_abcd: MOTwoElectronIntegral | None = Field(default=None, serialization_alias="MO_ABCD")
    mo_pqrs: MOTwoElectronIntegral | None = Field(default=None, serialization_alias="MO_PQRS")
    mo_ikjl: MOTwoElectronIntegral | None = Field(default=None, serialization_alias="MO_IKJL")
    mo_ikja: MOTwoElectronIntegral | None = Field(default=None, serialization_alias="MO_IKJA")
    mo_iajb: MOTwoElectronIntegral | None = Field(default=None, serialization_alias="MO_IAJB")
    mo_ibac: MOTwoElectronIntegral | None = Field(default=None, serialization_alias="MO_IBAC")
    mo_acbd: MOTwoElectronIntegral | None = Field(default=None, serialization_alias="MO_ACBD")
    mo_prqs: MOTwoElectronIntegral | None = Field(default=None, serialization_alias="MO_PRQS")
