import pytest

from opi.core import Calculator
from opi.input.simple_keywords import (
    BasisSet,
    Dft,
    LibXC,
    Method,
    Opt,
    ORCAKeyword,
    Scf,
    SimpleKeyword,
)
from opi.input.simple_keywords.scf import ScfSolver, ScfThreshold

"""
This module contains tests for simple keyword related operations such as:
- Add `ORCAKeyword` to `Calculator` object
- Clear all `ORCAKeyword` objects
- Getting `ORCAKeyword` object
- Checking whether `Calculator` object has a specific `ORCAKeyword` object
"""


@pytest.fixture()
def empty_calc() -> Calculator:
    """An empty instance of `Calculator`."""
    new_calc = Calculator("test", version_check=False)
    return new_calc


@pytest.fixture()
def calc():
    """An instance of `Calculator` with simple keywords."""
    calc = Calculator("test", version_check=False)
    calc.input.add_simple_keywords(Method.HF, BasisSet.DEF2_SVP, ORCAKeyword("ex"))
    return calc


@pytest.fixture(
    params=[
        (Method.HF,),
        (Method.HF, BasisSet.DEF2_SVP),
        (ORCAKeyword("ex"),),
    ]
)
def keywords(request) -> tuple:
    """Provide different keyword combinations for parameterized testing."""
    return request.param


@pytest.fixture()
def calc_with_keywords(keywords) -> Calculator:
    """An instance of `Calculator` with the above keywords."""
    new_calc = Calculator("test", version_check=False)
    new_calc.input.add_simple_keywords(*keywords)
    return new_calc


@pytest.mark.unit
@pytest.mark.input
def test_add_simple_keyword(calc_with_keywords: Calculator, keywords: tuple):
    """
    Test to add simple keywords to an empty `Calculator` object.
    """
    assert calc_with_keywords.input.has_simple_keywords(*keywords)


@pytest.mark.unit
@pytest.mark.input
def test_add_simple_keywords_strict(calc_with_keywords: Calculator, keywords: tuple):
    """Test addition of keywords with `strict=True`. When `strict=True`, a `ValueError` should be raised
    if keywords have already been added."""
    with pytest.raises(ValueError):
        calc_with_keywords.input.add_simple_keywords(keywords[0], strict=True)


@pytest.mark.unit
@pytest.mark.input
def test_clear_simple_keywords(calc: Calculator):
    """Test for `Input.clear_simple_keywords()`."""
    calc.input.clear_simple_keywords()
    assert not calc.input.simple_keywords


@pytest.mark.unit
@pytest.mark.input
def test_clear_simple_keywords_strict(empty_calc: Calculator):
    """Test for `Input.clear_simple_keywords()` with `strict=True`. When `strict=True`, a `ValueError` should be
    raised if there are no keywords to be removed."""
    with pytest.raises(ValueError):
        empty_calc.input.clear_simple_keywords(strict=True)


@pytest.mark.unit
@pytest.mark.input
def test_get_keywords(calc: Calculator, keywords: tuple):
    """Test for `Input.get_simple_keywords()`.
    Tests for both regular and string keywords."""
    returned_keywords = calc.input.get_simple_keywords(*keywords)
    for keyword in keywords:
        assert keyword in returned_keywords


@pytest.mark.unit
@pytest.mark.input
@pytest.mark.parametrize("keywords", [("ex",), ("hf",)])
def test_get_keyword_with_string(calc: Calculator, keywords: tuple):
    """Tests `Input.get_simple_keywords()` with a string.
    Tests for both regular and string keywords."""
    returned_keywords = calc.input.get_simple_keywords(*keywords)
    for keyword in keywords:
        assert ORCAKeyword(keyword) in returned_keywords


@pytest.mark.unit
@pytest.mark.input
def test_get_keyword_create_missing(empty_calc: Calculator, keywords: tuple):
    """Test `Input.get_simple_keywords()` with `create_missing=True`. When `create_missing=True`, the missing keyword
    gets created and added to simple keywords."""
    returned_keywords = empty_calc.input.get_simple_keywords(*keywords, create_missing=True)
    assert keywords[0] in returned_keywords


@pytest.mark.unit
@pytest.mark.input
def test_get_nonexistent_keyword(empty_calc: Calculator, keywords: tuple):
    """Test `Input.get_simple_keywords()` with a not yet added keyword."""
    returned_keywords = empty_calc.input.get_simple_keywords(*keywords)
    assert not returned_keywords


@pytest.mark.unit
@pytest.mark.input
@pytest.mark.parametrize(
    "keywords_tuple",
    [
        pytest.param(((Method.HF,), (True,)), id="method_hf"),
        pytest.param(((Method.HF_3C,), (False,)), id="method_hf3c_missing"),
        pytest.param(((Method.HF_3C, BasisSet.DEF2_SVP), (False, True)), id="combo_hf3c_sv"),
        pytest.param((("hf", "ex"), (True, True)), id="strings_hf_ex"),
    ],
)
def test_has_simple_keyword(calc: Calculator, keywords_tuple: tuple):
    """Test `Input.has_simple_keywords()` with different combinations of keywords and expected values."""
    keyword, result = keywords_tuple
    assert calc.input.has_simple_keywords(*keyword) == result


@pytest.mark.unit
@pytest.mark.input
@pytest.mark.parametrize(
    "left,right",
    [
        pytest.param("TightSCF", "tightscf", id="mixed_vs_lower"),
        pytest.param("PBE", "pbe", id="upper_vs_lower"),
        pytest.param("Def2-SVP", "DEF2-svp", id="mixed_vs_mixed"),
    ],
)
def test_simple_keyword_eq_is_case_insensitive(left: str, right: str):
    """Test that two `ORCAKeyword` objects that only differ in case compare equal and hash
    equally, matching `ORCAKeyword.format_orca()`, which lowercases the keyword."""
    assert ORCAKeyword(left) == ORCAKeyword(right)
    assert hash(ORCAKeyword(left)) == hash(ORCAKeyword(right))


@pytest.mark.unit
@pytest.mark.input
def test_add_simple_keywords_drops_case_insensitive_duplicate(empty_calc: Calculator):
    """Test `Input.add_simple_keywords()`: a keyword that only differs in case from an already
    added one is a duplicate and is dropped, keeping the spelling of the first occurrence."""
    empty_calc.input.add_simple_keywords("TightSCF")
    empty_calc.input.add_simple_keywords("tightscf", "TIGHTSCF")

    assert empty_calc.input.simple_keywords == [ORCAKeyword("TightSCF")]
    assert empty_calc.input.simple_keywords[0].keyword == "TightSCF"


@pytest.mark.unit
@pytest.mark.input
def test_add_simple_keywords_strict_raises_on_case_insensitive_duplicate(
    empty_calc: Calculator,
):
    """Test `Input.add_simple_keywords()` with `strict=True`: a keyword that only differs in case
    from an already added one raises a `ValueError`."""
    empty_calc.input.add_simple_keywords("TightSCF")

    with pytest.raises(ValueError):
        empty_calc.input.add_simple_keywords("tightscf", strict=True)


@pytest.mark.unit
@pytest.mark.input
def test_remove_simple_keywords_is_case_insensitive(empty_calc: Calculator):
    """Test `Input.remove_simple_keywords()`: a keyword added in mixed case can be removed
    through any other case spelling."""
    empty_calc.input.add_simple_keywords("TightSCF")
    empty_calc.input.remove_simple_keywords("TIGHTSCF")

    assert empty_calc.input.simple_keywords == []


@pytest.mark.unit
@pytest.mark.input
def test_simple_keyword_holds_all_groups():
    """Test that `SimpleKeyword` exposes the members of the individual keyword groups."""
    assert SimpleKeyword.HF is Method.HF
    assert SimpleKeyword.DEF2_SVP is BasisSet.DEF2_SVP
    assert SimpleKeyword.TIGHTSCF is Scf.TIGHTSCF
    assert SimpleKeyword.TIGHTOPT is Opt.TIGHTOPT


@pytest.mark.unit
@pytest.mark.input
def test_simple_keyword_excludes_libxc():
    """Test that `SimpleKeyword` resolves clashing names to `Dft` and not to `LibXC`."""
    assert SimpleKeyword.B3LYP.keyword == "b3lyp"
    assert SimpleKeyword.find_keyword("b3lyp") is SimpleKeyword.B3LYP
    with pytest.raises(ValueError):
        SimpleKeyword.find_keyword(LibXC.B3LYP)


@pytest.mark.unit
@pytest.mark.input
@pytest.mark.parametrize("query", ["def2-svp", "DEF2_SVP", ORCAKeyword("def2-svp")])
def test_simple_keyword_find_keyword(query):
    """Test that `SimpleKeyword.find_keyword()` resolves keyword strings, attribute names and `ORCAKeyword` objects."""
    assert SimpleKeyword.find_keyword(query) is BasisSet.DEF2_SVP


@pytest.mark.unit
@pytest.mark.input
def test_simple_keyword_creates_orca_keyword():
    """Test that calling `SimpleKeyword` creates an `ORCAKeyword` for ad-hoc keywords."""
    keyword = SimpleKeyword("ex", alias="example")

    assert type(keyword) is ORCAKeyword
    assert keyword == ORCAKeyword("ex")
    assert keyword.alias == ["example"]


@pytest.mark.unit
@pytest.mark.input
def test_find_keyword_ambiguous_alias():
    """Test that an alias shared by several keywords raises a `ValueError`, while a group in which
    the alias is unique still resolves it."""
    with pytest.raises(ValueError, match="ambiguous"):
        SimpleKeyword.find_keyword("tight")

    assert ScfThreshold.find_keyword("tight") is Scf.TIGHTSCF
    assert Opt.find_keyword("tight") is Opt.TIGHTOPT


@pytest.mark.unit
@pytest.mark.input
@pytest.mark.parametrize(
    "group, query",
    [(ScfThreshold, "tight"), (ScfThreshold, Scf.TIGHTSCF), (Scf, "TIGHTSCF")],
)
def test_validate_keyword(group, query):
    """Test that `SimpleKeywordBox.validate_keyword()` returns the matching keyword of the group."""
    assert group.validate_keyword(query) is Scf.TIGHTSCF


@pytest.mark.unit
@pytest.mark.input
@pytest.mark.parametrize(
    "group, query",
    [(ScfSolver, Scf.TIGHTSCF), (Opt, "tightscf"), (Dft, "foo"), (ScfThreshold, 3)],
)
def test_validate_keyword_raises(group, query):
    """Test that `SimpleKeywordBox.validate_keyword()` raises a `ValueError` for keywords that are
    not part of the group and for inputs that are neither a str nor an `ORCAKeyword`."""
    with pytest.raises(ValueError):
        group.validate_keyword(query)
