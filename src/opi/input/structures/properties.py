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
    Class to represent structure properties (e.g., total or relative energies).
    Currently, properties can only be read from XYZ files created with GOAT or DOCKER.

    Attributes
    ----------
    structure_id : int | None, default = None
        Number of the structure, within the XYZ file, from which the properties are.
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
        cls, xyz_file: Path | str | PathLike[str], mode: Literal["goat", "docker"] = "goat"
    ) -> "Properties":
        """
        Function for reading properties from the comment line of a single structure from a (multi-)XYZ file
        and returning a `Properties` object.

        Parameters
        ----------
        xyz_file : Path | str | PathLike[str]
            Name or path to XYZ file.
        mode: Literal["goat", "docker"], default = "goat"
            Define how the comment line should be processed, e.g, it is the comment line from a DOCKER or GOAT run.

        Returns
        --------
        Properties | None
            Properties object extracted from file or None if nothing could be extracted.

        Raises
        --------
        FileNotFoundError
            If the XYZ file cannot be found.
        ValueError
            If there is a problem with parsing the XYZ file.
        EOFError
            If the file is empty.
        """
        return cls.from_trj_xyz(xyz_file, n_struc_limit=1, mode=mode)[0]

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
        Function for reading multi-XYZ file and returning a list of `Properties`.

        Parameters
        ----------
        trj_file : Path | str | PathLike[str]
            Name or path to XYZ file with one or multiple structure(s).
        mode: Literal["goat", "docker"], default = "goat"
            Define how the comment line should be processed, e.g, it is the comment line from a DOCKER or GOAT run.
        comment_symbols: str | Sequence[str] | None, default: None
            List of symbols that indicate user comments in the XYZ data.
            User comments have to start with the given symbol, fill a whole line, and come before the actual XYZ data.
        n_struc_limit: int | None, default: None
            If >0, only read the first n structures.

        Returns
        --------
        list[Properties]
            Properties object extracted from file.

        Raises
        --------
        FileNotFoundError
            If the XYZ file cannot be found.
        ValueError
            If there is a problem with parsing the XYZ file.
        EOFError
            If the file is empty.
        """
        # > converting into Path
        trj_file = Path(trj_file)

        # > Check if file exists
        if not trj_file.exists():
            raise FileNotFoundError(f"XYZ file not found: {trj_file}")

        # > Open file and iterate over structures
        with TrackingTextIO(trj_file.open()) as tracked:
            properties_trj = list(
                cls._iter_xyz_structures(tracked, comment_symbols, mode, n_struc_limit)
            )
            if not properties_trj:
                raise EOFError(f"XYZ file {trj_file} is empty")
            return properties_trj

    @classmethod
    def from_xyz_block(
        cls, xyz_string: str, mode: Literal["goat", "docker"] = "goat"
    ) -> "Properties":
        """
        Function for reading a single XYZ file from a string and returning a `Properties` object.

        Parameters
        ----------
        xyz_string: str
            String that contains XYZ file data.
        mode: Literal["goat", "docker"], default = "goat"
            Define how the comment line should be processed, e.g, it is the comment line from a DOCKER or GOAT run.

        Returns
        --------
        Properties
            The `Properties` object extracted from string.

        Raises
        --------
        ValueError
            If there is a problem with parsing the XYZ string or if `n_struc_limit` is negative or 0.
        EOFError
            If the string is empty.
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
        Function for reading trajectory data from string and returning a list of `Properties`.

        Parameters
        ----------
        trj_string : Path | str | PathLike[str]
            String that contains one or multiple XYZ blocks (trajectory data).
        mode: Literal["goat", "docker"], default = "goat"
            Define how the comment line should be processed, e.g, it is the comment line from a DOCKER or GOAT run.
        comment_symbols: str | Sequence[str] | None, default: None
            List of symbols that indicate user comments in the XYZ data.
            User comments have to start with the given symbol, fill a whole line, and come before the actual XYZ data.
        n_struc_limit: int | None, default: None
            If >0, only read the first n structures.

        Returns
        --------
        list[Properties]: List of Properties extracted from string.

        Raises
        --------
        ValueError
            If there is a problem with parsing the XYZ data or if `n_struc_limit` is <= 0.
        EOFError
            If the string is empty.
        """
        with TrackingTextIO(trj_string) as tracked:
            properties_trj = list(
                cls._iter_xyz_structures(tracked, comment_symbols, mode, n_struc_limit)
            )
            if not properties_trj:
                raise EOFError("No XYZ data in string.")
            return properties_trj

    @classmethod
    def from_xyz_buffer(
        cls,
        xyz_lines: TrackingTextIO,
        /,
        *,
        comment_symbols: str | Sequence[str] | None = None,
        mode: Literal["goat", "docker"] = "goat",
    ) -> "Properties":
        """
        Function for reading from the comment line of a XYZ file from a buffer and converting it to a `Properties`
        object.

        Parameters
        ----------
        xyz_lines: TrackingTextIO
            A buffer that contains XYZ file data.
        comment_symbols: str | Sequence[str] | None, default: None
            List of symbols that indicate user comments in the XYZ data.
            User comments have to start with the given symbol, fill a whole line, and come before the actual XYZ data.
        mode: Literal["goat", "docker"], default = "goat"
            Define how the comment line should be processed, e.g, it is the comment line from a DOCKER or GOAT run.

        Returns
        --------
        Properties
            The `Properties` object extracted from the buffer.

        Raises
        --------
        ValueError
            When no valid properties can be read from the input buffer or the corresponding structure is incomplete.
        EOFError
            When no data is in the buffer.
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

        if not line:
            raise EOFError("No data available in the buffer.")

        # > Fetch number of atoms
        try:
            natoms = int(line.split()[0])
        except (ValueError, IndexError) as err:
            raise ValueError(
                f"Line {xyz_lines.line_number}: Could not read number of atoms at the beginning of XYZ data"
            ) from err

        # > Comment line
        line = xyz_lines.readline()
        if not line:
            raise ValueError(
                f"Line {xyz_lines.line_number}: Comment line is not present in XYZ data"
            )

        # > Analyse comment line
        properties = mode_functions[mode](line)

        # > Skip the remaining structure
        for iline in range(natoms):
            line = xyz_lines.readline()
            # > empty lines are not allowed
            if not line:
                raise ValueError(f"Line {xyz_lines.line_number}: Incomplete XYZ file buffer")

        return properties

    @classmethod
    def docker_energies(cls, line: str) -> "Properties":
        """Function for reading DOCKER energies from comment line of a DOCKER XYZ file and return them in `Properties`
        object."""
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
            raise ValueError("Could not parse DOCKER energies from comment line.") from err
        properties = Properties(
            structure_id=structure_id, energy_total=energy_total, energy_relative=energy_relative
        )
        return properties

    @classmethod
    def goat_energies(cls, line: str) -> "Properties":
        """Function for reading GOAT energies from comment line of a GOAT XYZ file and return them in `Properties`
        object."""
        numbers = [float(m) for m in re.findall(RGX_INT_AND_FLOAT, line)]
        # > Parse the comment line
        try:
            energy_total = numbers[0]
        except (IndexError, ValueError) as err:
            raise ValueError("Could not parse GOAT energies from comment line.") from err
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
        """
        Yield properties from the buffer until exhausted or the limit is reached.

        Parameters
        ----------
        tracked: TrackingTextIO
            A buffer that contains XYZ file data.
        comment_symbols: str | Sequence[str] | None, default: None
            List of symbols that indicate user comments in the XYZ data.
            User comments have to start with the given symbol, fill a whole line, and come before the actual XYZ data.
        mode: Literal["goat", "docker"], default = "goat"
            Define how the comment line should be processed, e.g, it is the comment line from a DOCKER or GOAT run.
        n_struc_limit: int | None, default: None
            If >0, only read the first n structures.

        Returns
        --------
        Iterator["Properties"]
            Iterator of `Properties` object extracted from the buffer.

        Raises
        --------
        ValueError
            If `n_struc_limit` is negative or zero.
        """

        if n_struc_limit is not None and n_struc_limit <= 0:
            raise ValueError("n_struc_limit must be None, or a positive integer")

        n_struc = 0
        while True:
            try:
                props = cls.from_xyz_buffer(tracked, comment_symbols=comment_symbols, mode=mode)
            except EOFError:
                break
            yield props
            n_struc += 1
            if n_struc_limit and n_struc >= n_struc_limit:
                break
