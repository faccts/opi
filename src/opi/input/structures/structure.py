import copy
import re
from collections.abc import Iterable, Iterator, Sequence
from os import PathLike
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast
from warnings import warn

import numpy as np
import numpy.typing as npt

# > RDKIT
from rdkit.Chem import AddHs, MolFromSmiles, MolFromXYZBlock
from rdkit.Chem.rdDistGeom import EmbedMolecule

from opi.input.structures.atom import (
    Atom,
    EmbeddingPotential,
    GhostAtom,
    PointCharge,
)
from opi.input.structures.coordinates import Coordinates
from opi.utils.element import ATOMIC_MASSES_FROM_ELEMENT, Element
from opi.utils.molbar import MolBarMode, call_molbar, requires_molbar
from opi.utils.rotconst import (
    PrincipalMoments,
    RotationalConstants,
    RotorType,
    moment_to_mhz,
)
from opi.utils.tracking_text_io import TrackingTextIO

__all__ = ("Structure",)


if TYPE_CHECKING:
    from ase import Atoms as AseAtoms  # noqa: F401
    from rdkit.Chem import Mol as RdkitMol

RGX_FRAG_ID = re.compile(r"(?<=\()\d+(?=\))")
RGX_ATOM_SYMBOL_FRAG_ID = re.compile(r"(?P<elem>[A-Za-z]{1,2})(\((?P<frag_id>\d+)\))?")


class Structure:
    """
    Class to model internal structure for ORCA calculations.

    Attributes
    ----------
    atoms: list[Atom | EmbeddingPotential | GhostAtom | PointCharge]
        Atoms in the molecule
    charge: int
        Charge of structure
    multiplicity: int
        Multiplicity of structure
    origin: Path | str
        Origin of the molecule, usually path to a file or some identifier

    """

    def __init__(
        self,
        atoms: Atom
        | EmbeddingPotential
        | GhostAtom
        | PointCharge
        | Sequence[Atom | EmbeddingPotential | GhostAtom | PointCharge]
        | Iterable[Atom | EmbeddingPotential | GhostAtom | PointCharge],
        charge: int = 0,
        multiplicity: int = 1,
        origin: Path | str | None = None,
    ) -> None:
        # // Atoms
        self._atoms: list[Atom | EmbeddingPotential | GhostAtom | PointCharge] = []
        self.atoms = cast(list[Atom | EmbeddingPotential | GhostAtom | PointCharge], atoms)
        # // Charge
        self._charge: int
        self.charge = charge
        # // Multiplicity
        self._multiplicity: int
        self.multiplicity = multiplicity

        # > Origin of the molecule. Typically, the path to the file or some identifier
        self.origin: Any | None = origin

    @property
    def atoms(self) -> list[Atom | EmbeddingPotential | GhostAtom | PointCharge]:
        return self._atoms

    @atoms.setter
    def atoms(
        self,
        value: Atom
        | EmbeddingPotential
        | GhostAtom
        | PointCharge
        | Sequence[Atom | EmbeddingPotential | GhostAtom | PointCharge]
        | Iterable[Atom | EmbeddingPotential | GhostAtom | PointCharge],
    ) -> None:
        """
        Parameters
        ----------
        value : Atom | DummyAtom| EmbeddingPotential | GhostAtom | PointCharge | Sequence[Atom | EmbeddingPotential | GhostAtom | PointCharge]| Iterable[Atom | EmbeddingPotential | GhostAtom | PointCharge]
        """
        if not isinstance(value, (Sequence, Iterable)):
            # > Assume a single Atom object
            value = [value]
        self._atoms = list(value)

    @property
    def real_atoms(self) -> list[Atom]:
        """
        Return only real `Atom` instances, excluding `GhostAtom`, `PointCharge`,
        and `EmbeddingPotential`. Note that `GhostAtom` is a subclass of `Atom`,
        so `type(a) is Atom` is used rather than `isinstance`.
        """
        return [a for a in self.atoms if type(a) is Atom]

    @property
    def charge(self) -> int:
        return self._charge

    @charge.setter
    def charge(self, value: int) -> None:
        """
        Parameters
        ----------
        value : int
        """
        if not isinstance(value, int):
            raise TypeError(f"{self.__class__.__name__}.charge: must be an integer")
        self._charge = value

    @property
    def multiplicity(self) -> int:
        return self._multiplicity

    @multiplicity.setter
    def multiplicity(self, value: int) -> None:
        """
        Parameters
        ----------
        value : int
        """
        if not isinstance(value, int):
            raise TypeError(f"{self.__class__.__name__}.multiplicity: must be an integer")
        elif value < 1:
            raise ValueError(f"{self.__class__.__name__}.multiplicity: must be positive")
        self._multiplicity = value

    @property
    def nelectrons(self) -> int:
        """
        Returns the number of electrons based on the cardinal numbers of atoms in the structure and the overall
        molecular charge. Note that the number of electrons returned by this function can be negative and should be
        checked!

        Returns
        ----------
        nelectrons : int
            Returns the number of electrons for the structure. Can be negative!
        """
        nelectrons = 0
        for atom in self.atoms:
            if isinstance(atom, Atom):
                nelectrons += atom.element.atomic_number
        nelectrons -= self.charge
        return nelectrons

    @property
    def nelec_is_odd(self) -> bool:
        """Returns a boolean indicating if the number of electrons is odd. Does not check for negative electrons."""
        return self.nelectrons % 2 == 1

    @property
    def nelec_is_even(self) -> bool:
        """Returns a boolean indicating if the number of electrons is even. Does not check for negative electrons."""
        return self.nelectrons % 2 == 0

    @property
    def multiplicity_is_odd(self) -> bool:
        """Returns a boolean indicating if the multiplicity is odd."""
        return self.multiplicity % 2 == 1

    @property
    def multiplicity_is_even(self) -> bool:
        """Returns a boolean indicating if the multiplicity is even."""
        return self.multiplicity % 2 == 0

    @property
    def nelec_and_multiplicity_even(self) -> bool:
        """Returns a boolean indicating if the number of electrons and the multiplicity are even."""
        return self.nelec_is_even and self.multiplicity_is_even

    @property
    def nelec_and_multiplicity_odd(self) -> bool:
        """Returns a boolean indicating if the number of electrons and the multiplicity are odd."""
        return self.nelec_is_odd and self.multiplicity_is_odd

    @property
    def multiplicity_is_possible(self) -> bool:
        """Returns a boolean indicating if the multiplicity can be realized with the number of electrons."""
        return not (self.nelec_and_multiplicity_even or self.nelec_and_multiplicity_odd)

    def set_ls_multiplicity(self) -> None:
        """
        Sets `multiplicity` to the lowest possible multiplicity based on the number of electrons (`multiplicity`
        will either be set to 1 or 2).
        """
        if self.nelec_is_even:
            self.multiplicity = 1
        else:
            self.multiplicity = 2

    @classmethod
    def combine_molecules(cls, structure1: "Structure", structure2: "Structure") -> "Structure":
        """
        function to combine two objects of `Molecule` class

        Parameters
        ----------
        structure1: Structure
            Define first structure to be combined
        structure2: Structure
            Define second structure to be combined

        Returns
        -------
        Structure:Combined structure
        """
        # data from structure2 will be concatenated to end of data for structure1
        new_atoms = structure1.atoms + structure2.atoms
        return Structure(atoms=new_atoms)

    def centered_structure(self) -> "Structure":
        """
        Return a new `Structure` centered at its centroid.
        Only `Atom` instances contribute to the centroid calculation;
        `GhostAtom`, `PointCharge`, and `EmbeddingPotential` are ignored.

        Returns
        -------
        Structure
            New `Structure` with centered coordinates.
        """
        new_structure = copy.deepcopy(self)
        real_indices = [i for i, a in enumerate(new_structure.atoms) if type(a) is Atom]
        centroid = new_structure.get_coordinates(only_atoms=real_indices).mean(axis=0)
        new_structure.set_coordinates(new_structure.get_coordinates() - centroid)
        return new_structure

    def format_orca(self) -> str:
        """
        Returns string representation of Molecule
        Iteratively calls Atom.format_orca() and compiles it all together to create string representation of Molecule

        Returns
        -------
            str:
                String representation of Molecule
        """
        # > First we check whether the multiplicity is possible with the numbers of electrons and warn if not
        if self.nelec_and_multiplicity_even:
            warn(
                "Inconsistent input: an even number of electrons cannot have even multiplicity",
                UserWarning,
            )

        if self.nelec_and_multiplicity_odd:
            warn(
                "Inconsistent input: an odd number of electrons cannot have odd multiplicity",
                UserWarning,
            )

        # String representation of Molecule class , mostly used for .xyz file
        text = f"* xyz {self.charge} {self.multiplicity}\n"
        for atom in self.atoms:
            text += f"{atom.format_orca()}\n"
        text += "*"

        return text

    def add_atom(
        self,
        new_atom: Atom | EmbeddingPotential | GhostAtom | PointCharge,
        position: int | None = None,
    ) -> None:
        """
        Adds Atom object at specified index.
        If index is None, Atom object appended to end of list

        Parameters
        ----------
        new_atom : Atom
            Atom model to be added to self.atoms
        position : int | None, default = None
            position at which Atom is supposed to be added , default value None

        Raises
        ------
        ValueError
          if index is an invalid value
        """
        # adds atom at a specified position
        if position is not None and (position < 0 or position > len(self.atoms)):
            raise ValueError("Invalid position")
        # In the case that e is a str , it is converted into object from Element
        # New atom added to self.atoms
        if position is None:
            self.atoms.append(new_atom)
        else:
            self.atoms.insert(position, new_atom)

    def delete_atom(self, index: int) -> None:
        """
        Deletes Atom at specified index

        Parameters
        ----------
        index : int
            specifies index of Atom to be deleted

        Raises
        ------
        ValueError
          if index is invalid value
        """
        # deletes atom at specific index
        if 0 <= index < len(self.atoms):
            self.atoms.pop(index)
        else:
            raise ValueError("Invalid index")

    def replace_atom(
        self, new_atom: Atom | EmbeddingPotential | GhostAtom | PointCharge, index: int
    ) -> None:
        """
        replaces Atom at index with a new Atom object

        Parameters
        ----------
        new_atom : Atom | EmbeddingPotential | GhostAtom | PointCharge
            new Atom object to replace the old Atom object
        index : int
            index of Atom to be replaced

        Raises
        ------
        ValueError
          if index is invalid value
        """
        # replaces atom at specific index with new_index
        if 0 <= index < len(self.atoms):
            self.atoms[index] = new_atom
        else:
            raise ValueError("Invalid index")

    def extract_substructure(self, indexes: list[int]) -> "Structure":
        """
        returns Molecule object that is a sub-molecule specified by indexes.

        Parameters
        ----------
        indexes : list[int]
            specifies indexes of Atom objects to be extracted

        Returns
        -------
        Molecule: new Molecule object
        """
        return Structure(atoms=[self.atoms[i] for i in indexes])

    def get_coordinates(
        self,
        only_atoms: Sequence[int] = (),
    ) -> npt.NDArray[np.float64]:
        """
        Return the coordinates of atoms as a numpy array.

        Parameters
        ----------
        only_atoms : Sequence[int], default: ()
            Indices of atoms in `self.atoms` to include. If empty, all
            atoms are included.

        Returns
        -------
        npt.NDArray[np.float64], shape (N, 3)
            Coordinates in the same order as the selected atoms.

            The `dtype` is explicitly set to `float64` to guarantee the return type
            regardless of how coordinates are stored internally.
        """
        atom_list = [self.atoms[i] for i in only_atoms] if only_atoms else self.atoms
        return np.array([a.coordinates.coordinates for a in atom_list], dtype=np.float64)

    def get_coordinates_at_centroid(
        self,
        only_atoms: Sequence[int] = (),
    ) -> npt.NDArray[np.float64]:
        """
        Return coordinates translated to the centroid.

        Parameters
        ----------
        only_atoms : Sequence[int], default: ()
            Indices of atoms in `self.atoms` to include. If empty, all
            atoms are included.

        Returns
        -------
        npt.NDArray[np.float64], shape (N, 3)
            Centroid-translated coordinates in the same order as the selected atoms.
        """
        coords = self.get_coordinates(only_atoms=only_atoms)
        return coords - np.mean(coords, axis=0, dtype=np.float64)

    def set_coordinates(self, coords: npt.NDArray[np.float64]) -> None:
        """
        Update the coordinates of all atoms in-place.

        Parameters
        ----------
        coords : npt.NDArray[np.float64], shape (N, 3)
            New coordinates for all atoms in the same order as `self.atoms`.

        Raises
        ------
        ValueError
            If *coords* shape does not match the number of atoms.
        """
        coords = np.asarray(coords, dtype=np.float64)
        if coords.shape != (len(self.atoms), 3):
            raise ValueError(
                f"coords shape {coords.shape} does not match expected ({len(self.atoms)}, 3)"
            )
        for atom, new_coord in zip(self.atoms, coords):
            atom.coordinates = new_coord

    def update_coordinates(self, array: npt.NDArray[np.float64]) -> None:
        """
        Validates dimensions of array first
        replace all coordinates of all atoms in Molecule object.
        Calls Atom.update_coordinates() iteratively , replacing the Atom.coordinates with rows from array argument

        Parameters
        ----------
        array : npt.NDArray[np.float64]
            new coordinates

        Raises
        ------
        ValueError
          in the case of wrong dimensions
        """
        # function to replace self.coord_block with another numpy array
        # dimensions checked first before proceeding
        if array.shape != (len(self.atoms), 3):
            raise ValueError(
                f"Invalid dimension ({array.shape}) coordinates. Expected shape: {(len(self.atoms), 3)}"
            )

        for i in range(len(array)):
            self.atoms[i].coordinates = array[i]

    def to_xyz_block(self) -> str:
        """Function to generate XYZ block"""
        # > Comment line will be empty
        xyz_block = f"{len(self)}\n\n"
        for atom in self.atoms:
            xyz_block += atom.format_xyz_line() + "\n"
        return xyz_block + "\n"

    @classmethod
    def from_xyz(
        cls,
        xyzfile: Path | str | PathLike[str],
        /,
        *,
        charge: int = 0,
        multiplicity: int = 1,
    ) -> "Structure":
        """
        Function for reading a xyz file and converting it to a molecular Structure

        Parameters
        ----------
        xyzfile : Path | str | PathLike[str]
            Name or path to xyz file
        charge : int, default: 0
            Charge of the molecule
        multiplicity : int, default: 1
            Electron spin multiplicity of the molecule

        Raises
        --------
        FileNotFoundError
            If the XYZ file cannot be found
        ValueError
            If there is a problem with parsing the XYZ file

        Returns
        --------
        `Structure`:`Structure object extracted from file
        """
        structures = cls.from_trj_xyz(
            xyzfile, charge=charge, multiplicity=multiplicity, n_struc_limit=1
        )
        return structures[0]

    @classmethod
    def from_trj_xyz(
        cls,
        trj_file: Path | str | PathLike[str],
        /,
        *,
        charge: int = 0,
        multiplicity: int = 1,
        comment_symbols: str | Sequence[str] | None = None,
        n_struc_limit: int | None = None,
    ) -> "list[Structure]":
        """
        Function for reading a xyz trajectory file and converting it to a list of molecular Structure

        Parameters
        ----------
        trj_file : Path | str | PathLike[str]
            Name or path to xyz file with one or multiple structure(s)
        charge : int, default: 0
            Charge of the molecule
        multiplicity : int, default: 1
            Electron spin multiplicity of the molecule
        comment_symbols: str | Sequence[str] | None, default: None
            List of symbols that indicate user comments in the xyz file. User comments are skipped before the actual xyz
            data starts. By default, no user comments are used. White-space only comments are not allowed and are
            silently ignored.
        n_struc_limit: int | None, default: None
            If >0, only read the first n structures.

        Raises
        --------
        FileNotFoundError
            If the XYZ file cannot be found.
        ValueError
            If there is a problem with parsing the XYZ file.
        EOFError
            If the file is empty.

        Returns
        --------
        list[Structure]: Molecular structure objects extracted from the xyz file.
        """
        # > converting into Path
        trj_file = Path(trj_file)

        # > Check if file exists
        if not trj_file.exists():
            raise FileNotFoundError(f"XYZ file not found: {trj_file}")

        with TrackingTextIO(trj_file.open()) as tracked:
            structures = list(
                cls._iter_xyz_structures(
                    tracked,
                    charge=charge,
                    multiplicity=multiplicity,
                    comment_symbols=comment_symbols,
                    n_struc_limit=n_struc_limit,
                )
            )
            if not structures:
                raise EOFError(f"XYZ file {trj_file} is empty")
            return structures

    @classmethod
    def from_xyz_block(
        cls,
        xyz_string: str,
        /,
        *,
        charge: int = 0,
        multiplicity: int = 1,
    ) -> "Structure":
        """
        Function for reading a xyz file from a string and converting it to a molecular Structure

        Parameters
        ----------
        xyz_string: str
            String that contains xyz file data
        charge : int, default: 0
            Charge of the molecule
        multiplicity : int, default: 1
            Electron spin multiplicity of the molecule

        Raises
        --------
        ValueError
            If there is a problem with parsing the XYZ file

        Returns
        --------
        Structure
            The `Structure` object extracted from file
        """
        return cls.from_trj_xyz_block(
            xyz_string, charge=charge, multiplicity=multiplicity, n_struc_limit=1
        )[0]

    @classmethod
    def from_trj_xyz_block(
        cls,
        trj_string: str,
        /,
        *,
        charge: int = 0,
        multiplicity: int = 1,
        comment_symbols: str | Sequence[str] | None = None,
        n_struc_limit: int | None = None,
    ) -> "list[Structure]":
        """
        Function for reading a XYZ trajectory data string and converting it to a list of molecular Structure

        Parameters
        ----------
        trj_string : Path | str | PathLike[str]
            String that contains multiple xyz blocks (trajectory data)
        charge : int, default: 0
            Charge of the molecule
        multiplicity : int, default: 1
            Electron spin multiplicity of the molecule
        comment_symbols: str | Sequence[str] | None, default: None
            List of symbols that indicate user comments in the xyz file. User comments are skipped before the actual xyz
            data starts. By default, no user comments are used. White-space only comments are not allowed and are
            silently ignored.
        n_struc_limit: int | None, default: None
            If >0, only read the first n structures.

        Returns
        --------
        list[Structure]: `Structure objects extracted from file

        Raises
        --------
        EOFError
            If the string is empty
        """
        with TrackingTextIO(trj_string) as tracked:
            structures = list(
                cls._iter_xyz_structures(
                    tracked,
                    charge=charge,
                    multiplicity=multiplicity,
                    comment_symbols=comment_symbols,
                    n_struc_limit=n_struc_limit,
                )
            )
            if not structures:
                raise EOFError("XYZ string is empty")
            return structures

    @classmethod
    def from_xyz_buffer(
        cls,
        xyz_lines: TrackingTextIO,
        *,
        charge: int = 0,
        multiplicity: int = 1,
        comment_symbols: str | Sequence[str] | None = None,
    ) -> "Structure":
        """
        Function for reading a xyz file from a buffer and converting it to a molecular Structure.

        Parameters
        ----------
        xyz_lines: TrackingTextIO
            A buffer that contains xyz file data
        charge : int, default: 0
            Molecular charge of the structure.
        multiplicity: int, default: 1
            Electron spin multiplicity of the structure.
        comment_symbols: str | Sequence[str] | None, default: None
            List of symbols that indicate user comments in the xyz file. User comments are skipped before the actual xyz
            data starts. By default, no user comments are used. White-space only comments are not allowed and are
            silently ignored.

        Returns
        --------
        Structure
            The `Structure` object extracted from the buffer.

        Raises
        --------
        ValueError
            When no valid structure can be read from the input buffer.
        EOFError
            When no data is in the buffer.
        """
        # > Try reading the string
        atoms: list[Atom] = []
        comments_tuple: tuple[str, ...] | None = None

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

        if not line:
            raise EOFError("No data available in the buffer.")

        # > Fetch number of atoms
        try:
            natoms = int(line.split()[0])
        except (ValueError, IndexError) as err:
            raise ValueError(
                f"Line {xyz_lines.line_number}: Could not read number of atoms at the beginning of xyz data"
            ) from err
        # > Skipping comment line
        if xyz_lines.readline() == "":
            raise ValueError(
                f"Line {xyz_lines.line_number}: Comment line is not present in xyz data"
            )

        # > Save position before coordinate lines start
        pos = xyz_lines.tell()

        # Read the atoms
        while line := xyz_lines.readline():
            # > Line should have at least 4 columns
            atom_cols = line.split()

            if len(atom_cols) < 4:
                # > If data is complete we can leave the loop
                if natoms == len(atoms):
                    # See if current line is start of next xyz block
                    try:
                        # check for natoms in line
                        int(line.split()[0])
                        # if it is, go back to last position
                        xyz_lines.seek(pos)
                        break
                    # if it is not, we do not have to change the position
                    except (IndexError, ValueError):
                        break
                # If read is not complete the line is invalid
                else:
                    raise ValueError(
                        f"Line {xyz_lines.line_number}: Invalidly formatted coordinate line"
                    )

            # > Get atom symbol.
            # >> First check if we have combination of atom symbol + fragment id
            match_atom_sym_frag_id = RGX_ATOM_SYMBOL_FRAG_ID.match(line.lstrip())
            if not match_atom_sym_frag_id:
                raise ValueError(f"Line {xyz_lines.line_number}: Could not find atom symbol.")

            atom_sym = match_atom_sym_frag_id.group("elem")
            try:
                element = Element(atom_sym)
            except Exception as err:
                raise ValueError(
                    f"Line {xyz_lines.line_number}: Invalid atom symbol: {atom_sym}"
                ) from err

            # > Fragment id
            # >> First, let's assume columns 2 through 4 are the coordinates.
            coords_cols = atom_cols[1:4]

            # > Check if the fragment id follows the atom symbol directly or is in a column of its own.
            if not (match_frag_id := match_atom_sym_frag_id.group("frag_id")):
                if match_frag_id := RGX_FRAG_ID.match(atom_cols[1]):
                    # > Coordinates are in columns 3 through 5
                    coords_cols = atom_cols[2:5]

            # > Convert string fragment id to integer
            frag_id = None
            if match_frag_id:
                try:
                    frag_id = int(match_frag_id)
                except ValueError as err:
                    raise ValueError(
                        f"Line {xyz_lines.line_number}: Invalid fragment id: {match_frag_id}"
                    ) from err

            # > Pass coordinates
            # // X
            try:
                coord_x = float(coords_cols[0])
            except (ValueError, IndexError) as err:
                raise ValueError(
                    f"Line {xyz_lines.line_number}: Invalid X coordinate: {atom_cols[1]}"
                ) from err
            # // Y
            try:
                coord_y = float(coords_cols[1])
            except (ValueError, IndexError) as err:
                raise ValueError(
                    f"Line {xyz_lines.line_number}: Invalid Y coordinate: {atom_cols[2]}"
                ) from err
            # // Z
            try:
                coord_z = float(coords_cols[2])
            except (ValueError, IndexError) as err:
                raise ValueError(
                    f"Line {xyz_lines.line_number}: Invalid Z coordinate: {atom_cols[3]}"
                ) from err

            # > Adding atom
            atoms.append(
                Atom(
                    element=element,
                    coordinates=Coordinates(coordinates=(coord_x, coord_y, coord_z)),
                    fragment_id=frag_id,
                )
            )

            # > Save last position in case the next line is the next xyz block
            pos = xyz_lines.tell()
        # << END OF LOOP

        # > Check number of atoms declared in file agrees with apparent number of atoms.
        if natoms != len(atoms):
            raise ValueError(f"{natoms} were expected but {len(atoms)} were found")

        return Structure(
            atoms=atoms,
            charge=charge,
            multiplicity=multiplicity,
        )

    @classmethod
    def from_smiles(
        cls,
        smiles: str,
        /,
        *,
        charge: int | None = None,
        multiplicity: int | None = None,
    ) -> "Structure":
        """
        Function to read SMILES string and convert string to 3D coordinate structure and create Molecule object with it
        to store in self.molecule.

        Parameters
        ----------
        smiles : str
            SMILES string to be converted
        charge : int | None
            Charge of the molecule, will overwrite charge obtained from SMILES string
        multiplicity : int | None
            Electron spin multiplicity of the molecule, will overwrite multiplicity obtained from SMILES
            (which is always 1 by default)

        Returns
        --------
        `Structure`:`Structure object extracted from file

        Raises
        ------
        RuntimeError
            If EmbedMolecule() is unsuccessful
        """
        mol = MolFromSmiles(smiles)
        if not mol:
            raise ValueError(f"Invalid SMILES string: {smiles}")

        mol = AddHs(mol)
        if not mol:
            raise ValueError("Error when running AddHs")

        res = EmbedMolecule(mol)
        if res < 0:
            raise RuntimeError("Failed to embed molecule")

        return cls.from_rdkitmol(mol, charge=charge, multiplicity=multiplicity)

    @classmethod
    def from_rdkitmol(
        cls,
        mol: "RdkitMol",
        /,
        *,
        charge: int | None = None,
        multiplicity: int | None = None,
    ) -> "Structure":
        """
        Function to convert a RDKit Mol object to Structure object

        Parameters
        ----------
        mol : RdkitMol
            RDKit Mol object to be converted
        charge : int | None
            Charge of the molecule, will overwrite charge obtained from RDKit Mol
        multiplicity : int | None
            Electron spin multiplicity of the molecule, will overwrite multiplicity obtained from RDKit Mol

        Returns
        ---------
        `Structure` : Structure object created from information given by RDKit Mol object
        """

        # Compute 3D coordinates if needed
        if not mol.GetConformer().Is3D():
            res = EmbedMolecule(mol)
            if res < 0:
                raise RuntimeError("Failed to embed molecule")

        conformer = mol.GetConformer()

        # Extract atoms
        atoms = []
        # RDKit saves charges and radical electrons as atomic properties
        # so to obtain the molecular charge and multiplicity we have to sum them
        rd_charge: int = 0
        rd_radical_electrons: int = 0
        for atom in mol.GetAtoms():  # type: ignore
            idx = atom.GetIdx()
            element = atom.GetSymbol()
            rd_charge += atom.GetFormalCharge()
            rd_radical_electrons += atom.GetNumRadicalElectrons()
            pos = conformer.GetAtomPosition(idx)
            atoms.append(Atom(element=Element(element), coordinates=pos))

        # multiplicity is the number of open-shell/radical electrons + 1
        rd_multiplicity = rd_radical_electrons + 1

        # if nothing is enforced, we use the rdkit Mol charge
        if charge is None:
            charge = rd_charge

        # if nothing is enforced, we use the rdkit Mol multiplicity
        if multiplicity is None:
            multiplicity = rd_multiplicity

        return Structure(atoms=atoms, charge=charge, multiplicity=multiplicity)

    def to_rdkitmol(self, structure: "Structure", /) -> "RdkitMol":
        """
        Function to convert Molecule object to RDKit Mol object
        The Structure is converted into XYZ file format, which is then read by RDKit.

        Parameters
        ----------
        structure : `Structure`
            Molecule object to be converted

        Returns
        -------
        RdkitMol : RDKit Mol object generated from `Structure` object
        """

        xyz_block = structure.to_xyz_block()
        return MolFromXYZBlock(xyz_block)

    def __len__(self) -> int:
        return len(self.atoms)

    @classmethod
    def from_ase(
        cls, ase_atoms: "AseAtoms", *, charge: int | None = None, multiplicity: int | None = None
    ) -> "Structure":
        """
        Function to generate Structure from `Atoms` object from the Atomic Simulation Environment (ASE).
        Since ORCA and OPI do not support structures with periodic boundary conditions these are ignored.

        Parameters
        ----------
        ase_atoms : AseAtoms
            The object "Atoms" from ase
        charge : int | None, default:  None
            Optional charge of the molecule, will overwrite charge from ase.
        multiplicity : int | None, default:  None
            Optional multiplicity of the molecule, will overwrite multiplicity from ase.

        Returns
        ----------
        Structure
            The Structure object generated from AseAtoms object

        Raises
        ----------
        ValueError
            If the ASE object does not include a usable structure.
        """
        symbols = ase_atoms.get_chemical_symbols()

        # > Try to get the positions from AseAtoms object as Numpy array.
        try:
            positions = np.asarray(ase_atoms.get_positions(), dtype=np.float64)
        except (TypeError, ValueError) as err:
            raise TypeError("Could not convert positions to a float64 NumPy array") from err

        # > Check that the positions array has at least two dimensions
        if positions.ndim < 2:
            raise TypeError("Positions array has to be at least two-dimensional")

        # > Check that the number of element symbols matches the number of atomic coordinates
        if len(symbols) != positions.shape[0]:
            raise ValueError(f"{len(symbols)} symbols and {positions.shape[0]} positions")

        atoms = []
        # > Build a list of atoms from element symbols and positions
        for iatom, ase_atom in enumerate(zip(symbols, positions)):
            symbol, raw_position = ase_atom
            # > Indicate the type for static type checking with mypy
            position = np.asarray(raw_position, dtype=np.float64)

            # > Get Element symbol
            try:
                element = Element(symbol)
            except (ValueError, IndexError):
                raise ValueError(f"Atom {iatom}: Could not convert {ase_atom[0]} to element symbol")

            coords_cols: list[float] = position.tolist()

            if len(coords_cols) < 3:
                raise ValueError(f"Invalid coordinates for atom number: {iatom}")

            # > Pass coordinates
            # // X
            try:
                coord_x = float(coords_cols[0])
            except (ValueError, IndexError) as err:
                raise ValueError(f"Atom {iatom}: Invalid X coordinate") from err
            # // Y
            try:
                coord_y = float(coords_cols[1])
            except (ValueError, IndexError) as err:
                raise ValueError(f"Atom {iatom}: Invalid Y coordinate") from err
            # // Z
            try:
                coord_z = float(coords_cols[2])
            except (ValueError, IndexError) as err:
                raise ValueError(f"Atom {iatom}: Invalid Z coordinate") from err

            # > Adding atom
            atoms.append(
                Atom(
                    element=element,
                    coordinates=Coordinates(coordinates=(coord_x, coord_y, coord_z)),
                )
            )

        # > Get charge if not supplied
        if charge is None:
            charges = ase_atoms.get_initial_charges()
            charge = int(round(np.sum(charges)))

        # > Get magnetic moment if no multiplicity supplied
        if multiplicity is None:
            magmoms = ase_atoms.get_initial_magnetic_moments()
            total_magnetization = np.sum(magmoms)
            spin = int(round(abs(total_magnetization)))
            multiplicity = spin + 1

        return cls(atoms=atoms, charge=charge, multiplicity=multiplicity)

    @classmethod
    def from_lists(
        cls,
        symbols: list[str | int],
        coordinates: list[tuple[float, float, float]],
        charge: int = 0,
        multiplicity: int = 1,
    ) -> "Structure":
        """
        Function for generating the Structure object from symbols and position lists. They are required to have the
        same length and need fulfill the typing.

        Parameters
        ----------
        symbols : list[str | int]
            List of symbols for elements, either as string or as atomic number
        coordinates: list[tuple[float, float, float]]
            List of tuples containing coordinates
        charge : int, default:  0
            Optional charge for the structure
        multiplicity : int, default:  1
            Optional multiplicity for the structure

        Returns
        ----------
        Structure
            The Structure object initialized from given lists.

        """
        atoms = []
        if len(symbols) != len(coordinates):
            raise ValueError(f"{len(symbols)} symbols and {len(coordinates)} coordinates")

        for element, coords in zip(symbols, coordinates):
            if isinstance(element, int):
                element = Element.from_atomic_number(element)
            elif isinstance(element, str):
                element = Element(element)
            else:
                raise ValueError(f"{element} cannot be converted to an element.")
            # > assert to make mypy happy
            assert isinstance(element, Element)
            atoms.append(Atom(element=element, coordinates=coords))

        return cls(atoms=atoms, charge=charge, multiplicity=multiplicity)

    # ------------------------------------------------------------------ #
    #  MOLBAR                                                            #
    # ------------------------------------------------------------------ #

    @requires_molbar
    def calculate_molbar(
        self,
        *,
        mode: "MolBarMode | str" = MolBarMode.MB,
    ) -> str:
        """
        Compute the MolBar barcode string for this `Structure`.

        MolBar (Molecular Barcode) was introduced by van Staalduinen and
        Bannwarth as a chemical identifier that overcomes limitations of
        SMILES and InChI for inorganic molecules and non-central stereochemistry
        (e.g. axial and planar chirality). It combines the conventional
        atomistic description with a fragment-based approach: fragment 3D
        structures are normalised with a specialised force field and
        characterised by physically inspired matrices derived solely from
        atomic positions.

        The resulting permutation-invariant representation
        is built from the eigenvalue spectra of these matrices, encoding both
        bonding and stereochemistry. See the original publication for details:

        <https://doi.org/10.1039/d4dd00208c>

        Only real `Atom` entries are passed to MolBar; `EmbeddingPotential`,
        `GhostAtom`, and `PointCharge` instances are silently skipped. Note
        that `GhostAtom` is a subclass of `Atom`, so an exact type check is
        used rather than `isinstance`.

        The total charge is taken from `charge`.

        MolBar is an optional dependency of OPI and can be installed with::

            pip install molbar

        Parameters
        ----------
        mode : MolBarMode | str, default MolBarMode.MB
            MolBar calculation mode. Accepts a `MolBarMode` member or a
            plain string (case-insensitive). `"mb"` computes the full barcode;
            `"topo"` computes only the topology part.

        Returns
        -------
        str
            The MolBar barcode string.

        Raises
        ------
        ImportError
            If MolBar is not installed.
        ValueError
            If *mode* is not a valid `MolBarMode` value.
        ValueError
            If this structure contains no real atoms.

        See Also
        --------
        calculate_molbar_data : Returns the barcode together with the full MolBar data dictionary.
        """
        return cast(
            str,
            self._get_molbar_from_coordinates(self._validate_molbar_mode(mode), return_data=False),
        )

    @requires_molbar
    def calculate_molbar_data(
        self,
        *,
        mode: "MolBarMode | str" = MolBarMode.MB,
    ) -> "tuple[str, dict[str, Any]]":
        """
        Compute the MolBar barcode string and full data dictionary for this
        `Structure`.

        Behaves identically to `calculate_molbar` regarding MolBar installation,
        atom filtering, and mode selection — see `calculate_molbar` for details.

        The data dictionary contains the following top-level keys:

        `"molbar"`
            The barcode string, identical to the `calculate_molbar` return value.
        `"atoms"`
            Per-atom information after MolBar's internal geometry normalisation,
            including `"atomic_numbers"`, `"positions"` (Å), and
            `"partial_charges"`.
        `"bonds"`
            Detected bond graph: `"bond_indices"` (pairs) and `"bond_orders"`.
        `"fragments"`
            List of disconnected fragments found in the structure.
        `"topo"`
            Topology-only barcode (the first component of the full barcode).

        See the MolBar documentation for an authoritative and up-to-date description of every key.

        Parameters
        ----------
        mode : MolBarMode | str, default MolBarMode.MB
            MolBar calculation mode. See `calculate_molbar` for details.

        Returns
        -------
        tuple[str, dict[str, Any]]
            A two-element tuple of the MolBar barcode string and the full
            MolBar data dictionary.

        Raises
        ------
        ImportError
            If MolBar is not installed.
        ValueError
            If *mode* is not a valid `MolBarMode` value.
        ValueError
            If this structure contains no real atoms.

        See Also
        --------
        calculate_molbar : Returns only the barcode string.
        """
        return cast(
            "tuple[str, dict[str, Any]]",
            self._get_molbar_from_coordinates(self._validate_molbar_mode(mode), return_data=True),
        )

    # ------------------------------------------------------------------ #
    #  RMSD                                                              #
    # ------------------------------------------------------------------ #

    def rmsd(
        self,
        other: "Structure",
        /,
        only_atoms: Sequence[int] = (),
        *,
        ignore_hs: bool = False,
    ) -> float:
        """
        Compute RMSD between this structure and *other* (no rotational alignment).

        Both structures are translated to their centroid before comparison.
        Neither `self` nor *other* is modified; all coordinate operations are
        performed on temporary arrays.

        Parameters
        ----------
        other : Structure
            Structure to compare against.
        only_atoms : Sequence[int], default: ()
            Atom indices to include. If non-empty, `ignore_hs` is ignored.
        ignore_hs : bool, default: False
            Exclude hydrogen atoms from the RMSD computation.

        Returns
        -------
        float
            RMSD in Ångström.

        Raises
        ------
        ValueError
            If the filtered atom sets differ in size or element order.
        """
        indices1 = self._filtered_atoms(only_atoms, ignore_hs)
        indices2 = other._filtered_atoms(only_atoms, ignore_hs)
        self._validate_rmsd_compatibility(
            cast(list[Atom], [self.atoms[i] for i in indices1]),
            cast(list[Atom], [other.atoms[i] for i in indices2]),
        )
        coords1 = self.get_coordinates_at_centroid(only_atoms=indices1)
        coords2 = other.get_coordinates_at_centroid(only_atoms=indices2)

        return self._rmsd_coords(coords1, coords2)

    def rmsd_kabsch(
        self,
        other: "Structure",
        /,
        only_atoms: Sequence[int] = (),
        *,
        ignore_hs: bool = False,
    ) -> float:
        """
        Compute RMSD between this structure and *other* using the Kabsch algorithm.

        Translates both structures to their centroid, then finds the optimal
        rotation matrix via SVD before computing RMSD.
        Neither `self` nor *other* is modified; all coordinate operations are
        performed on temporary arrays.

        Parameters
        ----------
        other : Structure
            Structure to compare against.
        only_atoms : Sequence[int], default: ()
            Atom indices to include. If non-empty, `ignore_hs` is ignored.
        ignore_hs : bool, default: False
            Exclude hydrogen atoms from the RMSD computation.

        Returns
        -------
        float
            RMSD in Ångström after optimal rotational alignment.

        Raises
        ------
        ValueError
            If the filtered atom sets differ in size or element order.
        """
        indices1 = self._filtered_atoms(only_atoms, ignore_hs)
        indices2 = other._filtered_atoms(only_atoms, ignore_hs)
        self._validate_rmsd_compatibility(
            cast(list[Atom], [self.atoms[i] for i in indices1]),
            cast(list[Atom], [other.atoms[i] for i in indices2]),
        )

        # Getting centered coordinates
        coords1 = self.get_coordinates_at_centroid(only_atoms=indices1)
        coords2 = other.get_coordinates_at_centroid(only_atoms=indices2)

        # Kabsch algorithm: find optimal rotation matrix via SVD
        # <https://doi.org/10.1107/S0567739476001873>

        # ------------------------------------------------------------------
        # Build covariance matrix
        # ------------------------------------------------------------------
        # H = A^T B
        # This matrix captures how coordinates from B (coords2) map onto A (coords1)
        H = coords1.T @ coords2

        # ------------------------------------------------------------------
        # Singular Value Decomposition (SVD)
        # ------------------------------------------------------------------
        # H = U S V^T
        # This decomposes the transformation into rotations + scaling
        U, _, Vt = np.linalg.svd(H)

        # ------------------------------------------------------------------
        # Optimal rotation matrix
        # ------------------------------------------------------------------
        # R = V U^T
        # Reflection correction: ensure det(R) = +1
        d = np.linalg.det(Vt.T @ U.T)
        D = np.diag([1.0, 1.0, d])

        R = Vt.T @ D @ U.T

        return self._rmsd_coords(coords1, coords2 @ R)

    # ------------------------------------------------------------------ #
    #  Moment of inertia                                                   #
    # ------------------------------------------------------------------ #

    def calc_moments_of_inertia(
        self,
        elem_masses: dict[str | Element, float] | None = None,
    ) -> PrincipalMoments | None:
        """
        Compute the principal axes and moments of inertia for this structure.

        Only `Atom` instances contribute; `GhostAtom`, `PointCharge`,
        and `EmbeddingPotential` atoms are silently ignored. Note that
        `GhostAtom` is a subclass of `Atom`, so an exact type check
        (`type(a) is Atom`) is used rather than `isinstance`.

        Parameters
        ----------
        elem_masses : dict[str | Element, float] | None, default: None
            Per-element mass overrides keyed by element symbol string or
            `Element` instance (e.g. `{"C": 13.003}`). If `None`, default
            atomic masses are used.

        Mass priority
        -------------
        atom.mass > elem_masses > default (ATOMIC_MASSES_FROM_ELEMENT)

        Returns
        -------
        PrincipalMoments | None
            Principal axes and moments of inertia in amu·Å², sorted ascending.
            Returns `None` if no `Atom` instances are present or all masses are zero.
        """
        atom_indices = [i for i, a in enumerate(self.atoms) if type(a) is Atom]
        if not atom_indices:
            return None
        coords = self.get_coordinates(only_atoms=atom_indices)

        masses = self._resolve_masses(elem_masses)

        # --- Filter out zero-mass atoms before computing the inertia tensor ---
        # This handles atoms explicitly assigned a mass of 0.0 via elem_masses
        mask = masses > 0.0
        if not np.any(mask):
            return None
        masses = masses[mask]
        coords = coords[mask]

        total_mass = float(masses.sum())
        com = (masses[:, None] * coords).sum(axis=0) / total_mass
        coords -= com

        inertia = np.zeros((3, 3), dtype=np.float64)
        for m, r in zip(masses, coords):
            inertia += m * (np.dot(r, r) * np.eye(3) - np.outer(r, r))

        moments_raw, axes = np.linalg.eigh(inertia)  # ascending order guaranteed
        # Clamp to zero: floating point arithmetic can produce very small
        # negative eigenvalues (e.g. -1e-15) for moments that are physically
        # zero, due to numerical noise in the inertia tensor.
        moments_raw = np.maximum(moments_raw, 0.0)

        return PrincipalMoments(
            Ia=float(moments_raw[0]),
            Ib=float(moments_raw[1]),
            Ic=float(moments_raw[2]),
            axes=axes,
        )

    def calc_rotor_type(
        self,
        moments: PrincipalMoments | None = None,
        **mass_kwargs: Any,
    ) -> RotorType | None:
        """
        Classify the molecular rotor type.

        Parameters
        ----------
        moments : PrincipalMoments | None, default: None
            Pre-computed principal moments (amu·Å², ascending). When
            `None` the moments are computed via
            :meth:`calc_moments_of_inertia()` using *mass_kwargs*.
        **mass_kwargs
            Forwarded to :meth:`calc_moments_of_inertia()` when `moments` is
            `None` (i.e. `elem_masses`).

        Returns
        -------
        RotorType | None
            `None` if the structure has no real atoms or all masses vanish.
        """
        if moments is None:
            moments = self.calc_moments_of_inertia(**mass_kwargs)
            if moments is None:
                return None
        return moments.rotor_type()

    def calc_rotational_constants(
        self,
        elem_masses: dict[str | Element, float] | None = None,
    ) -> RotationalConstants | None:
        """
        Compute rotational constants for this structure.

        Only `Atom` instances contribute; `GhostAtom`, `PointCharge`,
        and `EmbeddingPotential` atoms are silently ignored.

        Mass priority
        -------------
        atom.mass > elem_masses > default (ATOMIC_MASSES_FROM_ELEMENT)

        Parameters
        ----------
        elem_masses : dict[str | Element, float] | None, default: None
            Per-element mass overrides keyed by element symbol string or
            `Element` instance (e.g. `{"C": 13.003}`). Only applied to atoms
            that do not have a mass set directly via `atom.mass`. If `None`,
            masses fall back to default atomic masses.

        Returns
        -------
        RotationalConstants | None
            `None` if no `Atom` instances are present or all masses are zero.
        """
        pm = self.calc_moments_of_inertia(elem_masses=elem_masses)
        if pm is None:
            return None
        A = moment_to_mhz(pm.Ia)
        B = moment_to_mhz(pm.Ib)
        C = moment_to_mhz(pm.Ic)
        return RotationalConstants(A=A, B=B, C=C)

    @classmethod
    def _iter_xyz_structures(
        cls,
        tracked: TrackingTextIO,
        charge: int = 0,
        multiplicity: int = 1,
        comment_symbols: str | Sequence[str] | None = None,
        n_struc_limit: int | None = None,
    ) -> Iterator["Structure"]:
        """
        Yield properties from the buffer until exhausted or the limit is reached.

        Parameters
        ----------
        tracked: TrackingTextIO
            A buffer that contains XYZ file data.
        charge : int, default:  0
            Optional charge for the structure
        multiplicity : int, default:  1
            Optional multiplicity for the structure
        comment_symbols: str | Sequence[str] | None, default: None
            List of symbols that indicate user comments in the XYZ data.
            User comments have to start with the given symbol, fill a whole line, and come before the actual XYZ data.
        n_struc_limit: int | None, default: None
            If >0, only read the first n structures.

        Returns
        --------
        Iterator["Structure"]
            Iterator of `Structure` object extracted from the buffer.

        Raises
        --------
        ValueError
            If `n_struc_limit` is negative or zero.

        """

        if n_struc_limit is not None and n_struc_limit < 0:
            raise ValueError("n_struc_limit must be None, 0, or a positive integer")

        n_struc = 0
        while True:
            try:
                struct = cls.from_xyz_buffer(
                    tracked,
                    charge=charge,
                    multiplicity=multiplicity,
                    comment_symbols=comment_symbols,
                )
            except EOFError:
                break
            yield struct
            n_struc += 1
            if n_struc_limit and n_struc >= n_struc_limit:
                break

    # ------------------------------------------------------------------ #
    #  MOLBAR                                                            #
    # ------------------------------------------------------------------ #

    def _get_molbar_from_coordinates(
        self,
        mode: MolBarMode,
        return_data: bool,
    ) -> "str | tuple[str, dict[str, Any]]":
        """
        Shared implementation for `calculate_molbar` and `calculate_molbar_data`.

        Collects elements and coordinates from `real_atoms` via
        `get_coordinates`, and delegates to `call_molbar`.

        Parameters
        ----------
        mode : MolBarMode
            Already-validated calculation mode.
        return_data : bool
            If `True` returns `tuple[str, dict[str, Any]]`; if `False` returns `str`.

        Returns
        -------
        str | tuple[str, dict[str, Any]]
            Either the barcode string or the barcode string together with the
            full MolBar data dictionary, depending on *return_data*.

        Raises
        ------
        ValueError
            If this structure contains no real atoms.
        """
        if not self.real_atoms:
            raise ValueError(
                f"{self.__class__.__name__}: structure contains no real atoms; "
                "cannot build MolBar input."
            )

        # > Only real Atom instances are passed to MolBar; EmbeddingPotential,
        # > GhostAtom, and PointCharge entries are excluded via real_atoms.
        # > Note that GhostAtom is a subclass of Atom, so type(a) is Atom is
        # > used rather than isinstance inside the real_atoms property.

        # > OPI-native types (Element instances, NumPy array) are passed as-is;
        # > `call_molbar` handles the conversion to MolBar's expected format.
        real_indices = [i for i, a in enumerate(self.atoms) if type(a) is Atom]

        return call_molbar(
            elements=[atom.element for atom in self.real_atoms],
            coordinates=self.get_coordinates(only_atoms=real_indices),
            total_charge=self.charge,
            mode=mode,
            return_data=return_data,
        )

    def _validate_molbar_mode(self, mode: "MolBarMode | str") -> MolBarMode:
        """
        Validate and normalise a MolBar calculation mode.

        Parameters
        ----------
        mode : MolBarMode | str
            Calculation mode to validate.

        Returns
        -------
        MolBarMode
            The validated and normalised mode.

        Raises
        ------
        ValueError
            If *mode* is not a valid `MolBarMode` value.
        """
        # > Normalise and validate mode (case-insensitive via StringEnum._missing_)
        try:
            return MolBarMode(mode)
        except ValueError:
            raise ValueError(
                f"Invalid mode {mode!r}. Must be one of {[m.value for m in MolBarMode]}"
            )

    def _filtered_atoms(
        self,
        only_atoms: Sequence[int],
        ignore_hs: bool,
    ) -> list[int]:
        """
        Return indices of real `Atom` instances after applying `only_atoms`
        and `ignore_hs` filters.

        The final `type(a) is Atom` check ensures that explicitly indexed atoms
        (via `only_atoms`) cannot introduce `GhostAtom`, `PointCharge`, or
        `EmbeddingPotential` instances into the returned list. Note that `GhostAtom`
        is a subclass of `Atom`, so `isinstance` is intentionally avoided here.
        """
        if only_atoms:
            candidates = list(only_atoms)
        elif ignore_hs:
            candidates = [
                i for i, a in enumerate(self.atoms) if type(a) is Atom and a.element != Element.H
            ]
        else:
            candidates = [i for i, a in enumerate(self.atoms) if type(a) is Atom]
        return [i for i in candidates if type(self.atoms[i]) is Atom]

    @staticmethod
    def _validate_rmsd_compatibility(atoms1: list[Atom], atoms2: list[Atom]) -> None:
        """
        Raise `ValueError` if `atoms1` and `atoms2` differ in count or element order.
        """
        if len(atoms1) != len(atoms2):
            raise ValueError(
                f"Structures have different number of atoms: {len(atoms1)} vs {len(atoms2)}"
            )
        for i, (a, b) in enumerate(zip(atoms1, atoms2), start=1):
            if a.element != b.element:
                raise ValueError(f"Atom mismatch at position {i}: {a.element!r} != {b.element!r}")

    @staticmethod
    def _rmsd_coords(
        coords1: npt.NDArray[np.float64],
        coords2: npt.NDArray[np.float64],
    ) -> float:
        """
        Compute RMSD between two aligned (N, 3) coordinate arrays.
        """
        diff = coords1 - coords2
        return float(np.sqrt(np.sum(diff**2) / len(coords1)))

    def _resolve_masses(
        self,
        elem_masses: dict[str | Element, float] | None = None,
    ) -> npt.NDArray[np.float64]:
        """
        Resolve masses for all real `Atom` instances without mutating any atom.

        Parameters
        ----------
        elem_masses : dict[str | Element, float] | None, default: None
            Per-element mass overrides keyed by element symbol string or
            `Element` instance (e.g. `{"C": 13.003}`). If `None`, default
            atomic masses are used.

        Mass priority
        -------------
        atom.mass > elem_masses > default (ATOMIC_MASSES_FROM_ELEMENT)

        Returns
        -------
        npt.NDArray[np.float64], shape (N,)
            Masses in amu in the same order as `self.real_atoms`.
        """
        elem_masses = elem_masses or {}
        # Normalise keys to Element for consistent lookup
        normalised: dict[Element, float] = {}
        for k, v in elem_masses.items():
            normalised[Element(k) if isinstance(k, str) else k] = v

        masses_list: list[float] = []
        for atom in self.real_atoms:
            if atom.mass is not None:
                # Mass set directly on the atom is the most specific → highest priority
                m = atom.mass
            elif atom.element in normalised:
                # Per-element override is next
                m = normalised[atom.element]
            elif atom.element in ATOMIC_MASSES_FROM_ELEMENT:
                # Fall back to default atomic masses
                m = ATOMIC_MASSES_FROM_ELEMENT[atom.element]
            else:
                raise ValueError(
                    f"Unknown element '{atom.element.value}': no mass available. "
                    "Provide a mass via `elem_masses` or set `atom.mass` directly."
                )
            masses_list.append(m)
        return np.array(masses_list, dtype=np.float64)
