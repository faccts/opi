"""
Module that contains `BaseRunner` class which facilitates the execution of ORCA binaries.

Attributes
----------
RunnerType:
    Helper variable for type annotation.
P:
    ParamSpec helper variable.
R:
    Helper variable for type annotation.
"""

import os
import shutil
import subprocess
import warnings
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Concatenate, Final, ParamSpec, TypeVar, cast

from opi import ORCA_MINIMAL_VERSION
from opi.execution.run import run_subprocess_with_fanout
from opi.execution.text_stream import StreamTargetSpec
from opi.lib.orca_binary import OrcaBinary
from opi.utils.config import get_config
from opi.utils.misc import add_to_env, check_minimal_version, resolve_binary_name
from opi.utils.orca_version import OrcaVersion

RunnerType = TypeVar("RunnerType", bound="BaseRunner")
P = ParamSpec("P")
R = TypeVar("R")


def _orca_environment(
    runner: Callable[Concatenate[RunnerType, P], R], /
) -> Callable[Concatenate[RunnerType, P], R]:
    """
    Wrapper that temporarily modifies environment, to ensure that the correct ORCA and OpenMPI installation are found.
    Resets environment upon exiting.

    Parameters
    ----------
    runner : Callable[Concatenate[RunnerType, P], R]
        Function that is to be wrapped.
    """

    def wrapper(self: RunnerType, /, *args: Any, **kwargs: Any) -> R:
        org_env = os.environ.copy()
        try:
            # //////////////////////////////
            # > SETUP ENVIRONMENT
            # //////////////////////////////

            # > Updating necessary environmental variables.
            add_to_env("PATH", str(self._orca_bin_folder), prepend=True)
            add_to_env("LD_LIBRARY_PATH", str(self._orca_lib_folder), prepend=True)

            # > Setting Open MPI path
            if self._open_mpi_path:
                add_to_env("PATH", str(self._open_mpi_path / "bin"), prepend=True)
                add_to_env("LD_LIBRARY_PATH", str(self._open_mpi_path / "lib"), prepend=True)

            # //////////////////////////////
            # > Call Runner
            # //////////////////////////////
            return runner(self, *args, **kwargs)
        finally:
            os.environ = org_env  # type: ignore

    # << END OF INNER FUNC

    return wrapper


class _Unset(Enum):
    Value = "UNSET"


UNSET: Final = _Unset.Value


@dataclass(frozen=True)
class RunResult:
    binary: str
    args: tuple[str, ...]
    returncode: int
    stdout: str
    stderr: str

    def returncode_ok(self) -> bool:
        """Check for zero exit code"""
        return self.returncode == 0

    def check_returncode(self) -> None:
        """Raise RuntimeError exit code is non-zero."""
        if not self.returncode_ok():
            raise RuntimeError(
                f"Running '{self.binary}' with arguments {self.args} failed with exit code: {self.returncode}"
            )  # change to OpiExecutionError when PR #224 merged

    def get_signal(self) -> int | None:
        """Check and return IPC signals."""
        if self.returncode < 0:
            return abs(self.returncode)
        else:
            return None


class BaseRunner:
    """
    Base class that facilitates the execution of ORCA binaries.
    Makes sure that correct ORCA binary and MPI libraries are used.
    This class is intended to be subclassed to execute an ORCA binary.
    """

    def __init__(self, working_dir: Path | str | os.PathLike[str] | None = None) -> None:
        """
        Parameters
        ----------
        working_dir : Path | str | os.PathLike[str] | None, default = None
            Optional working directory for execution.
        """
        # > Working dir. Must exist!
        self._working_dir: Path = Path.cwd()
        self.working_dir: Path = cast(Path, working_dir)

        # //////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        # > ORCA & Open MPI Installation
        # //////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        # > Either the main ORCA folder contains a 'bin/' and a 'lib/' folder or all files are just contained in the main folder.
        self._orca_bin_folder: Path | None = None
        self._orca_lib_folder: Path | None = None
        # > Open MPI location
        # > The variable stores the path to base folder of Open MPI.
        # >> May stay `None` if Open MPI is already present in $PATH.
        self._open_mpi_path: Path | None = None

        self.set_orca_path()
        self.set_open_mpi_path()

    @property
    def working_dir(self) -> Path:
        return self._working_dir

    @working_dir.setter
    def working_dir(self, value: Path | str | os.PathLike[str] | None) -> None:
        """
        Parameters
        ----------
        value : Path | str | os.PathLike[str] | None
        """

        if value is None:
            # > Unsetting working_dir by setting it to CWD.
            # > Thereby, working_dir is never "unset".
            self._working_dir = Path.cwd()
        else:
            value = Path(value)
            if not value.is_dir():
                raise ValueError(
                    f"{self.__class__.__name__}.working_dir: {value} does is not a directory!"
                )
            # > Completely resolving path
            self._working_dir = value.expanduser().resolve()

    @_orca_environment
    def run(
        self,
        binary: OrcaBinary,
        args: Sequence[str] = (),
        /,
        *,
        stdin: str | None = None,
        stdout: StreamTargetSpec = (),
        stderr: StreamTargetSpec = (),
        cwd: Path | None = None,
        timeout: float | None = None,
        # deprecated
        stdin_str: _Unset | str | None = UNSET,
        capture: _Unset | bool = UNSET,
        silent: _Unset | bool = UNSET,
    ) -> RunResult:
        """
        Function that executes ORCA binary.

        The `stdout` and `stderr` arguments can be one or more `StreamTarget`.
        A stream target can be a file object, a path to a file to write to, a callable
        or the output can be captured into the `RunResult` using the target `subprocess.PIPE`.

        Parameters
        ----------
        binary : OrcaBinary
            Name of ORCA binary to be executed. Path is automatically resolved based on configuration.
        args : Sequence[str], default: ()
            Command line arguments to pass to ORCA binary
        stdin : str | None, default: None
            String to be passed to stdin.
        stdout : StreamTargetSpec, default: ()
            One or more target streams to pipe the subprocess `stdout` to.
        stderr : StreamTargetSpec, default: ()
            One or more target streams to pipe the subprocess `stderr` to.
        cwd : Path | None, default: None
            Set working directory for execution. Overrules `self.working_dir`.
        timeout : float | None, by default None
            Optional timeout in seconds to wait for process to complete. None or
            negative timeout denotes no timeout.
        stdin_str : _Unset | str | None, default: UNSET
            DEPRECATED, use `stdin` instead.
        capture : _Unset | bool, default: UNSET
            DEPRECATED, use `stdout`/`stderr`=`subprocess.PIPE` instead.
        silent : _Unset | bool, default: UNSET
            DEPRECATED, use `stdout`/`stderr`=`()` instead.

        Returns
        -------
        RunResult
            Completed ORCA run result.

        Raises
        ------
        ValueError
            Raised if an invalid ORCA binary is passed in.
        FileNotFound:
            Error if path to ORCA binary cannot be resolved.
        subprocess.TimeoutExpired
            Raised by `run_subprocess_with_fanout` if a timeout is set and the process
            times out.
        BaseException
            Raised by `run_subprocess_with_fanout`, after the process has finished, the
            first error accumulated from a failed write is raised.
        """

        if stdin_str is not UNSET:
            warnings.warn(
                "`stdin_str` is deprecated; use `stdin` instead.",
                DeprecationWarning,
                stacklevel=2,
            )
            stdin = stdin_str
        if capture is not UNSET:
            warnings.warn(
                "`capture` is deprecated; pass stdout=subprocess.PIPE and/or stderr=subprocess.PIPE instead.",
                DeprecationWarning,
                stacklevel=2,
            )
            # TODO: should we add `subprocess.PIPE` to `stdout` and `stderr` here?
        if silent is not UNSET:
            warnings.warn(
                "`silent` is deprecated; omit stdout/stderr for silent execution.",
                DeprecationWarning,
                stacklevel=2,
            )

        # > Get requested ORCA binary
        if not isinstance(binary, OrcaBinary):
            raise ValueError(f"`binary` must be of type OrcaBinary, not: {type(binary)}")
        orca_bin = str(self.get_orca_binary(binary))

        args = tuple(args)

        # > Assembling full call
        cmd = (orca_bin,) + args

        timeout_value = None if timeout is None or timeout < 0 else timeout

        # > Working dir
        if not cwd:
            cwd = self.working_dir

        # Run the binary
        result = run_subprocess_with_fanout(
            cmd,
            stdin=stdin,
            stdout=stdout,
            stderr=stderr,
            timeout=timeout_value,
            cwd=cwd,
        )

        return RunResult(
            binary=binary,
            args=args,
            returncode=result.returncode,
            stdout=result.stdout,
            stderr=result.stderr,
        )

    def get_version(self) -> OrcaVersion | None:
        """
        Get the ORCA version from the main ORCA binary.

        Returns
        -------
        OrcaVersion:
            Version of the ORCA.
        None:
            If the version could not be determined.
        """

        try:
            # > May raise subprocess.TimeoutExpired
            orca_proc = self.run(
                OrcaBinary.ORCA,
                ["--version"],
                stdout=subprocess.PIPE,
                timeout=5,
            )

            # > Pleasing type checker
            # assert isinstance(orca_proc, CompletedProcess)
            return OrcaVersion.from_output(orca_proc.stdout)

        except (subprocess.TimeoutExpired, ValueError, AssertionError):
            return None

    def check_version(self, *, ignore_errors: bool = False) -> bool | None:
        """
        Check if the ORCA version of the main binary is compatible with the current OPI version.
        ORCA does not include version tags in its auxiliary binaries.
        Their version is implied from the the main binary.

        Parameters
        ----------
        ignore_errors : bool, default: False
            False: Raises RuntimeError if version is not compatible or could not be determined.
            True: Return True if version is compatible, else return False. Also if the version could not be determined.

        Returns
        -------
        bool :
            True: If version is compatible.
            False: If version is not compatible.
        None :
            If version could not be determined.

        Raises
        ------
        RuntimeError: If `ignore_errors` is False and version is not compatible or could not be determined.
        """

        orca_vers = self.get_version()

        # > Path as string to ORCA binary
        try:
            orca_bin_str = f"\nORCA binary: {self.get_orca_binary(OrcaBinary.ORCA)}"
        except FileNotFoundError:
            orca_bin_str = ""

        if orca_vers is None:
            if ignore_errors:
                return None
            else:
                raise RuntimeError(
                    f"Could not determine version of ORCA binary."
                    f" Make sure ORCA is installed and configured correctly."
                    f" Minimally required ORCA version: {ORCA_MINIMAL_VERSION}{orca_bin_str}"
                )

        elif not check_minimal_version(orca_vers):
            if ignore_errors:
                return False
            else:
                raise RuntimeError(
                    f"ORCA version {orca_vers} is not supported. Make sure to install at least version:"
                    f" {ORCA_MINIMAL_VERSION}{orca_bin_str}"
                )
        else:
            return True

    @staticmethod
    def _determine_orca_paths(orca_path: Path, /) -> tuple[Path, Path]:
        """
        Determine the actual path to the folders that contains the ORCA binaries as well as the libraries.
        We allow several formats, to specify the path to ORCA.

        Parameters
        ----------
        orca_path : Path
            Can either point to:
                1) the main ORCA binary directly, which must have the name "orca".
                2) the folder which contains the main ORCA binary `orca` either `./orca` or `./bin/orca`

        Returns
        -------
        Path:
            The path to the folder that contains the ORCA binaries.
        Path:
            The path to the folder that contains the ORCA libraries.
        Both paths can coincide.
        """

        if not isinstance(orca_path, Path):
            raise TypeError(f"'orca_path' parameter is not a Path, but: {type(orca_path)}")

        # > Resolving path. This will also check if the target exists
        try:
            orca_path = orca_path.expanduser().resolve(strict=True)
        except FileNotFoundError:
            raise FileNotFoundError(f"ORCA path does not exist: {orca_path}")

        # > Case 1
        if orca_path.is_file() and orca_path.name == resolve_binary_name(OrcaBinary.ORCA):
            # > Check if the parent dir is 'bin/'
            if orca_path.parent.name == "bin":
                orca_bin_folder = orca_path.parent
                orca_lib_folder = orca_bin_folder.with_name("lib")
            else:
                orca_bin_folder = orca_path.parent
                orca_lib_folder = orca_bin_folder

        # > Case 2
        elif orca_path.is_dir():
            # > Check if the current dir contains a bin or a lib folder.
            if (orca_path / "bin").exists():
                orca_bin_folder = orca_path / "bin"
                orca_lib_folder = orca_path / "lib"
            else:
                orca_bin_folder = orca_path
                orca_lib_folder = orca_path

        # > NOT FOUND
        else:
            raise RuntimeError(f"Path to ORCA is invalid: {orca_path}")

        # > Make sure both folders exists
        assert orca_bin_folder is not None
        assert orca_lib_folder is not None
        # > Check that binary folder exists
        if not orca_bin_folder.is_dir():
            raise FileNotFoundError(
                f"The ORCA binary folder does not exists or is not a folder: {orca_bin_folder}"
            )
        # > If the bin and lib folder do not coincide, we also check the lib folder.
        if orca_bin_folder != orca_lib_folder and not orca_lib_folder.is_dir():
            raise FileNotFoundError(
                f"The ORCA library folder does not exists or is not a folder: {orca_lib_folder}"
            )

        return orca_bin_folder, orca_lib_folder

    def set_orca_path(self, orca_path: Path | None = None, /) -> None:
        """
        Determine and set the ORCA installation to be used.

        Parameters
        ----------
        orca_path : Path | None, default: None
        """

        # > Fetching OPI config. Needs to fetched first, as it might be empty or not exist.
        orca_path_config = None
        if config := get_config():
            orca_path_config = config.get("ORCA_PATH")

        # > Case 1: Path given via function parameters
        if orca_path is not None:
            if not isinstance(orca_path, Path):
                raise TypeError(f"'orca_path' parameter is not a Path, but: {type(orca_path)}")
            # << END OF IF
        # << END OF IF

        # > Case 2: $OPI_PATH
        elif opi_var_orca_path := os.environ.get("OPI_ORCA"):
            orca_path = Path(opi_var_orca_path)

        # > Case 3: Config file
        elif orca_path_config:
            orca_path = Path(orca_path_config)

        # > Case 4: $PATH
        elif var_orca_path := shutil.which("orca"):
            orca_path = Path(var_orca_path)

        # > NOT FOUND
        else:
            raise RuntimeError("Could not find ORCA.")

        # > Now determine the bin/ and lib/ folder
        self._orca_bin_folder, self._orca_lib_folder = self._determine_orca_paths(orca_path)

    def set_open_mpi_path(self, mpi_path: Path | None = None, /) -> None:
        """
        Determine and set the Open MPI installation to be used.

        Parameters
        ----------
        mpi_path : Path | None, default: None
        """

        # > Needs to fetched ahead of other check, as it might be empty or not exist.
        mpi_path_config = None
        if config := get_config():
            mpi_path_config = config.get("MPI_PATH")

        # > Case 1: Path given via function parameter
        if mpi_path is not None:
            if not isinstance(mpi_path, Path):
                raise TypeError(f"'mpi_path' parameter is not a Path, but: {type(mpi_path)}")
            # << END OF IF

        # > Case 2: $OPI_MPI
        elif opi_var_open_mpi_path := os.environ.get("OPI_MPI"):
            mpi_path = Path(opi_var_open_mpi_path)

        # > Case 3: Specified in config file
        elif mpi_path_config:
            mpi_path = Path(mpi_path_config)

        # > Case 4: MPI is already in the $PATH
        # >         Then we don't need to do anything.
        # >         Assumes that $LD_LIBRARY_PATH is also properly configured.
        # > Case 5: Not configured/installed at all.
        #           In this case, ORCA can only be executed with a single core.
        # <<< END OF IF-BLOCK

        # > Now determine the bin/ and lib/ folder
        if mpi_path:
            self._open_mpi_path = mpi_path.expanduser().resolve(strict=True)

    def get_orca_binary(self, binary: OrcaBinary, /) -> Path:
        """
        Get absolute path to any of ORCA binaries according to `self._orca_bin_path`.

        Parameters
        ----------
        binary : OrcaBinary
            Name of ORCA binary to search for.
        """

        assert self._orca_bin_folder is not None

        bin_name = resolve_binary_name(str(binary))

        # > Full path to ORCA binary
        orca_binary = self._orca_bin_folder / bin_name

        if not orca_binary.is_file():
            raise FileNotFoundError(f"The ORCA binary does not exist: {orca_binary}")
        else:
            return orca_binary
