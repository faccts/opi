import inspect
from pathlib import Path
from typing import Callable

import pytest


@pytest.fixture
def example_path_for() -> Callable[[Callable[..., object]], Path]:
    """Return the directory where the given function is defined."""

    def _get_path(fn: Callable[..., object]) -> Path:
        return Path(inspect.getfile(fn)).parent

    return _get_path


@pytest.fixture
def example_input_file(
    example_path_for: Callable[[Callable[..., object]], Path],
) -> Callable[[Callable[..., object], str], Path]:
    """Return inp.xyz from the directory where the given function is defined."""

    def _get(fn: Callable[..., object], filename: str = "inp.xyz") -> Path:
        path = example_path_for(fn) / filename
        assert path.exists(), f"Missing input file: {path}"
        return path

    return _get
