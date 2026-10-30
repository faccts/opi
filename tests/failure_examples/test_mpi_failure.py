#!/usr/bin/env python3
"""
Tests for error extraction capabilities from ORCA output files of parallel calculations in which
an MPI process is killed, e.g. by the out-of-memory killer of the operating system.
The kill is simulated by sending SIGKILL to one of the MPI processes of the calculation.
Only processes started by this test are ever signaled, so other jobs on the machine are safe.
"""

import os
import re
import signal
import threading
from pathlib import Path

import pytest

from opi.core import Calculator
from opi.input.simple_keywords import BasisSet, Method
from opi.input.structures import Structure

NCORES = 4


def _descendants(root: int) -> set[int]:
    """Return the PIDs of all processes below `root`, found via the parent PIDs in /proc."""
    parents: dict[int, int] = {}
    for entry in Path("/proc").iterdir():
        if not entry.name.isdigit():
            continue
        try:
            stat = (entry / "stat").read_text()
        except OSError:
            continue
        # > The parent PID is the second field after the command name, which may contain spaces.
        parents[int(entry.name)] = int(stat.rsplit(")", 1)[1].split()[1])
    found: set[int] = set()
    frontier = {root}
    while frontier:
        children = {pid for pid, ppid in parents.items() if ppid in frontier}
        frontier = children - found
        found |= children
    return found


def _mpi_ranks() -> list[int]:
    """Return the PIDs of the ORCA MPI processes started by this test process."""
    ranks = []
    for pid in _descendants(os.getpid()):
        try:
            argv0 = Path(f"/proc/{pid}/cmdline").read_bytes().split(b"\0")[0]
        except OSError:
            continue
        name = os.path.basename(argv0.decode(errors="replace"))
        if name.startswith("orca_") and name.endswith("_mpi"):
            ranks.append(pid)
    return sorted(ranks)


@pytest.mark.orca
@pytest.mark.skipif(not Path("/proc/self/stat").is_file(), reason="requires Linux /proc")
def test_mpi_rank_killed(tmp_path):
    """Test error_messages for an MPI process of the calculation that was killed by signal 9."""
    calc = Calculator(basename="job", working_dir=tmp_path)
    # > Usually a process of the first parallel module is killed. The molecule is large enough
    # > that the calculation is still running if the killer misses that module.
    calc.structure = Structure.from_smiles("c1ccc2ccccc2c1")
    calc.input.ncores = NCORES
    calc.input.add_simple_keywords(Method.HF, BasisSet.DEF2_TZVP)

    killed: list[int] = []
    done = threading.Event()

    def kill_one_rank() -> None:
        while not done.wait(0.2):
            ranks = _mpi_ranks()
            if len(ranks) == NCORES:
                os.kill(ranks[-1], signal.SIGKILL)
                killed.append(ranks[-1])
                return

    killer = threading.Thread(target=kill_one_rank)
    killer.start()
    try:
        # > write the input and run the calculation
        calc.write_and_run(timeout=600)
    finally:
        done.set()
        killer.join()
    assert killed, "The calculation finished before an MPI process could be killed"

    # > get the output and check some results
    output = calc.get_output()
    assert not output.terminated_normally()
    messages = output.error_messages()
    # > The failing ORCA module is reported first, the killed process as its cause after it
    assert messages[0].startswith("Error in ")
    # > The rank of the killed process is not known, as PIDs do not follow the ranks
    assert re.match(r"MPI process rank \d+ was terminated by signal 9 \(Killed\)", messages[-1])
