import re
from collections.abc import Iterator
from os import PathLike
from pathlib import Path
from typing import Literal, Sequence

from opi.utils.tracking_text_io import TrackingTextIO

__all__ = ("Properties",)

# > RE for finding floats and integers guarded by lookarounds that no letters are next to them
RGX_INT_AND_FLOAT = re.compile(
    r"(?<![A-Za-z])[+-]?(?:\d+\.\d*|\.\d+|\d+)(?:[Ee][+-]?\d+)?(?![A-Za-z])"
)


class Properties:
    """
    Class for keeping structure properties found in xyz files.

    Attributes
    ----------
    structure_id : int | None, default = None
        Number of the structure from which the properties are.
    energy_total : float | None, default = None
        Energy of a structure.
    energy_relative : float | None, default = None
        Relative energy of a structure (relative to any).
    """

    def __init__(
        self,
        structure_id: int | None = None,
        energy_total: float | None = None,
        energy_relative: float | None = None,
    ) -> None:
        self.structure_id: int | None = structure_id
        self.energy_total: float | None = energy_total
        self.energy_relative: float | None = energy_relative

    @classmethod
    def from_xyz(
        cls, xyzfile: Path | str | PathLike[str], mode: Literal["goat", "docker"] = "goat"
    ) -> "Properties":
        """
        Function for reading properties from the comment lines of a xyz file and return a Properties object.

        Parameters
        ----------
        xyzfile : Path | str | PathLike[str]
            Name or path to xyz file
        mode: Literal["goat", "docker"], default = "goat"
            Define how the comment line should be processed, e.g, it is the comment line from a DOCKER or GOAT run.

        Raises
        --------
        FileNotFoundError
            If the XYZ file cannot be found
        ValueError
            If there is a problem with parsing the XYZ file

        Returns
        --------
        Properties:Properties object extracted from file
        """
        return cls.from_trj_xyz(xyzfile, n_struc_limit=1, mode=mode)[0]

    @classmethod
    def from_trj_xyz(
        cls,
        trj_file: Path | str | PathLike[str],
        /,
        *,
        mode: Literal["goat", "docker"] = "goat",
        comment_symbols: str | Sequence[str] | None = None,
        n_struc_limit: int | None = None,
    ) -> "list[Properties]":
        """
        Function for reading multi-xyz file and returning a Properties object.

        Parameters
        ----------
        trj_file : Path | str | PathLike[str]
            Name or path to xyz file with one or multiple structure(s)
        comment_symbols: str | Sequence[str] | None, default: None
            List of symbols that indicate user comments in the xyz file. User comments are skipped before the actual xyz
            data starts. By default, no user comments are used. White-space only comments are not allowed and are
            silently ignored.
        n_struc_limit: int | None, default: None
            If >0, only read the first n structures.

        Raises
        --------
        FileNotFoundError
            If the XYZ file cannot be found
        ValueError
            If there is a problem with parsing the XYZ file

        Returns
        --------
        list[Properties]: Properties object extracted from file
        """
        # > converting into Path
        trj_file = Path(trj_file)

        # > Check if file exists
        if not trj_file.exists():
            raise FileNotFoundError(f"XYZ file not found: {trj_file}")

        # > Open file and iterate over structures
        with TrackingTextIO(trj_file.open()) as tracked:
            return list(cls._iter_xyz_structures(tracked, comment_symbols, mode, n_struc_limit))

    @classmethod
    def from_xyz_block(
        cls, xyz_string: str, mode: Literal["goat", "docker"] = "goat"
    ) -> "Properties":
        """
        Function for reading xyz data from string and return a Properties object.

        Parameters
        ----------
        xyz_string: str
            String that contains xyz file data
        mode: Literal["goat", "docker"], default = "goat"
            Define how the comment line should be processed, e.g, it is the comment line from a DOCKER or GOAT run.

        Raises
        --------
        ValueError
            If there is a problem with parsing the XYZ file

        Returns
        --------
        Properties
            The `Properties` object extracted from file
        """
        return cls.from_trj_xyz_block(xyz_string, n_struc_limit=1, mode=mode)[0]

    @classmethod
    def from_trj_xyz_block(
        cls,
        trj_string: str,
        /,
        *,
        mode: Literal["goat", "docker"] = "goat",
        comment_symbols: str | Sequence[str] | None = None,
        n_struc_limit: int | None = None,
    ) -> "list[Properties]":
        """
        Function for reading trajectory data from string and returning a Properties object. What is read depends on the
        mode Literal.

        Parameters
        ----------
        trj_string : Path | str | PathLike[str]
            String that contains one or multiple xyz blocks (trajectory data)
        mode: Literal["goat", "docker"], default = "goat"
            Define how the comment line should be processed, e.g, it is the comment line from a DOCKER or GOAT run.
        comment_symbols: str | Sequence[str] | None, default: None
            List of symbols that indicate user comments in the xyz file. User comments are skipped before the actual xyz
            data starts. By default, no user comments are used. White-space only comments are not allowed and are
            silently ignored.
        n_struc_limit: int | None, default: None
            If >0, only read the first n structures.

        Returns
        --------
        list[Properties]: Properties objects extracted from file
        """
        with TrackingTextIO(trj_string) as tracked:
            return list(cls._iter_xyz_structures(tracked, comment_symbols, mode, n_struc_limit))

    @classmethod
    def from_xyz_buffer(
        cls,
        xyz_lines: TrackingTextIO,
        /,
        *,
        comment_symbols: str | Sequence[str] | None = None,
        mode: Literal["goat", "docker"] = "goat",
    ) -> "Properties | None":
        """
        Function for reading from the comment line of a xyz file from a buffer and converting it to a Properties object.
        What is read depends on the `mode` Literal, e.g, total energies from a GOAT xyz file.

        Parameters
        ----------
        xyz_lines: TrackingTextIO
            A buffer that contains xyz file data
        comment_symbols: str | Sequence[str] | None, default: None
            List of symbols that indicate user comments in the xyz file. User comments are skipped before the actual xyz
            data starts. By default, no user comments are used. White-space only comments are not allowed and are
            silently ignored.
        mode: Literal["goat", "docker"], default = "goat"
            Define how the comment line should be processed, e.g, it is the comment line from a DOCKER or GOAT run.

        Raises
        --------
        ValueError
            When no valid properties can be read from the input buffer or the corresponding structure is incomplete

        Returns
        --------
        Properties | None
            The `Properties` object extracted from the buffer or None if the buffer was empty.
        """
        # > Select mode
        mode_functions = {
            "goat": cls.goat_energies,
            "docker": cls.docker_energies,
        }

        comments_tuple: tuple[str, ...] | None = None

        # > Convert comments to tuple
        if isinstance(comment_symbols, str):
            comments_tuple = (comment_symbols,)
        elif isinstance(comment_symbols, Sequence):
            comments_tuple = tuple(comment_symbols)

        # > Skip arbitrary number of empty and user comment lines at the beginning
        while line := xyz_lines.readline():
            if not line.lstrip():
                continue
            # > Check for comment line. Ignore empty/whitespace lines
            elif comments_tuple and line.lstrip().startswith(comments_tuple):
                continue
            else:
                break

        # > No data available in the buffer
        if not line:
            return None

        # > Fetch number of atoms
        try:
            natoms = int(line.split()[0])
        except (ValueError, IndexError) as err:
            raise ValueError(
                f"Line {xyz_lines.line_number}: Could not read number of atoms at the beginning of xyz data"
            ) from err

        # > Comment line
        line = xyz_lines.readline()
        if not line:
            raise ValueError(
                f"Line {xyz_lines.line_number}: Comment line is not present in xyz data"
            )

        # > Analyse comment line
        properties = mode_functions[mode](line)

        # > Skip the remaining structure
        for iline in range(natoms):
            line = xyz_lines.readline()
            # > empty lines are not allowed
            if not line:
                raise ValueError(f"Line {xyz_lines.line_number}: Incomplete xyz file buffer")

        return properties

    @classmethod
    def docker_energies(cls, line: str) -> "Properties":
        """Function for reading DOCKER energies from comment line of a DOCKER xyz file."""
        numbers = [float(m) for m in re.findall(RGX_INT_AND_FLOAT, line)]
        # > Parse the comment line
        try:
            # > ID of the structure
            structure_id = int(numbers[0])
            # > Total energy is second number (Eh)
            energy_total = numbers[1]
            # > Relative energy is the third number (kcal/mol)
            energy_relative = numbers[2]
        except (IndexError, ValueError) as err:
            raise ValueError("Could not parse docker energies from comment line.") from err
        properties = Properties(
            structure_id=structure_id, energy_total=energy_total, energy_relative=energy_relative
        )
        return properties

    @classmethod
    def goat_energies(cls, line: str) -> "Properties":
        """Function for reading GOAT energies from comment line of a GOAT xyz file."""
        numbers = [float(m) for m in re.findall(RGX_INT_AND_FLOAT, line)]
        # > Parse the comment line
        try:
            energy_total = numbers[0]
        except (IndexError, ValueError) as err:
            raise ValueError("Could not parse docker energies from comment line.") from err
        properties = Properties(
            energy_total=energy_total,
        )
        return properties

    @classmethod
    def _iter_xyz_structures(
        cls,
        tracked: TrackingTextIO,
        comment_symbols: str | Sequence[str] | None,
        mode: Literal["goat", "docker"],
        n_struc_limit: int | None,
    ) -> Iterator["Properties"]:
        """Yield properties from the buffer until exhausted or the limit is reached."""

        if n_struc_limit is not None and n_struc_limit < 0:
            raise ValueError("n_struc_limit must be None, 0, or a positive integer")

        n_struc = 0
        while True:
            props = cls.from_xyz_buffer(tracked, comment_symbols=comment_symbols, mode=mode)
            if props is None:
                break
            yield props
            n_struc += 1
            if n_struc_limit and n_struc >= n_struc_limit:
                break
