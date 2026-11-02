import shutil
from pathlib import Path
from tempfile import TemporaryDirectory

from pydantic import Field

from opi.execution.core import Runner
from opi.input.structures.atom import Atom, GhostAtom
from opi.input.structures.coordinates import Coordinates
from opi.input.structures.structure import Structure
from opi.output.models.json.gbw.properties.cite import Cite
from opi.output.models.json.gbw.properties.header import OrcaHeader
from opi.output.models.json.gbw.properties.molecule import Molecule
from opi.output.models.json_loadable import JSONLoadable
from opi.utils.element import Element


class GbwResults(JSONLoadable):
    """
    This class contains all the information from the baseman.json file

    Attributes
    ----------
    orca header: OrcaHeader
        Contains information from the ORCA-Header
    citations: List[Cite]
        Contains the paper that are necessary to cite
    molecule: Molecule
        Contains information about the molecule
    """

    orca_header: OrcaHeader | None = Field(alias="orca header", serialization_alias="ORCA Header")
    citations: list[Cite] | None = Field(default=None, serialization_alias="Citations")
    molecule: Molecule | None = Field(default=None, serialization_alias="Molecule")

    class Configuration:
        allow_population_by_field_name = True

    @classmethod
    def from_gbw_file(
        cls,
        gbw_file: Path | str,
        /,
        *,
        reuse_json: bool = False,
        config: dict[str, bool | str | list[str | int]] | None = None,
    ) -> "GbwResults":
        """
        Creates an object from a binary gbw file by converting it with `orca_2json` and initializing from the `.json` file.

        Parameters
        ----------
        gbw_file : Path | str
            Path to the binary gbw file.
        reuse_json : bool, default: False
            If True, an existing gbw-JSON file is used.
        config : dict[str, bool | str | list[str | int]] | None, default: None
            Determine contents of the gbw-JSON file. Does nothing if the JSON file is reused and not re-created.

        Returns
        -------
        GbwResults
            Object created from the gbw file.

        Raises
        ------
        FileNotFoundError
            Raised if `gbw_file` does not point to a file, or if `orca_2json` did not create a JSON
            file.
        ValueError
            Raised if the created JSON is invalid.
        """
        gbw_file = Path(gbw_file).expanduser().resolve()
        if not gbw_file.is_file():
            raise FileNotFoundError(f"File {gbw_file} not found")

        force = not reuse_json

        runner = Runner(working_dir=gbw_file.parent)
        runner.create_gbw_json(gbw_file.stem, force=force, config=config, suffix=gbw_file.suffix)

        # > `orca_2json` does not signal failure through its return code, so a missing JSON file is
        # > the only indication that the conversion did not work.
        gbw_json_file = gbw_file.with_suffix(".json")
        if not gbw_json_file.is_file():
            raise FileNotFoundError(
                f"orca_2json did not create {gbw_json_file} from {gbw_file}. "
                "The gbw file may be corrupt or written by an incompatible ORCA version."
            )

        return cls.from_json_file(gbw_json_file)

    def get_structure(self) -> Structure | None:
        """
        Returns the molecular structure stored in the gbw file as `Structure` object.
        Silently returns None if no structure is available.

        Atoms carrying basis functions but no nuclear charge are returned as `GhostAtom`.

        Returns
        -------
        structure: Structure | None
            Structure generated from the gbw data or None if no structure is available.

        Raises
        ------
        ValueError
            Raised if an atom entry is present but lacks a usable element or coordinates.
        """
        molecule = self.molecule
        if molecule is None or not molecule.atoms:
            return None

        atoms: list[Atom] = []
        for gbw_atom in molecule.atoms:
            # > Determine the element, preferably from the atomic number.
            if gbw_atom.elementnumber is not None:
                element = Element.from_atomic_number(gbw_atom.elementnumber)
            elif gbw_atom.elementlabel is not None:
                element = Element(gbw_atom.elementlabel)
            else:
                raise ValueError("Atom in gbw data has neither an element number nor a label")

            # > Unlike the cartesians in the property JSON, gbw coordinates are already in Angstrom.
            coords = gbw_atom.coords
            if coords is None or len(coords) != 3:
                raise ValueError(f"Atom {element} in gbw data has invalid coordinates: {coords}")
            coordinates = Coordinates((coords[0], coords[1], coords[2]))

            # > A ghost atom carries basis functions but no nuclear charge. Atoms with an ECP keep
            # > their effective charge (e.g. 6.0 for oxygen), so they are never mistaken for one.
            is_ghost = gbw_atom.nuclearcharge == 0.0 and element != Element.X
            atom_type = GhostAtom if is_ghost else Atom
            atoms.append(atom_type(element=element, coordinates=coordinates))

        structure = Structure(
            atoms,
            charge=molecule.charge if molecule.charge is not None else 0,
            multiplicity=molecule.multiplicity if molecule.multiplicity is not None else 1,
        )
        if molecule.basename:
            structure.origin = molecule.basename

        return structure

    def to_gbw_file(self, gbw_file: Path | str, /, *, runner: Runner | None = None) -> Path:
        """
        Write a gbw file from the results by dumping them into a gbw-JSON file and converting that
        file with `orca_2json <json-file> -gbw`.

        Parameters
        ----------
        gbw_file : Path | str
            Path to the gbw file to be written. An existing file is overwritten.
        runner : Runner | None, default: None
            Runner used to execute `orca_2json`. By default, a new `Runner` is created.

        Returns
        -------
        Path
            Path to the written gbw file.

        Raises
        ------
        ValueError
            If the results lack data that is required to create a gbw file.
        IsADirectoryError
            If `gbw_file` points to a folder.
        FileNotFoundError
            If the parent folder of `gbw_file` does not exist.
        RuntimeError
            If `orca_2json` did not create a gbw file.
        """
        self._check_gbw_writable()

        gbw_file = Path(gbw_file)
        if gbw_file.is_dir():
            raise IsADirectoryError(f"Path of gbw file is a folder: {gbw_file}")
        if not gbw_file.parent.is_dir():
            raise FileNotFoundError(f"Folder of gbw file does not exist: {gbw_file.parent}")

        if runner is None:
            runner = Runner()

        # > `orca_2json` determines the name of the gbw file from the name of the JSON file, hence
        # > the JSON file is written into a temporary folder to not overwrite any existing files.
        # > That folder is created next to the gbw file, so that `orca_2json` runs in the folder of
        # > the gbw file and both files stay on the same file system.
        with TemporaryDirectory(dir=gbw_file.parent) as tmpdir:
            tmp_dir = Path(tmpdir)
            json_file = self.to_json_file(tmp_dir / f"{gbw_file.stem}.json")
            # > Passing only the name of the JSON file, as ORCA binaries are run in the folder of
            # > the files they work on.
            result = runner.run_orca_2json([json_file.name, "-gbw"], working_dir=tmp_dir)

            # > `orca_2json` appends "_copy" to the stem of the JSON file
            tmp_gbw_file = json_file.with_name(f"{json_file.stem}_copy.gbw")
            if not result.returncode_ok() or not tmp_gbw_file.is_file():
                raise RuntimeError(
                    f"orca_2json failed to create a gbw file from {gbw_file.stem}.json"
                )

            return Path(shutil.move(tmp_gbw_file, gbw_file))

    def _check_gbw_writable(self) -> None:
        """
        Check that all data required by `orca_2json` to create a gbw file is present.
        Missing data makes `orca_2json` fail or even crash, so it is checked beforehand.

        Raises
        ------
        ValueError
            If required data is missing.
        """
        molecule = self.molecule
        if molecule is None:
            raise ValueError("Cannot write gbw file: no molecule present")
        if molecule.hftyp is None:
            raise ValueError("Cannot write gbw file: HF type of the molecule is missing")

        if not molecule.atoms:
            raise ValueError("Cannot write gbw file: no atoms present")
        if any(atom.basis is None for atom in molecule.atoms):
            raise ValueError("Cannot write gbw file: basis set of at least one atom is missing")

        molecular_orbitals = molecule.molecularorbitals
        if molecular_orbitals is None or not molecular_orbitals.mos:
            raise ValueError("Cannot write gbw file: no molecular orbitals present")
        if any(mo.mocoefficients is None for mo in molecular_orbitals.mos):
            raise ValueError(
                "Cannot write gbw file: MO coefficients of at least one molecular orbital are missing"
            )
