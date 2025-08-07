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
    charge: StrictInt | None, default = None
        Charge of the molecule
    mult: StrictPositiveInt | None, default = None
        Multiplicity of the molecule
    numofatoms: StrictPositiveInt | None, default = None
        Numbers of atoms in the molecule
    numofelectrons: StrictNonNegativeInt | None, default = None
        Number of electrons in the molecule
    numoffcelectrons: StrictNonNegativeInt | None, default = None
        Number of fc electrons
    numofcorrelectrons: StrictNonNegativeInt | None, default = None
        Number of corr electrons
    numofbasisfuncts: PositiveInt | None, default = None
        Number of basis function
    numofauxcbasisfuncts: StrictNonNegativeInt | None, default = None
        Number of auxiliary C basis function
    numofauxjbasisfuncts: StrictNonNegativeInt | None, default = None
        Number of auxiliary J basis function
    numofauxjkbasisfuncts: StrictNonNegativeInt | None, default = None
        Number of auxiliary JK basis function
    numofcabsbasisfuncts: StrictNonNegativeInt | None, default = None
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
