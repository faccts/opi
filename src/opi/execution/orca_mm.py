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

from contextlib import contextmanager
from pathlib import Path
import tempfile
from typing import Iterable, Iterator, Literal, Sequence

from opi.exceptions import OrcaMmError
from opi.execution.base import BaseRunner
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
    Adds `infix` to the `path` whilst preserving the given `suffix`.

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
    >>> path = Path.cwd() / "system.ORCAFF.prms"
    >>> suffix = ".ORCAFF.prms
    >>> _replace_infix(path, "_merged", suffix)
    Path("system_merged.ORCAFF.prms")
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
    """

    _orca_ff_suffix = ".ORCAFF.prms"

    @staticmethod
    @contextmanager
    def _expect_output_files(*expected_outputs: Path) -> Iterator[None]:
        """
        Context manager that checks expected output files after command execution.

        Parameters
        ----------
        *expected_outputs : Path
            Output files that must exist after the wrapped command has finished successfully.
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
        arguments: Sequence[str],
        *,
        raise_on_error: bool = True,
        silent: bool = True,
        timeout: int = -1,
    ):
        """
        Execute `orca_mm` with the provided subcommand and arguments.

        Parameters
        ----------
        command : OrcaMmCommand
            `orca_mm` subcommand to execute.
        arguments : Sequence[str]
            Command-line arguments passed to the subcommand.
        raise_on_error : bool, default: True
            Raise `OrcaMmException` if `orca_mm` writes anything to STDERR.
        silent : bool, default: True
            Capture and discard STDOUT and STDERR.
        timeout : int, default: -1
            Optional timeout in seconds to wait for process to complete.

        Raises
        ------
        OrcaMmException
            If `raise_on_error` is set and `orca_mm` reports an error.
        """
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "stderr.txt"
            self.run(
                OrcaBinary.ORCA_MM,
                [f"-{command}"] + list(arguments),
                stderr=path,
                silent=silent,
                timeout=timeout,
            )
            if raise_on_error and path.exists() and (error := path.read_text()):
                raise OrcaMmError(command, arguments, error)

    def run_convff(
        self,
        ffinput: ForcefieldType,
        ff_files: Iterable[Path],
        *,
        force: bool = False,
        raise_on_error: bool = True,
        silent: bool = True,
        timeout: int = -1,
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
        raise_on_error : bool, default: True
            Raise `OrcaMmException` if `orca_mm` reports an error.
        silent : bool, default: True
            Capture and discard STDOUT and STDERR.
        timeout : int, default: -1
            Optional timeout in seconds to wait for process to complete.

        Returns
        -------
        Path
            Path to generated ORCA forcefield file (`*.ORCAFF.prms`).
        """
        ff_files = list(ff_files)

        if len(ff_files) == 0:
            raise ValueError("Must supply at least 1 forcefield file.")

        # `orca_mm -convff` will generate a file with the same stem as the first file but the suffix replaced by '.ORCAFF.prms'.
        # For example:
        # - `orca_mm -convff -CHARMM 1C1E.psf par_all36_prot.prm toppar_water_ions_namd.str` -> `1C1E.ORCAFF.prms`
        # - `orca_mm -convff -AMBER complex.prmtop` -> `complex.ORCAFF.prms`
        # - `orca_mm -convff -OPENMM complex.xml` -> `complex.ORCAFF.prms`
        expected_output = ff_files[0].with_suffix(self._orca_ff_suffix)

        # If the expected forcefield file already exists and `force` is not specified, we skip running `orca_mm`
        if expected_output.is_file() and not force:
            return expected_output

        # Make sure that the forcefield file does not exist so that we can ensure that `orca_mm` succeeds.
        expected_output.unlink(missing_ok=True)

        arguments = [f"-{ffinput}"] + [str(f) for f in ff_files]
        with self._expect_output_files(expected_output):
            self.run_orca_mm(
                "convff", arguments, raise_on_error=raise_on_error, silent=silent, timeout=timeout
            )

        return expected_output

    def run_splitff(
        self,
        orcaff_file: Path,
        *atoms: int,
        raise_on_error: bool = True,
        silent: bool = True,
        timeout: int = -1,
    ) -> list[Path]:
        """
        Execute `orca_mm -splitff` and split an ORCA forcefield file at selected atom indices.

        Parameters
        ----------
        orcaff_file : Path
            Path to ORCA forcefield file (`*.ORCAFF.prms`) that will be split.
        *atoms : int
            1-based atom indices used as split points.
        raise_on_error : bool, default: True
            Raise `OrcaMmException` if `orca_mm` reports an error.
        silent : bool, default: True
            Capture and discard STDOUT and STDERR.
        timeout : int, default: -1
            Optional timeout in seconds to wait for process to complete.

        Returns
        -------
        list[Path]
            Paths to generated split forcefield files.
        """
        sorted_atoms = list(sorted(atoms))

        if len(sorted_atoms) == 0:
            raise ValueError("Must supply at least 1 atom.")

        if any(atom < 1 for atom in sorted_atoms):
            raise ValueError("All atoms must be positive integers.")

        expected_outputs = [
            _add_infix_to_path(orcaff_file, f"_split{split + 1}", self._orca_ff_suffix)
            for split in range(len(sorted_atoms) + 1)
        ]

        arguments = [f"{orcaff_file}"] + [str(atom) for atom in sorted_atoms]
        with self._expect_output_files(*expected_outputs):
            self.run_orca_mm(
                "splitff", arguments, raise_on_error=raise_on_error, silent=silent, timeout=timeout
            )

        return expected_outputs

    def run_mergeff(
        self,
        *orcaff_files: Path,
        raise_on_error: bool = True,
        silent: bool = True,
        timeout: int = -1,
    ) -> Path:
        """
        Execute `orca_mm -mergeff` to merge multiple ORCA forcefield files.

        Parameters
        ----------
        *orcaff_files : Path
            ORCA forcefield files (`*.ORCAFF.prms`) to merge.
        raise_on_error : bool, default: True
            Raise `OrcaMmException` if `orca_mm` reports an error.
        silent : bool, default: True
            Capture and discard STDOUT and STDERR.
        timeout : int, default: -1
            Optional timeout in seconds to wait for process to complete.

        Returns
        -------
        Path
            Path to merged ORCA forcefield file.
        """
        if len(orcaff_files) < 2:
            raise ValueError("Must provide at least 2 orca ff files to merge")

        expected_output = _add_infix_to_path(orcaff_files[0], "_merged", self._orca_ff_suffix)

        arguments = [str(f) for f in orcaff_files]
        with self._expect_output_files(expected_output):
            self.run_orca_mm(
                "mergeff", arguments, raise_on_error=raise_on_error, silent=silent, timeout=timeout
            )

        return expected_output

    def run_repeatff(
        self,
        orcaff_file: Path,
        repeat: int,
        *,
        raise_on_error: bool = True,
        silent: bool = True,
        timeout: int = -1,
    ) -> Path:
        """
        Execute `orca_mm -repeatff` to repeat a forcefield topology a fixed number of times.

        Parameters
        ----------
        orcaff_file : Path
            ORCA forcefield file (`*.ORCAFF.prms`) to repeat.
        repeat : int
            Number of repetitions. Must be a positive integer.
        raise_on_error : bool, default: True
            Raise `OrcaMmException` if `orca_mm` reports an error.
        silent : bool, default: True
            Capture and discard STDOUT and STDERR.
        timeout : int, default: -1
            Optional timeout in seconds to wait for process to complete.

        Returns
        -------
        Path
            Path to repeated ORCA forcefield file.
        """
        if repeat < 1:
            raise ValueError("'repeat' must be a positive integer")

        expected_output = _add_infix_to_path(orcaff_file, f"_repeat{repeat}", self._orca_ff_suffix)

        arguments = [f"{orcaff_file}", str(repeat)]
        with self._expect_output_files(expected_output):
            self.run_orca_mm(
                "repeatff",
                arguments,
                raise_on_error=raise_on_error,
                silent=silent,
                timeout=timeout,
            )

        return expected_output

    def run_splitpdb(
        self,
        pdb_file: Path,
        *atoms: int,
        raise_on_error: bool = True,
        silent: bool = True,
        timeout: int = -1,
    ) -> list[Path]:
        """
        Execute `orca_mm -splitpdb` and split a PDB structure at selected atom indices.

        Parameters
        ----------
        pdb_file : Path
            Path to PDB file that will be split.
        *atoms : int
            1-based atom indices used as split points.
        raise_on_error : bool, default: True
            Raise `OrcaMmException` if `orca_mm` reports an error.
        silent : bool, default: True
            Capture and discard STDOUT and STDERR.
        timeout : int, default: -1
            Optional timeout in seconds to wait for process to complete.

        Returns
        -------
        list[Path]
            Paths to generated split PDB files.
        """
        sorted_atoms = list(sorted(atoms))

        if len(sorted_atoms) == 0:
            raise ValueError("Must supply at least 1 atom.")

        if any(atom < 1 for atom in sorted_atoms):
            raise ValueError("All atoms must be positive integers.")

        expected_outputs = [
            _add_infix_to_path(pdb_file, f"_split{split + 1}", ".pdb")
            for split in range(len(sorted_atoms) + 1)
        ]

        arguments = [f"{pdb_file}"] + [str(atom) for atom in sorted_atoms]
        with self._expect_output_files(*expected_outputs):
            self.run_orca_mm(
                "splitpdb", arguments, raise_on_error=raise_on_error, silent=silent, timeout=timeout
            )

        return expected_outputs

    def run_mergepdb(
        self,
        *pdb_files: Path,
        raise_on_error: bool = True,
        silent: bool = True,
        timeout: int = -1,
    ) -> Path:
        """
        Execute `orca_mm -mergepdb` to merge multiple PDB files.

        Parameters
        ----------
        *pdb_files : Path
            PDB files to merge.
        raise_on_error : bool, default: True
            Raise `OrcaMmException` if `orca_mm` reports an error.
        silent : bool, default: True
            Capture and discard STDOUT and STDERR.
        timeout : int, default: -1
            Optional timeout in seconds to wait for process to complete.

        Returns
        -------
        Path
            Path to merged PDB file.
        """
        if len(pdb_files) < 2:
            raise ValueError("Must provide at least 2 orca ff files to merge")

        expected_output = _add_infix_to_path(pdb_files[0], "_merged", ".pdb")

        arguments = [str(f) for f in pdb_files]
        with self._expect_output_files(expected_output):
            self.run_orca_mm(
                "mergepdb", arguments, raise_on_error=raise_on_error, silent=silent, timeout=timeout
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
        raise_on_error: bool = True,
        silent: bool = True,
        timeout: int = -1,
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
        raise_on_error : bool, default: True
            Raise `OrcaMmException` if `orca_mm` reports an error.
        silent : bool, default: True
            Capture and discard STDOUT and STDERR.
        timeout : int, default: -1
            Optional timeout in seconds to wait for process to complete.

        Returns
        -------
        Path
            Path to generated ORCA forcefield file (`*.ORCAFF.prms`).
        """
        expected_output = structure_file.with_suffix(self._orca_ff_suffix)

        arguments = [str(structure_file)]

        if charge is not None:
            arguments.extend(("-C", str(charge)))

        if multiplicity is not None:
            if multiplicity < 1:
                raise ValueError("Multiplicity must be a positive integer")
            arguments.extend(("-M", str(multiplicity)))

        if nproc is not None:
            arguments.extend(("-nproc", str(nproc)))

        if charge_option is not None:
            arguments.append(f"-{charge_option}")

        if oxidation_states is not None:
            for element, oxidation_state in oxidation_states.items():
                arguments.extend(("-CEL", str(element), f"{float(oxidation_state):.1f}"))

        with self._expect_output_files(expected_output):
            self.run_orca_mm(
                "makeff", arguments, raise_on_error=raise_on_error, silent=silent, timeout=timeout
            )

        return expected_output

    def run_get_h_dist(
        self,
        structure_file: Path,
        *,
        raise_on_error: bool = True,
        silent: bool = True,
        timeout: int = -1,
    ) -> Path:
        """
        Execute `orca_mm -getHDist` to generate hydrogen-distance parameters from a structure.

        Parameters
        ----------
        structure_file : Path
            Input structure file for hydrogen-distance analysis.
        raise_on_error : bool, default: True
            Raise `OrcaMmException` if `orca_mm` reports an error.
        silent : bool, default: True
            Capture and discard STDOUT and STDERR.
        timeout : int, default: -1
            Optional timeout in seconds to wait for process to complete.

        Returns
        -------
        Path
            Path to generated `*.H_DIST.prms` file.
        """
        expected_output = structure_file.with_suffix(".H_DIST.prms")

        arguments = [str(structure_file)]
        with self._expect_output_files(expected_output):
            self.run_orca_mm(
                "getHDist", arguments, raise_on_error=raise_on_error, silent=silent, timeout=timeout
            )

        return expected_output
