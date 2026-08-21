"""
Module that contains `OrcaMmRunner` class which facilitates execution of `orca_mm`.

Attributes
----------
OrcaMmCommand:
    Helper type for supported `orca_mm` commands.
ForcefieldType:
    Helper type for supported forcefield input formats used by `-convff`.
ChargeOption:
    Helper type for supported charge calculation options used by `-makeff`.
"""

import subprocess
from contextlib import contextmanager
from pathlib import Path
from typing import Iterable, Iterator, Literal, Sequence

from opi.exceptions import OrcaMmError
from opi.execution.base import BaseRunner, RunResult
from opi.execution.text_stream import StreamTargetSpec, concatentate_stream_targets
from opi.lib.orca_binary import OrcaBinary

OrcaMmCommand = Literal[
    "convff", "splitff", "mergeff", "repeatff", "splitpdb", "mergepdb", "makeff", "getHDist"
]
ForcefieldType = Literal["amber", "charmm", "openmm"]

ChargeOption = Literal[
    "PBE",
    "PBEOpt",
    "PBEOptH",
    "XTB",
    "XTBOpt",
    "XTBOptH",
    "XTBOptPBE",
    "noChargeCalc",
]


def _add_infix_to_path(path: Path, infix: str, suffix: str) -> Path:
    """
    Return a path with `infix` inserted while preserving the given `suffix`.

    Unlike `Path.suffix`, `suffix` is treated as a literal ending and may contain
    multiple dot-separated components, such as `.ORCAFF.prms`.

    Parameters
    ----------
    path : Path
        Source file path.
    infix : str
        String inserted before `suffix` in the filename.
    suffix : str
        Suffix of file path to preserve.

    Returns
    -------
    Path
        Updated path in the same directory.

    Examples
    --------
    >>> path = Path("system.ORCAFF.prms")
    >>> _add_infix_to_path(path, "_merged", ".ORCAFF.prms") == Path(
    ...     "system_merged.ORCAFF.prms"
    ... )
    True
    """

    return path.parent / f"{path.name.removesuffix(suffix)}{infix}{suffix}"


class OrcaMmRunner(BaseRunner):
    """
    This class should be used to execute `orca_mm` commands.

    All command-specific methods delegate to `run_orca_mm`.
    The following methods wrap the supported `orca_mm` commands:
    - `run_convff` (`orca_mm -convff`)
    - `run_splitff` (`orca_mm -splitff`)
    - `run_mergeff` (`orca_mm -mergeff`)
    - `run_repeatff` (`orca_mm -repeatff`)
    - `run_splitpdb` (`orca_mm -splitpdb`)
    - `run_mergepdb` (`orca_mm -mergepdb`)
    - `run_makeff` (`orca_mm -makeff`)
    - `run_get_h_dist` (`orca_mm -getHDist`)

    Each command-specific method follows the same execution pattern: validate its
    command options, derive the expected output paths, assemble the command-line
    arguments, execute `orca_mm`, and verify that the expected files were generated.
    """

    _orca_ff_suffix = ".ORCAFF.prms"

    @staticmethod
    def _assert_files_exist(*files: Path) -> None:
        """
        Validate that all supplied paths point to existing files.

        Parameters
        ----------
        *files : Path
            Input file paths to validate.

        Raises
        ------
        FileNotFoundError
            If one or more paths do not point to existing files.
        """
        missing_files = [path for path in files if not path.is_file()]
        if not missing_files:
            return

        formatted_files = ", ".join(f"'{path}'" for path in missing_files)
        raise FileNotFoundError(f"Input file(s) do not exist: {formatted_files}.")

    @staticmethod
    @contextmanager
    def _expect_output_files(*expected_outputs: Path) -> Iterator[None]:
        """
        Context manager that checks expected output files after command execution.

        Parameters
        ----------
        *expected_outputs : Path
            Output files that must exist after the wrapped command has finished successfully.

        Raises
        ------
        FileNotFoundError
            If one or more expected output files do not exist after execution.
        """
        try:
            yield
        except Exception:
            raise

        missing_outputs = [path for path in expected_outputs if not path.exists()]
        if len(missing_outputs) == 0:
            return

        formatted_outputs = ", ".join(f"'{path}'" for path in missing_outputs)
        raise FileNotFoundError(f"Expected output file(s) do not exist: {formatted_outputs}.")

    def run_orca_mm(
        self,
        command: OrcaMmCommand,
        args: Sequence[str],
        *,
        stdout: StreamTargetSpec = (),
        stderr: StreamTargetSpec = (),
        cwd: Path | None = None,
        timeout: float | None = None,
        raise_on_error: bool = True,
    ) -> RunResult:
        """
        Execute `orca_mm` with the provided subcommand and arguments.

        Parameters
        ----------
        command : OrcaMmCommand
            `orca_mm` subcommand to execute.
        args : Sequence[str]
            Command-line arguments passed to the subcommand.
        stdout : StreamTargetSpec, default: ()
            One or more target streams to pipe the subprocess STDOUT to.
        stderr : StreamTargetSpec, default: ()
            One or more target streams to pipe the subprocess STDERR to.
        cwd : Path | None, default: None
            Working directory for execution. Overrides `self.working_dir` when provided.
        timeout : float | None, by default None
            Optional timeout in seconds to wait for the process to complete.
        raise_on_error : bool, default: True
            Raise `OrcaMmError` if `orca_mm` exits with a nonzero return code.

        Returns
        -------
        RunResult
            Completed `orca_mm` run result.

        Raises
        ------
        OrcaMmError
            If `raise_on_error` is set and `orca_mm` exits with a nonzero return code.
        """

        # > Capture STDERR when it may be needed to construct an `OrcaMmError`.
        if raise_on_error:
            stderr = concatentate_stream_targets(
                stderr,
                subprocess.PIPE,
            )

        # > Delegate binary execution and stream handling to `BaseRunner`.
        result = self.run(
            OrcaBinary.ORCA_MM,
            (f"-{command}", *args),
            stdout=stdout,
            stderr=stderr,
            cwd=cwd,
            timeout=timeout,
        )

        # > Raise `OrcaMmError` on unsuccessful `orca_mm` execution.
        if raise_on_error and not result.returncode_ok():
            raise OrcaMmError(command, args, result.stderr)

        return result

    def _run_orca_mm_and_expect(
        self,
        command: OrcaMmCommand,
        args: Sequence[str],
        expected_outputs: Path | Sequence[Path],
        *,
        stdout: StreamTargetSpec = (),
        stderr: StreamTargetSpec = (),
        timeout: float | None = None,
        raise_on_error: bool = True,
    ) -> RunResult:
        """
        Execute an `orca_mm` command and verify that its expected outputs were generated.

        Parameters
        ----------
        command : OrcaMmCommand
            `orca_mm` subcommand to execute.
        args : Sequence[str]
            Command-line arguments passed to the subcommand.
        expected_outputs : Path | Sequence[Path]
            Output file path or paths that must exist after successful execution.
        stdout : StreamTargetSpec, default: ()
            One or more target streams to pipe the subprocess STDOUT to.
        stderr : StreamTargetSpec, default: ()
            One or more target streams to pipe the subprocess STDERR to.
        timeout : float | None, default: None
            Optional timeout in seconds to wait for the process to complete.
        raise_on_error : bool, default: True
            Raise `OrcaMmError` if `orca_mm` exits with a nonzero return code.

        Returns
        -------
        RunResult
            Completed `orca_mm` run result.

        Raises
        ------
        OrcaMmError
            If `raise_on_error` is set and `orca_mm` exits with a nonzero return code.
        FileNotFoundError
            If one or more expected output files do not exist after execution.
        """
        if isinstance(expected_outputs, Path):
            expected_outputs = (expected_outputs,)

        with self._expect_output_files(*expected_outputs):
            return self.run_orca_mm(
                command,
                args,
                stdout=stdout,
                stderr=stderr,
                timeout=timeout,
                raise_on_error=raise_on_error,
            )

    def run_convff(
        self,
        ffinput: ForcefieldType,
        ff_files: Iterable[Path],
        *,
        force: bool = False,
        stdout: StreamTargetSpec = (),
        stderr: StreamTargetSpec = (),
        timeout: float | None = None,
        raise_on_error: bool = True,
    ) -> Path:
        """
        Executes the `orca_mm` binary with the `-convff` flag and passes in the
        forcefield type and forcefield files as arguments to the binary.

        Parameters
        ----------
        ffinput : ForcefieldType
            Input forcefield format (`amber`, `charmm`, or `openmm`).
        ff_files : Iterable[Path]
            Input forcefield file(s) to convert.
        force : bool, default: False
            Overwrite existing output file if present.
        stdout : StreamTargetSpec, default: ()
            One or more target streams to pipe the subprocess STDOUT to.
        stderr : StreamTargetSpec, default: ()
            One or more target streams to pipe the subprocess STDERR to.
        timeout : float | None, by default None
            Optional timeout in seconds to wait for process to complete.
        raise_on_error : bool, default: True
            Raise `OrcaMmError` if `orca_mm` exits with a nonzero return code.

        Returns
        -------
        Path
            Path to generated ORCA forcefield file (`*.ORCAFF.prms`).

        Raises
        ------
        ValueError
            If no forcefield input files are supplied.
        FileNotFoundError
            If an input file is missing or the expected output is not generated.
        OrcaMmError
            If `raise_on_error` is set and `orca_mm` exits with a nonzero return code.
        """
        # > `convff` requires at least one source forcefield file.
        ff_files = tuple(ff_files)

        if len(ff_files) == 0:
            raise ValueError("Must supply at least 1 forcefield file.")

        self._assert_files_exist(*ff_files)

        # > Derive the output path generated from the first forcefield file.
        # > `orca_mm -convff` replaces its ending with `.ORCAFF.prms`.
        # > For example:
        # > - `orca_mm -convff -CHARMM 1C1E.psf par_all36_prot.prm toppar_water_ions_namd.str` -> `1C1E.ORCAFF.prms`
        # > - `orca_mm -convff -AMBER complex.prmtop` -> `complex.ORCAFF.prms`
        # > - `orca_mm -convff -OPENMM complex.xml` -> `complex.ORCAFF.prms`
        expected_output = ff_files[0].with_suffix(self._orca_ff_suffix)

        # > Reuse an existing forcefield unless the caller explicitly requests regeneration using `force`.
        if expected_output.is_file() and not force:
            return expected_output

        # > Remove stale output so the post-run existence check validates this execution.
        expected_output.unlink(missing_ok=True)

        # > Assemble the format option followed by the forcefield input paths.
        arguments = [f"-{ffinput}"] + [str(f) for f in ff_files]

        # > Execute the command and verify that it generated the expected forcefield.
        self._run_orca_mm_and_expect(
            "convff",
            arguments,
            expected_output,
            stdout=stdout,
            stderr=stderr,
            raise_on_error=raise_on_error,
            timeout=timeout,
        )

        return expected_output

    def run_splitff(
        self,
        orcaff_file: Path,
        *atoms: int,
        stdout: StreamTargetSpec = (),
        stderr: StreamTargetSpec = (),
        timeout: float | None = None,
        raise_on_error: bool = True,
    ) -> list[Path]:
        """
        Execute `orca_mm -splitff` and split an ORCA forcefield file at selected atom indices.

        Parameters
        ----------
        orcaff_file : Path
            Path to ORCA forcefield file (`*.ORCAFF.prms`) that will be split.
        *atoms : int
            1-based atom indices used as split points.
        stdout : StreamTargetSpec, default: ()
            One or more target streams to pipe the subprocess STDOUT to.
        stderr : StreamTargetSpec, default: ()
            One or more target streams to pipe the subprocess STDERR to.
        timeout : float | None, by default None
            Optional timeout in seconds to wait for process to complete.
        raise_on_error : bool, default: True
            Raise `OrcaMmError` if `orca_mm` exits with a nonzero return code.

        Returns
        -------
        list[Path]
            Paths to generated split forcefield files.

        Raises
        ------
        ValueError
            If no split points are supplied or an atom index is not positive.
        FileNotFoundError
            If the input file is missing or an expected output is not generated.
        OrcaMmError
            If `raise_on_error` is set and `orca_mm` exits with a nonzero return code.
        """
        self._assert_files_exist(orcaff_file)

        # > Normalize the split points before validating and passing them to `orca_mm`.
        sorted_atoms = list(sorted(atoms))

        if len(sorted_atoms) == 0:
            raise ValueError("Must supply at least 1 atom.")

        if any(atom < 1 for atom in sorted_atoms):
            raise ValueError("All atoms must be positive integers.")

        # > A split at N atom indices produces N + 1 forcefield files.
        expected_outputs = [
            _add_infix_to_path(orcaff_file, f"_split{split + 1}", self._orca_ff_suffix)
            for split in range(len(sorted_atoms) + 1)
        ]

        # > Assemble the source forcefield path followed by the ordered split points.
        arguments = [f"{orcaff_file}"] + [str(atom) for atom in sorted_atoms]

        # > Execute the command and verify that every split forcefield was generated.
        self._run_orca_mm_and_expect(
            "splitff",
            arguments,
            expected_outputs,
            stdout=stdout,
            stderr=stderr,
            raise_on_error=raise_on_error,
            timeout=timeout,
        )

        return expected_outputs

    def run_mergeff(
        self,
        *orcaff_files: Path,
        stdout: StreamTargetSpec = (),
        stderr: StreamTargetSpec = (),
        timeout: float | None = None,
        raise_on_error: bool = True,
    ) -> Path:
        """
        Execute `orca_mm -mergeff` to merge multiple ORCA forcefield files.

        Parameters
        ----------
        *orcaff_files : Path
            ORCA forcefield files (`*.ORCAFF.prms`) to merge.
        stdout : StreamTargetSpec, default: ()
            One or more target streams to pipe the subprocess STDOUT to.
        stderr : StreamTargetSpec, default: ()
            One or more target streams to pipe the subprocess STDERR to.
        timeout : float | None, by default None
            Optional timeout in seconds to wait for process to complete.
        raise_on_error : bool, default: True
            Raise `OrcaMmError` if `orca_mm` exits with a nonzero return code.

        Returns
        -------
        Path
            Path to merged ORCA forcefield file.

        Raises
        ------
        ValueError
            If fewer than two forcefield files are supplied.
        FileNotFoundError
            If an input file is missing or the expected output is not generated.
        OrcaMmError
            If `raise_on_error` is set and `orca_mm` exits with a nonzero return code.
        """
        # > A merge requires at least two source forcefields.
        if len(orcaff_files) < 2:
            raise ValueError("Must provide at least 2 orca ff files to merge")

        self._assert_files_exist(*orcaff_files)

        # > `orca_mm` derives the merged output name from the first input file.
        expected_output = _add_infix_to_path(orcaff_files[0], "_merged", self._orca_ff_suffix)

        # > Assemble the forcefield paths in the order supplied by the caller.
        arguments = [str(f) for f in orcaff_files]

        # > Execute the command and verify that the merged forcefield was generated.
        self._run_orca_mm_and_expect(
            "mergeff",
            arguments,
            expected_output,
            stdout=stdout,
            stderr=stderr,
            raise_on_error=raise_on_error,
            timeout=timeout,
        )

        return expected_output

    def run_repeatff(
        self,
        orcaff_file: Path,
        repeat: int,
        *,
        stdout: StreamTargetSpec = (),
        stderr: StreamTargetSpec = (),
        timeout: float | None = None,
        raise_on_error: bool = True,
    ) -> Path:
        """
        Execute `orca_mm -repeatff` to repeat a forcefield topology a fixed number of times.

        Parameters
        ----------
        orcaff_file : Path
            ORCA forcefield file (`*.ORCAFF.prms`) to repeat.
        repeat : int
            Number of repetitions. Must be a positive integer.
        stdout : StreamTargetSpec, default: ()
            One or more target streams to pipe the subprocess STDOUT to.
        stderr : StreamTargetSpec, default: ()
            One or more target streams to pipe the subprocess STDERR to.
        timeout : float | None, by default None
            Optional timeout in seconds to wait for process to complete.
        raise_on_error : bool, default: True
            Raise `OrcaMmError` if `orca_mm` exits with a nonzero return code.

        Returns
        -------
        Path
            Path to repeated ORCA forcefield file.

        Raises
        ------
        ValueError
            If `repeat` is not positive.
        FileNotFoundError
            If the input file is missing or the expected output is not generated.
        OrcaMmError
            If `raise_on_error` is set and `orca_mm` exits with a nonzero return code.
        """
        self._assert_files_exist(orcaff_file)

        # > Validate `repeat` is a positive integer.
        if repeat < 1:
            raise ValueError("'repeat' must be a positive integer")

        # > `orca_mm` includes the repeat count in the generated filename.
        expected_output = _add_infix_to_path(orcaff_file, f"_repeat{repeat}", self._orca_ff_suffix)

        # > Assemble the source forcefield path and requested repeat count.
        arguments = [f"{orcaff_file}", str(repeat)]

        # > Execute the command and verify that the repeated forcefield was generated.
        self._run_orca_mm_and_expect(
            "repeatff",
            arguments,
            expected_output,
            stdout=stdout,
            stderr=stderr,
            raise_on_error=raise_on_error,
            timeout=timeout,
        )

        return expected_output

    def run_splitpdb(
        self,
        pdb_file: Path,
        *atoms: int,
        stdout: StreamTargetSpec = (),
        stderr: StreamTargetSpec = (),
        timeout: float | None = None,
        raise_on_error: bool = True,
    ) -> list[Path]:
        """
        Execute `orca_mm -splitpdb` and split a PDB structure at selected atom indices.

        Parameters
        ----------
        pdb_file : Path
            Path to PDB file that will be split.
        *atoms : int
            1-based atom indices used as split points.
        stdout : StreamTargetSpec, default: ()
            One or more target streams to pipe the subprocess STDOUT to.
        stderr : StreamTargetSpec, default: ()
            One or more target streams to pipe the subprocess STDERR to.
        timeout : float | None, by default None
            Optional timeout in seconds to wait for process to complete.
        raise_on_error : bool, default: True
            Raise `OrcaMmError` if `orca_mm` exits with a nonzero return code.

        Returns
        -------
        list[Path]
            Paths to generated split PDB files.

        Raises
        ------
        ValueError
            If no split points are supplied or an atom index is not positive.
        FileNotFoundError
            If the input file is missing or an expected output is not generated.
        OrcaMmError
            If `raise_on_error` is set and `orca_mm` exits with a nonzero return code.
        """
        self._assert_files_exist(pdb_file)

        # > Normalize the split points before validating and passing them to `orca_mm`.
        sorted_atoms = list(sorted(atoms))

        if len(sorted_atoms) == 0:
            raise ValueError("Must supply at least 1 atom.")

        if any(atom < 1 for atom in sorted_atoms):
            raise ValueError("All atoms must be positive integers.")

        # > A split at N atom indices produces N + 1 PDB files.
        expected_outputs = [
            _add_infix_to_path(pdb_file, f"_split{split + 1}", ".pdb")
            for split in range(len(sorted_atoms) + 1)
        ]

        # > Assemble the source PDB path followed by the ordered split points.
        arguments = [f"{pdb_file}"] + [str(atom) for atom in sorted_atoms]

        # > Execute the command and verify that every split PDB was generated.
        self._run_orca_mm_and_expect(
            "splitpdb",
            arguments,
            expected_outputs,
            stdout=stdout,
            stderr=stderr,
            raise_on_error=raise_on_error,
            timeout=timeout,
        )

        return expected_outputs

    def run_mergepdb(
        self,
        *pdb_files: Path,
        stdout: StreamTargetSpec = (),
        stderr: StreamTargetSpec = (),
        timeout: float | None = None,
        raise_on_error: bool = True,
    ) -> Path:
        """
        Execute `orca_mm -mergepdb` to merge multiple PDB files.

        Parameters
        ----------
        *pdb_files : Path
            PDB files to merge.
        stdout : StreamTargetSpec, default: ()
            One or more target streams to pipe the subprocess STDOUT to.
        stderr : StreamTargetSpec, default: ()
            One or more target streams to pipe the subprocess STDERR to.
        timeout : float | None, by default None
            Optional timeout in seconds to wait for process to complete.
        raise_on_error : bool, default: True
            Raise `OrcaMmError` if `orca_mm` exits with a nonzero return code.

        Returns
        -------
        Path
            Path to merged PDB file.

        Raises
        ------
        ValueError
            If fewer than two PDB files are supplied.
        FileNotFoundError
            If an input file is missing or the expected output is not generated.
        OrcaMmError
            If `raise_on_error` is set and `orca_mm` exits with a nonzero return code.
        """
        # > A merge requires at least two source PDB files.
        if len(pdb_files) < 2:
            raise ValueError("Must provide at least 2 PDB files to merge")

        self._assert_files_exist(*pdb_files)

        # > `orca_mm` derives the merged output name from the first input file.
        expected_output = _add_infix_to_path(pdb_files[0], "_merged", ".pdb")

        # > Assemble the PDB paths in the order supplied by the caller.
        arguments = [str(f) for f in pdb_files]

        # > Execute the command and verify that the merged PDB was generated.
        self._run_orca_mm_and_expect(
            "mergepdb",
            arguments,
            expected_output,
            stdout=stdout,
            stderr=stderr,
            raise_on_error=raise_on_error,
            timeout=timeout,
        )

        return expected_output

    def run_makeff(
        self,
        structure_file: Path,
        *,
        charge: int | None = None,
        multiplicity: int | None = None,
        nproc: int | None = None,
        charge_option: ChargeOption | None = None,
        oxidation_states: dict[str, float] | None = None,
        stdout: StreamTargetSpec = (),
        stderr: StreamTargetSpec = (),
        timeout: float | None = None,
        raise_on_error: bool = True,
    ) -> Path:
        """
        Execute `orca_mm -makeff` to generate an ORCA forcefield file from a structure file.

        Parameters
        ----------
        structure_file : Path
            Input structure file for forcefield generation.
        charge : int | None, default: None
            Total molecular charge passed via `-C`.
        multiplicity : int | None, default: None
            Spin multiplicity passed via `-M`. Must be a positive integer.
        nproc : int | None, default: None
            Number of processes passed via `-nproc`.
        charge_option : ChargeOption | None, default: None
            Charge-calculation mode for forcefield generation.
        oxidation_states : dict[str, float] | None, default: None
            Optional element-to-oxidation-state mapping passed via repeated `-CEL` flags.
        stdout : StreamTargetSpec, default: ()
            One or more target streams to pipe the subprocess STDOUT to.
        stderr : StreamTargetSpec, default: ()
            One or more target streams to pipe the subprocess STDERR to.
        timeout : float | None, by default None
            Optional timeout in seconds to wait for process to complete.
        raise_on_error : bool, default: True
            Raise `OrcaMmError` if `orca_mm` exits with a nonzero return code.

        Returns
        -------
        Path
            Path to generated ORCA forcefield file (`*.ORCAFF.prms`).

        Raises
        ------
        ValueError
            If `multiplicity` is not positive.
        FileNotFoundError
            If the input file is missing or the expected output is not generated.
        OrcaMmError
            If `raise_on_error` is set and `orca_mm` exits with a nonzero return code.
        """
        self._assert_files_exist(structure_file)

        # > Derive the forcefield path generated from the input structure filename.
        expected_output = structure_file.with_suffix(self._orca_ff_suffix)

        # > Start the command with the mandatory structure path.
        arguments = [str(structure_file)]

        # > Add the optional molecular charge and spin multiplicity.
        if charge is not None:
            arguments.extend(("-C", str(charge)))

        if multiplicity is not None:
            if multiplicity < 1:
                raise ValueError("Multiplicity must be a positive integer")
            arguments.extend(("-M", str(multiplicity)))

        # > Add the optional process count and charge-calculation mode.
        if nproc is not None:
            arguments.extend(("-nproc", str(nproc)))

        if charge_option is not None:
            arguments.append(f"-{charge_option}")

        # > Add one element-specific oxidation-state option per mapping entry.
        if oxidation_states is not None:
            for element, oxidation_state in oxidation_states.items():
                arguments.extend(("-CEL", str(element), f"{float(oxidation_state):.1f}"))

        # > Execute the command and verify that the forcefield was generated.
        self._run_orca_mm_and_expect(
            "makeff",
            arguments,
            expected_output,
            stdout=stdout,
            stderr=stderr,
            raise_on_error=raise_on_error,
            timeout=timeout,
        )

        return expected_output

    def run_get_h_dist(
        self,
        structure_file: Path,
        *,
        stdout: StreamTargetSpec = (),
        stderr: StreamTargetSpec = (),
        timeout: float | None = None,
        raise_on_error: bool = True,
    ) -> Path:
        """
        Execute `orca_mm -getHDist` to generate hydrogen-distance parameters from a structure.

        Parameters
        ----------
        structure_file : Path
            Input structure file for hydrogen-distance analysis.
        stdout : StreamTargetSpec, default: ()
            One or more target streams to pipe the subprocess STDOUT to.
        stderr : StreamTargetSpec, default: ()
            One or more target streams to pipe the subprocess STDERR to.
        timeout : float | None, by default None
            Optional timeout in seconds to wait for process to complete.
        raise_on_error : bool, default: True
            Raise `OrcaMmError` if `orca_mm` exits with a nonzero return code.

        Returns
        -------
        Path
            Path to generated `*.H_DIST.prms` file.

        Raises
        ------
        FileNotFoundError
            If the input file is missing or the expected output is not generated.
        OrcaMmError
            If `raise_on_error` is set and `orca_mm` exits with a nonzero return code.
        """
        self._assert_files_exist(structure_file)

        # > Derive the hydrogen-distance parameter path from the input structure filename.
        expected_output = structure_file.with_suffix(".H_DIST.prms")

        # > Execute the command with the structure path and verify its generated output.
        arguments = [str(structure_file)]
        self._run_orca_mm_and_expect(
            "getHDist",
            arguments,
            expected_output,
            stdout=stdout,
            stderr=stderr,
            raise_on_error=raise_on_error,
            timeout=timeout,
        )

        return expected_output
