"""
Optional interface to ASE (https://wiki.fysik.dtu.dk/ase/).

ASE is an optional dependency of OPI. See pyproject.toml for details.
"""

from __future__ import annotations

from functools import wraps
from importlib import import_module
from typing import Any, Callable, TypeVar

__all__ = ("requires_ase",)


# ============================================================
# Decorators
# ============================================================

_T = TypeVar("_T")


def requires_ase(func: Callable[..., _T]) -> Callable[..., _T]:
    """
    Decorator that lazily imports ASE on first call and caches it.

    Apply to any function or method that needs ASE at runtime.
    On the first invocation, `ase` is imported via `importlib.import_module`
    and its `Atoms` class is injected as `AseAtoms` into the globals of the
    *decorated function's own module* (`func.__globals__`).

    The decorated module is expected to declare the name for type checkers:

        if TYPE_CHECKING:
            from ase import Atoms as AseAtoms  # noqa: F401
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> _T:
        namespace = func.__globals__
        if namespace.get("AseAtoms") is None:
            try:
                module = import_module("ase")
            except ImportError as error:
                raise ImportError(
                    "ASE is not installed. It is an optional dependency of OPI."
                ) from error
            namespace["AseAtoms"] = module.Atoms
        return func(*args, **kwargs)

    return wrapper
