from opi.output.models.base.strict_types import StrictNonNegativeInt
from opi.output.models.json.gbw.properties.mo import MO


class MOData:
    """Wrapper class for MO to additional hold the index and spin channel."""

    def __init__(self, index: StrictNonNegativeInt, channel: str, mo: MO):
        self.index = index
        self.channel = channel
        self.mo = mo

    def __str__(self) -> str:
        """Returns the index and the channel of the MO"""
        return f"{self.__class__.__name__} Index: {self.index}, Type: {self.channel}"

    @property
    def orbitalenergy(self) -> float | None:
        return self.mo.orbitalenergy

    @property
    def occupancy(self) -> float | None:
        return self.mo.occupancy

    @property
    def mocoefficients(self) -> list[float] | None:
        return self.mo.mocoefficients
