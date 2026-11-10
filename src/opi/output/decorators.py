"""
Decorators for the getters of `opi.output.core.Output`.
"""

import functools
from collections.abc import Callable
from typing import TYPE_CHECKING, Any, Concatenate, ParamSpec, TypeVar

from opi.exceptions import OpiOutputMissingValueError

if TYPE_CHECKING:
    from opi.output.core import Output

_P = ParamSpec("_P")
_R = TypeVar("_R")


def _is_missing(value: Any) -> bool:
    """Whether a getter result means that no value was found (None or a tuple of only None)."""
    if value is None:
        return True
    return isinstance(value, tuple) and all(v is None for v in value)


def raise_on_missing_value(
    getter: Callable[Concatenate["Output", _P], _R],
) -> Callable[Concatenate["Output", _P], _R]:
    """
    Decorator for `Output` getters that raises `OpiOutputMissingValueError` instead of returning None,
    if `Output.raise_on_missing` is set.
    Only the getter called by the user raises. Getters called by other getters still return None,
    so that optional values (e.g. the charge of a structure) do not raise.
    """

    @functools.wraps(getter)
    def wrapper(self: "Output", /, *args: _P.args, **kwargs: _P.kwargs) -> _R:
        self._getter_depth += 1
        try:
            result = getter(self, *args, **kwargs)
        finally:
            self._getter_depth -= 1

        if self.raise_on_missing and self._getter_depth == 0 and _is_missing(result):
            raise OpiOutputMissingValueError(
                f"`Output.{getter.__name__}()` found no value in the output of '{self.basename}'."
            )
        return result

    return wrapper
