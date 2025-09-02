from pydantic import StrictBool

from opi.output.models.base.get_item import GetItem
from opi.output.models.base.strict_types import (
    StrictFiniteFloat,
    StrictNonNegativeFloat,
    StrictNonNegativeInt,
    StrictPositiveFloat,
)


class ThermochemistryEnergy(GetItem):
    """
    This class contains information about the thermochemistry and energies calculated in the calculation

    Attributes
    ----------
    temperature: StrictNonNegativeFloat | None, default = None
        The temperature simulated in the calculation
    pressure: StrictNonNegativeFloat | None, default = None
       The pressure simulated in the calculation
    totalmass: StrictPositiveFloat | None, default = None
       The total mass of the molecule(s)
    spindegeneracy: StrictNonNegativeInt | None, default = None
        Degeneracy of the spin
    elenergy: StrictFiniteFloat | None, default = None
        Electron energy
    transenergy: StrictFiniteFloat | None, default = None
        Energy of the transition
    rotenergy: StrictFiniteFloat | None, default = None
        Energy of the rotation
    vibenergy: StrictFiniteFloat | None, default = None
        Energy of the vibration
    freqscalingfactor: StrictPositiveFloat | None, default = None
        Scaling factor of the frequencies
    freq: list[list[StrictFiniteFloat]] | None, default = None
        list of all frequencies
    zpe: StrictPositiveFloat | None, default = None
        Zero point energy
    innerenergyu: StrictFiniteFloat | None, default = None
        Inner Energy of the system
    enthalpyh: StrictFiniteFloat | None, default = None
        Enthalpy of the system
    qel: StrictFiniteFloat | None, default = None
        Gibbs electron energy
    qrot: StrictNonNegativeFloat | None, default = None
        Gibbs energy for Rotations
    qvib: StrictNonNegativeFloat | None, default = None
        Gibbs energy for vibration
    entropys: StrictFiniteFloat | None, default = None
        Entropy of the system
    freeenergyg: StrictFiniteFloat | None, default = None
        Gibbs (free) energy of the system
    islinear: StrictBool | None, default = None
        Is the molecular linear (true), else false
    """

    temperature: StrictNonNegativeFloat | None = None
    pressure: StrictNonNegativeFloat | None = None
    totalmass: StrictPositiveFloat | None = None
    spindegeneracy: StrictNonNegativeInt | None = None
    elenergy: StrictFiniteFloat | None = None
    transenergy: StrictFiniteFloat | None = None
    rotenergy: StrictFiniteFloat | None = None
    vibenergy: StrictFiniteFloat | None = None
    numoffreqs: StrictNonNegativeInt | None = None
    freqscalingfactor: StrictPositiveFloat | None = None
    freq: list[list[StrictFiniteFloat]] | None = None
    zpe: StrictPositiveFloat | None = None
    innerenergyu: StrictFiniteFloat | None = None
    enthalpyh: StrictFiniteFloat | None = None
    qel: StrictFiniteFloat | None = None
    qrot: StrictNonNegativeFloat | None = None
    qvib: StrictNonNegativeFloat | None = None
    entropys: StrictFiniteFloat | None = None
    freeenergyg: StrictFiniteFloat | None = None
    islinear: StrictBool | None = None
