from typing import Literal

from opi.output.models.base.strict_types import (
    StrictFiniteFloat,
    StrictNonNegativeInt,
    StrictPositiveInt,
)
from opi.output.models.json.property.properties.energy import Energy


class CasEnergyBase(Energy):
    """Base class for information about CAS energies

    Attributes
    ----------
    numofelectrons: StrictNonNegativeInt | None, default = None
        Number of electrons
    numoffcelectrons: StrictNonNegativeInt | None, default = None
        Number of FC electrons
    numofactiveel: StrictNonNegativeInt | None, default = None
        Number of active electrons
    numofactiveorbs: StrictNonNegativeInt | None, default = None
        number oof active orbitals
    numofmultiplicities: StrictPositiveInt | None, default = None
        Number of multiplicities
    totalnumofroots: StrictNonNegativeInt | None, default = None
        Total number of roots
    finalenergy: StrictFiniteFloat | None, default = None
        Final energy
    energies: list[list[StrictFiniteFloat]] | None, default = None
        list of all CasSCF energies
    irreps: list[list[StrictFiniteFloat]] | None, default = None
        list of all irreducible representations of CASSCF states
    multiplicities: list[list[StrictFiniteFloat]] | None, default = None
        list of all multiplicities of CASSCF states
    numofroots: list[list[StrictFiniteFloat]] | None, default = None
        list of number of roots for all CASSCF states
    """

    numofelectrons: StrictNonNegativeInt | None = None
    numoffcelectrons: StrictNonNegativeInt | None = None
    numofactiveel: StrictNonNegativeInt | None = None
    numofactiveorbs: StrictNonNegativeInt | None = None
    numofmultiplicities: StrictPositiveInt | None = None
    totalnumofroots: StrictNonNegativeInt | None = None
    finalenergy: StrictFiniteFloat | None = None
    casscfenergies: (
        list[
            tuple[
                StrictNonNegativeInt,
                StrictPositiveInt,
                StrictNonNegativeInt,
                StrictNonNegativeInt,
                StrictFiniteFloat,
            ]
        ]
        | None
    ) = None


class CasEnergy(CasEnergyBase):
    """This class contains information about the CASSCF energy"""

    method: Literal["CASSCF"]


class Caspt2Energy(CasEnergyBase):
    """This class contains information about NEVPT2/CASPT2 energies"""

    method: Literal["CASSCF IC-PT2: NEVPT2/CASPT2"]
