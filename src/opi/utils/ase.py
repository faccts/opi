"""
Optional interface to ASE (https://wiki.fysik.dtu.dk/ase/).

ASE is an optional dependency of OPI. See pyproject.toml for details.
"""

from __future__ import annotations

import importlib.util
from collections.abc import Sequence
from functools import wraps
from importlib import import_module
from typing import TYPE_CHECKING, Any, Callable, TypeVar

import numpy as np
import numpy.typing as npt

from opi.utils.element import Element

if TYPE_CHECKING:
    from ase import Atoms as AseAtoms

__all__ = (
    "build_ase_atoms",
    "requires_ase",
)

# > Populated on first use by the `@_import_ase` decorator (see below).
ase_atoms_cls: "type[AseAtoms] | None" = None


# ============================================================
# Decorators
# ============================================================

_T = TypeVar("_T")


def _ase_available() -> bool:
    """Return `True` if ASE is installed, without importing it."""
    return importlib.util.find_spec("ase") is not None


def requires_ase(func: Callable[..., _T]) -> Callable[..., _T]:
    """
    Decorator that raises `ImportError` if ASE is not installed.

    Apply to any method that calls `build_ase_atoms()` to ensure a clear error
    message is raised at call time rather than at import time.
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> _T:
        if not _ase_available():
            raise ImportError("ASE is not installed. It is an optional dependency of OPI.")
        return func(*args, **kwargs)

    return wrapper


def _import_ase(func: Callable[..., _T]) -> Callable[..., _T]:
    """
    Decorator that lazily imports ASE on first call and caches it.
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> _T:
        if globals()["ase_atoms_cls"] is None:
            module = import_module("ase")
            globals()["ase_atoms_cls"] = module.Atoms
        return func(*args, **kwargs)

    return wrapper


# ============================================================
# Free helper function
# ============================================================


@_import_ase
def build_ase_atoms(
    elements: Sequence[Element | str],
    coordinates: npt.NDArray[np.float64] | Sequence[Sequence[float]],
    total_charge: int,
    multiplicity: int,
) -> "AseAtoms":
    """
    Thin wrapper around the `ase.Atoms` constructor.

    This is the boundary at which OPI-native datatypes are converted into the
    plain types ASE expects. Conversions are performed here, as late as
    possible, so callers can pass their natural data (`Element` instances, a
    NumPy coordinate array) without knowing ASE's input format.

    The ASE import is handled by the `@_import_ase` decorator, which imports
    the package on first call and caches the `Atoms` class in the module globals.

    Parameters
    ----------
    elements : Sequence[Element | str]
        Elements for all real atoms, as `Element` instances, element-symbol
        strings, or a mix of both.
    coordinates : npt.NDArray[np.float64] | Sequence[Sequence[float]]
        Cartesian coordinates in Angstrom, shape (N, 3), as a NumPy array or a
        nested sequence.
    total_charge : int
        Total charge of the structure. Stored in `Atoms.info["charge"]`.
    multiplicity : int
        Spin multiplicity of the structure. Stored in `Atoms.info["spin"]`.

    Returns
    -------
    AseAtoms
        ASE `Atoms` object holding the given elements and coordinates, with
        charge and multiplicity transported via `Atoms.info`.
    """

    # > Convert OPI-native types to the plain types ASE understands.
    element_symbols: list[str] = [Element(e).value for e in elements]
    coords = np.asarray(coordinates, dtype=np.float64)

    # > The @_import_ase decorator guarantees this is populated by call time.
    assert ase_atoms_cls is not None

    return ase_atoms_cls(
        symbols=element_symbols,
        positions=coords,
        info={"charge": total_charge, "spin": multiplicity},
    )
