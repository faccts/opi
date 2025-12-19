from pydantic import Field

from opi.output.models.json.gbw.properties.cite import Cite
from opi.output.models.json.gbw.properties.header import OrcaHeader
from opi.output.models.json.gbw.properties.molecule import Molecule
from opi.output.models.json_loadable import JSONLoadable


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
