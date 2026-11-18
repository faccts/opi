"""
Helpers for optional dependencies of OPI. See pyproject.toml for the available extras.
"""

from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from importlib.util import find_spec
from typing import ParamSpec, TypeVar

__all__ = ("requires_optional",)

_P = ParamSpec("_P")
_T = TypeVar("_T")


def requires_optional(
    module: str, /, *, name: str, package: str
) -> Callable[[Callable[_P, _T]], Callable[_P, _T]]:
    """
    Create a decorator that raises `ImportError` if an optional dependency is not installed.

    The availability is checked at call time via `importlib.util.find_spec`, so neither the
    decorator nor the decorated function's module has to import the dependency. The signature of
    the decorated function is preserved for type checkers.

    Parameters
    ----------
    module : str
        Name of the module to look for, e.g. "pyscf".
    name : str
        Name of the dependency as shown in the error message, e.g. "PySCF".
    package : str
        Name of the package to install, as shown in the error message, e.g. "pyscf".

    Returns
    -------
    Callable[[Callable[_P, _T]], Callable[_P, _T]]
        Decorator for functions and methods that need the dependency at runtime.
    """

    def decorator(func: Callable[_P, _T]) -> Callable[_P, _T]:
        @wraps(func)
        def wrapper(*args: _P.args, **kwargs: _P.kwargs) -> _T:
            if find_spec(module) is None:
                raise ImportError(
                    f"{name} is not installed. It is an optional dependency of OPI, "
                    f"install it with `pip install {package}`."
                )
            return func(*args, **kwargs)

        return wrapper

    return decorator
