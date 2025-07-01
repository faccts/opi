from opi.input.simple_keywords.base import (
    SimpleKeyword,
    SimpleKeywordBox,
)

__all__ = ("Opt",)


class Opt(SimpleKeywordBox):
    """Enum to store all simple keywords of type Opt.

    Attributes
    ----------
    OPT : SimpleKeyword
        Perform geometry optimization
    CRUDEOPT : SimpleKeyword
        Geometry optimization with thresholds
    INTERPOPT : SimpleKeyword
        Geometry optimization with thresholds
    LOOSEOPT : SimpleKeyword
        Geometry optimization with thresholds
    NORMALOPT : SimpleKeyword
        Geometry optimization with thresholds
    SLOPPYOPT : SimpleKeyword
        Geometry optimization with thresholds
    TIGHTOPT : SimpleKeyword
        Geometry optimization with thresholds
    VERYTIGHTOPT : SimpleKeyword
        Geometry optimization with thresholds
    OPTH : SimpleKeyword
        Optimize only hydrogen atoms
    COPT : SimpleKeyword
        Perform geometry optimization (cartesian coordinates)
    L_OPT : SimpleKeyword
        Perform geometry optimization
    L_OPTH : SimpleKeyword
        Optimize only hydrogen atoms
    OPTTS : SimpleKeyword
        optimize transition state
    OPTTS_GMF : SimpleKeyword
        optimize transition state
    QMMMOPT : SimpleKeyword
        Optimize the geometry with qmmm
    QMMMOPT_PDYNAMO : SimpleKeyword
        Optimize the geometry with qmmm
    RIGIDBODYOPT : SimpleKeyword
        Optimize fragments as rigid bodies
    CI_OPT : SimpleKeyword
        conical-intersection optimization
    MECP_OPT : SimpleKeyword
        MECP optimization
    """

    OPT = SimpleKeyword("opt")
    CRUDEOPT = SimpleKeyword("crudeopt")
    INTERPOPT = SimpleKeyword("interpopt")
    LOOSEOPT = SimpleKeyword("looseopt")
    NORMALOPT = SimpleKeyword("normalopt")
    SLOPPYOPT = SimpleKeyword("sloppyopt")
    TIGHTOPT = SimpleKeyword("tightopt")
    VERYTIGHTOPT = SimpleKeyword("verytightopt")
    OPTH = SimpleKeyword("opth")
    COPT = SimpleKeyword("copt")
    L_OPT = SimpleKeyword("l-opt")
    L_OPTH = SimpleKeyword("l-opth")
    OPTTS = SimpleKeyword("optts")
    OPTTS_GMF = SimpleKeyword("optts(gmf)")
    QMMMOPT = SimpleKeyword("qmmmopt")
    QMMMOPT_PDYNAMO = SimpleKeyword("qmmmopt/pdynamo")
    RIGIDBODYOPT = SimpleKeyword("rigidbodyopt")
    CI_OPT = SimpleKeyword("ci-opt")
    MECP_OPT = SimpleKeyword("mecp-opt")
