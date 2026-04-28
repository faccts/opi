from pathlib import Path

import pytest

from opi.execution.orca_mm import OrcaMmException, OrcaMmRunner


def _set_fake_orca_path(self, orca_path: Path | None = None) -> None:
    self._orca_bin_folder = Path("/tmp")
    self._orca_lib_folder = Path("/tmp")


def _set_fake_open_mpi_path(self, mpi_path: Path | None = None) -> None:
    self._open_mpi_path = None


@pytest.mark.unit
def test_run_orca_mm_handles_deleted_empty_stderr(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(OrcaMmRunner, "set_orca_path", _set_fake_orca_path)
    monkeypatch.setattr(OrcaMmRunner, "set_open_mpi_path", _set_fake_open_mpi_path)

    runner = OrcaMmRunner()

    def fake_run(binary, args, /, *, stderr=None, silent=True, timeout=-1):
        assert stderr is not None
        stderr.write_text("")
        stderr.unlink()
        return None

    monkeypatch.setattr(runner, "run", fake_run)

    runner.run_orca_mm("convff", ["-amber", "test.prm"])


@pytest.mark.unit
def test_run_orca_mm_raises_when_stderr_contains_output(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(OrcaMmRunner, "set_orca_path", _set_fake_orca_path)
    monkeypatch.setattr(OrcaMmRunner, "set_open_mpi_path", _set_fake_open_mpi_path)

    runner = OrcaMmRunner()

    def fake_run(binary, args, /, *, stderr=None, silent=True, timeout=-1):
        assert stderr is not None
        stderr.write_text("orca_mm failed")
        return None

    monkeypatch.setattr(runner, "run", fake_run)

    with pytest.raises(OrcaMmException, match="orca_mm failed"):
        runner.run_orca_mm("convff", ["-amber", "test.prm"])
