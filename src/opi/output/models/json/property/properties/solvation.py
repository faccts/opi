from pydantic import StrictStr

from opi.output.models.base.get_item import GetItem
from opi.output.models.base.strict_types import (
    StrictFiniteFloat,
    StrictPositiveFloat,
    StrictPositiveInt,
    StrictPositiveFloatOrMinusOne
)


class SolvDetails(GetItem):
    """
    This class contains information about the solvation Calculation

    Attributes
    ---------
    solvent: StrictStr | None, default = None
        Name of the solvent
    epsilon: StrictPositiveFloatOrMinusOne | None, default = None
        Dielectric constant of the solvent
    refrac: StrictPositiveFloat | None, default = None
        Refraction index of the solvent
    rsolv: StrictPositiveFloat | None, default = None
        Radiation of the solvent
    surfacetype: StrictStr | None, default = None
        Type of the solvation surface
    npoints: StrictPositiveInt | None, default = None
        Number of points
    surfacearea: StrictPositiveFloat | None, default = None
        Surface area
    cpcmdielenergy: StricFinitetFloat | None, default = None
        Total solvation energy
    """

    solvent: StrictStr | None = None
    epsilon: StrictPositiveFloatOrMinusOne | None = None
    refrac: StrictPositiveFloat | None = None
    rsolv: StrictPositiveFloat | None = None
    surfacetype: StrictStr | None = None
    npoints: StrictPositiveInt | None = None
    surfacearea: StrictPositiveFloat | None = None
    cpcmdielenergy: StrictFiniteFloat | None = None
