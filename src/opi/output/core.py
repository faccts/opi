"""
This module contains the main class for output handling.
It's mostly based on the ORCA's two JSONs files.
"""

import json
from pathlib import Path
from typing import Any, cast
from warnings import warn

from pydantic import StrictStr

from opi.execution.core import Runner
from opi.input.structures import Atom, Coordinates, Structure
from opi.output.grepper.recipes import (
    has_geometry_optimization_converged,
    has_scf_converged,
    has_terminated_normally,
)
from opi.output.models.base.strict_types import StrictFiniteFloat
from opi.output.models.json.gbw.gbw_results import GbwResults
from opi.output.models.json.property.properties.energy import Energy
from opi.output.models.json.property.properties.energy_list import EnergyList
from opi.output.models.json.property.property_results import (
    PropertyResults,
)
from opi.utils.misc import check_minimal_version, lowercase
from opi.utils.orca_version import OrcaVersion
from opi.utils.units import AU_TO_ANGST


class Output:
    """
    Class that handles of ORCA output, especially the `<basename>.json` `<basename>.property.json`

    Attributes
    ----------
    basename: str
        Basename of the job.
    working_dir: Path
        Optional path to the working directory.
    do_create_gbw_json: bool, default: False
        Switch that determines if gbw-json file is created if missing.
    do_create_property_json: PropertyResults
        Switch that determines if property-json file is created if missing.
    results_properties: PropertyResults
        Properties parsed from `property.json`.
        Should be preferred over `property_json_data`.
    results_gbw: GbwResults
        Data parsed from `<basename>.json`.
        Should be preferred over `gbw_json_data`.
    property_json_data: dict[str, Any]
        JSON tree read from `<basename>.property.json`.
    gbw_json_data: dict[str, Any]
        JSON tree of read from `<basename>.json`.
    do_redump_jsons: bool, default: False
        Redump JSONs files after parsing. This is mostly meant for debugging.
    """

    def __init__(
        self,
        basename: str,
        *,
        working_dir: Path | None = None,
        create_gbw_json: bool = False,
        create_property_json: bool = False,
        version_check: bool = True,
        parse: bool = False,
    ):
        """
        ORCA output parser that is mainly based on the JSON-property and JSON-GBW file.
        It can also read strings from the output file (if present).
        All files are determined based on the job basename given at initialization.

        Arguments
        ---------
        basename: str
            Basename of the job.
        working_dir: Path
            Optional path to the working directory.
        create_gbw_json: bool = False
            Whether the JSON gbw-file should be created by calling `orca_2json`, will not overwrite an existing JSON-file
            Usually, this is already done by `Calculator` if used.
        create_property_json: bool = False
            Whether the JSON property-file should be created by calling orca_2json,
            will not overwrite an existing JSON-file.
            Usually, this is already done by `Calculator` if used.
        version_check: bool, default: True
            If True, check if the ORCA version stored in JSON-property file is compliant with the minimal supported ORCA version of this interface.
            A warning is printed if the version check is not passed.
            If the version check runs into an error a ValueError is raised.
        parse: bool, default: False
            True: Create (if turned on by `create_gbw_json/create_property_json`) and parse JSONs files at the end of the initialization.
            False: Only return an Output object. In order to use the object to access the JSON data,
                   `Output.parse()` has to be called first.
        """
        self.basename = basename
        self.do_version_check = version_check

        self.working_dir = working_dir.expanduser().resolve() if working_dir else Path.cwd()
        if not self.working_dir.is_dir():
            raise FileNotFoundError(f"Working dir does not exist: {working_dir}")

        # // JSON PATHS
        self.gbw_json_file = self.get_file(".json")
        self.property_json_file = self.get_file(".property.json")

        # > // SWITCHES: CREATE JSON FILES
        self.do_create_gbw_json = create_gbw_json
        self.do_create_property_json = create_property_json

        # > // REDUMP JSON AFTER PARSING
        self.do_redump_jsons: bool = False

        # > // RAW JSON TREES
        self.gbw_json_data: dict[str, Any] | None = None
        self.property_json_data: dict[str, Any] | None = None

        # // PARSED JSON TREES
        self.results_properties: PropertyResults | None = None
        self.results_gbw: GbwResults | None = None

        # // CREATE AND PARSE JSONS FILES
        if parse:
            self.parse()

    def parse(self, read_prop_json: bool = True, read_gbw_json: bool = True) -> None:
        """
        Create property- and gbw-JSON file (according to `do_create_property_json` and `self.do_create_gbw_json`)
        and parse them.
        Skips the parsing for the gbw or prop json file when the respective bool is false. It defaults to true

        Parameters
        ----------
        read_prop_json: bool, default: True
            Whether or not to read the property JSON file
        read_gbw_json: bool, default: True
            Whether or not to read the gbw JSON file
        """
        # // Create JSONs files
        if self.do_create_gbw_json:
            self.create_gbw_json()
        if self.do_create_property_json:
            self.create_property_json()

        # // PARSE JSONS
        # // Property JSON
        if read_prop_json:
            self.property_json_data = self._process_json_file(self.property_json_file)
            # > Check in property json whether version fits:
            if self.do_version_check:
                self.check_version()
            self.results_properties = PropertyResults(**self.property_json_data)
        else:
            if self.do_version_check:
                warn("No version check possible.")

        # // GBW JSON file
        if read_gbw_json:
            self.gbw_json_data = self._process_json_file(self.gbw_json_file)
            self.results_gbw = GbwResults(**self.gbw_json_data)

        # > Redump JSON files
        if self.do_redump_jsons:
            self._redump_jsons()

    def _read_json(self, json_file: Path, /) -> dict[str, Any]:
        """
        Read a JSON file and return its JSON tree.

        Parameters
        ---------
        json_file: Path
            Path to the JSON file to be read.

        Returns
        -------
        dict[str, Any]
            The JSON tree.

        Raises
        ------
        FileNotFoundError
            If the Path leads to no file
        """

        if not json_file.is_file():
            raise FileNotFoundError(f"JSON file does not exist: {json_file}")

        with json_file.open() as f_json:
            json_data: dict[str, Any] = json.load(f_json)
            return json_data

    def _process_json_file(self, json_file: Path, /) -> dict[str, Any]:
        """
        Read the JSON file and convert all keys to lowercase.

        Parameters
        ----------
        json_file : Path
            Path to JSON file to be read.
        """

        json_data: dict[str, Any] = self._read_json(json_file)
        # > Convert all keys to lowercase.
        lowercase(json_data)
        return json_data

    def _redump_jsons(self) -> None:
        """Redump both JSON files as read and parse by `PropertyResults` and `GbwResults`."""

        assert self.gbw_json_file
        assert self.results_gbw
        redumped_gbw_json_file = self.gbw_json_file.with_suffix(".interface.json")
        self._dump_json(self.results_gbw, redumped_gbw_json_file)

        assert self.property_json_file
        assert self.results_properties
        redumped_property_json_file = self.property_json_file.with_suffix(".interface.json")
        self._dump_json(self.results_properties, redumped_property_json_file)

    def _dump_json(self, result: GbwResults | PropertyResults, json_file: Path, /) -> None:
        """
        Dump `GbwResults` or `PropertyResults` to a JSON file.

        Parameters
        ----------
        result : GbwResults | PropertyResults
            Results to be dumped.
        json_file : Path
            Path to JSON file to be written.
        """

        json_string: str = result.model_dump_json(indent=2)
        json_file.write_text(json_string)

    def get_file(self, suffix: str, /) -> Path:
        """
        Get path to file, by specifying file suffix (including the leading dot).
        Fullpath will be inferred from `self.working_dir` and `self.basename`.

        Parameters
        ----------
        suffix : str
            Suffix of file. Must include the leading dot.
        """
        return self.working_dir / (self.basename + suffix)

    def _get_version(self) -> "OrcaVersion":
        """Gets the ORCA version from the property-JSON file."""

        # > Path to property JSON needs to be set
        try:
            assert self.property_json_data
            return OrcaVersion.from_json(self.property_json_data)
        except AssertionError:
            raise ValueError(
                "Could not determine ORCA version, as JSON-property file has not been parsed."
            )
        except ValueError:
            raise

    def check_version(self) -> None:
        """
        Check if the version from the property-JSON file fits to minimally support ORCA version of the current OPI version.
        """
        try:
            version = self._get_version()
        except ValueError:
            warn("Could not determine ORCA version from JSON file. Subsequent error might occur.")
        else:
            if not check_minimal_version(version):
                raise RuntimeError(
                    f"JSON property file was created with unsupported ORCA version: {version}"
                )

    def _create_runner(self) -> "Runner":
        """Create a `Runner` object passing on `self.working_dir`."""
        return Runner(working_dir=self.working_dir)

    def create_gbw_json(self, *, force: bool = False, config: dict[str, Any] | None = None) -> None:
        """
        Thin-wrapper around `Runner.create_jsons()`.
        Creates the `<basename>.json` file.

        Parameters
        ----------
        force : bool, default = False
            Overwrite any existing ORCA GBW JSON file.
        config : dict[str | Any] | None, default = None
            Determine contents of gbw-json file.
            For details about the configuration refer to the ORCA manual "9.3.2 Configuration file"
        """
        runner = self._create_runner()
        runner.create_gbw_json(self.basename, config=config, force=force)

    def create_property_json(self, *, force: bool = False) -> None:
        """
        Thin-wrapper around `Runner.create_property_json()`.
        Create the `<basename>.property.json` file

        Parameters
        ----------
        force : bool, default = None
            Overwrite any existing ORCA property JSON file.
        """
        runner = self._create_runner()
        runner.create_property_json(self.basename, force=force)

    def create_jsons(self, *, force: bool = False) -> None:
        """
        Thin-wrapper around `Runner.create_jsons()`.
        Create the `<basename>.json` and the `<basename>.property.json` file

        Parameters
        ----------
        force : bool, default: None
            Overwrite any existing ORCA property and GBW JSON files.
        """
        runner = self._create_runner()
        runner.create_jsons(self.basename, force=force)

    def get_outfile(self) -> Path:
        """
        The full path to the ".out" file.
        """
        return self.get_file(".out")

    def terminated_normally(self) -> bool:
        """
        Determine if ORCA terminated normally, by looking for "ORCA TERMINATED NORMALLY" in the ".out" file.
        If the ".out" file does not exist, also return False.

        Returns
        -------
        bool
            True if "ORCA TERMINATED NORMALLY" is found in ".out" file else False
        """
        outfile = self.get_outfile()
        try:
            return has_terminated_normally(outfile)
        except FileNotFoundError:
            return False

    def scf_converged(self) -> bool:
        """
        Determine if ORCA SCF converged, by looking for "SUCCESS" in the ".out" file.
        Check only if ORCA SCF was actually requested.
        If the ".out" file does not exist, also return False.

        Returns
        -------
        bool
            True if "SUCCESS" is found in ".out" file else False
        """
        outfile = self.get_outfile()
        try:
            return has_scf_converged(outfile)
        except FileNotFoundError:
            return False

    def geometry_optimization_converged(self) -> bool:
        """
        Determine if ORCA geometry optimization converged, by looking for "HURRAY" in the ".out" file.
        Check only if ORCA geometry optimization was actually requested.
        If the ".out" file does not exist, also return False.

        Returns
        -------
        bool
            True if "HURRAY" is found in ".out" file else False
        """
        outfile = self.get_outfile()
        try:
            return has_geometry_optimization_converged(outfile)
        except FileNotFoundError:
            return False

    def _safe_get(self, *attrs: str | int) -> Any | None:
        """
        Safely access a nested chain of attributes or list indices on the output object.

        This method walks through a sequence of attributes (str) or indices (int),
        returning the nested value if all lookups succeed and none of the intermediate
        objects are None. If any step fails—due to a missing attribute, invalid index,
        or None encountered in the chain—it returns None instead of raising an exception.

        Parameters
        ----------
        *attrs : str | int
            A sequence of strings (attribute names) and/or integers (list or indexable
            container indices) that define the path to follow.

        Returns
        -------
        Any | None
            The resolved value at the end of the access path if all steps succeed;
            otherwise, None. Should be cast into the correct type for usage.

        Examples
        --------
            self._safe_get("results_properties", "geometries", index, "geometry")
            is equivalent to:
            self.results_properties.geometries[index].geometry
            but returns None if any part of the chain is missing or None, in a mypy-friendly way.
        """
        current = self
        for attr in attrs:
            if current is None:
                return None
            try:
                if isinstance(attr, int) and isinstance(current, list):
                    current = current[attr]
                elif isinstance(attr, str):
                    current = getattr(current, attr)
                else:
                    raise TypeError
            except (AttributeError, IndexError, TypeError):
                return None
        return current

    def _get_cartesians(
        self, index: int
    ) -> list[tuple[StrictStr, StrictFiniteFloat, StrictFiniteFloat, StrictFiniteFloat]] | None:
        """
        Returns cartesian coordinates from the output object for a specified index.

        Parameters
        ----------
        index : int
            index of geometry to return.

        Returns
        ----------
        cartesians: list[tuple[StrictStr, StrictFiniteFloat, StrictFiniteFloat, StrictFiniteFloat]] | None
            List containing the cartesian coordinates or None.
        """
        # > Safely get the cartesian coordinates
        cartesians = self._safe_get(
            "results_properties", "geometries", index, "geometry", "coordinates", "cartesians"
        )
        # > Cast them into the correct type
        if cartesians is not None:
            cartesians = cast(
                list[tuple[StrictStr, StrictFiniteFloat, StrictFiniteFloat, StrictFiniteFloat]],
                cartesians,
            )

        return cartesians

    def get_structure(self, *, index: int = -1) -> Structure:
        """
        Returns structure from ORCA job as Structure object. By default, the final structure is returned.

        Parameters
        ----------
        index : int, default: -1
            index of geometry to return (default: final)

        Returns
        ----------
        structure: Structure
            Returns structure object generated from the output for the given index.

        Raises
        ----------
        ValueError
            If no geometry with the requested index is available.
        """

        atoms: list[Atom] = []
        # > Get Cartesian coordinates
        cartesians = self._get_cartesians(index)

        if cartesians:
            for entry in cartesians:
                # > Get element symbol
                elem = entry[0]
                # > Get coordinates and convert to angstrom
                x = entry[1] * AU_TO_ANGST
                y = entry[2] * AU_TO_ANGST
                z = entry[3] * AU_TO_ANGST
                # > Generate atom and append to list
                atom = Atom(element=elem, coordinates=Coordinates((x, y, z)))
                atoms.append(atom)

            structure = Structure(atoms)
            return structure

        else:
            raise ValueError(
                f"Requested Cartesian coordinates for geometry with index {index} are not available."
            )

    def get_final_energy(self) -> StrictFiniteFloat | None:
        """
        Easy access to the final single point energy.

        Returns
        ----------
        final_energy: StrictFiniteFloat | None
            Returns the final energy of the ORCA calculation or None if there is none in the output.
        """

        # > Get the final energy
        final_energy = self._safe_get("results_properties", "single_point_data", "finalenergy")

        if final_energy is not None:
            final_energy = cast(StrictFiniteFloat, final_energy)

        return final_energy

    def get_energies(self, *, index: int = -1) -> dict[str, Energy] | None:
        """
        Return a dictionary with different energy types for the geometry at a given index.

        Parameters
        ----------
        index : int, default: -1
            Index of the geometry for which the energy should be returned. The default -1 refers to the final geometry.

        Returns
        -------
        energy_dict : dict[str, Energy] | None
            Dictionary where keys identify the energy type. If multiple energies of the same type are present, an index is
            appended after the first one, e.g., SCF, SCF_1, SCF_2, etc. If no energy is available None is returned.

        Notes
        -----
        Common keys include:
            - **Unknown**     : No information about the energy is provided.
            - **SCF**         : SCF energy from HF, DFT, or SQM methods.
            - **MDCI(SD)**    : Typically the (DLPNO-)CCSD energy.
            - **MDCI(SD(T))** : Typically the (DLPNO-)CCSD(T) energy.
            - **CASSCF**      : CASSCF energy.
            - **MP2**         : MP2 energy.
            - **TDA/CIS**     : TDA-TD-DFT or CIS energy.
        """

        # > Energy dict to populate & return
        energy_dict: dict[str, Energy] = {}

        # > Get the list of energies to be converted to a dictionary
        energy_list = self._safe_get("results_properties", "geometries", index, "energy")

        if energy_list is not None:
            energy_list = cast(EnergyList, energy_list)
        else:
            return None

        for energy in energy_list:
            if not energy.method:
                key = "Unknown"
            else:
                key = energy.method
            # > Add index at the end if multiple energies of the same type are present
            index = 1
            while key in energy_dict:
                key = f"{key}_{index}"
                index += 1
            energy_dict[key] = energy

        return energy_dict
