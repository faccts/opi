"""
Optional interface to MolBar (https://git.rwth-aachen.de/bannwarthlab/molbar).

MolBar is not a dependency of OPI. Install it separately::

    pip install molbar
"""

from __future__ import annotations

import importlib.util
from collections.abc import Sequence
from functools import wraps
from importlib import import_module
from typing import Any, Callable, TypeVar

import numpy as np
import numpy.typing as npt

from opi.models.string_enum import StringEnum
from opi.utils.element import Element

__all__ = (
    "MolBarMode",
    "call_molbar",
    "requires_molbar",
)

# > Populated on first use by the `@_import_molbar` decorator (see below).
# > Declared here so the name resolves for type checkers and at call time,
# > before the first invocation has cached the real function.
# > For the exact function signature, consult MolBar's documentation.
get_molbar_from_coordinates: Callable[..., str | tuple[str, dict[str, Any]]] | None = None


# ============================================================
# Mode classification
# ============================================================


class MolBarMode(StringEnum):
    """
    Molbar's calculations modes.
    More details about these can be found: <https://bannwarthlab.pages.rwth-aachen.de/molbardocs/>

    Entries in the enum can be resolved case-insensitively.

    Attributes
    ----------
    MB : str
        Full MolBar barcode (`mb`).
    TOPO : str
        Topology-only barcode (`topo`).
    """

    MB = "mb"
    TOPO = "topo"


# ============================================================
# Decorators
# ============================================================

_T = TypeVar("_T")


def _molbar_available() -> bool:
    """Return `True` if MolBar is installed, without importing it."""
    return importlib.util.find_spec("molbar") is not None


def requires_molbar(func: Callable[..., _T]) -> Callable[..., _T]:
    """
    Decorator that raises `ImportError` if MolBar is not installed.

    Apply to any method that calls `call_molbar()` to ensure a clear error
    message is raised at call time rather than at import time. Availability is
    checked via `importlib.util.find_spec` so the decorator does not import
    MolBar itself.
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> _T:
        if not _molbar_available():
            raise ImportError("MolBar is not installed. Install it with: pip install molbar")
        return func(*args, **kwargs)

    return wrapper


def _import_molbar(func: Callable[..., _T]) -> Callable[..., _T]:
    """
    Decorator that lazily imports MolBar on first call and caches it.

    MolBar has heavy dependencies and `opi.utils.molbar` is imported
    transitively on almost any OPI import (via `structure.py`). Deferring the
    import means users who never compute a barcode never pay the cost. On the
    first invocation of the decorated function, `molbar.barcode` is imported
    via `importlib.import_module` and `get_molbar_from_coordinates` is injected
    into this module's `globals()`; subsequent calls reuse the cached global,
    so the import happens at most once and only when actually needed.

    Warnings
    --------
    The first-call import-and-cache step is **not thread-safe**. If two threads
    call the decorated function concurrently before the first import has
    completed, the import may run more than once. This is harmless in practice
    (the module is cached in `sys.modules` and the resulting function is
    identical) but is noted here for completeness.
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> _T:
        if globals()["get_molbar_from_coordinates"] is None:
            module = import_module("molbar.barcode")
            globals()["get_molbar_from_coordinates"] = module.get_molbar_from_coordinates
        return func(*args, **kwargs)

    return wrapper


# ============================================================
# Free helper function
# ============================================================


@_import_molbar
def call_molbar(
    elements: Sequence[Element | str],
    coordinates: npt.NDArray[np.float64] | Sequence[Sequence[float]],
    total_charge: int,
    mode: MolBarMode,
    return_data: bool,
) -> "str | tuple[str, dict[str, Any]]":
    """
    Thin wrapper around `molbar.barcode.get_molbar_from_coordinates`.

    This is the boundary at which OPI-native datatypes are converted into the
    plain types MolBar expects. Conversions are performed here, as late as
    possible, so callers can pass their natural data (`Element` instances, a
    NumPy coordinate array) without knowing MolBar's input format.

    The MolBar import is handled by the `@_import_molbar` decorator, which
    imports the package on first call and caches it in the module globals.

    Parameters
    ----------
    elements : Sequence[Element | str]
        Elements for all real atoms, as `Element` instances, element-symbol
        strings, or a mix of both.
    coordinates : npt.NDArray[np.float64] | Sequence[Sequence[float]]
        Cartesian coordinates in Ångström, shape (N, 3), as a NumPy array or a
        nested sequence.
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

    # > Convert OPI-native types to the plain types MolBar understands.
    element_symbols: list[str] = [Element(e).value for e in elements]
    coords = np.asarray(coordinates, dtype=np.float64)

    # > The @_import_molbar decorator guarantees this is populated by call time.
    assert get_molbar_from_coordinates is not None

    return get_molbar_from_coordinates(
        coords,
        element_symbols,
        total_charge=total_charge,
        return_data=return_data,
        mode=mode,
    )
