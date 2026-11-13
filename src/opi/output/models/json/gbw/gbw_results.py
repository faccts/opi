import shutil
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import TYPE_CHECKING

import numpy.typing as npt
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
from opi.utils.pyscf import requires_pyscf

if TYPE_CHECKING:
    # > PySCF is an optional dependency and only imported for type annotations
    from pyscf.scf.hf import SCF


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
            charge=molecule.charge,
            multiplicity=molecule.multiplicity,
        )
        if molecule.basename:
            structure.origin = molecule.basename

        return structure

    @requires_pyscf
    def to_pyscf(self) -> "SCF":
        """
        Create a PySCF mean-field object from the molecular orbital data, e.g., to use ORCA's
        orbitals in PySCF. Requires the optional dependency PySCF.

        The basis set and effective core potentials are transferred exactly and the molecular
        orbitals are reordered into PySCF's convention for basis functions.

        The returned object holds the orbitals (`mo_coeff`), occupation numbers (`mo_occ`), and
        orbital energies (`mo_energy`), but no SCF has been run with it. It is a Hartree-Fock
        object (`scf.RHF`, `scf.UHF`, or `scf.ROHF`) according to the HF type of the
        calculation, also for Kohn-Sham calculations, as the functional is not part of the gbw
        data. CASSCF orbitals are returned as `scf.RHF` object holding the natural orbitals.

        Likewise, a relativistic Hamiltonian (DKH, ZORA, X2C) is not part of the gbw data. For
        such calculations, the returned object does not reproduce ORCA's energy, unless a
        corresponding Hamiltonian is set up in PySCF. ORCA's X2C (with its default point nucleus)
        is reproduced by `mf.x2c()`, if PySCF uses ORCA's speed of light
        (`pyscf.lib.param.LIGHT_SPEED = 137.0359895`).

        For an open shell of degenerate orbitals (e.g., the pi orbitals of OH), ORCA's ROHF
        averages over the configurations and stores fractional occupation numbers. As PySCF's
        ROHF represents a single determinant, these are replaced by integer occupation numbers
        and a warning is issued; the energy then differs from ORCA's.

        Returns
        -------
        pyscf.scf.hf.SCF
            PySCF mean-field object holding the molecular orbitals.

        Raises
        ------
        ImportError
            If PySCF is not installed.
        ValueError
            If the gbw data lacks atoms, basis sets, or molecular orbitals.

        Warns
        -----
        UserWarning
            If fractional ROHF occupation numbers are replaced by integer ones.
        """
        from opi.output.models.json.gbw._pyscf_converter import gbw_to_pyscf

        return gbw_to_pyscf(self)

    @classmethod
    @requires_pyscf
    def from_pyscf(
        cls,
        mf: "SCF",
        /,
        *,
        mo_coeff: npt.ArrayLike | None = None,
        mo_occ: npt.ArrayLike | None = None,
        mo_energy: npt.ArrayLike | None = None,
    ) -> "GbwResults":
        """
        Create gbw data from a PySCF mean-field object, e.g., to use PySCF's orbitals in ORCA.
        Requires the optional dependency PySCF.

        Write the result into a gbw file with `to_gbw_file()` and read it in ORCA with
        `! MORead` and `%moinp`.

        Parameters
        ----------
        mf : pyscf.scf.hf.SCF
            PySCF mean-field object of RHF, UHF, or ROHF type (including Kohn-Sham). Its molecule
            must use spherical basis functions and scalar ECPs.
        mo_coeff : array_like | None, default: None
            Molecular orbitals to use instead of `mf.mo_coeff`, e.g., localized or natural
            orbitals, with the shape (n_ao, n_mo), or (2, n_ao, n_mo) for unrestricted orbitals.
            Requires `mo_occ`. Restricted orbitals of an open-shell molecule are stored as ROHF
            type orbitals. Note that a gbw file can only be written with as many orbitals as
            basis functions.
        mo_occ : array_like | None, default: None
            Occupation numbers to use instead of `mf.mo_occ`.
        mo_energy : array_like | None, default: None
            Orbital energies to use instead of `mf.mo_energy`. If `mo_coeff` is given without
            orbital energies, these are set to zero.

        Returns
        -------
        GbwResults
            gbw data holding the structure, basis set, effective core potentials, and molecular
            orbitals.

        Raises
        ------
        ImportError
            If PySCF is not installed.
        ValueError
            If the molecule uses Cartesian basis functions or ECPs with spin-orbit terms, if the
            calculation is periodic, if the orbitals are generalized, four-component, or complex,
            or if orbitals or occupation numbers are missing or of inconsistent shape.

        Warns
        -----
        UserWarning
            If the mean-field object uses a relativistic (X2C) Hamiltonian, which is not part of
            the gbw data.
        """
        from opi.output.models.json.gbw._pyscf_converter import gbw_from_pyscf

        return gbw_from_pyscf(mf, mo_coeff=mo_coeff, mo_occ=mo_occ, mo_energy=mo_energy)

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
                message = f"orca_2json failed to create a gbw file from {gbw_file.stem}.json"
                # > `orca_2json` of ORCA 6.1.1 fails silently for shells above l = 8
                if self._max_shell_letter() in ("m", "n"):
                    message += (
                        ". The basis set contains shells above l = 8, which orca_2json may not "
                        "support."
                    )
                raise RuntimeError(message)

            return Path(shutil.move(tmp_gbw_file, gbw_file))

    def _max_shell_letter(self) -> str | None:
        """Letter of the highest angular momentum of the basis set, or None if there is none."""
        order = "spdfghiklmn"
        letters: list[str] = []
        if self.molecule is not None:
            for atom in self.molecule.atoms or []:
                for shell in atom.basis or []:
                    if shell.shell is not None and shell.shell.lower() in order:
                        letters.append(shell.shell.lower())
        return max(letters, key=order.index) if letters else None

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
        # > `orca_2json` silently writes a corrupt gbw file, if there are fewer orbitals than basis
        # > functions, e.g., after removing linear dependencies
        n_ao = len(molecular_orbitals.mos[0].mocoefficients or [])
        n_spin = 2 if molecule.hftyp.lower() == "uhf" else 1
        if any(len(mo.mocoefficients or []) != n_ao for mo in molecular_orbitals.mos):
            raise ValueError("Cannot write gbw file: molecular orbitals differ in size")
        if len(molecular_orbitals.mos) != n_spin * n_ao:
            raise ValueError(
                f"Cannot write gbw file: {len(molecular_orbitals.mos)} molecular orbitals present, "
                f"but {n_spin * n_ao} are required for {n_ao} basis functions"
            )
