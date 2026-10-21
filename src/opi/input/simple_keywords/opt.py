from opi.input.simple_keywords.base import (
    ORCAKeyword,
    SimpleKeywordBox,
)

__all__ = ("Opt",)


class OptThreshold(SimpleKeywordBox):
    CRUDEOPT = ORCAKeyword("crudeopt", alias="crude")
    """ORCAKeyword: Geometry optimization with thresholds."""
    LOOSEOPT = ORCAKeyword("looseopt", alias="loose")
    """ORCAKeyword: Geometry optimization with thresholds."""
    NORMALOPT = ORCAKeyword("normalopt", alias="normal")
    """ORCAKeyword: Geometry optimization with thresholds."""
    SLOPPYOPT = ORCAKeyword("sloppyopt", alias="sloppy")
    """ORCAKeyword: Geometry optimization with thresholds."""
    TIGHTOPT = ORCAKeyword("tightopt", alias="tight")
    """ORCAKeyword: Geometry optimization with thresholds."""
    VERYTIGHTOPT = ORCAKeyword("verytightopt", alias="verytight")
    """ORCAKeyword: Geometry optimization with thresholds."""


class Opt(OptThreshold):
    """Enum to store all simple keywords of type Opt."""

    OPT = ORCAKeyword("opt")
    """ORCAKeyword: Perform a geometry optimization."""
    INTERPOPT = ORCAKeyword("interpopt")
    """ORCAKeyword: Geometry optimization with thresholds."""
    OPTH = ORCAKeyword("opth")
    """ORCAKeyword: Optimize only hydrogen atoms."""
    COPT = ORCAKeyword("copt")
    """ORCAKeyword: Perform geometry optimization (cartesian coordinates)."""
    L_OPT = ORCAKeyword("l-opt")
    """ORCAKeyword: Perform geometry optimization."""
    L_OPTH = ORCAKeyword("l-opth")
    """ORCAKeyword: Optimize only hydrogen atoms."""
    OPTTS = ORCAKeyword("optts")
    """ORCAKeyword: optimize transition state."""
    OPTTS_GMF = ORCAKeyword("optts(gmf)")
    """ORCAKeyword: optimize transition state."""
    QMMMOPT = ORCAKeyword("qmmmopt")
    """ORCAKeyword: Optimize the geometry with qmmm."""
    QMMMOPT_PDYNAMO = ORCAKeyword("qmmmopt/pdynamo")
    """ORCAKeyword: Optimize the geometry with qmmm."""
    RIGIDBODYOPT = ORCAKeyword("rigidbodyopt")
    """ORCAKeyword: Optimize fragments as rigid bodies."""
    CI_OPT = ORCAKeyword("ci-opt")
    """ORCAKeyword: conical-intersection optimization."""
    MECP_OPT = ORCAKeyword("mecp-opt")
    """ORCAKeyword: MECP optimization."""
