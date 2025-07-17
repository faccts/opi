"""
This module contains the main class for output handling.
It's mostly based on the ORCA's two JSONs files.
"""

import json
from pathlib import Path
from typing import Any, cast
from warnings import warn

from pydantic import StrictInt, StrictStr

from opi.execution.core import Runner
from opi.input.structures import Atom, Coordinates, Structure
from opi.output.cube import CubeOutput
from opi.output.grepper.recipes import (
    has_geometry_optimization_converged,
    has_scf_converged,
    has_terminated_normally,
)
from opi.output.hftypes import Hftypes
from opi.output.models.base.strict_types import (
    StrictFiniteFloat,
    StrictNonNegativeInt,
    StrictPositiveInt,
)
from opi.output.models.json.gbw.gbw_results import GbwResults
from opi.output.models.json.gbw.properties.mos import MO
from opi.output.models.json.property.properties.energy import Energy
from opi.output.models.json.property.properties.energy_list import EnergyList
from opi.output.models.json.property.property_results import (
    PropertyResults,
)
from opi.utils.misc import check_minimal_version, lowercase
from opi.utils.orca_version import OrcaVersion
from opi.utils.units import AU_TO_ANGST, AU_TO_EV


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

    def run_orca_plot(
        self, stdin_list: list[str], *, suffix: str = ".gbw", timeout: int = -1
    ) -> None:
        """
        Executes orca_plot and passes it an input list stdin_list that specifies what to plot.

        Parameters
        ----------
        stdin_list : list[str]
            Input list for interactive orca_plot session
        suffix : str, default ".gbw"
            Determines the suffix of the gbw file to use.
        timeout : int, default: = -1
            Timeout in seconds to wait for ORCA process.
            If value is smaller than zero, wait indefinitely.

        Raises
        ----------
        ValueError
            If the input string is empty a ValueError is raised.
        FileNotFoundError
            If the gbwfile {basename}{suffix} is not found.
        """
        runner = self._create_runner()
        gbwfile = self.working_dir / f"{self.basename}{suffix}"

        # if no input for orca_plot is given
        if not stdin_list:
            raise ValueError("No input (stdin_list) supplied for orca_plot, but input is required!")

        runner.run_orca_plot(gbwfile, stdin_list, timeout=timeout)

    def plot_mo(
        self,
        index: StrictNonNegativeInt,
        /,
        *,
        operator: StrictNonNegativeInt = 0,
        resolution: StrictNonNegativeInt = 40,
        timeout: int = 300,
    ) -> CubeOutput | None:
        """
        Generates and returns the cube file for a molecular orbital by running the orca_plot binary.
        **Attention:** will terminate orca_plot after 300 seconds by default. If you plot something large you will have
        to adapt this threshold or set it to -1 for waiting indefinitely!

        Parameters
        ----------
        index: StrictNonNegativeInt
            Index of the MO to plot.
        operator : StrictNonNegativeInt, default=0
            Operator of the MO, alpha MOs are indicated by 0 and beta MOs by 1.
        resolution: StrictNonNegativeInt, default=40
            Resolution of the generated cube file. Higher numbers result in smoother plots, but also in longer orca_plot
            run time and a larger cube file.
        timeout: int, default = 300
            Time after which orca_plot will be stopped. 300 seconds should be sufficient for most MOs but when something
            large is plotted set this to a larger value or to -1 for waiting indefinitely long.

        Returns
        -------
        CubeOutput | None
            Returns the cube output object or returns None if the cube file cannot be retrieved.
        """

        operator_list = ["a", "b"]

        # > Define input string for orca_plot.
        # > If anything goes wrong orca_plot should exit.
        stdin_list = [
            "1",  # Select type of plot
            "1",  # Enter MO plot
            "2",  # Select index of orbital
            str(index),  # Enter index
            "3",  # Select alpha/beta operator
            str(operator),  # Enter alpha/beta (0/1)
            "4",  # Select the resolution (grid size) settings
            str(resolution),  # Enter resolution
            "5",  # Select the output format
            "7",  # Request cube file format
            "11",  # Perform the plotting
            "12",  # Exit the program
        ]
        self.run_orca_plot(stdin_list, timeout=timeout)

        # > get the resulting cube file as string
        cube_file = self.working_dir / f"{self.basename}.mo{index}{operator_list[operator]}.cube"

        if not cube_file.is_file():
            return None

        return CubeOutput(cube_file)

    def plot_density(
        self, /, *, resolution: StrictNonNegativeInt = 40, timeout: int = 600, suffix: str = ".scfp"
    ) -> CubeOutput | None:
        """
        Generates and returns the cube file for the density by running the orca_plot binary.
        **Attention:** will terminate orca_plot after 600 seconds by default. If you plot something large you will have
        to adapt this threshold or set it to -1 for waiting indefinitely!

        Parameters
        ----------
        resolution: StrictNonNegativeInt, default=40
            Resolution of the generated cube file. Higher numbers result in smoother plots, but also in longer orca_plot
            run time and a larger cube file.
        timeout: int, default = 600
            Time after which orca_plot will be stopped. 600 seconds should be sufficient for most MOs but when something
            large is plotted set this to a larger value or to -1 for waiting indefinitely long.
        suffix: str, default = ".scfp"
            suffix for selecting different densities, e.g., FOD via ".scfp_fod".
        Returns
        -------
        CubeOutput | None
            Returns the cube output object or returns None if the cube file cannot be retrieved.
        """
        # > Define input string for orca_plot.
        # > If anything goes wrong orca_plot should exit.
        stdin_list = [
            "1",  # Select type of plot
            "2",  # Enter density plot
            "n",  # Do not use the default density
            f"{self.basename}{suffix}",  # Select density file
            "4",  # Select the resolution (grid size) settings
            str(resolution),  # Enter resolution
            "5",  # Select the output format
            "7",  # Request cube file format
            "11",  # Perform the plotting
            "12",  # Exit the program
        ]
        self.run_orca_plot(stdin_list, timeout=timeout)

        # > get the resulting cube file as string
        cube_file = self.working_dir / f"{self.basename}.eldens.cube"

        if not cube_file.is_file():
            return None

        return CubeOutput(cube_file)

    def plot_spin_density(
        self,
        /,
        *,
        resolution: StrictNonNegativeInt = 40,
        timeout: int = 600,
    ) -> CubeOutput | None:
        """
        Generates and returns the cube file for the spin-density by running the orca_plot binary. Note that for RHF/RKS
        calculations the density will be returned.
        **Attention:** will terminate orca_plot after 600 seconds by default. If you plot something large you will have
        to adapt this threshold or set it to -1 for waiting indefinitely!

        Parameters
        ----------
        resolution: StrictNonNegativeInt, default=40
            Resolution of the generated cube file. Higher numbers result in smoother plots, but also in longer orca_plot
            run time and a larger cube file.
        timeout: int, default = 600
            Time after which orca_plot will be stopped. 600 seconds should be sufficient for most MOs but when something
            large is plotted set this to a larger value or to -1 for waiting indefinitely long.

        Returns
        -------
        CubeOutput | None
            Returns the cube output object or returns None if the cube file cannot be retrieved.
        """
        # > Define input string for orca_plot.
        # > If anything goes wrong orca_plot should exit.
        stdin_list = [
            "1",  # Select type of plot
            "3",  # Enter spin density plot
            "y",  # Use default density
            "4",  # Select the resolution (grid size) settings
            str(resolution),  # Enter resolution
            "5",  # Select the output format
            "7",  # Request cube file format
            "11",  # Perform the plotting
            "12",  # Exit the program
        ]
        self.run_orca_plot(stdin_list, timeout=timeout)

        # > get the resulting cube file as string
        cube_file = self.working_dir / f"{self.basename}.spindens.cube"

        if not cube_file.is_file():
            return None

        return CubeOutput(cube_file)

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

    def get_hftype(self) -> Hftypes | None:
        """
        Get the HFType from GBW json file.

        Returns
        -------
        hftype : Hftypes | None
        """
        hftype = self._safe_get("results_gbw", "molecule", "hftyp")
        if hftype is not None:
            hftype = cast(str, hftype)
            try:
                hftype = Hftypes(hftype)
                return hftype
            except ValueError:
                return None
        else:
            return None

    def get_charge(self) -> StrictInt | None:
        """
        Get the molecular charge from the json properties file.

        Returns
        -------
        charge : int | None
        """
        charge = self._safe_get("results_properties", "calculation_info", "charge")

        if charge is not None:
            charge = cast(int, charge)

        return charge

    def get_mult(self) -> StrictPositiveInt | None:
        """
        Get the molecular electron multiplicity from the json properties file.

        Returns
        -------
        mult : int | None
        """
        mult = self._safe_get("results_properties", "calculation_info", "mult")

        if mult is not None:
            mult = cast(int, mult)

        return mult

    def get_nelectrons(
        self, *, spin_resolved: bool = False
    ) -> tuple[int, int | None] | tuple[None, None]:
        """
        Get the number of electrons from property results. If requested separated into alpha and beta.

        Parameters
        -------
        spin_resolved: bool, default=False
            If True, the numbers of electrons are returned as alpha and beta electrons separately, if False,
            the total number of electrons is returned.

        Returns
        -------
        nalpha : int | None
            * None: if no electrons could be retrieved, or no multiplicity for spin resolution is available.
            * int:
                * if `spin_resolved == False`, the total number of electrons
                * if `spin_resolved == True`, the number of alpha electrons.
        nbeta : int | None
            * None:
                * if no electrons could be retrieved, or no multiplicity for spin resolution is available.
                * if `spin_resolved == False`
            * int : number of beta electrons (requires `spin_resolved == True`)
        """
        nel = self._safe_get("results_properties", "calculation_info", "numofelectrons")

        if nel is not None:
            nel = cast(int, nel)
        else:
            return None, None

        # > Return total number of electrons
        if not spin_resolved:
            return nel, None

        # > Get the electron spin multiplicity
        mult = self.get_mult()
        if mult is None:
            return None, None

        # > Calculate amount of alpha and beta electrons
        nalpha = nel // 2 + (mult - 1)
        nbeta = nel - nalpha

        # > Return spin resolved number of electrons
        return nalpha, nbeta

    def get_final_energy(self, *, index: int = -1) -> StrictFiniteFloat | None:
        """
        Easy access to the final single point energy.

        Parameters
        ----------
        index : int, default: -1
            Index of the geometry for which the energy should be returned. The default -1 refers to the final geometry.
            Silently ignores if the requested index is not available and returns None.

        Returns
        ----------
        final_energy: StrictFiniteFloat | None
            Returns the final energy of the ORCA calculation or None if there is none in the output for the requested index.
        """

        # > Get the final energy
        final_energy = self._safe_get(
            "results_properties", "geometries", index, "single_point_data", "finalenergy"
        )

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
            Silently ignores if the requested index is not available and returns None.

        Returns
        -------
        energy_dict : dict[str, Energy] | None
            Dictionary where keys identify the energy type. If multiple energies of the same type are present, an index is
            appended after the first one, e.g., SCF, SCF_1, SCF_2, etc. If no energy for the requested index is available None is returned.

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

    def get_gradient(self, *, index: int = -1) -> list[StrictFiniteFloat] | None:
        """
        Easy access to the nuclear gradient

        Parameters
        ----------
        index : int, default: -1
            index of geometry for which the gradient is to be returned. The default -1 refers to the final geometry.
            **Attention:** In a normal geometry optimization ORCA does not calculate the gradient for the final
            geometry, so the default index will return None. You can request the gradient for the structure one step
            before the final one with the index -2. For most intents and purposes, the last and second to last
            geometries, energies and gradients are the same within the given tolerances.

        Returns
        ----------
        list[StrictFiniteFloat] | None
            Returns nuclear gradient (packed in order x1, y1, z1, x2 y2, z2, ... in Eh/Bohr) for the given index
            or None if it cannot be obtained.
        """
        # > Safely get the gradient
        gradient = self._safe_get(
            "results_properties", "geometries", index, "nuclear_gradient", 0, "grad"
        )

        # > Cast them into the correct type
        if gradient is not None:
            gradient = cast(
                list[list[StrictFiniteFloat]],
                gradient,
            )
            flat = [inner[0] for inner in gradient]
            gradient = flat

        return gradient

    def get_structure(self, *, index: int = -1, with_fragments: bool = True) -> Structure | None:
        """
        Returns structure from ORCA job as Structure object (by default the final structure).
        Silently returns None of no structure is available.

        Parameters
        ----------
        index : int, default: -1
            index of geometry to return. The default -1 refers to the final geometry.
        with_fragments : bool, default: True
            whether the fragment IDs should be added as well to the structure (if available)

        Returns
        ----------
        structure: Structure | None
            Returns structure object generated from the output for the given index or None if no structure is available.
        """

        atoms: list[Atom] = []
        # > Get Cartesian coordinates
        cartesians = self._get_cartesians(index)

        if cartesians is None:
            return None

        for line in cartesians:
            elem, x_au, y_au, z_au = line
            # > Get coordinates and convert to angstrom
            x = x_au * AU_TO_ANGST
            y = y_au * AU_TO_ANGST
            z = z_au * AU_TO_ANGST
            # > Generate atom and append to list
            atom = Atom(element=elem, coordinates=Coordinates((x, y, z)))
            atoms.append(atom)

        if with_fragments:
            # > Get fragment IDs
            fragments = self._get_fragments(index)

            if fragments:
                for atom, frag in zip(atoms, fragments):
                    atom.fragment_id = frag[0]

        structure = Structure(atoms)

        # > Add charge data
        charge = self.get_charge()
        if charge is not None:
            structure.charge = charge

        # > Add multiplicity data
        mult = self.get_mult()
        if mult is not None:
            structure.multiplicity = mult
        return structure

    def _get_cartesians(
        self, index: int, /
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

    def _get_fragments(self, index: int, /) -> list[list[StrictPositiveInt]] | None:
        """
        Returns fragment ids from the output object for a specified geometry index.

        Parameters
        ----------
        index : int
            index of geometry to return.

        Returns
        ----------
        fragments: list[tuple[StrictStr, StrictFiniteFloat, StrictFiniteFloat, StrictFiniteFloat]] | None
            List containing the cartesian coordinates or None.
        """
        # > Safely get the fragment IDs
        fragments = self._safe_get(
            "results_properties", "geometries", index, "geometry", "fragments"
        )
        # > Cast them into the correct type
        if fragments:
            fragments = cast(
                list[list[StrictPositiveInt]],
                fragments,
            )

        return fragments

    def get_mos(self) -> dict[str, list[MO]] | None:
        """
        Returns a dictionary with list(s) of molecular orbitals.

        Returns
        -------
        dict[str, list[MO]] | None
            Dictionary containing the molecular orbitals as lists.

        Notes
        -----
        The keys are:
            - **mos**     : RHF/ROHF orbitals
            - **alpha**   : UHF alpha orbitals
            - **beta**    : UHF beta orbitals
        """
        molecular_orbitals = self._safe_get("results_gbw", "molecule", "molecularorbitals", "mos")
        if molecular_orbitals is not None:
            mos = {}
            cast(list[MO], molecular_orbitals)
            # > Get the hftype (e.g. rhf / uhf)
            hftype = self.get_hftype()
            # > Sort for UHF
            if hftype == Hftypes.UHF:
                offset = len(molecular_orbitals) // 2
                mos["alpha"] = molecular_orbitals[:offset]
                mos["beta"] = molecular_orbitals[offset:]
            else:
                mos["mos"] = molecular_orbitals
            return mos
        else:
            return None

    @staticmethod
    def _find_homo(mo_list: list[MO]) -> int | None:
        """
        Find and return the index of the highest occupied molecular orbital HOMO in energy ordered list of MOs.

        Parameter
        -------
        mo_list: list[MO]

        Returns
        -------
        int | None
            index of HOMO, or None, if the HOMO could not be found.
        """

        # > Search for the index of the LUMO
        index = next((i for i, mo in enumerate(mo_list) if mo.occupancy == 0), None)
        if index is not None and index >= 1:
            # > HOMO is LUMO-1
            index -= 1
            return index

        return None

    def get_homo(self) -> MO | None:
        """
        Returns the highest occupied molecular orbital (HOMO, or SOMO for UHF)

        Returns
        -------
        MO | None
            Returns the HOMO (or SOMO), or None, if the HOMO could not be found
        """
        homo: MO | None = None
        mos = self.get_mos()

        if mos is not None:
            for channel in mos:
                # > find homo for spin channel
                index = self._find_homo(mos[channel])
                if index is not None:
                    channel_homo = mos[channel][index]
                    if channel_homo.orbitalenergy is not None:
                        # > Check if spin channel homo is the actual homo
                        if homo is None:
                            homo = channel_homo
                        else:
                            # > Compare energies and pick highest
                            if (
                                homo.orbitalenergy is not None
                                and channel_homo.orbitalenergy > homo.orbitalenergy
                            ):
                                homo = channel_homo
        return homo

    @staticmethod
    def _find_lumo(mo_list: list[MO]) -> int | None:
        """
        Find and return the index of the lowest unoccupied molecular orbital LUMO in energy ordered list of MOs.

        Parameter
        -------
        mo_list: list[MO]

        Returns
        -------
        int | None
            index of LUMO, or None, if the LUMO could not be found.
        """
        index = next((i for i, mo in enumerate(mo_list) if mo.occupancy == 0), None)
        if index is not None:
            return index

        return None

    def get_lumo(self) -> MO | None:
        """
        Returns the lowest unoccupied molecular orbital (LUMO)

        Returns
        -------
        MO | None
            Returns the LUMO, or None, if the LUMO could not be found
        """
        lumo: MO | None = None
        mos = self.get_mos()

        if mos is not None:
            for channel in mos:
                # > find lumo for spin channel
                index = self._find_lumo(mos[channel])
                if index is not None:
                    channel_lumo = mos[channel][index]
                    if channel_lumo.orbitalenergy is not None:
                        # > Check if spin channel lumo is the actual lumo
                        if lumo is None:
                            lumo = channel_lumo
                        else:
                            # > pick lowest lumo
                            if (
                                lumo.orbitalenergy is not None
                                and channel_lumo.orbitalenergy < lumo.orbitalenergy
                            ):
                                lumo = channel_lumo
        return lumo

    def get_hl_gap(self) -> float | None:
        """
        Returns the HOMO-LUMO gap in eV

        Returns
        -------
        float | None
            Returns the HOMO-LUMO gap in eV or None if the gap could not be obtained.
        """
        homo = self.get_homo()
        lumo = self.get_lumo()

        if homo is not None and lumo is not None:
            if homo.orbitalenergy is not None and lumo.orbitalenergy is not None:
                return (lumo.orbitalenergy - homo.orbitalenergy) * AU_TO_EV

        return None
