from opi.input.simple_keywords.base import (
    ORCAKeyword,
    SimpleKeywordBox,
)

__all__ = ("Task",)


class Task(SimpleKeywordBox):
    """Enum to store all simple keywords of type Task."""

    SP = ORCAKeyword("sp")
    """ORCAKeyword: Perform a single point energy calculation (default)."""
    ENGRAD = ORCAKeyword("engrad")
    """ORCAKeyword: Energy and gradient."""
    OPT = ORCAKeyword("opt")
    """ORCAKeyword: Perform a geometry optimization."""
    FREQ = ORCAKeyword("freq")
    """ORCAKeyword: Analytical frequency calculation."""
    NUMFREQ = ORCAKeyword("numfreq")
    """ORCAKeyword: Numerical frequency calculation."""
    MD = ORCAKeyword("md")
    """ORCAKeyword: Molecular dynamics."""
    EDA = ORCAKeyword("eda")
    """ORCAKeyword: Perform an energy decomposition analysis (EDA)."""
    AUTOFRAG = ORCAKeyword("autofrag")
    """ORCAKeyword: Automatic detection of fragments.."""
    CIM = ORCAKeyword("cim")
    """ORCAKeyword: Calculate energy with clusters in molecule approach.."""
    SOLVATOR = ORCAKeyword("solvator")
    """ORCAKeyword: Use the solvator for explicit solvation."""
    ENMGRAD = ORCAKeyword("enmgrad")
    """ORCAKeyword: Energy normal mode gradient."""
    CALCESTHESS = ORCAKeyword("calcesthess")
    """ORCAKeyword: Calculate an approximate hessian."""
    MT = ORCAKeyword("mt")
    """ORCAKeyword: mode trajectory."""
    NMSCAN = ORCAKeyword("nmscan")
    """ORCAKeyword: normal mode scan."""
    PRINTTHERMOCHEM = ORCAKeyword("printthermochem")
    """ORCAKeyword: Only do thermostatistical corrections."""
    PROPERTIESONLY = ORCAKeyword("propertiesonly")
    """ORCAKeyword: Only calc properties."""
    NUMNAC = ORCAKeyword("numnac")
    """ORCAKeyword: Numerical non-adiabatic coupling."""
