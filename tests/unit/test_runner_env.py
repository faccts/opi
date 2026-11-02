from __future__ import annotations

import os
import subprocess
import sys
import textwrap
import threading
from pathlib import Path

import pytest

from opi.execution.base import BaseRunner
from opi.execution.run import run_subprocess_with_fanout
from opi.lib.orca_binary import OrcaBinary


@pytest.fixture
def no_config(monkeypatch: pytest.MonkeyPatch):
    """Ignore any local OPI config file, so that only the fake ORCA installation is picked up."""
    monkeypatch.setattr("opi.execution.base.get_config", lambda: None)
    monkeypatch.delenv("OPI_MPI", raising=False)


def _make_fake_orca(root: Path, /) -> Path:
    """
    Create a fake ORCA installation whose `orca` binary prints its own `$PATH`.

    Parameters
    ----------
    root : Path
        Folder in which the fake `bin/` and `lib/` folders are created.
    """
    bin_folder = root / "bin"
    bin_folder.mkdir(parents=True)
    (root / "lib").mkdir()

    orca = bin_folder / "orca"
    orca.write_text(
        textwrap.dedent(
            f"""\
            #!{sys.executable}
            import os
            print(os.environ.get("PATH", ""))
            """
        )
    )
    orca.chmod(0o755)

    return root


@pytest.mark.unit
def test_subprocess_fanout_env():
    """Test that the environment passed to the subprocess is used by the child."""
    result = run_subprocess_with_fanout(
        [sys.executable, "-c", "import os; print(os.environ['OPI_TEST_VAR'])"],
        stdout=subprocess.PIPE,
        env={**os.environ, "OPI_TEST_VAR": "42"},
    )

    assert result.returncode == 0
    assert result.stdout == "42\n"
    # > The environment of the current process must not have been touched.
    assert "OPI_TEST_VAR" not in os.environ


@pytest.mark.unit
def test_runner_build_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, no_config: None):
    """Test that the ORCA installation is prepended to the runner environment only."""
    orca_root = _make_fake_orca(tmp_path / "orca")
    monkeypatch.setenv("OPI_ORCA", str(orca_root))

    runner = BaseRunner(working_dir=tmp_path)
    org_env = os.environ.copy()

    env = runner._build_env()

    assert env["PATH"].split(os.pathsep)[0] == str(orca_root / "bin")
    assert env["LD_LIBRARY_PATH"].split(os.pathsep)[0] == str(orca_root / "lib")
    # > Building the environment must not modify the environment of the current process.
    assert os.environ == org_env


@pytest.mark.unit
@pytest.mark.skipif(sys.platform == "win32", reason="Fake ORCA binary requires a shebang.")
def test_runner_env_isolated_across_threads(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, no_config: None
):
    """
    Test that concurrent runners do not interfere via the environment of the current process.

    Modifying `os.environ` in-place reallocates the environment of the whole process, which
    makes the `fork()`/`exec()` of a subprocess spawned by another thread fail sporadically
    with `OSError: [Errno 14] Bad address`. Each runner must therefore hand its own
    environment to its subprocess and leave `os.environ` alone.
    """
    n_runners = 8

    runners = []
    for i in range(n_runners):
        orca_root = _make_fake_orca(tmp_path / f"orca_{i}")
        monkeypatch.setenv("OPI_ORCA", str(orca_root))
        runners.append(BaseRunner(working_dir=tmp_path))

    org_env = os.environ.copy()
    child_paths: dict[int, str] = {}
    barrier = threading.Barrier(n_runners)

    def run(index: int, /) -> None:
        # > Make sure that all threads spawn their subprocess at the same time.
        barrier.wait()
        result = runners[index].run(OrcaBinary.ORCA, stdout=subprocess.PIPE)
        child_paths[index] = result.stdout.strip()

    threads = [threading.Thread(target=run, args=(i,)) for i in range(n_runners)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert len(child_paths) == n_runners
    # > Every child must have seen the ORCA installation of its own runner.
    for i, path in child_paths.items():
        assert path.split(os.pathsep)[0] == str(tmp_path / f"orca_{i}" / "bin")
    # > No run may have leaked into the environment of the current process.
    assert os.environ == org_env
