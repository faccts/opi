import json
import re
from pathlib import Path
from typing import Any

import pytest
from jsonschema import ValidationError as SchemaValidationError
from jsonschema import validate

from opi.output.models.json.gbw.properties.atoms import Atoms
from opi.output.models.json.gbw.properties.base import Base
from opi.output.models.json.gbw.properties.cite import Cite
from opi.output.models.json.gbw.properties.header import OrcaHeader
from opi.output.models.json.gbw.properties.mo import MO
from opi.output.models.json.gbw.properties.molecular_orbitals import (
    MolecularOrbitals,
)
from opi.output.models.json.gbw.properties.molecule import Molecule
from opi.output.models.json.gbw.properties.paper import Paper
from opi.output.models.json.gbw.properties.tddft import TdDft
from opi.output.models.json.property.properties.auto_ci_energy import AutoCiEnergy
from opi.output.models.json.property.properties.bs import BrokenSym
from opi.output.models.json.property.properties.calc_info import CalcInfo
from opi.output.models.json.property.properties.calc_status import (
    CalculationStatus,
)
from opi.output.models.json.property.properties.calc_time import (
    CalculationTiming,
)
from opi.output.models.json.property.properties.cas_energy import CasEnergy
from opi.output.models.json.property.properties.chem_shift import (
    ChemicalShift,
)
from opi.output.models.json.property.properties.ci_psi import CiPsi
from opi.output.models.json.property.properties.coord import Coordinates
from opi.output.models.json.property.properties.dft_energy import DftEnergy
from opi.output.models.json.property.properties.dipole_moment import DipoleMoment
from opi.output.models.json.property.properties.efg_tensor import EfgTensor
from opi.output.models.json.property.properties.energy_extrap import (
    EnergyExtrapolation,
)
from opi.output.models.json.property.properties.energy_list import (
    EnergyList,
)
from opi.output.models.json.property.properties.geometries import Geometries
from opi.output.models.json.property.properties.geometry import Geometry
from opi.output.models.json.property.properties.gradient import NucGradient
from opi.output.models.json.property.properties.gtensor import Gtensor
from opi.output.models.json.property.properties.hess import Hessian
from opi.output.models.json.property.properties.hirshfeld_population_analysis import (
    HirshfeldPopulationAnalysis,
)
from opi.output.models.json.property.properties.led import Led
from opi.output.models.json.property.properties.mayer_population_analysis import (
    MayerPopulationAnalysis,
)
from opi.output.models.json.property.properties.mbis_population_analysis import (
    MbisPopulationAnalysis,
)
from opi.output.models.json.property.properties.mdci_energy import (
    Mdcisd_t_Energies,
    MdcisdEnergies,
)
from opi.output.models.json.property.properties.mp2_energy import Mp2Energy
from opi.output.models.json.property.properties.nat_orbitals import (
    NaturalOrbitals,
)
from opi.output.models.json.property.properties.pal import PalFlags
from opi.output.models.json.property.properties.polarizability import (
    Polarizability,
)
from opi.output.models.json.property.properties.population_analysis import (
    PopulationAnalysis,
)
from opi.output.models.json.property.properties.quadrupole_moment import (
    QuadrupoleMoment,
)
from opi.output.models.json.property.properties.roci_en import RoCiEnergy
from opi.output.models.json.property.properties.scf_energy import ScfEnergy
from opi.output.models.json.property.properties.solvation import (
    SolvDetails,
)
from opi.output.models.json.property.properties.spectrum import Spectrum
from opi.output.models.json.property.properties.spin_coupling import (
    SpinSpinCoupling,
)
from opi.output.models.json.property.properties.tensor import Tensor
from opi.output.models.json.property.properties.thermo import (
    ThermochemistryEnergy,
)
from opi.output.models.json.property.properties.van_der_waals_correction import (
    VdwCorrection,
)
from opi.utils.misc import lowercase

###############################################################################
# Usage of this fixture
# Eg.: the testing of the class Spectrum in the file uvvis.property.json and roci.property.json:
#   @mark.parametrize("validate_json_schema",[["uvvis", "property", "absorption_spectrum", "Spectrum"], ["roci",  "property", "absorption_spectrum", "Spectrum"]], indirect = True)
#   def test_absorption(validate_json_schema):
#       assert validate_json_schema
# This way two tests are performed, indirect = True is needed to enable the indirect usage of parameter in the fixture.
# Order of the tuple: the name of the json file without suffixes, the type of json file (gbw.json or property.json),
# the key to access the right branch in the json file, the name of the class.
###############################################################################
# Adding a new Type for testing
# import module
# add Type to the dict valid type in function "get_schema" line 115
# "type_name": TypeName
###############################################################################


def _extract_index(key: str, /) -> tuple[str, int | str | None]:
    rgx = re.compile(
        r"^(?P<key>[a-zA-Z_][a-zA-Z0-9_]*)"
        r"(?:\[(?P<index>\d+|([\"'])\w+\3)\])?$"
    )

    match = rgx.match(key)
    if not match:
        return key, None

    base_key = match.group("key")
    index = match.group("index")

    if index is not None:
        try:
            index = int(index)
        except ValueError:
            pass
    return base_key, index


@pytest.fixture
def validate_json_schema(request: tuple[str, str, str, str]) -> bool:
    """
    fixture for testing the pydantic data types representing the Json objects with validation via jsonschema.
    Parameters are giving through a tuple named request and can be accessed via request.param[n] with n as an int.
    The four parameter given are in order: the name of the json file without suffixes, the type of json file (gbw.json or property.json),
    the key to access the right branch in the json file, the name of the class.

    Parameter
    ---------
    request: tuple[str, str, str, str]
        the name of the json file without suffixes, the type of json file (gbw.json or property.json),
        the key to access the right branch in the json file, the name of the class.

    Returns
    -------
    bool
        True if Type is a valid representation of the json object else False
    """
    json_file_name = request.param[0]
    type_of_json_file = request.param[1]
    key_in_json_file = request.param[2]
    name_of_datatype = request.param[3]

    # > Dissect key, as it might contain an index, e.g. "Geometries[2]" or "Data['test']"
    key_in_json_file, index = _extract_index(key_in_json_file)
    type_schema: dict = get_schema(name_of_datatype)
    type_as_json: dict = get_json_for_test(
        json_file_name, type_of_json_file, key_in_json_file, index
    )
    try:
        validate(instance=type_as_json, schema=type_schema)
        return True
    except SchemaValidationError as e:
        print("JSON is invalid:", e, type(type_as_json))
        return False


def get_schema(type_name: str) -> dict[str, Any]:
    """
    Produces a JSON scheme for the Class

    Parameter
    ---------
    type_name: str
        Name of Type

    Raises
    ------
    ValueError

    Returns
    -------
    dict[str, Any]
        JSON scheme of the class
    """
    # > valid_types are all types that occur in the gbw_json and property.json file
    valid_types = {
        "BrokenSym": BrokenSym,
        "CalcInfo": CalcInfo,
        "CalculationStatus": CalculationStatus,
        "CalculationTiming": CalculationTiming,
        "ChemicalShift": ChemicalShift,
        "CiPsi": CiPsi,
        "Coordinates": Coordinates,
        "DftEnergy": DftEnergy,
        "Dipole": DipoleMoment,
        "EfgTensor": EfgTensor,
        "EnergyExtrapolation": EnergyExtrapolation,
        "EnergyList": EnergyList,
        "Geometries": Geometries,
        "Geometry": Geometry,
        "Gtensor": Gtensor,
        "Hessian": Hessian,
        "HirshfeldPopulationAnalysis": HirshfeldPopulationAnalysis,
        "Led": Led,
        "MayerPopulationAnalysis": MayerPopulationAnalysis,
        "MbisPopAnalysis": MbisPopulationAnalysis,
        "ScfEnergy": ScfEnergy,
        "Mdcisd_Energies": MdcisdEnergies,
        "Mdcisd_t_Energies": Mdcisd_t_Energies,
        "Mp2Energy": Mp2Energy,
        "CasEnergy": CasEnergy,
        "AutoCiEnergy": AutoCiEnergy,
        "NaturalOrbitals": NaturalOrbitals,
        "NucGradient": NucGradient,
        "PalFlags": PalFlags,
        "Polarizability": Polarizability,
        "PopulationAnalysis": PopulationAnalysis,
        "QuadrupoleMoment": QuadrupoleMoment,
        "RoCiEnergy": RoCiEnergy,
        "SolvDetails": SolvDetails,
        "Spectrum": Spectrum,
        "SpinSpinCoupling": SpinSpinCoupling,
        "Tensor": Tensor,
        "ThermochemistryEnergy": ThermochemistryEnergy,
        "VdwCorrection": VdwCorrection,
        "Atoms": Atoms,
        "Base": Base,
        "Cite": Cite,
        "OrcaHeader": OrcaHeader,
        "MolecularOrbitals": MolecularOrbitals,
        "Molecule": Molecule,
        "MO": MO,
        "Paper": Paper,
        "TdDft": TdDft,
    }

    if type_name not in valid_types:
        raise ValueError
    else:
        schema = valid_types[type_name].model_json_schema()
    return schema


def get_json_for_test(
    json_file_name: str, type_of_json_file: str, key: str, index: str | int | None
) -> dict[str, Any]:
    """
    Parses the json file, and prepares the dictionary for testing

    Attributes
    ----------
    json_file_name: str
        Name of the JSON file used for the test
    type_of_json_file
        property if property.json else gbw
    key: None | str, default = None
        Key for the object that is handled by the tested class

    Returns
    -------
    dict[str, Any]
        A dictionary containing the part of the JSON file that is meddled by the tested class
    """

    data_from_file: dict[str, Any] = get_complete_json(json_file_name, type_of_json_file)
    unified_data = data_from_file
    lowercase(unified_data)
    test_json_struct = shorter_json(unified_data, key, index)

    return test_json_struct


def get_complete_json(json_file_name: str, type_of_json_file: str) -> dict[str, Any]:
    """
    Parses the json file according to the example number

    Attributes
    ----------
    example_number: int
        number of tested example
    type_of_json_file
        property if property.json else gbw

    Return
    ------
    dict[str, Any]
        The JSONfile as a Python dictionary

    """
    if type_of_json_file == "property":
        json_file_name += ".property"
    path_name = Path(__file__).resolve().parent / "json_files" / f"{json_file_name}.json"

    with open(path_name) as json_file:
        data_from_file: dict[str, Any] = json.load(json_file)
        return data_from_file


def shorter_json(
    complete_json: dict[str, Any], key: str, index: str | int | None
) -> dict[str, Any]:
    """
    Shortens the dictionary so it only contains the object that is parsed by the tested class

    Attributes
    ----------
    complete_json: dict[str, Any]
        The complete json as a dictionary
    key: str
        key for the object that is processed by the tested class
    index: str | int | None
        Optional index for lists or dict data types.

    Returns
    -------
    dict[str, Any]
        The shortened JSON as a dictionary
    """

    path_to_key = looking_for_key(complete_json, key)
    test_json = complete_json
    try:
        # > accesses the right branch of the json file step by step
        for key_index in range(len(path_to_key)):
            test_json = test_json[path_to_key[key_index]]

        # > If an index is giving, try to fetch the object from the container type.
        if index is not None:
            test_json = test_json[index]
        # > checks if the object accessed by the key is a list and returns the first value, since only dicts can be validated
        elif isinstance(test_json, list):
            test_json = test_json[0]

    except KeyError as error:
        print(error)
    return test_json


def looking_for_key(
    dictionary: dict[str, Any], key: str, path: list[str] | None = None
) -> list[str]:
    """
    Searching the path to the key in the dictionary

    Attributes
    ----------
    dictionary: dict[str, Any]
        The dictionary that get searched
    key: str
        The searched key
    path: list[str] | None default = None
        The current path in the dictionary

    Returns
    -------
    list[str]
        list with the key leading to the searched key
    """
    if not path:
        path = []
    path_to_key: list[str] = path
    if isinstance(dictionary, dict) and key not in path_to_key:
        for k, v in dictionary.items():
            new_path = path + [k]
            if k == key:
                path_to_key = new_path
                return path_to_key
            elif key not in path_to_key:
                path_to_key = looking_for_key(v, key, new_path)
    elif isinstance(dictionary, list):
        for index, item in enumerate(dictionary):
            if key not in path_to_key:
                new_path = path + [index]
                path_to_key = looking_for_key(item, key, new_path)
    return path_to_key
