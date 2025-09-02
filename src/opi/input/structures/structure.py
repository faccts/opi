import re
from collections.abc import Iterator
from io import StringIO
from os import PathLike
from pathlib import Path
from typing import TYPE_CHECKING, Any, Iterable, Sequence, cast

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
from opi.utils.element import Element

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

    def format_orca(self) -> str:
        """
        Returns string representation of Molecule
        Iteratively calls Atom.format_orca() and compiles it all together to create string representation of Molecule

        Returns
        -------
            str:
                String representation of Molecule
        """
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
        if position is not None and (position <= 0 or position > len(self.atoms) + 1):
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

        Returns
        --------
        `Structure`:`Structure object extracted from file
        """
        # > converting into Path
        xyzfile = Path(xyzfile)

        # > Check if file exists
        if not xyzfile.exists():
            raise FileNotFoundError(f"XYZ file not found: {xyzfile}")

        with xyzfile.open() as f_xyz:
            structure = cls.from_xyz_buffer(f_xyz, charge=charge, multiplicity=multiplicity)
            structure.origin = xyzfile.expanduser().resolve()
            return structure

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

        Returns
        --------
        Structure
            The `Structure` object extracted from file
        """
        with StringIO(xyz_string) as f_xyz:
            return cls.from_xyz_buffer(f_xyz, charge=charge, multiplicity=multiplicity)

    @classmethod
    def from_xyz_buffer(
        cls,
        xyz_lines: Iterator[str],
        *,
        charge: int = 0,
        multiplicity: int = 1,
    ) -> "Structure":
        """
        Function for reading a xyz file from a buffer and converting it to a molecular Structure.

        Parameters
        ----------
        xyz_lines: Iterator[str]
            A buffer that contains xyz file data
        charge : int, default = 0
            Molecular charge of the structure.
        multiplicity: int, default = 1
            Electron spin multiplicity of the structure.

        Returns
        --------
        The `Structure` object extracted from the buffer
        """
        # > Try reading the string
        atoms = []

        # > Fetch number of atoms
        try:
            natoms = int(next(xyz_lines).split()[0])
        except (ValueError, IndexError, StopIteration) as err:
            raise ValueError("Could not read number of atoms in line 1 from xyz data") from err
        # > Skipping comment line
        try:
            next(xyz_lines)
        except StopIteration as err:
            raise ValueError("Comment line is not present in xyz data") from err

        # > Read atoms
        iline = 2
        for line in xyz_lines:
            iline += 1
            # > Line should have at least 4 columns
            atom_cols = line.split()
            if len(atom_cols) < 4:
                raise ValueError(f"Line {iline}: Invalidly formatted coordinate line")

            # > Get atom symbol.
            # >> First check if we have combination of atom symbol + fragment id
            match_atom_sym_frag_id = RGX_ATOM_SYMBOL_FRAG_ID.match(line.lstrip())
            if not match_atom_sym_frag_id:
                raise ValueError(f"Line {iline}: Could not find atom symbol.")

            atom_sym = match_atom_sym_frag_id.group("elem")
            try:
                element = Element(atom_sym)
            except Exception as err:
                raise ValueError(f"Line {iline}: Invalid atom symbol: {atom_sym}") from err

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
                    raise ValueError(f"Line {iline}: Invalid fragment id: {match_frag_id}") from err

            # > Pass coordinates
            # // X
            try:
                coord_x = float(coords_cols[0])
            except (ValueError, IndexError) as err:
                raise ValueError(f"Line {iline}: Invalid X coordinate: {atom_cols[1]}") from err
            # // Y
            try:
                coord_y = float(coords_cols[1])
            except (ValueError, IndexError) as err:
                raise ValueError(f"Line {iline}: Invalid Y coordinate: {atom_cols[2]}") from err
            # // Z
            try:
                coord_z = float(coords_cols[2])
            except (ValueError, IndexError) as err:
                raise ValueError(f"Line {iline}: Invalid Z coordinate: {atom_cols[3]}") from err

            # > Adding atom
            atoms.append(
                Atom(
                    element=element,
                    coordinates=Coordinates(coordinates=(coord_x, coord_y, coord_z)),
                    fragment_id=frag_id,
                )
            )
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
        charge : int | None, default = None
            Optional charge of the molecule, will overwrite charge from ase.
        multiplicity : int | None, default = None
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
        charge : int, default = 0
            Optional charge for the structure
        multiplicity : int, default = 1
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
