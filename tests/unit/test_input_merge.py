from pathlib import Path

import pytest

from opi.input import ArbitraryStringPos, Input
from opi.input.blocks import Block, BlockMethod, BlockScf
from opi.input.simple_keywords import BasisSet, Dft, Scf, Task

"""
This module contains tests for the merging of two `Input` objects through `Input.__or__()`,
covering each component that is merged:
- Simple keywords
- Blocks
- Arbitrary strings
- The special input variables `ncores`, `memory` and `moinp`
"""


# ---------------------------------------------------------------------------
# Simple keywords
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.input
def test_input_or_combines_simple_keywords_of_both_sides():
    """Test for `Input.__or__()`: keywords added to only one side are all present in the merge,
    in order, with those of the left-hand input first."""
    left = Input()
    left.add_simple_keywords(Dft.B3LYP)
    right = Input()
    right.add_simple_keywords(BasisSet.DEF2_TZVP, Task.SP)

    merged = left | right

    assert merged.simple_keywords == [Dft.B3LYP, BasisSet.DEF2_TZVP, Task.SP]


@pytest.mark.unit
@pytest.mark.input
def test_input_or_drops_duplicate_simple_keywords():
    """Test for `Input.__or__()`: a keyword held by both sides appears only once in the merge."""
    left = Input()
    left.add_simple_keywords(Dft.B3LYP, Scf.TIGHTSCF)
    right = Input()
    right.add_simple_keywords(Dft.B3LYP, BasisSet.DEF2_TZVP)

    merged = left | right

    assert len(merged.simple_keywords) == 3
    assert set(merged.simple_keywords) == {Dft.B3LYP, Scf.TIGHTSCF, BasisSet.DEF2_TZVP}


@pytest.mark.unit
@pytest.mark.input
def test_input_or_preserves_simple_keyword_order():
    """Test for `Input.__or__()`: the keywords keep the order in which they were added, those of
    the left-hand input first. A duplicate keeps the position of its first occurrence, so a
    keyword held by both sides stays at its left-hand position."""
    left = Input()
    left.add_simple_keywords(Task.SP, Dft.B3LYP)
    right = Input()
    right.add_simple_keywords(Scf.TIGHTSCF, Dft.B3LYP, BasisSet.DEF2_TZVP)

    merged = left | right

    assert merged.simple_keywords == [
        Task.SP,
        Dft.B3LYP,
        Scf.TIGHTSCF,
        BasisSet.DEF2_TZVP,
    ]


# ---------------------------------------------------------------------------
# Blocks
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.input
def test_input_or_keeps_block_present_only_in_self():
    """Test for `Input.__or__()`: a block that only the left operand holds is carried over."""
    left = Input()
    left.add_blocks(BlockScf(maxiter=300))
    right = Input()

    merged = left | right

    assert set(merged.blocks) == {"scf"}
    assert merged.get_block("scf").maxiter == 300


@pytest.mark.unit
@pytest.mark.input
def test_input_or_keeps_block_present_only_in_other():
    """Test for `Input.__or__()`: a block that only the right operand holds is carried over, with
    its own block class rather than as an arbitrary block."""
    left = Input()
    right = Input()
    right.add_blocks(BlockScf(maxiter=125))

    merged = left | right

    assert set(merged.blocks) == {"scf"}
    assert merged.get_block("scf").maxiter == 125
    assert isinstance(merged.get_block("scf"), BlockScf)


@pytest.mark.unit
@pytest.mark.input
def test_input_or_merges_block_held_by_both_sides():
    """Test for `Input.__or__()`: a block modelled by both sides is merged field-wise, with the
    value of the right operand taking precedence on a conflict."""
    left = Input()
    left.add_blocks(BlockScf(maxiter=300, convergence="tight"))
    right = Input()
    right.add_blocks(BlockScf(maxiter=125))

    merged = left | right

    assert merged.get_block("scf").maxiter == 125
    assert merged.get_block("scf").convergence == "tight"


@pytest.mark.unit
@pytest.mark.input
def test_input_or_keeps_disjoint_blocks_of_both_sides():
    """Test for `Input.__or__()`: blocks modelling different ORCA blocks are kept side by side."""
    left = Input()
    left.add_blocks(BlockScf(maxiter=300))
    right = Input()
    right.add_blocks(BlockMethod(d3s6=0.64))

    merged = left | right

    assert set(merged.blocks) == {"scf", "method"}
    assert merged.get_block("scf").maxiter == 300
    assert merged.get_block("method").d3s6 == 0.64


@pytest.mark.unit
@pytest.mark.input
def test_input_or_merges_arbitrary_blocks_of_the_same_name():
    """Test for `Input.__or__()`: arbitrary blocks are merged by the name they are given, combining
    the options of both sides, with the option of the right operand winning a conflict."""
    left = Input()
    left.add_blocks(Block(name="arbit", values={"first": "1", "shared": "left"}))
    right = Input()
    right.add_blocks(Block(name="arbit", values={"second": "2", "shared": "right"}))

    merged = left | right

    assert set(merged.blocks) == {"arbit"}
    assert merged.get_block("arbit").get_option("first") == "1"
    assert merged.get_block("arbit").get_option("second") == "2"
    assert merged.get_block("arbit").get_option("shared") == "right"


@pytest.mark.unit
@pytest.mark.input
def test_input_or_keeps_options_of_a_one_sided_arbitrary_block():
    """Test for `Input.__or__()`: an arbitrary block held by only one side keeps its name and its
    options through the copy, as both live on private attributes rather than pydantic fields."""
    left = Input()
    left.add_blocks(Block(name="solo", values={"only": "kept"}))
    right = Input()

    merged = left | right

    assert merged.get_block("solo").name == "solo"
    assert merged.get_block("solo").get_option("only") == "kept"


@pytest.mark.unit
@pytest.mark.input
def test_input_or_copies_a_one_sided_block():
    """Test for `Input.__or__()`: a block that only one side holds is copied into the merge, so
    that the merged input shares no block instance with either operand."""
    left = Input()
    left.add_blocks(BlockScf(maxiter=300))
    right = Input()
    right.add_blocks(BlockMethod(d3s6=0.64))

    merged = left | right

    assert merged.get_block("scf") is not left.get_block("scf")
    assert merged.get_block("method") is not right.get_block("method")
    assert merged.get_block("scf").maxiter == 300
    assert merged.get_block("method").d3s6 == 0.64


@pytest.mark.unit
@pytest.mark.input
def test_input_or_does_not_mutate_a_one_sided_block_through_the_merge():
    """Test for `Input.__or__()`: since a one-sided block is copied rather than shared, modifying
    the block of the merged input leaves the block of the operand it came from untouched."""
    left = Input()
    left.add_blocks(BlockScf(maxiter=300))
    right = Input()

    merged = left | right
    merged.get_block("scf").maxiter = 125

    assert left.get_block("scf").maxiter == 300


@pytest.mark.unit
@pytest.mark.input
def test_input_or_merged_block_is_distinct_from_both_operands():
    """Test for `Input.__or__()`: where both sides hold a block of the same name, the merge result
    is a new instance and neither operand's block is mutated."""
    left_block = BlockScf(maxiter=300)
    right_block = BlockScf(maxiter=125)
    left = Input()
    left.add_blocks(left_block)
    right = Input()
    right.add_blocks(right_block)

    merged = left | right

    assert merged.get_block("scf") is not left_block
    assert merged.get_block("scf") is not right_block
    assert left_block.maxiter == 300
    assert right_block.maxiter == 125


# ---------------------------------------------------------------------------
# Arbitrary strings
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.input
def test_input_or_concatenates_arbitrary_strings_with_self_first():
    """Test for `Input.__or__()`: the arbitrary strings of both sides are concatenated, those of
    the left operand first."""
    left = Input()
    left.add_arbitrary_string("left string")
    right = Input()
    right.add_arbitrary_string("right string")

    merged = left | right

    assert [str(string) for string in merged.arbitrary_strings] == ["left string", "right string"]


@pytest.mark.unit
@pytest.mark.input
def test_input_or_keeps_duplicate_arbitrary_strings():
    """Test for `Input.__or__()`: unlike simple keywords, arbitrary strings are not de-duplicated,
    as the same string may legitimately be needed twice."""
    left = Input()
    left.add_arbitrary_string("same string")
    right = Input()
    right.add_arbitrary_string("same string")

    merged = left | right

    assert [str(string) for string in merged.arbitrary_strings] == ["same string", "same string"]


@pytest.mark.unit
@pytest.mark.input
def test_input_or_preserves_arbitrary_string_position():
    """Test for `Input.__or__()`: an arbitrary string is carried over with its position, which is
    not part of its equality and could therefore be lost silently."""
    left = Input()
    left.add_arbitrary_string("top string", pos=ArbitraryStringPos.TOP)
    right = Input()
    right.add_arbitrary_string("bottom string", pos=ArbitraryStringPos.BOTTOM)

    merged = left | right

    positions = {str(string): string.pos for string in merged.arbitrary_strings}
    assert positions["top string"] is ArbitraryStringPos.TOP
    assert positions["bottom string"] is ArbitraryStringPos.BOTTOM


# ---------------------------------------------------------------------------
# Special input variables
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.input
def test_input_or_other_special_variables_take_precedence():
    """Test for `Input.__or__()`: where both sides set `ncores` and `memory`, the values of the
    right operand are kept."""
    left = Input()
    left.ncores = 4
    left.memory = 2000
    right = Input()
    right.ncores = 8
    right.memory = 4000

    merged = left | right

    assert merged.ncores == 8
    assert merged.memory == 4000


@pytest.mark.unit
@pytest.mark.input
def test_input_or_falls_back_to_self_special_variables():
    """Test for `Input.__or__()`: where the right operand leaves `ncores` and `memory` unset, the
    values of the left operand are kept."""
    left = Input()
    left.ncores = 4
    left.memory = 2000
    right = Input()

    merged = left | right

    assert merged.ncores == 4
    assert merged.memory == 2000


@pytest.mark.unit
@pytest.mark.input
@pytest.mark.parametrize("variable", ["ncores", "memory"])
def test_input_or_treats_zero_as_unset(variable: str):
    """Test for `Input.__or__()`: `ncores` and `memory` are carried over on truthiness, so a `0` on
    the right operand falls back to the value of the left one, as the docstring states."""
    left = Input()
    setattr(left, variable, 4)
    right = Input()
    setattr(right, variable, 0)

    merged = left | right

    assert getattr(merged, variable) == 4


@pytest.mark.unit
@pytest.mark.input
def test_input_or_moinp_of_other_takes_precedence(tmp_path: Path):
    """Test for `Input.__or__()`: `moinp` follows the same precedence as the other special input
    variables. The setter requires an existing file, hence the two temporary ones."""
    left_gbw = tmp_path / "left.gbw"
    left_gbw.touch()
    right_gbw = tmp_path / "right.gbw"
    right_gbw.touch()
    left = Input()
    left.moinp = left_gbw
    right = Input()
    right.moinp = right_gbw

    merged = left | right

    assert merged.moinp == right_gbw.resolve()


@pytest.mark.unit
@pytest.mark.input
def test_input_or_falls_back_to_self_moinp(tmp_path: Path):
    """Test for `Input.__or__()`: `moinp` of the left operand is kept when the right is unset."""
    left_gbw = tmp_path / "left.gbw"
    left_gbw.touch()
    left = Input()
    left.moinp = left_gbw
    right = Input()

    merged = left | right

    assert merged.moinp == left_gbw.resolve()


# ---------------------------------------------------------------------------
# Result and operands as a whole
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.input
def test_input_or_returns_new_instance_without_mutating_operands():
    """Test for `Input.__or__()`: the merge is returned as a new `Input` and neither operand gains
    the keywords, blocks, arbitrary strings or special variables of the other."""
    left = Input()
    left.add_simple_keywords(Dft.B3LYP)
    left.add_blocks(BlockScf(maxiter=300))
    left.add_arbitrary_string("left string")
    left.ncores = 4
    right = Input()
    right.add_simple_keywords(BasisSet.DEF2_TZVP)
    right.add_blocks(BlockMethod(d3s6=0.64))
    right.add_arbitrary_string("right string")
    right.ncores = 8

    merged = left | right

    assert merged is not left
    assert merged is not right
    assert left.simple_keywords == [Dft.B3LYP]
    assert set(left.blocks) == {"scf"}
    assert [str(string) for string in left.arbitrary_strings] == ["left string"]
    assert left.ncores == 4
    assert right.simple_keywords == [BasisSet.DEF2_TZVP]
    assert set(right.blocks) == {"method"}
    assert [str(string) for string in right.arbitrary_strings] == ["right string"]
    assert right.ncores == 8


@pytest.mark.unit
@pytest.mark.input
def test_input_or_of_two_empty_inputs_is_empty():
    """Test for `Input.__or__()`: merging two untouched inputs yields an untouched input."""
    merged = Input() | Input()

    assert merged.simple_keywords == []
    assert merged.blocks == {}
    assert merged.arbitrary_strings == []
    assert merged.ncores is None
    assert merged.memory is None
    assert merged.moinp is None


@pytest.mark.unit
@pytest.mark.input
def test_input_or_result_is_writable_to_orca_input():
    """Test for `Input.__or__()`: the merged input formats itself for the ORCA input file, carrying
    the keywords, blocks and arbitrary strings of both sides into it."""
    left = Input()
    left.add_simple_keywords(Dft.B3LYP)
    left.add_blocks(BlockScf(maxiter=300))
    right = Input()
    right.add_simple_keywords(BasisSet.DEF2_TZVP)
    right.add_blocks(Block(name="arbit", values={"opt": "7"}))
    right.add_arbitrary_string("right string")

    formatted = (left | right).format_before_coords()

    assert "b3lyp" in formatted
    assert "def2-tzvp" in formatted
    assert "maxiter 300" in formatted
    assert "%arbit" in formatted
    assert "right string" in formatted


@pytest.mark.unit
@pytest.mark.input
@pytest.mark.parametrize("other", [None, 5, "scf", BlockScf(maxiter=300)])
def test_input_or_rejects_non_input(other: object):
    """Test for `Input.__or__()`: merging with something that is not an `Input` returns
    `NotImplemented`, so that Python fails the `|` operation with a `TypeError`."""
    with pytest.raises(TypeError):
        Input() | other
