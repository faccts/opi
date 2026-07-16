"""
Optional interface to MolBar (https://git.rwth-aachen.de/bannwarthlab/molbar).

MolBar is not a dependency of OPI. Install it separately::

    pip install molbar
"""

from __future__ import annotations

from functools import wraps
from typing import Any, Callable, TypeVar, cast

from opi.models.string_enum import StringEnum

__all__ = (
    "MolBarMode",
    "requires_molbar",
)

# ============================================================
# MolBar optional import
# ============================================================

# MolBar is an optional dependency. The decorator below guards every method
# that calls it and raises a clear ImportError if it is not installed.
try:
    from molbar.barcode import get_molbar_from_coordinates  # type: ignore
except ImportError:
    # Ensure the name exists in the global namespace so the decorator can
    # check it unconditionally without a NameError.
    get_molbar_from_coordinates = None  # type: ignore[assignment,unused-ignore]

# ============================================================
# Mode classification
# ============================================================


class MolBarMode(StringEnum):
    """Valid calculation modes for `Structure.to_molbar`.

    Matching is case-insensitive: pass `"MB"`, `"mb"`, or `"Mb"`
    and all will be accepted.

    Attributes
    ----------
    MB : str
        Full MolBar barcode (`"mb"`).
    TOPO : str
        Topology-only barcode (`"topo"`).
    """

    MB = "mb"
    TOPO = "topo"


# ============================================================
# Decorator
# ============================================================

_T = TypeVar("_T")


def requires_molbar(func: Callable[..., _T]) -> Callable[..., _T]:
    """
    Decorator that raises `ImportError` if MolBar is not installed.

    Apply to any method that calls `molbar.barcode.get_molbar_from_coordinates`
    to ensure a clear error message is raised at call time rather than at
    import time.
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> _T:
        if get_molbar_from_coordinates is None:
            raise ImportError("MolBar is not installed. Install it with: pip install molbar")
        return func(*args, **kwargs)

    return wrapper


# ============================================================
# Free helper function
# ============================================================


def call_molbar(
    elements: list[str],
    coordinates: list[list[float]],
    total_charge: int,
    mode: MolBarMode,
    return_data: bool,
) -> "str | tuple[str, dict[str, Any]]":
    """
    Thin wrapper around `molbar.barcode.get_molbar_from_coordinates`.

    Parameters
    ----------
    elements : list[str]
        Element symbols for all real atoms.
    coordinates : list[list[float]]
        Cartesian coordinates in Ångström, shape (N, 3).
    total_charge : int
        Total charge of the structure.
    mode : MolBarMode
        Already-validated calculation mode.
    return_data : bool
        If `True` returns `tuple[str, dict[str, Any]]`; if `False` returns `str`.

    Returns
    -------
    str | tuple[str, dict[str, Any]]
        Either the barcode string or the barcode string together with the
        full MolBar data dictionary, depending on *return_data*.
    """

    return cast(
        "str | tuple[str, dict[str, Any]]",
        get_molbar_from_coordinates(  # type: ignore[operator,unused-ignore]
            coordinates,
            elements,
            total_charge=total_charge,
            return_data=return_data,
            mode=mode,
        ),
    )
