import os
import shutil
from abc import ABC
from pathlib import Path
from typing import cast

__all__ = (
    "BaseStructureFile",
    "XyzFile",
    "PdbFile",
    "GzmtFile",
)


class BaseStructureFile(ABC):
    """
    Class to model structure file.
    The structure file is directly passed to ORCA. This interface does not read or modify the contents of the file.

    Attributes
    ----------
    _type: str
        Type of the structure file.
        Use as prefix for ORCA input: `*<_type>file`
    """

    _type: str

    def __init__(
        self,
        file: Path | str | os.PathLike[str],
        /,
        *,
        charge: int = 0,
        multiplicity: int = 1,
    ):
        self._file: Path
        self.file = cast(Path, file)
        self.charge = charge
        self.multiplicity = multiplicity

    @property
    def file(self) -> Path:
        return self._file

    @file.setter
    def file(self, val: Path | str | os.PathLike[str]) -> None:
        """
        Parameters
        ----------
        val : Path | str | os.PathLike[str]
        """
        self._file = Path(val).expanduser().resolve(strict=True)

    def format_orca(self, working_dir: Path | None, /, *, original_path: bool = False) -> str:
        """
        Format respectively line in ORCA input. If the file lies within the working directory a relative path is
        used. If no working directory is set just the filename is employed.

        Parameters
        ----------
        working_dir : Path | None
            Path to the working directory.
        original_path : bool, default False
            If True, the original path will not be altered.

        Raises
        ------
        ValueError
            If relative path is requested and cannot be resolved.
        """
        filename: str | Path
        if original_path:
            filename = self.file
        elif working_dir is not None:
            filename = self.file.relative_to(working_dir)
        else:
            filename = self.file.name
        return f"*{self._type}file {self.charge} {self.multiplicity} {filename}"

    def copy_to(self, dest: Path, /) -> bool:
        """
        Copy the structure file to the destination.

        Parameters
        ----------
        dest : Path
            Copy the self.file to dest.
            dest can point to a file or a folder. For details see documentation of `shutil.copy()`.

        Raises
        ------
        OSError
            If structure file cannot be copied.

        Returns
        -------
        bool:
            True if the file was copied, False otherwise.
        """
        try:
            shutil.copy(self.file, dest)
            return True
        except shutil.SameFileError:
            # > Ignoring error
            pass
        except OSError as err:
            raise OSError(
                f"Could not copy {self.file} to {dest}. The latter does not exist."
            ) from err
        return False


class XyzFile(BaseStructureFile):
    """
    Class to model .xyz structure file.
    """

    _type = "xyz"


class PdbFile(BaseStructureFile):
    """
    Class to model .pdb structure file.
    """

    _type = "pdb"


class GzmtFile(BaseStructureFile):
    """
    Class to model .gzmt structure file.
    """

    _type = "gzmt"
