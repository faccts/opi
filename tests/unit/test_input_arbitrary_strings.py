import pytest

from opi.core import Calculator
from opi.input import ArbitraryString, ArbitraryStringPos


@pytest.fixture
def empty_calc():
    """An empty instance of `Calculator`."""
    empty_calc = Calculator("test", version_check=False)
    return empty_calc


@pytest.fixture
def calc():
    """An instance of `Calculator` with arbitrary strings."""
    calc = Calculator("test", version_check=False)
    calc.input.add_arbitrary_string("top test", pos=ArbitraryStringPos.TOP)
    calc.input.add_arbitrary_string("bottom test", pos=ArbitraryStringPos.BOTTOM)
    calc.input.add_arbitrary_string("before coords test", pos=ArbitraryStringPos.BEFORE_COORDS)
    return calc


@pytest.mark.parametrize(
    "string",
    [
        "test",
    ],
)
def test_add_arbitrary_strings(empty_calc: Calculator, string: str):
    """Test for `Input.add_arbitrary_string()`"""
    empty_calc.input.add_arbitrary_string(string)
    assert ArbitraryString(string) in empty_calc.input.arbitrary_strings


@pytest.mark.parametrize(
    "string, position",
    [
        ("no given position", None),
        ("toptest", ArbitraryStringPos.TOP),
        ("beforecoords", ArbitraryStringPos.BEFORE_COORDS),
        ("Bottom", ArbitraryStringPos.BOTTOM),
    ],
)
def test_add_arbitrary_strings_pos(
    empty_calc: Calculator, string: str, position: ArbitraryStringPos
):
    """Test for `Input.add_arbitrary_string()` with and without specific position."""
    empty_calc.input.add_arbitrary_string(string, pos=position)
    assert ArbitraryString(string, pos=position) in empty_calc.input.arbitrary_strings


def test_add_arbitrary_string_default_pos(empty_calc: Calculator):
    """Test for `Input.add_arbitrary_string()` with default position."""
    empty_calc.input.add_arbitrary_string("test")
    assert (
        ArbitraryString("test", pos=ArbitraryStringPos.BEFORE_COORDS)
        in empty_calc.input.arbitrary_strings
    )


def test_add_arbitrary_strings_not_str(empty_calc: Calculator):
    """Test for adding a non-string to arbitrary strings."""
    with pytest.raises(TypeError):
        empty_calc.input.add_arbitrary_string(1234)


def test_add_empty_string(empty_calc: Calculator):
    """Test for adding an empty string to arbitrary strings."""
    with pytest.raises(ValueError):
        empty_calc.input.add_arbitrary_string("")


@pytest.mark.parametrize(
    "remove_param, removed_string",
    [
        ("top test", [ArbitraryString("top test")]),
        ("bottom test", ArbitraryString("bottom test")),
        ("before coords test", ArbitraryString("before coords test")),
    ],
)
def test_remove_string(
    calc: Calculator, remove_param: str | ArbitraryString, removed_string: ArbitraryString
):
    """Test for removing a string from the arbitrary strings in the `Input` class."""
    calc.input.remove_arbitrary_string(remove_param)
    assert removed_string not in calc.input.arbitrary_strings


def test_remove_arbitrary_string_strict(empty_calc: Calculator):
    """Test for `Input.remove_arbitrary_string()` with `strict=True`. When `strict=True`,
    a `ValueError` is raised if no `ArbitraryString` instance is found."""
    with pytest.raises(ValueError):
        empty_calc.input.remove_arbitrary_string("test", strict=True)


def test_clear_arbitrary_strings(calc: Calculator):
    """Test for `Input.clear_arbitrary_strings()`."""
    calc.input.clear_arbitrary_strings()
    assert not calc.input.arbitrary_strings


def test_clear_arbitrary_strings_strict(empty_calc: Calculator):
    """Test for `Input.clear_arbitrary_strings()` with `strict=True`. When `strict=True`, a `ValueError`
    is raised if no `ArbitraryString` instance is found."""
    with pytest.raises(ValueError):
        empty_calc.input.clear_arbitrary_strings(strict=True)
