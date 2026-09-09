from pathlib import Path

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

    orca_header: OrcaHeader | None = Field(alias="orca header")
    citations: list[Cite] | None = None
    molecule: Molecule | None = None

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
