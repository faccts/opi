from opi.output.models.base.get_item import GetItem
from opi.output.models.base.strict_types import StrictNonNegativeFloat, StrictNonNegativeInt
from opi.output.models.json.gbw.properties.molecular_two_electron_integral import (
    MolecularTwoElectronIntegral,
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
    mo_ijkl : MolecularTwoElectronIntegral
        Molecular orbital basis two electron integrals in Coulomb order, 0-external
    mo_ijka : MolecularTwoElectronIntegral
        Molecular orbital basis two electron integrals in Coulomb order, 1-external
    mo_ijab : MolecularTwoElectronIntegral
        Molecular orbital basis two electron integrals in Coulomb order, 2-external
    mo_iabc : MolecularTwoElectronIntegral
        Molecular orbital basis two electron integrals in Coulomb order, 3-external
    mo_abcd : MolecularTwoElectronIntegral
        Molecular orbital basis two electron integrals in Coulomb order, 4-external
    mo_pqrs : MolecularTwoElectronIntegral
        Molecular orbital basis two electron integrals in Coulomb order, all
    mo_ikjl : MolecularTwoElectronIntegral
        Molecular orbital basis two electron integrals in Exchange order, 0-external
    mo_ikja : MolecularTwoElectronIntegral
        Molecular orbital basis two electron integrals in Exchange order, 1-external
    mo_iajb : MolecularTwoElectronIntegral
        Molecular orbital basis two electron integrals in Exchange order, 2-external
    mo_ibac : MolecularTwoElectronIntegral
        Molecular orbital basis two electron integrals in Exchange order, 3-external
    mo_acbd : MolecularTwoElectronIntegral
        Molecular orbital basis two electron integrals in Exchange order, 4-external
    mo_prqs : MolecularTwoElectronIntegral
        Molecular orbital basis two electron integrals in Exchange order, all
    """

    orbwin: list[StrictNonNegativeInt] | None = None
    thresh: StrictNonNegativeFloat | None = None
    ao_pqrs: list[list[TwoElectronIntegralElement]] | None = None
    ao_prqs: list[list[TwoElectronIntegralElement]] | None = None
    mo_ijkl: MolecularTwoElectronIntegral | None = None
    mo_ijka: MolecularTwoElectronIntegral | None = None
    mo_ijab: MolecularTwoElectronIntegral | None = None
    mo_iabc: MolecularTwoElectronIntegral | None = None
    mo_abcd: MolecularTwoElectronIntegral | None = None
    mo_pqrs: MolecularTwoElectronIntegral | None = None
    mo_ikjl: MolecularTwoElectronIntegral | None = None
    mo_ikja: MolecularTwoElectronIntegral | None = None
    mo_iajb: MolecularTwoElectronIntegral | None = None
    mo_ibac: MolecularTwoElectronIntegral | None = None
    mo_acbd: MolecularTwoElectronIntegral | None = None
    mo_prqs: MolecularTwoElectronIntegral | None = None
