import pytest

from opi.core import Calculator
from opi.input.blocks import (
    Block,
    BlockABC,
    BlockEprnmr,
    BlockMethod,
    BlockScf,
    Nuclei,
    NucleiFlag,
)
from opi.utils.element import Element

"""
This module contains tests for block-related operations including:
- Addition of blocks
- Removal of blocks
- Getting of blocks
- Checking whether block exists in a `Calculator` object
- Clearing all blocks
- Merging of blocks (`Block.__or__` and the default merge-on-add behavior of `Input.add_blocks()`)
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


# ---------------------------------------------------------------------------
# `Block.__or__` (merging two `Block` instances directly)
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.input
def test_block_or_combines_disjoint_fields():
    """Test for `Block.__or__()`: fields set on only one side are both present in the merge."""
    left = BlockScf(maxiter=100)
    right = BlockScf(convergence="tight")

    merged = left | right

    assert merged.maxiter == 100
    assert merged.convergence == "tight"


@pytest.mark.unit
@pytest.mark.input
def test_block_or_other_takes_precedence_on_conflict():
    """Test for `Block.__or__()`: when both sides set the same field, `other`'s value wins."""
    left = BlockScf(maxiter=100)
    right = BlockScf(maxiter=200)

    merged = left | right

    assert merged.maxiter == 200


@pytest.mark.unit
@pytest.mark.input
def test_block_or_preserves_self_field_left_unset_by_other():
    """Test for `Block.__or__()`: a field left unset (`None`) on `other` does not clobber the
    value already present on `self`."""
    left = BlockScf(maxiter=100)
    right = BlockScf(convergence="tight")

    merged = left | right

    assert merged.maxiter == 100
    assert left.maxiter == 100


@pytest.mark.unit
@pytest.mark.input
def test_block_or_returns_new_instance_without_mutating_operands():
    """Test for `Block.__or__()`: the result is a new `Block` instance of the same type; neither
    operand is mutated."""
    left = BlockScf(maxiter=100)
    right = BlockScf(convergence="tight")

    merged = left | right

    assert isinstance(merged, BlockScf)
    assert merged is not left
    assert merged is not right
    assert left.convergence is None
    assert right.maxiter is None


@pytest.mark.unit
@pytest.mark.input
def test_block_or_nested_block_field_is_replaced_wholesale():
    """Test for `Block.__or__()`: a nested `BaseModel` field (e.g. `nuclei`) set on both sides is
    replaced wholesale by `other`'s value rather than being merged field-by-field."""
    left = BlockEprnmr(
        gtensor=1,
        nuclei=Nuclei(atom=Element.HYDROGEN, flags=NucleiFlag(adip=True, aiso=True)),
    )
    right = BlockEprnmr(nuclei=Nuclei(atom=Element.CARBON, flags=NucleiFlag(aorb=True)))

    merged = left | right

    assert merged.nuclei == right.nuclei
    assert merged.gtensor == 1  # preserved from `left`, untouched by `right`


@pytest.mark.unit
@pytest.mark.input
def test_block_or_combines_arbitrary_options():
    """Test for `Block.__or__()`: arbitrary options added via `add_option()` live on a private,
    non-model attribute, but are still carried over into the merge from both sides."""
    left = BlockScf(maxiter=100)
    left.add_option("foo", "bar")
    right = BlockScf(convergence="tight")
    right.add_option("baz", "qux")

    merged = left | right

    assert merged.get_option("foo") == "bar"
    assert merged.get_option("baz") == "qux"


@pytest.mark.unit
@pytest.mark.input
def test_block_or_other_option_takes_precedence_on_conflict():
    """Test for `Block.__or__()`: when both sides set the same arbitrary option, `other`'s value
    wins, just as it does for fields."""
    left = BlockScf()
    left.add_option("foo", "bar")
    right = BlockScf()
    right.add_option("foo", "qux")

    merged = left | right

    assert merged.get_option("foo") == "qux"


@pytest.mark.unit
@pytest.mark.input
def test_block_or_does_not_mutate_operand_options():
    """Test for `Block.__or__()`: the merged options are held by a dictionary of their own, so
    adding an option to the merged block does not leak back into either operand."""
    left = BlockScf()
    left.add_option("foo", "bar")
    right = BlockScf()

    merged = left | right
    merged.add_option("baz", "qux")

    assert not left.has_option("baz")
    assert not right.has_option("baz")


@pytest.mark.unit
@pytest.mark.input
def test_block_or_other_default_overrides_self_explicit_value():
    """Test for `Block.__or__()`: `aftercoord` has a non-`None` default (`False`), so it is always
    included by `model_dump(exclude_none=True)`. As a result, `other`'s default silently overrides
    an explicit value set on `self`, even though `other` never touched it."""
    left = BlockScf(maxiter=100, aftercoord=True)
    right = BlockScf(convergence="tight")  # aftercoord left at its default (False)

    merged = left | right

    assert merged.aftercoord is False


@pytest.mark.unit
@pytest.mark.input
@pytest.mark.parametrize(
    "left,right",
    [
        (BlockScf(maxiter=100), BlockMethod(d3s6=0.64)),
        (Block(name="arbit"), Block(name="other_arbit")),
        (BlockScf(maxiter=100), Block(name="arbit")),
    ],
    ids=["two_implemented", "two_arbitrary", "implemented_and_arbitrary"],
)
def test_block_or_rejects_blocks_of_different_names(left: BlockABC, right: BlockABC):
    """Test for `Block.__or__()`: merging blocks that model different ORCA blocks raises a
    `ValueError`, as the merged block could only carry one of the two names."""
    with pytest.raises(ValueError):
        left | right


@pytest.mark.unit
@pytest.mark.input
def test_block_or_rejects_non_block():
    """Test for `Block.__or__()`: merging with something that is not a block at all is not
    implemented, so Python raises a `TypeError` for the unsupported operand."""
    with pytest.raises(TypeError):
        BlockScf(maxiter=100) | "scf"


# ---------------------------------------------------------------------------
# `Block.__or__` (merging two arbitrary blocks, which are named at runtime)
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.input
def test_arbitrary_block_or_combines_options_of_both_sides():
    """Test for `Block.__or__()` on arbitrary blocks: an arbitrary block keeps everything it holds
    in arbitrary options, so merging two of them combines those options."""
    left = Block(name="arbit", values={"first": "1"})
    right = Block(name="arbit", values={"second": "2"})

    merged = left | right

    assert merged.get_option("first") == "1"
    assert merged.get_option("second") == "2"


@pytest.mark.unit
@pytest.mark.input
def test_arbitrary_block_or_result_is_writable_to_orca_input():
    """Test for `Block.__or__()` on arbitrary blocks: the merged block still formats itself for the
    ORCA input, carrying the options of both sides under the shared block name."""
    left = Block(name="arbit", values={"first": "1"})
    right = Block(name="arbit", values={"second": "2"})

    merged = left | right

    assert merged.format_orca() == "%arbit\n    first 1\n    second 2\nend"


@pytest.mark.unit
@pytest.mark.input
def test_add_blocks_merges_existing_arbitrary_block(empty_calc: Calculator):
    """Test for `Input.add_blocks()`: an arbitrary block added twice under the same name is merged
    like any implemented block, combining the options of both."""
    empty_calc.input.add_blocks(Block(name="arbit", values={"first": "1"}))
    empty_calc.input.add_blocks(Block(name="arbit", values={"second": "2"}))

    assert len(empty_calc.input.blocks) == 1
    merged = empty_calc.input.get_block("arbit")
    assert merged.get_option("first") == "1"
    assert merged.get_option("second") == "2"


# ---------------------------------------------------------------------------
# `Input.add_blocks()` merge-on-add default behavior
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.input
def test_add_blocks_merges_existing_block_by_default(calc: Calculator):
    """Test for `Input.add_blocks()`: adding a block of a type that is already present, without
    `strict` or `overwrite`, merges it into the existing block instead of replacing it wholesale."""
    calc.input.add_blocks(BlockMethod(d3s6=0.75))

    merged = calc.input.get_block("method")
    assert merged.d3s6 == 0.75  # new value takes precedence
    assert merged.d3a1 == 0.3065  # preserved from the previously-added block
    assert merged.d3s8 == 0.9147
    assert merged.d3a2 == 5.0570


@pytest.mark.unit
@pytest.mark.input
def test_add_blocks_merge_combines_multiple_new_blocks_of_same_type(empty_calc: Calculator):
    """Test for `Input.add_blocks()`: passing several blocks of the same type in a single call
    merges them sequentially, even when none was previously present."""
    empty_calc.input.add_blocks(BlockMethod(d3s6=0.64), BlockMethod(d3a1=0.3065))

    assert len(empty_calc.input.blocks) == 1
    merged = empty_calc.input.get_block("method")
    assert merged.d3s6 == 0.64
    assert merged.d3a1 == 0.3065


@pytest.mark.unit
@pytest.mark.input
def test_add_blocks_merge_produces_object_distinct_from_both_inputs(empty_calc: Calculator):
    """Test for `Input.add_blocks()`: the stored, merged block is a new instance rather than
    either of the two blocks that were merged."""
    first = BlockMethod(d3s6=0.64)
    second = BlockMethod(d3a1=0.3065)
    empty_calc.input.add_blocks(first, second)

    merged = empty_calc.input.get_block("method")
    assert merged is not first
    assert merged is not second


@pytest.mark.unit
@pytest.mark.input
def test_add_blocks_merge_does_not_mutate_previously_stored_block(calc: Calculator):
    """Test for `Input.add_blocks()`: merging on add replaces the stored block with a new
    instance; the block object that was stored before does not get its fields mutated in place."""
    previously_stored = calc.input.get_block("method")

    calc.input.add_blocks(BlockMethod(d3s6=0.75))

    assert previously_stored.d3s6 == 0.64
    assert calc.input.blocks["method"] is not previously_stored
