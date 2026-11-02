from pathlib import Path

import pytest

from opi.output.core import Output

"""
Unit tests for Output cleanup functions.

This module contains tests for the file-deletion helpers:
- `Output.cleanup_files()`
- `Output.cleanup_temp_files()`
- `Output._delete_files()`
"""


def _make_output(basename: str, working_dir: Path) -> Output:
    output = Output(basename, working_dir=working_dir, version_check=False)
    return output


def _create_file(directory: Path, *names: str) -> None:
    for name in names:
        (directory / name).touch()


@pytest.mark.unit
@pytest.mark.output
def test_cleanup_files_deletes_matching_basename_files(tmp_path: Path):
    """`cleanup_files()` deletes all files matching the basename, including files whose
    name only contains the basename as a prefix, and leaves unrelated files untouched."""
    _create_file(tmp_path, "job.out", "job.gbw", "job_1.gbw", "unrelated.txt")
    output = _make_output("job", tmp_path)

    output.cleanup_files()

    remaining = {p.name for p in tmp_path.iterdir()}
    assert remaining == {"unrelated.txt"}


@pytest.mark.unit
@pytest.mark.output
def test_cleanup_files_explicit_basename_overrides_self_basename(tmp_path: Path):
    """`cleanup_files(basename=...)` deletes files for the given basename, not `self.basename`."""
    _create_file(tmp_path, "job_1.out", "job_2.out")
    output = _make_output("job_1", tmp_path)

    output.cleanup_files(basename="job_2")

    remaining = {p.name for p in tmp_path.iterdir()}
    assert remaining == {"job_1.out"}


@pytest.mark.unit
@pytest.mark.output
def test_cleanup_files_raises_without_basename(tmp_path: Path):
    """`cleanup_files()` raises `ValueError` rather than deleting everything in `working_dir`."""
    _create_file(tmp_path, "unrelated.txt")
    output = _make_output("", tmp_path)

    with pytest.raises(ValueError, match="No basename specified"):
        output.cleanup_files()

    assert (tmp_path / "unrelated.txt").exists()


@pytest.mark.unit
@pytest.mark.output
@pytest.mark.parametrize("basename", ["../secret", "sub/job", "/secret"])
def test_cleanup_files_rejects_path_separators_in_basename(tmp_path: Path, basename: str):
    """A basename containing a path separator, or that is itself an absolute path, must be
    rejected rather than letting the glob pattern escape `working_dir`.
    """
    working_dir = tmp_path / "workdir"
    working_dir.mkdir()
    _create_file(tmp_path, "secret_file.txt")
    output = _make_output(basename, working_dir)

    with pytest.raises(ValueError, match="path separators"):
        output.cleanup_files()

    assert (tmp_path / "secret_file.txt").exists()


@pytest.mark.unit
@pytest.mark.output
def test_cleanup_temp_files_deletes_only_temp_suffixes(tmp_path: Path):
    """`cleanup_temp_files()` only deletes `.tmp.*`/`.proc.*` files, not other job files."""
    _create_file(tmp_path, "job.out", "job.gbw", "job.tmp", "job.proc", "job_scan.tmp")
    output = _make_output("job", tmp_path)

    output.cleanup_temp_files()

    remaining = {p.name for p in tmp_path.iterdir()}
    assert remaining == {"job.out", "job.gbw"}


@pytest.mark.unit
@pytest.mark.output
def test_delete_files_empty_suffixes_deletes_all(tmp_path: Path):
    """An empty `suffixes` sequence behaves like no filter at all: all files matching
    the basename are deleted, same as omitting `suffixes`."""
    _create_file(tmp_path, "job.out", "job.gbw", "unrelated.txt")
    output = _make_output("job", tmp_path)

    output._delete_files(None, suffixes=())

    remaining = {p.name for p in tmp_path.iterdir()}
    assert remaining == {"unrelated.txt"}
