import json
import os
import platform
import shutil
import socket
import subprocess
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Any

import pytest

# > Version of the notebook summary schema. Bump when the layout changes incompatibly.
NOTEBOOK_SUMMARY_SCHEMA_VERSION = 1

# > Stash keys shared between the notebook test and the summary hook in conftest.py.
# > They live here rather than in conftest.py on purpose: pytest imports conftest.py under
# > its own module name, so importing it directly could yield a second module instance with
# > distinct -- and therefore non-matching -- key objects.
NOTEBOOK_RESULTS: "pytest.StashKey[list[NotebookResult]]" = pytest.StashKey()
NOTEBOOK_RUN_CONFIG: "pytest.StashKey[NotebookRunConfig]" = pytest.StashKey()
NOTEBOOK_RUN_START: "pytest.StashKey[tuple[float, str]]" = pytest.StashKey()


def _is_separator(line: str) -> bool:
    """Return True if the line contains only dashes, equals signs, and spaces (ORCA separator line)."""
    stripped = line.strip()
    return bool(stripped) and all(c in "-= " for c in stripped)


@dataclass(frozen=True)
class JsonFilesExporter:
    json_files_dir: Path
    prefix: str
    enabled: bool

    def export_jsons_from(
        self,
        src_dir: Path,
        *,
        recursive: bool = False,
        overwrite: bool = True,
        gbw_subdir: str = "gbw",
        property_subdir: str = "property",
    ) -> tuple[list[Path], list[Path]]:
        """
        Copy JSON files from src_dir into tests/json_files/<plain_subdir|property_subdir>.

        - plain:     *.json excluding *.property.json
        - property:  *.property.json

        Destination filenames are prefixed:
            <prefix>__<original_filename>

        Returns: (plain_dests, property_dests)
        """
        pattern = "**/*.json" if recursive else "*.json"
        sources = sorted(p for p in src_dir.glob(pattern) if p.is_file())

        plain_out = self.json_files_dir / gbw_subdir
        prop_out = self.json_files_dir / property_subdir
        plain_out.mkdir(parents=True, exist_ok=True)
        prop_out.mkdir(parents=True, exist_ok=True)

        plain_dests: list[Path] = []
        prop_dests: list[Path] = []

        for src in sources:
            name = src.name

            is_property = name.endswith(".property.json")
            if is_property:
                dst = prop_out / f"{self.prefix}_{name}"
                prop_dests.append(dst)
            else:
                # it's a .json from the glob, but not a .property.json
                dst = plain_out / f"{self.prefix}_{name}"
                plain_dests.append(dst)

            if not self.enabled:
                continue

            if dst.exists() and not overwrite:
                raise FileExistsError(f"JSON file exists (overwrite disabled): {dst}")

            shutil.copy2(src, dst)

        if self.enabled and not (plain_dests or prop_dests):
            raise FileNotFoundError(f"No JSON files found in {src_dir} (pattern={pattern!r})")

        return plain_dests, prop_dests


@dataclass(frozen=True)
class OutFileExporter:
    out_file: Path
    enabled: bool

    @staticmethod
    def _extract_orca_blocks(src: Path) -> str:
        """
        Extract only the `Grepper`-relevant blocks from a full ORCA .out file.

        Strips all system-specific info (paths, hostnames, timings) and keeps only:
          - Total Charge / Multiplicity lines (once each)
          - Each CARTESIAN COORDINATES (ANGSTROEM) block
          - Each FINAL SINGLE POINT ENERGY line (with surrounding separator lines)
          - Each CARTESIAN GRADIENT block
        """
        result: list[str] = []
        charge_done = False
        mult_done = False
        prev_line = ""

        with src.open() as f:
            it = (raw.rstrip("\n") for raw in f)
            # pending holds the already-fetched next line, giving one line of lookahead
            pending: str | None = next(it, None)

            while pending is not None:
                line = pending
                pending = next(it, None)

                # Charge line (emit once)
                if (
                    not charge_done
                    and "Total Charge" in line
                    and "Charge" in line
                    and "...." in line
                ):
                    result.append(line)
                    charge_done = True
                    prev_line = line
                    continue

                # Mult line (emit once)
                if not mult_done and "Multiplicity" in line and "Mult" in line and "...." in line:
                    result.append(line)
                    mult_done = True
                    prev_line = line
                    continue

                # CARTESIAN COORDINATES block
                if "CARTESIAN COORDINATES (ANGSTROEM)" in line:
                    result.append("")
                    if _is_separator(prev_line):
                        result.append(prev_line)
                    result.append(line)
                    if pending is not None:
                        result.append(pending)  # separator after header
                        pending = next(it, None)
                    while pending is not None and pending.strip():
                        result.append(pending)
                        pending = next(it, None)
                    result.append("")
                    continue

                # FINAL SINGLE POINT ENERGY line (with surrounding separators)
                if "FINAL SINGLE POINT ENERGY" in line:
                    result.append("")
                    if _is_separator(prev_line):
                        result.append(prev_line)
                    result.append(line)
                    if pending is not None and _is_separator(pending):
                        result.append(pending)
                        prev_line = pending
                        pending = next(it, None)
                    else:
                        prev_line = line
                    result.append("")
                    continue

                # CARTESIAN GRADIENT block (match exact header, not "CARTESIAN GRADIENT NORMS")
                if line.strip() == "CARTESIAN GRADIENT":
                    result.append("")
                    if _is_separator(prev_line):
                        result.append(prev_line)
                    result.append(line)
                    if pending is not None:
                        result.append(pending)  # separator after header
                        pending = next(it, None)
                    if pending is not None:
                        result.append(pending)  # blank line between separator and data
                        pending = next(it, None)
                    while pending is not None and pending.strip():
                        result.append(pending)
                        pending = next(it, None)
                    result.append("")
                    continue

                prev_line = line

        # Collapse consecutive blank lines into one
        cleaned: list[str] = []
        prev_blank = False
        for ln in result:
            if not ln.strip():
                if not prev_blank:
                    cleaned.append(ln)
                prev_blank = True
            else:
                cleaned.append(ln)
                prev_blank = False

        return "\n".join(cleaned).rstrip() + "\n"

    def export_from(self, src: Path) -> None:
        """Extract grepper-relevant blocks from src and write to self.out_file."""
        if not self.enabled:
            return
        content = self._extract_orca_blocks(src)
        self.out_file.write_text(content)


@dataclass
class NotebookResult:
    """
    Outcome of executing a single documentation notebook.

    One instance is created per parametrized notebook test and collected into the
    pytest config stash, from where `write_notebook_summary` serialises it.
    """

    name: str
    path: str
    started_at: str
    workdir: str
    # > "passed" | "failed" | "timeout" | "skipped" | "error"
    status: str = "error"
    returncode: int | None = None
    duration_s: float | None = None
    error_kind: str | None = None
    error_message: str | None = None
    log_tail: str | None = None
    artifacts: str | None = None


@dataclass
class NotebookRunConfig:
    """Notebook-run settings recorded in the summary so a result can be reproduced."""

    notebooks_dir: str
    skipped: list[str] = field(default_factory=list)
    cell_timeout_s: int = 0
    notebook_timeout_s: int = 0
    artifacts_dir: str | None = None


def _git(rootpath: Path, *args: str) -> str | None:
    """
    Run a read-only `git` command in `rootpath` and return its stripped stdout.

    Returns
    -------
    str | None
        The command output, or None if git is unavailable or the command failed.
    """
    try:
        proc = subprocess.run(
            ["git", "-C", str(rootpath), *args],
            capture_output=True,
            text=True,
            timeout=15,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if proc.returncode != 0:
        return None
    return proc.stdout.strip()


def _package_version(name: str) -> str | None:
    """Return the installed version of `name`, or None if it is not installed."""
    try:
        return version(name)
    except PackageNotFoundError:
        return None


def _orca_version() -> str | None:
    """
    Return the ORCA version string, or None if ORCA cannot be reached.

    Deliberately broad in what it swallows: a missing or broken ORCA must never
    prevent the summary file from being written, since the summary is the only
    channel through which an unattended run reports anything at all.
    """
    try:
        from opi.execution.core import Runner

        orca_version = Runner().get_version()
    except Exception:
        return None
    return str(orca_version) if orca_version is not None else None


def collect_run_metadata(rootpath: Path) -> dict[str, Any]:
    """
    Gather run-level provenance for the notebook summary.

    Parameters
    ----------
    rootpath : Path
        Repository root, used for the `git` queries.

    Returns
    -------
    dict[str, Any]
        Nested mapping with `git`, `slurm` and `versions` sections.
    """
    dirty = _git(rootpath, "status", "--porcelain")
    return {
        "hostname": socket.gethostname(),
        "user": os.environ.get("USER") or os.environ.get("LOGNAME"),
        "git": {
            "commit": _git(rootpath, "rev-parse", "HEAD"),
            "branch": _git(rootpath, "rev-parse", "--abbrev-ref", "HEAD"),
            "describe": _git(rootpath, "describe", "--tags", "--always"),
            # > None (git unavailable) is not the same as "clean"; keep it distinguishable.
            "dirty": None if dirty is None else bool(dirty),
        },
        "slurm": {
            "job_id": os.environ.get("SLURM_JOB_ID"),
            "array_job_id": os.environ.get("SLURM_ARRAY_JOB_ID"),
            "array_task_id": os.environ.get("SLURM_ARRAY_TASK_ID"),
            "partition": os.environ.get("SLURM_JOB_PARTITION"),
            "nodelist": os.environ.get("SLURM_JOB_NODELIST"),
            "cpus_per_task": os.environ.get("SLURM_CPUS_PER_TASK"),
        },
        "versions": {
            "python": platform.python_version(),
            "opi": _package_version("orca-pi"),
            "orca": _orca_version(),
            "nbconvert": _package_version("nbconvert"),
        },
    }


def write_notebook_summary(
    path: Path,
    results: list[NotebookResult],
    *,
    rootpath: Path,
    run_config: NotebookRunConfig,
    exit_status: int,
    started_monotonic: float,
    started_at: str,
) -> None:
    """
    Write the machine-readable notebook summary to `path`, atomically.

    The file is written to a sibling temporary file and then `os.replace`d into
    position, so a concurrent reader never observes a half-written summary. This
    matters because the canonical summary is overwritten in place on every run.

    Parameters
    ----------
    path : Path
        Destination of the summary file.
    results : list[NotebookResult]
        One entry per notebook that was collected.
    rootpath : Path
        Repository root, forwarded to `collect_run_metadata`.
    run_config : NotebookRunConfig
        Settings the run was executed with.
    exit_status : int
        pytest's session exit status.
    started_monotonic : float
        `time.monotonic()` captured at session start, used for the wall time.
    started_at : str
        ISO-8601 timestamp captured at session start.
    """
    counts = {"total": len(results)}
    for status in ("passed", "failed", "timeout", "skipped", "error"):
        counts[status] = sum(1 for r in results if r.status == status)

    summary: dict[str, Any] = {
        "schema_version": NOTEBOOK_SUMMARY_SCHEMA_VERSION,
        "status": "completed",
        "run": {
            "started_at": started_at,
            "finished_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "wall_time_s": round(time.monotonic() - started_monotonic, 1),
            "exit_status": exit_status,
            **collect_run_metadata(rootpath),
            "config": asdict(run_config),
            "totals": counts,
        },
        "notebooks": [asdict(r) for r in results],
    }

    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(summary, indent=2, sort_keys=False) + "\n")
    os.replace(tmp, path)
