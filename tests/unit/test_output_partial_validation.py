import warnings

import pytest
from pydantic import ValidationError

from opi.output.models.json.property.properties.calc_info import CalcInfo
from opi.output.models.json.property.property_results import PropertyResults


class TestPartialValidation:
    """Validation failures in individual fields should not abort the whole model."""

    @pytest.mark.unit
    @pytest.mark.output
    def test_strict_true_raises(self) -> None:
        """With strict=True (default), a bad field raises ValidationError."""
        with pytest.raises(ValidationError):
            CalcInfo.model_validate({"charge": "not-an-int", "mult": 1}, context={"strict": True})

    @pytest.mark.unit
    @pytest.mark.output
    def test_strict_false_drops_field(self) -> None:
        """With strict=False, a bad field becomes None and a UserWarning is emitted."""
        # > Catch the user warning from the validation fallback
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            result = CalcInfo.model_validate(
                {"charge": "not-an-int", "mult": 1}, context={"strict": False}
            )

        assert result.charge is None
        assert result.mult == 1
        # > Check if the discarded field `charge` is in the warning message
        assert any("charge" in str(w.message) for w in caught)

    @pytest.mark.unit
    @pytest.mark.output
    def test_valid_fields_unaffected(self) -> None:
        """Fields that pass validation are still populated normally."""
        result = CalcInfo.model_validate({"charge": 0, "mult": 1, "numofatoms": 3})
        assert result.charge == 0
        assert result.mult == 1
        assert result.numofatoms == 3

    @pytest.mark.unit
    @pytest.mark.output
    def test_nested_invalid_field_becomes_none(self) -> None:
        """Validation failure in a nested model only drops the failing field there."""
        # > Catch the user warning from the validation fallback
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            result = PropertyResults.model_validate(
                {"calculation_info": {"charge": "bad", "mult": 1}},
                context={"strict": False},
            )

        assert result.calculation_info is not None
        assert result.calculation_info.charge is None
        assert result.calculation_info.mult == 1
        # > Check if the discarded field `charge` is in the warning message
        assert any("charge" in str(w.message) for w in caught)
