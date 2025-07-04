from opi.input.simple_keywords.base import (
    SimpleKeyword,
    SimpleKeywordBox,
)

__all__ = ("Opt",)


class Opt(SimpleKeywordBox):
    """Enum to store all simple keywords of type Opt"""

    OPT = SimpleKeyword("opt")  # Perform geometry optimization
    CRUDEOPT = SimpleKeyword("crudeopt")  # Geometry optimization with thresholds
    INTERPOPT = SimpleKeyword("interpopt")  # Geometry optimization with thresholds
    LOOSEOPT = SimpleKeyword("looseopt")  # Geometry optimization with thresholds
    NORMALOPT = SimpleKeyword("normalopt")  # Geometry optimization with thresholds
    SLOPPYOPT = SimpleKeyword("sloppyopt")  # Geometry optimization with thresholds
    TIGHTOPT = SimpleKeyword("tightopt")  # Geometry optimization with thresholds
    VERYTIGHTOPT = SimpleKeyword("verytightopt")  # Geometry optimization with thresholds
    OPTH = SimpleKeyword("opth")  # Optimize only hydrogen atoms
    COPT = SimpleKeyword("copt")  # Perform geometry optimization (cartesian coordinates)
    L_OPT = SimpleKeyword("l-opt")  # Perform geometry optimization
    L_OPTH = SimpleKeyword("l-opth")  # Optimize only hydrogen atoms
    OPTTS = SimpleKeyword("optts")  # optimize transition state
    OPTTS_GMF = SimpleKeyword("optts(gmf)")  # optimize transition state
    QMMMOPT = SimpleKeyword("qmmmopt")  # Optimize the geometry with qmmm
    QMMMOPT_PDYNAMO = SimpleKeyword("qmmmopt/pdynamo")  # Optimize the geometry with qmmm
    RIGIDBODYOPT = SimpleKeyword("rigidbodyopt")  # Optimize fragments as rigid bodies
    CI_OPT = SimpleKeyword("ci-opt")  # conical-intersection optimization
    MECP_OPT = SimpleKeyword("mecp-opt")  # MECP optimization
