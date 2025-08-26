from typing import Any

import numpy as np
import numpy.typing as npt

from opi.input.structures.coordinates import Coordinates
from opi.utils.element import Element

__all__ = ("Atom", "GhostAtom", "PointCharge", "EmbeddingPotential")

FMT_COORD = "30.16f"


class _CoordLineBase:
    """
    Base class to model a single line of coordinates for the ORCA .inp file
    """

    def __init__(
        self,
        coordinates: Coordinates
        | tuple[int | float, int | float, int | float]
        | npt.NDArray[np.float64],
        fragment_id: int | None = None,
        nuclear_charge: float | int | None = None,
        mass: float | int | None = None,
        append_str: str | None = None,
    ) -> None:
        # // Coordinates
        self._coordinates: Coordinates
        self.coordinates = coordinates
        # -------------------------
        # Special Parameters
        # -------------------------
        # // Fragment ID
        self._fragment_id: int | None = None
        self.fragment_id = fragment_id
        # // Isotope
        self._nuclear_charge: float | None = None
        self.nuclear_charge = nuclear_charge
        self._mass: float | None = None
        self.mass = mass
        # // Append string
        self.append_str: str | None = append_str

    @property
    def coordinates(self) -> Coordinates:
        return self._coordinates

    @coordinates.setter
    def coordinates(
        self,
        value: Coordinates | tuple[int | float, int | float, int | float] | npt.NDArray[np.float64],
    ) -> None:
        """
        Parameters
        ----------
        value : Coordinates | tuple[int | float, int | float, int | float] | npt.NDArray[np.float64]
        """
        self._coordinates = Coordinates(value)

    @property
    def fragment_id(self) -> int | None:
        return self._fragment_id

    @fragment_id.setter
    def fragment_id(self, value: int | None) -> None:
        """
        Parameters
        ----------
        value : int | None
        """
        if value is not None and value < 1:
            raise ValueError(f"{self.__class__.__name__}.fragment_id: must be positive")
        self._fragment_id = value

    @property
    def nuclear_charge(self) -> float | None:
        return self._nuclear_charge

    @nuclear_charge.setter
    def nuclear_charge(self, value: float | int | None) -> None:
        """
        Parameters
        ----------
        value : float | int | None
        """
        if value is not None:
            if value < 0:
                raise ValueError(f"{self.__class__.__name__}.nuclear_charge: must be positive")
            else:
                # > Converting potential float into float
                value = float(value)
        self._nuclear_charge = value

    @property
    def mass(self) -> float | None:
        return self._mass

    @mass.setter
    def mass(self, value: float | int | None) -> None:
        """
        Parameters
        ----------
        value : float | int | None
        """
        if value is not None:
            if value < 0:
                raise ValueError(f"{self.__class__.__name__}.mass: must be positive")
            else:
                # > Converting potential float into float
                value = float(value)
        self._mass = value

    def format_orca(self) -> str:
        """Returns string representation of the Atom in the syntax of the '*xyz'-block in ORCA"""

        # > Formatting coordinate line
        # // Fragment ID
        string = self._fmt_fragment_id()
        # // Coordinates
        string += f" {self._fmt_coordinates()}"
        # // Mass + Nuclear Charge
        string += f" {self._fmt_mass_nuclear_charge()}"
        # // Append string
        string += f" {self._fmt_append_str()}"
        # > Stripping any trailing whitespaces
        return string.rstrip()

    def _fmt_fragment_id(self) -> str:
        if self.fragment_id is not None:
            return f"({self.fragment_id:d})"
        else:
            return ""

    def _fmt_coordinates(self) -> str:
        coords_str = f"{self.coordinates.x:{FMT_COORD}}"
        # // y-Coordinate
        coords_str += f" {self.coordinates.y:{FMT_COORD}}"
        # // Z-Coordinate
        coords_str += f" {self.coordinates.z:{FMT_COORD}}"

        return coords_str

    def _fmt_mass_nuclear_charge(self) -> str:
        string = ""
        # // Mass
        if self.mass is not None:
            string += f" M={self.mass:.6g}"
        # // Nuclear charge
        if self.nuclear_charge is not None:
            string += f" Z={self.nuclear_charge:.3g}"
        return string

    def _fmt_append_str(self) -> str:
        if self.append_str:
            return f"{self.append_str:s}"
        else:
            return ""

    def get_coords_as_list(self) -> list[float] | tuple[()]:
        """
        Returns coordinates of Atom object as list

        Returns
        -------
        list[float] | list[int]
            Coordinates in the form of a list
        """
        # returns coordinates of Atom
        return self.coordinates.to_list()


class _CoordLineWithElementBase(_CoordLineBase):
    """
    Base class to model a coordinate line with an element.
    """

    def __init__(self, element: Any | None = None, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self._element: Any | None = element

    def _fmt_element(self) -> str:
        return str(self._element)

    def format_orca(self) -> str:
        return f"{self._fmt_element()}{super().format_orca()}"

    def format_xyz_line(self) -> str:
        """For atom as it would appear in an XYZ file."""
        return f"{self._fmt_element()} {super()._fmt_coordinates()}"


class _CoordLineWithSymbolAndChargeBase(_CoordLineWithElementBase):
    """
    Base class to model a coordinate line with element, symbol and charge
    """

    def __init__(self, charge: float | int, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self._charge: float
        self.charge = charge

    @property
    def charge(self) -> float:
        return self._charge

    @charge.setter
    def charge(self, value: float | int) -> None:
        """
        Parameters
        ----------
        value : float | int
        """
        if value is None:
            raise ValueError(f"{self.__class__.__name__}.charge: cannot be None")
        self._charge = float(value)

    def _fmt_charge(self) -> str:
        """Formatting charge with fixed-format: width=6, precision=3"""
        return f"{self.charge:6.3f}"

    def format_orca(self) -> str:
        """Returns string representation of the Atom in the syntax of the '*xyz'-block in ORCA"""

        # > Formatting coordinate line
        # // Element
        string = self._fmt_element()
        # // Fragment ID - No space before fragment-id
        string += self._fmt_fragment_id()
        # // Charge
        string += f" {self._fmt_charge()}"
        # // Coordinates
        string += f" {self._fmt_coordinates()}"
        # // Mass + Nuclear Charge
        string += f" {self._fmt_mass_nuclear_charge()}"
        # // Append string
        string += f" {self._fmt_append_str()}"
        # > Stripping any trailing whitespaces
        return string.rstrip()


class Atom(_CoordLineWithElementBase):
    """
    Class to model singular atom in a structure.

    Attributes
    -----------
    element: `Element`
        Specify what element the atom is
    coordinates: `Coordinates`
        Define coordinates in Cartesian space
    fragment_id: int
        Define id of fragment
    nuclear_charge: float | int
        Define nuclear charge of atom
    mass: float | int
        Define mass of atom
    append_str: str
        Append an arbitrary string to coordinate line if needed
    """

    def __init__(self, element: Element | str, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self._element: Element
        self.element = element

    @property
    def element(self) -> Element:
        return self._element

    @element.setter
    def element(self, value: Element | str) -> None:
        """
        Parameters
        ----------
        value : Element | str
        """
        if not value:
            raise ValueError(f"{self.__class__.__name__}.element: cannot be empty")
        self._element = Element(value)


class GhostAtom(Atom):
    """
    Class to model ghost atom.
    """

    def _fmt_element(self) -> str:
        # > Adding ':' after element symbol
        return f"{super()._fmt_element()}:"


class PointCharge(_CoordLineWithSymbolAndChargeBase):
    """
    Class to model point charge.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self._element = "Q"


class EmbeddingPotential(_CoordLineWithSymbolAndChargeBase):
    """
    Class to model embedding potential
    """

    def _fmt_element(self) -> str:
        # > Adding '>' after element symbol
        return f"{super()._fmt_element()}>"
