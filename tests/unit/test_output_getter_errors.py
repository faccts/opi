"""
Unit tests for the errors raised by the `Output` getters.

The getters return None if a value is not in the output, but raise if they are used incorrectly:
- `OpiOutputNotParsedError` if the JSON files were not parsed
- `OpiOutputIndexError` if the requested geometry or gbw index does not exist
- `TypeError` if the requested geometry or gbw index is not an integer
"""

import shutil
from pathlib import Path

import numpy as np
import pytest

from opi.exceptions import OpiOutputIndexError, OpiOutputNotParsedError
from opi.output.core import Output

FALLBACK_OUT = Path(__file__).parents[1] / "fixtures" / "job_fallback.out"

# > Lines as written by ORCA
_COORDINATES = (
    "CARTESIAN COORDINATES (ANGSTROEM)\n---------------------------------\n  H  0.0  0.0  0.0\n\n"
)
_S2 = "Expectation value of <S**2>     :     {}\nIdeal value S*(S+1) for S=0.5   :     0.750000\n"


@pytest.mark.unit
@pytest.mark.output
def test_not_parsed_error_points_to_parse(empty_output_object: Output):
    """Test that the error for unparsed output tells the user to call `Output.parse()`."""
    with pytest.raises(OpiOutputNotParsedError, match=r"Output\.parse\(\)"):
        empty_output_object.get_dipole()


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("task", ["led"])
def test_not_parsed_error_for_gbw_results_only(output_object_factory, task: str):
    """Test that only gbw getters raise if just the gbw JSON was not parsed."""
    output_object = output_object_factory(task)
    output_object.results_gbw = None
    with pytest.raises(OpiOutputNotParsedError, match="read_gbw_json"):
        output_object.get_mos()
    assert output_object.get_dipole() is not None


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("task", ["led"])
def test_index_error_for_gbw_index(output_object_factory, task: str):
    """
    Test that gbw indices work within range (also negative ones) and raise `OpiOutputIndexError`
    outside of it, which includes that no gbw results were found.
    """
    output_object = output_object_factory(task)
    n_gbw = len(output_object.results_gbw)
    assert output_object.get_mos(gbw_index=-n_gbw) == output_object.get_mos(gbw_index=0)
    for gbw_index in (n_gbw, -n_gbw - 1):
        with pytest.raises(OpiOutputIndexError, match="gbw results"):
            output_object.get_mos(gbw_index=gbw_index)
    output_object.results_gbw = []
    with pytest.raises(OpiOutputIndexError, match="0 gbw results"):
        output_object.get_mos()
    with pytest.raises(OpiOutputIndexError, match="0 gbw results"):
        output_object.get_int_overlap()


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("task", ["led"])
def test_index_error_for_negative_index(output_object_factory, task: str):
    """Test that negative indices work within range and raise `OpiOutputIndexError` outside of it."""
    output_object = output_object_factory(task)
    n_geometries = len(output_object.results_properties.geometries)
    assert output_object.get_dipole(index=-n_geometries) is not None
    with pytest.raises(OpiOutputIndexError, match="geometries"):
        output_object.get_dipole(index=-n_geometries - 1)


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("task", ["led"])
@pytest.mark.parametrize("getter", ["get_final_energy", "get_structure", "get_gradient"])
def test_index_error_for_fallback_getters(
    output_object_factory, tmp_path: Path, task: str, getter: str
):
    """
    Test that an index out of range for the JSON geometries raises, even if the `.out` file
    contains more blocks (e.g. from a final evaluation) that the fallback would find.
    """
    output_object = output_object_factory(task)
    shutil.copy(FALLBACK_OUT, tmp_path / f"{output_object.basename}.out")
    output_object.working_dir = tmp_path
    n_geometries = len(output_object.results_properties.geometries)
    # > The `.out` file has a value for this index, the JSON output does not
    assert FALLBACK_OUT.read_text().count("FINAL SINGLE POINT ENERGY") > n_geometries
    with pytest.raises(OpiOutputIndexError, match="geometries"):
        getattr(output_object, getter)(index=n_geometries)


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("task", ["led"])
def test_empty_geometry_list_returns_none(output_object_factory, task: str):
    """
    Test that an output without geometries returns None instead of raising.
    ORCA writes an empty geometry list to the property JSON for e.g. GFN-FF.
    """
    output_object = output_object_factory(task)
    output_object.results_properties.geometries = []
    assert output_object.get_dipole() is None


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("getter", ["get_final_energy", "get_structure", "get_gradient"])
def test_index_error_in_fallback_file(output_no_json: Output, getter: str):
    """Test that an index out of range of the blocks in the `.out` file raises for unparsed output."""
    assert getattr(output_no_json, getter)(index=0) is not None
    with pytest.raises(OpiOutputIndexError, match="output file"):
        getattr(output_no_json, getter)(index=10**6)


@pytest.mark.unit
@pytest.mark.output
def test_missing_block_in_fallback_file_returns_none(output_no_json: Output):
    """Test that a value whose block is missing from an existing `.out` file returns None."""
    assert "Expectation value of <S**2>" not in FALLBACK_OUT.read_text()
    assert output_no_json.get_s2(index=0) == (None, None)


@pytest.mark.unit
@pytest.mark.output
def test_fallback_for_aborted_optimization(output_no_json: Output):
    """
    Test that the final geometry of an aborted optimization, whose energy was not calculated
    anymore, gets the last calculated energy, but no gradient.
    """
    outfile = output_no_json.get_outfile()
    energy = output_no_json.get_final_energy()
    outfile.write_text(outfile.read_text() + _COORDINATES)
    assert output_no_json.get_final_energy() == energy
    assert output_no_json.get_gradient() is None


@pytest.mark.unit
@pytest.mark.output
def test_fallback_file_values_belong_to_their_geometry(output_no_json: Output):
    """
    Test that the `.out` file fallback reads the values of the requested geometry. ORCA does not
    calculate a gradient for the final geometry of an optimization, so the last gradient block
    belongs to the second to last geometry.
    """
    text = FALLBACK_OUT.read_text()
    assert text.count("CARTESIAN GRADIENT") == text.count("CARTESIAN COORDINATES (ANGSTROEM)") - 1
    assert output_no_json.get_gradient(index=-1) is None
    assert output_no_json.get_gradient(index=-2) is not None


@pytest.fixture
def output_opt_with_out(output_object_factory, tmp_path: Path) -> Output:
    """
    Parsed output of the geometry optimization together with its `.out` file. The `.out` file
    fixture is extracted from the same calculation as the JSON fixture.
    """
    output_object = output_object_factory("opt")
    shutil.copy(FALLBACK_OUT, tmp_path / f"{output_object.basename}.out")
    output_object.working_dir = tmp_path
    return output_object


@pytest.mark.unit
@pytest.mark.output
def test_fallback_for_values_missing_from_json(output_opt_with_out: Output):
    """
    Test that values missing from the property JSON (e.g. the gradients of an ExtOpt run) are
    taken from the section of the `.out` file that belongs to the requested geometry. ORCA does not
    calculate a gradient for the final geometry of an optimization, so the last gradient block of
    the `.out` file belongs to the second to last geometry.
    """
    geometries = output_opt_with_out.results_properties.geometries
    gradients = [output_opt_with_out.get_gradient(index=i) for i in range(len(geometries))]
    assert gradients[-1] is None
    for geometry in geometries:
        geometry.nuclear_gradient = None
    assert output_opt_with_out.get_gradient(index=0, fallback=False) is None
    for index, gradient in enumerate(gradients):
        fallback_gradient = output_opt_with_out.get_gradient(index=index)
        if gradient is None:
            assert fallback_gradient is None
        else:
            assert fallback_gradient == pytest.approx(gradient, abs=1e-8)


@pytest.mark.unit
@pytest.mark.output
def test_fallback_if_geometries_do_not_match(output_opt_with_out: Output):
    """
    Test that only the final geometry is assigned to the last section of the `.out` file if the
    number of geometries differs from the property JSON, as the other sections cannot be assigned.
    """
    text = FALLBACK_OUT.read_text()
    # > Drop the first geometry from the `.out` file
    first_geometry = text.index("CARTESIAN COORDINATES (ANGSTROEM)")
    second_geometry = text.index("CARTESIAN COORDINATES (ANGSTROEM)", first_geometry + 1)
    output_opt_with_out.get_outfile().write_text(text[second_geometry:])
    geometries = output_opt_with_out.results_properties.geometries
    final_energy = geometries[-1].single_point_data.finalenergy
    for geometry in geometries:
        geometry.single_point_data = None
    assert output_opt_with_out.get_final_energy(index=0) is None
    assert output_opt_with_out.get_final_energy(index=-1) == pytest.approx(final_energy, abs=1e-11)
    assert output_opt_with_out.get_final_energy(
        index=len(geometries) - 1
    ) == output_opt_with_out.get_final_energy(index=-1)


@pytest.mark.unit
@pytest.mark.output
def test_fallback_without_geometries_in_out_file(output_opt_with_out: Output, tmp_path: Path):
    """
    Test the `.out` file fallback for an output without "CARTESIAN COORDINATES (ANGSTROEM)"
    blocks (e.g. for some xTB jobs): without property JSON, the index counts the values, with
    property JSON only the final geometry gets the last value.
    """
    energies = "FINAL SINGLE POINT ENERGY       -1.5\nFINAL SINGLE POINT ENERGY       -2.5\n"
    (tmp_path / "job.out").write_text(energies)
    output = Output("job", working_dir=tmp_path, version_check=False)
    assert output.get_final_energy(index=0) == -1.5
    assert output.get_final_energy(index=-1) == -2.5
    with pytest.raises(OpiOutputIndexError, match="2 values"):
        output.get_final_energy(index=2)

    output_opt_with_out.get_outfile().write_text(energies)
    for geometry in output_opt_with_out.results_properties.geometries:
        geometry.single_point_data = None
    assert output_opt_with_out.get_final_energy(index=0) is None
    assert output_opt_with_out.get_final_energy(index=-1) == -2.5


@pytest.mark.unit
@pytest.mark.output
def test_json_is_authoritative(output_opt_with_out: Output, output_no_json: Output):
    """
    Test that values in the property JSON are preferred over the `.out` file. The property JSON
    holds the energies with more digits than the `.out` file, so they are only equal to the JSON
    values if those were used.
    """
    geometries = output_opt_with_out.results_properties.geometries
    for index, geometry in enumerate(geometries):
        energy = output_opt_with_out.get_final_energy(index=index)
        energy_from_out = output_no_json.get_final_energy(index=index)
        assert energy == geometry.single_point_data.finalenergy
        assert energy == pytest.approx(energy_from_out, abs=1e-11)
        assert energy != energy_from_out


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("task", ["opt"])
def test_numpy_integer_index(output_object_factory, task: str):
    """Test that numpy integers (e.g. from `numpy.argmin()`) are accepted as index."""
    output_object = output_object_factory(task)
    energies = output_object.get_energies(index=0)
    assert energies is not None
    assert output_object.get_energies(index=np.int64(0)) == energies
    assert output_object.get_final_energy(index=np.int64(0)) == output_object.get_final_energy(
        index=0
    )
    with pytest.raises(OpiOutputIndexError):
        output_object.get_energies(index=np.int64(len(output_object.results_properties.geometries)))


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("index", [0.0, "0", None, np.bool_(True)])
def test_type_error_for_non_integer_index(
    output_object_factory, output_no_json: Output, empty_output_object: Output, index
):
    """
    Test that an index that is not an integer raises a `TypeError` instead of returning None,
    also if the output is not parsed.
    """
    output_object = output_object_factory("opt")
    getters = [
        lambda: output_object.get_energies(index=index),
        lambda: output_object.get_final_energy(index=index),
        lambda: output_object.get_mos(gbw_index=index),
        lambda: output_no_json.get_final_energy(index=index),
        lambda: output_no_json.get_s2(index=index),
        lambda: empty_output_object.get_dipole(index=index),
    ]
    for getter in getters:
        with pytest.raises(TypeError, match="integer"):
            getter()


@pytest.mark.unit
@pytest.mark.output
def test_get_s2_per_geometry(tmp_path: Path):
    """
    Test that `get_s2()` returns the S² of the requested geometry and raises
    `OpiOutputIndexError` for an index out of range of the geometries in the `.out` file.
    """
    (tmp_path / "job.out").write_text(
        _COORDINATES + _COORDINATES + _S2.format("0.758102") + _COORDINATES + _S2.format("0.753000")
    )
    output = Output("job", version_check=False)
    output.working_dir = tmp_path
    assert output.get_s2(index=0) == (None, None)
    assert output.get_s2(index=1) == (0.758102, 0.75)
    assert output.get_s2(index=-1) == (0.753, 0.75)
    with pytest.raises(OpiOutputIndexError, match="output file"):
        output.get_s2(index=3)


@pytest.mark.unit
@pytest.mark.output
def test_not_parsed_error_in_get_s2(empty_output_object: Output):
    """Test that `get_s2()` raises `OpiOutputNotParsedError` without parsed output and `.out` file."""
    with pytest.raises(OpiOutputNotParsedError):
        empty_output_object.get_s2()


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("task", ["opt"])
def test_index_error_in_get_s2_for_rhf(output_object_factory, tmp_path: Path, task: str):
    """
    Test that `get_s2()` checks the index for RHF as well, against the `.out` file if the property
    JSON is unavailable.
    """
    output_object = output_object_factory(task)
    output_object.results_properties = None
    shutil.copy(FALLBACK_OUT, tmp_path / f"{output_object.basename}.out")
    output_object.working_dir = tmp_path
    assert output_object.get_s2(index=-1) == (0.0, 0.0)
    with pytest.raises(OpiOutputIndexError, match="output file"):
        output_object.get_s2(index=10**6)


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("task", ["led"])
def test_recreate_gbw_results_with_negative_index(
    output_object_factory, monkeypatch: pytest.MonkeyPatch, task: str
):
    """Test that `recreate_gbw_results()` reloads the gbw results for a negative index."""
    output_object = output_object_factory(task)
    # > Recreating the gbw JSON needs ORCA, the existing file is reloaded instead
    monkeypatch.setattr(output_object, "create_gbw_json", lambda **_: None)
    old_results = output_object.results_gbw[-1]
    output_object.recreate_gbw_results({}, -1)
    assert output_object.results_gbw[-1] is not old_results
    assert output_object.results_gbw[-1] == old_results


def _output_with_unreadable_gbw_file(source: Path, tmp_path: Path, unreadable: int) -> Output:
    """
    Output whose three gbw JSON files are copies of `source`, except for the one at index
    `unreadable`, which contains invalid JSON.
    """
    gbw_json_files = [tmp_path / f"job.{i}.json" for i in range(3)]
    for i, gbw_json_file in enumerate(gbw_json_files):
        if i == unreadable % len(gbw_json_files):
            gbw_json_file.write_text("invalid JSON")
        else:
            shutil.copy(source, gbw_json_file)
    output = Output("job", working_dir=tmp_path, version_check=False)
    output.gbw_json_files = gbw_json_files
    with pytest.warns(UserWarning, match="Could not read JSON file"):
        output.parse_gbw(do_create_gbw_json=False)
    return output


@pytest.mark.unit
@pytest.mark.output
def test_missing_gbw_json_file_without_warning(tmp_path: Path, recwarn: pytest.WarningsRecorder):
    """
    Test that a missing gbw JSON file is represented by None without a warning, as ORCA cannot
    create it for some methods (e.g. GFN-FF).
    """
    output = Output("job", working_dir=tmp_path, version_check=False)
    output.gbw_json_files = [tmp_path / "job.json"]
    output.parse_gbw(do_create_gbw_json=False)
    assert output.results_gbw == [None]
    assert not [w for w in recwarn if "Could not read JSON file" in str(w.message)]


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("task", ["led"])
def test_unreadable_gbw_file_keeps_indices(output_object_factory, tmp_path: Path, task: str):
    """
    Test that a gbw JSON file that cannot be read is represented by None, so that the gbw
    indices still refer to the files in `gbw_json_files`.
    """
    source = output_object_factory(task).gbw_json_files[0]
    output = _output_with_unreadable_gbw_file(source, tmp_path, 1)
    assert len(output.results_gbw) == len(output.gbw_json_files)
    assert output.results_gbw[1] is None
    assert output.get_mos(gbw_index=1) is None
    assert output.get_mos(gbw_index=2) is not None
    with pytest.raises(OpiOutputIndexError, match="3 gbw results"):
        output.get_mos(gbw_index=3)


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("task", ["led"])
def test_recreate_gbw_results_for_unreadable_file(
    output_object_factory, monkeypatch: pytest.MonkeyPatch, tmp_path: Path, task: str
):
    """
    Test that `recreate_gbw_results()` with a negative index fills in the results of the gbw JSON
    file that could not be read before, without touching the others.
    """
    source = output_object_factory(task).gbw_json_files[0]
    output = _output_with_unreadable_gbw_file(source, tmp_path, -1)
    first_results = output.results_gbw[0]
    # > Recreating the gbw JSON needs ORCA, the file is copied instead
    monkeypatch.setattr(
        output, "create_gbw_json", lambda **_: shutil.copy(source, output.gbw_json_files[-1])
    )
    output.recreate_gbw_results({}, -1)
    assert output.results_gbw[-1] is not None
    assert output.results_gbw[0] is first_results
