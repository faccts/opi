import pytest

from opi.input.simple_keywords import SimpleKeyword
from opi.simple_tasks import FreqTask, SinglePointTask

"""
Unit tests for SimpleTask.from_string classmethod:
- Returns an instance of the concrete task subclass
- Keyword string parsing: splits on whitespace, strips leading ! characters
- Bypasses task_settings/method_settings (both remain unset)
"""


# ---------------------------------------------------------------------------
# Return type
# ---------------------------------------------------------------------------
@pytest.mark.unit
@pytest.mark.simpletasks
def test_from_string_returns_single_point_task() -> None:
    """SinglePointTask.from_string returns a SinglePointTask instance."""
    result = SinglePointTask.from_string("B3LYP def2-SVP SP")
    assert isinstance(result, SinglePointTask)


@pytest.mark.unit
@pytest.mark.simpletasks
def test_from_string_returns_freq_task() -> None:
    """FreqTask.from_string returns a FreqTask instance."""
    result = FreqTask.from_string("B3LYP def2-SVP FREQ")
    assert isinstance(result, FreqTask)


@pytest.mark.unit
@pytest.mark.simpletasks
def test_from_string_leaves_settings_unset() -> None:
    """from_string bypasses the typed settings system entirely."""
    result = SinglePointTask.from_string("B3LYP def2-SVP SP")
    assert result.task_settings is None
    assert result.method_settings is None


# ---------------------------------------------------------------------------
# Keyword parsing
# ---------------------------------------------------------------------------
@pytest.mark.unit
@pytest.mark.simpletasks
def test_from_string_keywords_without_exclamation() -> None:
    """Keywords without ! are parsed and added to the input correctly."""
    result = SinglePointTask.from_string("B3LYP def2-SVP")
    assert result.input.has_simple_keywords(SimpleKeyword("B3LYP"), SimpleKeyword("def2-SVP")) == (
        True,
        True,
    )


@pytest.mark.unit
@pytest.mark.simpletasks
def test_from_string_strips_exclamation_prefix() -> None:
    """Leading ! attached directly to a keyword is stripped before adding it."""
    result = SinglePointTask.from_string("!B3LYP !def2-SVP")
    assert result.input.has_simple_keywords(SimpleKeyword("B3LYP"), SimpleKeyword("def2-SVP")) == (
        True,
        True,
    )


@pytest.mark.unit
@pytest.mark.simpletasks
def test_from_string_splits_on_arbitrary_whitespace() -> None:
    """Keywords separated by repeated or mixed whitespace are still parsed individually."""
    result = SinglePointTask.from_string("B3LYP   def2-SVP\tSP")
    assert result.input.has_simple_keywords(
        SimpleKeyword("B3LYP"), SimpleKeyword("def2-SVP"), SimpleKeyword("SP")
    ) == (True, True, True)
