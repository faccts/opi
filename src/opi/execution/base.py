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
from contextlib import nullcontext
from io import TextIOWrapper
from pathlib import Path
from subprocess import CompletedProcess
from typing import Any, Callable, Concatenate, ParamSpec, Sequence, TypeVar, cast

from opi import ORCA_MINIMAL_VERSION
from opi.lib.orca_binary import OrcaBinary
from opi.utils.config import get_config
from opi.utils.misc import add_to_env, check_minimal_version, delete_empty_file, resolve_binary_name
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
        stdin_str: str | None = None,
        stdout: Path | None = None,
        stderr: Path | None = None,
        silent: bool = True,
        capture: bool = False,
        cwd: Path | None = None,
        timeout: int = -1,
    ) -> subprocess.CompletedProcess[str] | None:
        """
        Function that executes ORCA binary.

        Parameters
        ----------
        binary : OrcaBinary
            Name of ORCA binary to be executed. Path is automatically resolved based on configuration.
        args : Sequence[str], default: ()
            Command line arguments to pass to ORCA binary.
        stdin_str: str | None = None
            String to be passed to stdin.
        stdout : Path | None, default: None
            Dump STDOUT to a file.
        stderr : Path | None, default: None
            Dump STDERR to a file.
        silent : bool, default: True
            Redirect STDOUT and STDERR to null-device.
            Is overruled respectively by `stdout` and `stderr` and `capture`.
        capture : bool, default: False
            Capture STDOUT and STDERR and return with `CompletedProcess[str]` object.
            Is overruled respectively by `stdout` and `stderr`.
        cwd : Path | None, default: None
            Set working directory for execution. Overrules `self.working_dir`.
        timeout : int, default: -1
            Optional timeout in seconds to wait for process to complete.

        Returns
        -------
        subprocess.subprocess.CompletedProcess[str] | None:
            Completed ORCA process.

        Raises
        ------
        FileNotFound:
          Error if path to ORCA binary cannot be resolved.
        subprocess.TimeoutExpired:
            If `timeout>-1` and the process times out.
        """

        # ------------------------------------------------------------
        def determine_dump(source: Path | None = None) -> TextIOWrapper:
            """
            Determine where to dump `source` to.

            Parameters
            ----------
            source : Path | None, default: None
            """

            if source:
                return source.open("w")
            elif capture:
                return cast(TextIOWrapper, nullcontext(subprocess.PIPE))
            elif silent:
                return Path(os.devnull).open("w")
            else:
                return cast(TextIOWrapper, nullcontext())

        # ------------------------------------------------------------

        if not isinstance(binary, OrcaBinary):
            raise ValueError(f"`binary` must be of type OrcaBinary, not: {type(binary)}")

        # > Working dir
        if not cwd:
            cwd = self.working_dir

        # > Get requested ORCA binary
        orca_bin = self.get_orca_binary(binary)

        # > STDOUT and STDERR capturing/dumping
        outfile = determine_dump(stdout)
        errfile = determine_dump(stderr)

        # > Assembling full call
        cmd = [str(orca_bin)]
        if args:
            cmd += list(args)

        # Run the binary
        proc = None
        try:
            with outfile as f_out, errfile as f_err:
                proc = subprocess.run(
                    cmd,
                    input=stdin_str,
                    stdout=f_out,
                    stderr=f_err,
                    cwd=cwd,
                    text=True,
                    timeout=timeout if timeout > 0 else None,
                )
            return proc
        except subprocess.TimeoutExpired:
            raise
        finally:
            # > Delete empty STDOUT and STDERR dumps
            if stdout:
                delete_empty_file(stdout)
            if stderr:
                delete_empty_file(stderr)

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
            orca_proc = self.run(OrcaBinary.ORCA, ["--version"], capture=True, timeout=5)

            # > Pleasing type checker
            assert isinstance(orca_proc, CompletedProcess)
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
