import re
from io import StringIO
from os import PathLike
from pathlib import Path
from typing import Literal, Sequence

from opi.utils.textio import TrackingTextIO

__all__ = ("Properties",)

RGX_INT_AND_FLOAT = re.compile(r"[+-]?(?:\d+\.\d*|\.\d+|\d+)(?:[Ee][+-]?\d+)?")


class Properties:
    """
    Class for keeping additional Structure properties found, e.g., in an xyz file.

    Attributes
    ----------
    structure_id : int
        Number of the structure from which the properties are.
    energy_total : float
        Energy of a structure.
    energy_relative : float
        Relative energy of a structure.
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
        Function for reading xyz file and return a Properties object.

        Parameters
        ----------
        xyzfile : Path | str | PathLike[str]
            Name or path to xyz file

        Raises
        --------
        FileNotFoundError
            If the XYZ file cannot be found
        ValueError
            If there is a problem with parsing the XYZ file

        Returns
        --------
        `Properties`:`Properties object extracted from file
        """
        properties_list = cls.from_trj_xyz(xyzfile, struc_limit=1, mode=mode)
        properties = properties_list[0]
        return properties

    @classmethod
    def from_trj_xyz(
        cls,
        trj_file: Path | str | PathLike[str],
        /,
        *,
        mode: Literal["goat", "docker"] = "goat",
        comment_symbols: str | Sequence[str] | None = None,
        struc_limit: int | None = None,
    ) -> "list[Properties]":
        """
        Function for reading multi-xyz file and returning a Properties object.

        Parameters
        ----------
        trj_file : Path | str | PathLike[str]
            Name or path to xyz file with multiple structures
        comment_symbols: str | Sequence[str] | None, default: None
            List of symbols that indicate user comments in the xyz file. User comments are skipped before the actual xyz
            data starts. By default, no user comments are used. White-space only comments are not allowed and are
            silently ignored.
        struc_limit: int | None, default: None
            Limit of structures that should be considered from the trj.xyz file. With the default, None, all structures are
            considered.

        Raises
        --------
        FileNotFoundError
            If the XYZ file cannot be found
        ValueError
            If there is a problem with parsing the XYZ file

        Returns
        --------
        `list[Properties]`:`Properties object extracted from file
        """
        properties_list: list[Properties] = []

        # > converting into Path
        trj_file = Path(trj_file)

        # > Check if file exists
        if not trj_file.exists():
            raise FileNotFoundError(f"XYZ file not found: {trj_file}")

        with trj_file.open() as f_xyz:
            tracked = TrackingTextIO(f_xyz)
            n_struc: int = 0
            while True:
                try:
                    properties = cls.from_xyz_buffer(
                        tracked, comment_symbols=comment_symbols, mode=mode
                    )
                    if properties is None:
                        break
                    properties_list.append(properties)
                except ValueError:
                    raise
                n_struc += 1
                # > Break if limit of allowed structures is reached
                if struc_limit is not None and n_struc >= struc_limit:
                    break
        return properties_list

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

        Raises
        --------
        ValueError
            If there is a problem with parsing the XYZ file

        Returns
        --------
        Properties
            The `Properties` object extracted from file
        """
        properties_list = cls.from_trj_xyz_block(xyz_string, struc_limit=1, mode=mode)
        return properties_list[0]

    @classmethod
    def from_trj_xyz_block(
        cls,
        trj_string: str,
        /,
        *,
        mode: Literal["goat", "docker"] = "goat",
        comment_symbols: str | Sequence[str] | None = None,
        struc_limit: int | None = None,
    ) -> "list[Properties]":
        """
        Function for reading multi-xyz data from string and returning a Properties object.

        Parameters
        ----------
        trj_string : Path | str | PathLike[str]
            String that contains multiple xyz file data (trajectory data)
        comment_symbols: str | Sequence[str] | None, default: None
            List of symbols that indicate user comments in the xyz file. User comments are skipped before the actual xyz
            data starts. By default, no user comments are used. White-space only comments are not allowed and are
            silently ignored.
        struc_limit: int | None, default: None
            Limit of structures that should be read from the trj.xyz string. With the default, None, all structures are
            read.

        Returns
        --------
        `list[Properties]`:`Properties objects extracted from file
        """
        properties_list: list[Properties] = []

        with StringIO(trj_string) as f_xyz:
            tracked = TrackingTextIO(f_xyz)
            n_struc: int = 0
            while True:
                try:
                    properties = cls.from_xyz_buffer(
                        tracked, comment_symbols=comment_symbols, mode=mode
                    )
                    if properties is None:
                        break
                    properties_list.append(properties)
                except ValueError:
                    raise
                n_struc += 1
                # > Break if limit of allowed structures is reached
                if struc_limit is not None and n_struc >= struc_limit:
                    break
        return properties_list

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

        Parameters
        ----------
        xyz_lines: TrackingTextIO
            A buffer that contains xyz file data
        comment_symbols: str | Sequence[str] | None, default: None
            List of symbols that indicate user comments in the xyz file. User comments are skipped before the actual xyz
            data starts. By default, no user comments are used. White-space only comments are not allowed and are
            silently ignored.

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
        while (line := xyz_lines.readline()) != "":
            if not line.lstrip():
                continue
            # > Check for comment line. Ignore empty/whitespace lines
            elif comments_tuple and line.lstrip().startswith(comments_tuple):
                continue
            else:
                break

        # > No data available in the buffer
        if line == "":
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
        if line == "":
            raise ValueError(
                f"Line {xyz_lines.line_number}: Comment line is not present in xyz data"
            )

        # > Analyse comment line
        properties = mode_functions[mode](line)

        # > Skip the remaining structure
        for iline in range(natoms):
            line = xyz_lines.readline()
            # > empty lines are not allowed
            if line == "":
                raise ValueError(f"Line {xyz_lines.line_number}: Incomplete xyz file buffer")

        return properties

    @classmethod
    def docker_energies(cls, line: str) -> "Properties":
        """Function for reading docker energies from string and return a Properties object."""
        numbers = [float(m) for m in re.findall(RGX_INT_AND_FLOAT, line)]
        # > Parse the comment line
        try:
            # > ID of the structure
            structure_id = int(numbers[0])
            # > Total energy is second number (Eh)
            energy_total = numbers[1]
            # > Relative energy is the third number (kcal/mol)
            energy_relative = numbers[2]
        except IndexError:
            raise ValueError("Could not parse docker energies from comment line.")
        properties = Properties(
            structure_id=structure_id, energy_total=energy_total, energy_relative=energy_relative
        )
        return properties

    @classmethod
    def goat_energies(cls, line: str) -> "Properties":
        """Function for reading goat energies from string and return a Properties object."""
        numbers = [float(m) for m in re.findall(RGX_INT_AND_FLOAT, line)]
        # > Parse the comment line
        try:
            energy_total = numbers[0]
        except IndexError:
            raise ValueError("Could not parse docker energies from comment line.")
        properties = Properties(
            energy_total=energy_total,
        )
        return properties
