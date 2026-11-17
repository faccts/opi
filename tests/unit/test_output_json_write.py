import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest

from opi.execution.core import Runner
from opi.output.models.json.gbw.gbw_results import GbwResults
from opi.output.models.json.property.property_results import PropertyResults
from opi.output.models.json_loadable import JSONLoadable

"""
Tests for dumping results back into JSON data and for writing a gbw file from `GbwResults`.

The unit tests only check the dumped JSON data against the committed JSON fixtures, while the
actual conversion into a gbw file requires ORCA and is therefore not part of the CI.
"""

# > Fixture of a calculation that contains molecular orbitals
GBW_JSON = "gbw/test_exmp003_opt_job.json"
PROPERTY_JSON = "property/test_exmp003_opt_job.property.json"


def collect_keys(obj: Any, keys: set[str], /) -> set[str]:
    """Recursively collect all keys of a JSON tree."""
    if isinstance(obj, dict):
        for key, value in obj.items():
            keys.add(key)
            collect_keys(value, keys)
    elif isinstance(obj, list):
        for item in obj:
            collect_keys(item, keys)
    return keys


@pytest.mark.unit
@pytest.mark.output
def test_to_json_uses_orca_keys(json_dir: Path) -> None:
    """The dumped JSON data must use the key spelling of the JSON file written by ORCA."""
    for json_file in sorted(json_dir.glob("gbw/*.json")):
        orca_keys = collect_keys(json.loads(json_file.read_text()), set())
        dumped_keys = collect_keys(GbwResults.from_json_file(json_file).to_json(), set())

        assert dumped_keys, f"nothing was dumped for {json_file.name}"
        assert not dumped_keys - orca_keys, (
            f"keys of {json_file.name} are not spelled like in the file written by ORCA"
        )


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    ("results_class", "json_name"), [(GbwResults, GBW_JSON), (PropertyResults, PROPERTY_JSON)]
)
def test_to_json_file(
    json_dir: Path,
    tmp_path: Path,
    results_class: type[JSONLoadable],
    json_name: str,
) -> None:
    """The written JSON file must be readable again."""
    results = results_class.from_json_file(json_dir / json_name)
    json_file = results.to_json_file(tmp_path / "job.json")

    assert json_file.is_file()
    assert results_class.from_json_file(json_file) == results


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize(
    ("drop_data", "match"),
    [
        (lambda r: setattr(r, "molecule", None), "no molecule"),
        (lambda r: setattr(r.molecule, "hftyp", None), "HF type"),
        (lambda r: setattr(r.molecule, "atoms", None), "no atoms"),
        (lambda r: setattr(r.molecule.atoms[0], "basis", None), "basis set"),
        (lambda r: setattr(r.molecule, "molecularorbitals", None), "no molecular orbitals"),
        (
            lambda r: setattr(r.molecule.molecularorbitals.mos[0], "mocoefficients", None),
            "MO coefficients",
        ),
    ],
)
def test_to_gbw_file_incomplete_results(
    json_dir: Path,
    tmp_path: Path,
    drop_data: Callable[[GbwResults], None],
    match: str,
) -> None:
    """Data that `orca_2json` requires to create a gbw file must be checked upfront."""
    results = GbwResults.from_json_file(json_dir / GBW_JSON)
    drop_data(results)

    with pytest.raises(ValueError, match=match):
        results.to_gbw_file(tmp_path / "job.gbw")


@pytest.mark.unit
@pytest.mark.output
def test_to_gbw_file_invalid_target(json_dir: Path, tmp_path: Path) -> None:
    """The path of the gbw file must point to a file in an existing folder."""
    results = GbwResults.from_json_file(json_dir / GBW_JSON)

    with pytest.raises(IsADirectoryError):
        results.to_gbw_file(tmp_path)
    with pytest.raises(FileNotFoundError):
        results.to_gbw_file(tmp_path / "missing" / "job.gbw")


@pytest.mark.orca
@pytest.mark.output
def test_to_gbw_file(json_dir: Path, tmp_path: Path) -> None:
    """The gbw file written by `orca_2json` must hold the molecular orbitals of the results."""
    results = GbwResults.from_json_file(json_dir / GBW_JSON)
    # > `orca_2json` is run in a folder other than the current working directory
    gbw_file = results.to_gbw_file(tmp_path / "job.gbw")

    assert gbw_file.is_file()
    # > Neither the temporary folder nor the intermediate JSON file may be left behind
    assert [file.name for file in tmp_path.iterdir()] == [gbw_file.name]

    # > Convert the gbw file back into a gbw-JSON file and compare the molecular orbitals
    Runner(working_dir=tmp_path).run_orca_2json([gbw_file.name]).check_returncode()
    reparsed = GbwResults.from_json_file(gbw_file.with_suffix(".json"))

    assert reparsed.molecule is not None
    assert results.molecule is not None
    assert reparsed.molecule.molecularorbitals == results.molecule.molecularorbitals
