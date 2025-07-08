from opi.input.simple_keywords.base import (
    SimpleKeyword,
    SimpleKeywordBox,
)

__all__ = ("Task",)


class Task(SimpleKeywordBox):
    """Enum to store all simple keywords of type Task."""

    SP = SimpleKeyword("sp")
    """SimpleKeyword: Perform a single point energy calculation (default)."""
    ENGRAD = SimpleKeyword("engrad")
    """SimpleKeyword: Energy and gradient."""
    OPT = SimpleKeyword("opt")
    """SimpleKeyword: Perform a geometry optimization."""
    FREQ = SimpleKeyword("freq")
    """SimpleKeyword: Analytical frequency calculation."""
    NUMFREQ = SimpleKeyword("numfreq")
    """SimpleKeyword: Numerical frequency calculation."""
    MD = SimpleKeyword("md")
    """SimpleKeyword: Molecular dynamics."""
    EDA = SimpleKeyword("eda")
    """SimpleKeyword: Perform an energy decomposition analysis (EDA)."""
    AUTOFRAG = SimpleKeyword("autofrag")
    """SimpleKeyword: Automatic detection of fragments.."""
    CIM = SimpleKeyword("cim")
    """SimpleKeyword: Calculate energy with clusters in molecule approach.."""
    SOLVATOR = SimpleKeyword("solvator")
    """SimpleKeyword: Use the solvator for explicit solvation."""
    ENMGRAD = SimpleKeyword("enmgrad")
    """SimpleKeyword: Energy normal mode gradient."""
    CALCESTHESS = SimpleKeyword("calcesthess")
    """SimpleKeyword: Calculate an approximate hessian."""
    MT = SimpleKeyword("mt")
    """SimpleKeyword: mode trajectory."""
    NMSCAN = SimpleKeyword("nmscan")
    """SimpleKeyword: normal mode scan."""
    PRINTTHERMOCHEM = SimpleKeyword("printthermochem")
    """SimpleKeyword: Only do thermostatistical corrections."""
    PROPERTIESONLY = SimpleKeyword("propertiesonly")
    """SimpleKeyword: Only calc properties."""
    NUMNAC = SimpleKeyword("numnac")
    """SimpleKeyword: Numerical non-adiabatic coupling."""
