from typing import cast

import numpy as np
import numpy.typing as npt

__all__ = ("Coordinates",)


class Coordinates:
    """
    Coordinates of an atom in Cartesian space.

    Can be initialized using a tuple, numpy arrays or another instance of `Coordinates`.

    Attributes
    ----------
    coordinates: Column vector with three rows.
    """

    def __init__(
        self,
        coordinates: "Coordinates | tuple[int | float, int | float, int | float] | npt.NDArray[np.float64]",
    ) -> None:
        self._coordinates: npt.NDArray[np.float64] = np.zeros((3,), dtype=np.float64)
        self.coordinates = cast(npt.NDArray[np.float64], coordinates)

    @property
    def coordinates(self) -> npt.NDArray[np.float64]:
        return self._coordinates

    @coordinates.setter
    def coordinates(
        self,
        values: "Coordinates | tuple[int | float, int | float, int | float] | npt.NDArray[np.float64]",
    ) -> None:
        """
        Parameters
        ----------
        values : Coordinates | tuple[int | float, int | float, int | float] | npt.NDArray[np.float64]
        """
        # > If `values` is an object of the class then just copy the underlying array
        if isinstance(values, Coordinates):
            values = values.coordinates

        tup3d = np.array(values, dtype=np.float64)
        if tup3d.shape != (3,):
            raise ValueError(f"{self.__class__.__name__}.coordinates: invalid shape: {tup3d.shape}")

        self._coordinates = tup3d

    def to_list(self) -> list[float]:
        """
        Returns coordinates as list
        """
        coords = self.coordinates.tolist()
        return cast(list[float], coords)

    @property
    def x(self) -> np.float64:
        """x-coordinate"""
        return cast(np.float64, self.coordinates[0])

    @x.setter
    def x(self, value: int | float | np.float64) -> None:
        """
        Parameters
        ----------
        value : int | float | np.float64
        """
        self.coordinates[0] = value

    @property
    def y(self) -> np.float64:
        """y-coordinate"""
        return cast(np.float64, self.coordinates[1])

    @y.setter
    def y(self, value: int | float | np.float64) -> None:
        """
        Parameters
        ----------
        value : int | float | np.float64
        """
        self.coordinates[1] = value

    @property
    def z(self) -> np.float64:
        """z-coordinate"""
        return cast(np.float64, self.coordinates[2])

    @z.setter
    def z(self, value: int | float | np.float64) -> None:
        """
        Parameters
        ----------
        value : int | float | np.float64
        """
        self.coordinates[2] = value
