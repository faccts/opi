from opi.input.simple_keywords.base import (
    SimpleKeyword,
    SimpleKeywordBox,
)

__all__ = ("Opt",)


class OptThreshold(SimpleKeywordBox):
    CRUDEOPT = SimpleKeyword("crudeopt", alias="crude")
    """SimpleKeyword: Geometry optimization with thresholds."""
    LOOSEOPT = SimpleKeyword("looseopt", alias="loose")
    """SimpleKeyword: Geometry optimization with thresholds."""
    NORMALOPT = SimpleKeyword("normalopt", alias="normal")
    """SimpleKeyword: Geometry optimization with thresholds."""
    SLOPPYOPT = SimpleKeyword("sloppyopt", alias="sloppy")
    """SimpleKeyword: Geometry optimization with thresholds."""
    TIGHTOPT = SimpleKeyword("tightopt", alias="tight")
    """SimpleKeyword: Geometry optimization with thresholds."""
    VERYTIGHTOPT = SimpleKeyword("verytightopt", alias="verytight")
    """SimpleKeyword: Geometry optimization with thresholds."""


class Opt(OptThreshold):
    """Enum to store all simple keywords of type Opt."""

    OPT = SimpleKeyword("opt")
    """SimpleKeyword: Perform a geometry optimization."""
    INTERPOPT = SimpleKeyword("interpopt")
    """SimpleKeyword: Geometry optimization with thresholds."""
    OPTH = SimpleKeyword("opth")
    """SimpleKeyword: Optimize only hydrogen atoms."""
    COPT = SimpleKeyword("copt")
    """SimpleKeyword: Perform geometry optimization (cartesian coordinates)."""
    L_OPT = SimpleKeyword("l-opt")
    """SimpleKeyword: Perform geometry optimization."""
    L_OPTH = SimpleKeyword("l-opth")
    """SimpleKeyword: Optimize only hydrogen atoms."""
    OPTTS = SimpleKeyword("optts")
    """SimpleKeyword: optimize transition state."""
    OPTTS_GMF = SimpleKeyword("optts(gmf)")
    """SimpleKeyword: optimize transition state."""
    QMMMOPT = SimpleKeyword("qmmmopt")
    """SimpleKeyword: Optimize the geometry with qmmm."""
    QMMMOPT_PDYNAMO = SimpleKeyword("qmmmopt/pdynamo")
    """SimpleKeyword: Optimize the geometry with qmmm."""
    RIGIDBODYOPT = SimpleKeyword("rigidbodyopt")
    """SimpleKeyword: Optimize fragments as rigid bodies."""
    CI_OPT = SimpleKeyword("ci-opt")
    """SimpleKeyword: conical-intersection optimization."""
    MECP_OPT = SimpleKeyword("mecp-opt")
    """SimpleKeyword: MECP optimization."""
