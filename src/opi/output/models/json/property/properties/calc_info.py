from pydantic import StrictInt

from opi.output.models.base.get_item import GetItem
from opi.output.models.base.strict_types import (
    StrictNonNegativeInt,
    StrictPositiveInt,
)


class CalcInfo(GetItem):
    """
    Contains the information about the Job done by ORCA

    Attributes
    ----------
    charge: StrictInt
        Charge of the molecule
    mult: StrictPositiveInt
        Multiplicity of the molecule
    numofatoms: StrictPositiveInt
        Numbers of atoms in the molecule
    numofelectrons: StrictNonNegativeInt
        Number of electrons in the molecule
    numoffcelectrons: StrictNonNegativeInt
        Number of fc electrons
    numofcorrelectrons: StrictNonNegativeInt
        Number of corr electrons
    numofbasisfuncts: PositiveInt
        Number of basis function
    numofauxcbasisfuncts: StrictNonNegativeInt
        Number of auxiliary C basis function
    numofauxjbasisfuncts: StrictNonNegativeInt
        Number of auxiliary J basis function
    numofauxjkbasisfuncts: StrictNonNegativeInt
        Number of auxiliary JK basis function
    numofcabsbasisfuncts: StrictNonNegativeInt
        Number of CABs basis function
    """

    charge: StrictInt | None = None
    mult: StrictPositiveInt | None = None
    numofatoms: StrictPositiveInt | None = None
    numofelectrons: StrictNonNegativeInt | None = None
    numoffcelectrons: StrictNonNegativeInt | None = None
    numofcorrelectrons: StrictNonNegativeInt | None = None
    numofbasisfuncts: StrictNonNegativeInt | None = None
    numofauxcbasisfuncts: StrictNonNegativeInt | None = None
    numofauxjbasisfuncts: StrictNonNegativeInt | None = None
    numofauxjkbasisfuncts: StrictNonNegativeInt | None = None
    numofcabsbasisfuncts: StrictNonNegativeInt | None = None
