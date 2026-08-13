import pytest

from opi.core import Calculator
from opi.input.blocks import BlockABC, BlockEprnmr, BlockMethod, BlockScf, Nuclei, NucleiFlag
from opi.utils.element import Element

"""
This module contains tests for block-related operations including:
- Addition of blocks
- Removal of blocks
- Getting of blocks
- Checking whether block exists in a `Calculator` object
- Clearing all blocks
"""


@pytest.fixture
def empty_calc():
    """An empty instance of `Calculator`."""
    return Calculator("test", version_check=False)


@pytest.fixture
def calc():
    """An instance of `Calculator` with multiple instances of `BlockABC`."""
    calc = Calculator("test", version_check=False)
    calc.input.add_blocks(
        BlockMethod(
            d3s6=0.64,
            d3a1=0.3065,
            d3s8=0.9147,
            d3a2=5.0570,
        ),
        BlockEprnmr(
            gtensor=True,
            nuclei=Nuclei(atom=Element.HYDROGEN, flags=NucleiFlag(adip=True, aiso=True, aorb=True)),
        ),
    )
    return calc


@pytest.fixture
def empty_test_block():
    """An empty instance of `BlockABC`."""
    return BlockScf()


@pytest.fixture
def calc_with_test_block(empty_test_block):
    """An instance of `Calculator` with an empty test block."""
    calc = Calculator("test", version_check=False)
    calc.input.add_blocks(empty_test_block)
    return calc


@pytest.fixture(
    params=[
        (
            BlockEprnmr(
                gtensor=True,
                nuclei=Nuclei(
                    atom=Element.HYDROGEN, flags=NucleiFlag(adip=True, aiso=True, aorb=True)
                ),
            ),
        ),
        (
            BlockEprnmr(
                gtensor=True,
                nuclei=Nuclei(
                    atom=Element.HYDROGEN, flags=NucleiFlag(adip=True, aiso=True, aorb=True)
                ),
            ),
            BlockMethod(d3s6=0.64, d3a1=0.3065),
        ),
    ]
)
def blocks(request) -> tuple:
    """Provide different block combinations for parameterized testing."""
    return request.param


@pytest.mark.unit
@pytest.mark.input
def test_add_blocks(empty_calc: Calculator, blocks: tuple):
    """Test for `Input.add_blocks()` with singular and multiple blocks."""
    empty_calc.input.add_blocks(*blocks)
    assert empty_calc.input.has_blocks(*blocks)


@pytest.mark.unit
@pytest.mark.input
def test_add_blocks_strict(calc: Calculator, blocks: tuple):
    """Test for `Input.add_blocks()` with `strict=True`. When `strict=True`, a `ValueError` should be raised
    if that BlockABC instance has already been added."""
    with pytest.raises(ValueError):
        calc.input.add_blocks(*blocks, strict=True)


@pytest.mark.unit
@pytest.mark.input
def test_add_blocks_overwrite(calc: Calculator):
    """Test for `Input.add_blocks()` with `overwritten=True`. When `overwritten=True`, the existing `BlockABC` instance
    should be overwritten if it exists."""
    calc.input.add_blocks(BlockMethod(d3s6=0.75), overwrite=True)

    assert calc.input.blocks["method"].d3s6 == 0.75


@pytest.mark.unit
@pytest.mark.input
@pytest.mark.parametrize(
    "blocks,expected",
    [
        ((BlockEprnmr(),), (False,)),
        ((BlockEprnmr(), BlockMethod()), (False, False)),
    ],
)
def test_remove_block(calc: Calculator, blocks: tuple, expected: tuple):
    """Test for `Input.remove_blocks()`.
    Test for singular and multiple blocks."""
    calc.input.remove_blocks(*blocks)
    assert calc.input.has_blocks(*blocks) == expected


@pytest.mark.unit
@pytest.mark.input
def test_remove_blocks_strict(calc: Calculator, empty_test_block: BlockABC):
    """Test for `Input.remove_blocks()` with `strict = True`."""
    with pytest.raises(ValueError):
        calc.input.remove_blocks(empty_test_block, strict=True)


@pytest.mark.unit
@pytest.mark.input
def test_has_block_empty_calc(empty_calc: Calculator, empty_test_block: BlockABC):
    """Test for `Input.has_blocks()` when no blocks have been added."""
    calc = empty_calc
    assert calc.input.has_blocks(empty_test_block) == (False,)


@pytest.mark.unit
@pytest.mark.input
@pytest.mark.parametrize(
    "blocks, expected",
    [
        ((BlockMethod(),), (True,)),
        ((BlockMethod(), BlockEprnmr()), (True, True)),
        ((BlockScf(),), (False,)),
    ],
)
def test_has_block(calc: Calculator, blocks: tuple, expected: tuple):
    """Test for `Input.has_blocks()` with different combinations of blocks and expected results"""
    assert calc.input.has_blocks(*blocks) == expected


@pytest.mark.unit
@pytest.mark.input
def test_get_block_empty(empty_calc: Calculator):
    """Test for `Input.get_block()` when no blocks have been added."""
    returned_block = empty_calc.input.get_blocks(BlockMethod)
    assert not returned_block


@pytest.mark.unit
@pytest.mark.input
def test_get_block(calc_with_test_block: Calculator, empty_test_block: BlockABC):
    """Test for `Input.get_blocks()`. Blocks are keyed by the name of the ORCA block."""
    type_instance = type(empty_test_block)
    assert calc_with_test_block.input.get_blocks(type_instance) == {"scf": empty_test_block}


@pytest.mark.unit
@pytest.mark.input
def test_get_blocks_create_missing(empty_calc: Calculator, empty_test_block: BlockABC):
    """Test for `Input.get_blocks()` with `create_missing=True`."""
    type_instance = type(empty_test_block)
    returned_blocks = empty_calc.input.get_blocks(type_instance, create_missing=True)
    assert "scf" in returned_blocks


@pytest.mark.unit
@pytest.mark.input
@pytest.mark.parametrize("name", ["scf", "SCF", "%scf", "  % SCF  "])
def test_normalize_block_name(name: str):
    """Test that `BlockABC.normalize_name()` normalizes the spellings of an ORCA block name."""
    assert BlockABC.normalize_name(name) == "scf"


@pytest.mark.unit
@pytest.mark.input
def test_blocks_keyed_by_name(calc: Calculator):
    """Test that blocks are stored under the name of the ORCA block they model."""
    assert list(calc.input.blocks) == ["method", "eprnmr"]


@pytest.mark.unit
@pytest.mark.input
def test_get_block_by_name(calc_with_test_block: Calculator, empty_test_block: BlockABC):
    """Test that a block can be looked up by any spelling of its ORCA block name."""
    assert calc_with_test_block.input.get_blocks("  %SCF ") == {"scf": empty_test_block}


@pytest.mark.unit
@pytest.mark.input
def test_block_abc_is_abstract():
    """Test that the abstract `BlockABC` cannot be instantiated, as it models no ORCA block.
    `ABC` alone would not prevent it, since `BlockABC` defines no abstract method."""
    with pytest.raises(TypeError):
        BlockABC()


@pytest.mark.unit
@pytest.mark.input
def test_block_abc_class_rejected(calc: Calculator):
    """Test that the abstract `BlockABC` does not identify a block when passed as a class."""
    with pytest.raises(ValueError):
        calc.input.has_blocks(BlockABC)


@pytest.mark.unit
@pytest.mark.input
def test_block_without_name(empty_calc: Calculator):
    """Test that a subclass which defines no `_name` reports so instead of failing on a
    missing private attribute."""

    class BlockWithoutName(BlockABC):
        pass

    block = BlockWithoutName()

    with pytest.raises(AttributeError, match="does not define the name of an ORCA block"):
        block.name
    with pytest.raises(AttributeError, match="does not define the name of an ORCA block"):
        empty_calc.input.add_blocks(block)


@pytest.mark.unit
@pytest.mark.input
@pytest.mark.parametrize("not_a_block", [dict, Element, 42, None, BlockScf])
def test_add_blocks_not_a_block(empty_calc: Calculator, not_a_block):
    """Test that `Input.add_blocks()` rejects anything but a block instance, block classes included."""
    with pytest.raises(TypeError):
        empty_calc.input.add_blocks(not_a_block)

    assert not empty_calc.input.blocks


@pytest.mark.unit
@pytest.mark.input
@pytest.mark.parametrize("not_a_block", [dict, Element, 42, None])
def test_blocks_not_a_block(calc: Calculator, not_a_block):
    """Test that anything but a block, a block class or a block name raises a `TypeError`.
    Since every class is an instance of `type`, unrelated classes must be rejected as well."""
    with pytest.raises(TypeError):
        calc.input.has_blocks(not_a_block)
    with pytest.raises(TypeError):
        calc.input.remove_blocks(not_a_block)
    with pytest.raises(TypeError):
        calc.input.get_blocks(not_a_block)


@pytest.mark.unit
@pytest.mark.input
def test_clear_blocks(calc: Calculator):
    """Test for `Input.clear_blocks()`."""
    calc.input.clear_blocks()
    assert not calc.input.blocks


@pytest.mark.unit
@pytest.mark.input
def test_clear_blocks_strict(empty_calc: Calculator):
    """Test for `Input.clear_blocks()` with `strict=True`."""
    with pytest.raises(ValueError):
        empty_calc.input.clear_blocks(strict=True)
