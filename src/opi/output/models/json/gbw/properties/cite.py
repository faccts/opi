from opi.output.models.base.get_item import GetItem
from opi.output.models.json.gbw.properties.paper import Paper


class Cite(GetItem):
    """
    This class contains the keys for the papers that are necessary to cite

    Attributes
    ----------
    RN231: Paper | None, default None
        Key for the ORCA 2022 paper
    RN232: Paper | None, default None
        Key for the SHARK paper
    """

    rn231: Paper | None = None
    rn232: Paper | None = None
