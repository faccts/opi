import pytest

from opi.core import Calculator
from opi.input.blocks import Block, BlockABC, BlockScf

"""
This module contains tests for arbitrary blocks (`Block`) such as:
- Naming of an arbitrary block
- Options of an arbitrary block
- Formatting for the ORCA input file
- Addition, getting and removal of arbitrary blocks in a `Calculator` object
"""


@pytest.fixture
def empty_calc():
    """An empty instance of `Calculator`."""
    return Calculator("test", version_check=False)


@pytest.fixture
def arbitrary_block():
    """An instance of `Block` with a single option."""
    return Block("myblock", {"opt1": "val1"})


@pytest.fixture
def calc(arbitrary_block):
    """An instance of `Calculator` with two arbitrary blocks."""
    calc = Calculator("test", version_check=False)
    calc.input.add_blocks(arbitrary_block, Block("otherblock", {"opt2": "val2"}))
    return calc


@pytest.mark.unit
@pytest.mark.input
@pytest.mark.parametrize(
    "name",
    [
        "myblock",
        "MyBlock",
        "  myblock  ",
        "%myblock",
        "  % MyBlock  ",
    ],
)
def test_arbitrary_block_name(name: str):
    """Test that the name of an `Block` is normalized."""
    assert Block(name).name == "myblock"


@pytest.mark.unit
@pytest.mark.input
@pytest.mark.parametrize(
    "name",
    [
        "",
        "   ",
        "\n",
        "%",
    ],
)
def test_arbitrary_block_invalid_name(name: str):
    """Test that an invalid name for an `Block` raises a `ValueError`."""
    with pytest.raises(ValueError):
        Block(name)


@pytest.mark.unit
@pytest.mark.input
@pytest.mark.parametrize(
    "name",
    [
        "scf",
        "SCF",
        "%scf",
    ],
)
def test_arbitrary_block_implemented_name(name: str):
    """Test that an `Block` cannot take the name of an implemented block."""
    with pytest.raises(ValueError):
        Block(name)


@pytest.mark.unit
@pytest.mark.input
def test_arbitrary_block_registry():
    """Test that implemented blocks are registered by name, while `Block` is not."""
    assert BlockABC.get_block_class("scf") is BlockScf
    assert Block.get_block_name() is None

    Block("myblock")
    assert BlockABC.get_block_class("myblock") is None


@pytest.mark.unit
@pytest.mark.input
def test_arbitrary_block_options(arbitrary_block: Block):
    """Test that options of an `Block` are accessible case-insensitively."""
    arbitrary_block.add_option("Opt2", "val2")

    assert arbitrary_block.get_option("OPT1") == "val1"
    assert arbitrary_block.has_option("opt2")


@pytest.mark.unit
@pytest.mark.input
def test_arbitrary_block_format_orca(arbitrary_block: Block):
    """Test for `BlockABC.format_orca()` of an `Block`."""
    assert arbitrary_block.format_orca() == "%myblock\n    opt1 val1\nend"


@pytest.mark.unit
@pytest.mark.input
def test_add_arbitrary_blocks(calc: Calculator):
    """Test that arbitrary blocks with different names do not overwrite each other."""
    assert calc.input.has_blocks("myblock", "otherblock") == (True, True)
    assert calc.input.format_before_coords().count("%myblock") == 1


@pytest.mark.unit
@pytest.mark.input
def test_add_arbitrary_blocks_same_name_strict(calc: Calculator):
    """Test for `Input.add_blocks()` with `strict=True` and an already added arbitrary block."""
    with pytest.raises(ValueError):
        calc.input.add_blocks(Block("myblock"), strict=True)


@pytest.mark.unit
@pytest.mark.input
def test_add_arbitrary_blocks_same_name_overwrite(calc: Calculator):
    """Test for `Input.add_blocks()` with `overwrite=True` and an already added arbitrary block."""
    calc.input.add_blocks(Block("myblock", {"opt3": "val3"}), overwrite=True)

    assert len(calc.input.blocks) == 2
    assert calc.input.blocks["myblock"].get_option("opt3") == "val3"


@pytest.mark.unit
@pytest.mark.input
def test_get_arbitrary_block(calc: Calculator, arbitrary_block: Block):
    """Test for `Input.get_blocks()` with the name of an arbitrary block."""
    assert calc.input.get_blocks("MyBlock") == {"myblock": arbitrary_block}


@pytest.mark.unit
@pytest.mark.input
@pytest.mark.parametrize("remove_param", ["myblock", "%MyBlock", Block("myblock")])
def test_remove_arbitrary_block(calc: Calculator, remove_param: str | Block):
    """Test for `Input.remove_blocks()` with the name or an instance of an arbitrary block."""
    calc.input.remove_blocks(remove_param)
    assert calc.input.has_blocks("myblock", "otherblock") == (False, True)


@pytest.mark.unit
@pytest.mark.input
def test_arbitrary_block_class_rejected(calc: Calculator):
    """Test that the `Block` class itself does not identify a block, as it is named at runtime."""
    with pytest.raises(ValueError):
        calc.input.has_blocks(Block)


@pytest.mark.unit
@pytest.mark.input
def test_get_arbitrary_block_create_missing(empty_calc: Calculator):
    """Test that an arbitrary block cannot be created from its name, as no class implements it."""
    assert empty_calc.input.get_blocks("myblock", create_missing=True) == {}
