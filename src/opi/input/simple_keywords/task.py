from opi.input.simple_keywords.base import (
    SimpleKeyword,
    SimpleKeywordBox,
)

__all__ = ("Task",)


class Task(SimpleKeywordBox):
    """Enum to store all simple keywords of type Task.

    Attributes
    ----------
    SP : SimpleKeyword
        Perform a single point energy calculation (default)
    ENGRAD : SimpleKeyword
        Energy and gradient
    OPT : SimpleKeyword
        Perform a geometry optimization
    FREQ : SimpleKeyword
        Analytical frequency calculation
    NUMFREQ : SimpleKeyword
        Numerical frequency calculation
    MD : SimpleKeyword
        Molecular dynamics
    EDA : SimpleKeyword
        Perform an energy decomposition analysis (EDA)
    AUTOFRAG : SimpleKeyword
        Automatic detection of fragments.
    CIM : SimpleKeyword
        Calculate energy with clusters in molecule approach.
    SOLVATOR : SimpleKeyword
        Use the solvator for explicit solvation
    ENMGRAD : SimpleKeyword
        Energy normal mode gradient
    CALCESTHESS : SimpleKeyword
        Calculate an approximate hessian
    MT : SimpleKeyword
        mode trajectory
    NMSCAN : SimpleKeyword
        normal mode scan
    PRINTTHERMOCHEM : SimpleKeyword
        Only do thermostatistical corrections
    PROPERTIESONLY : SimpleKeyword
        Only calc properties
    NUMNAC : SimpleKeyword
        Numerical non-adiabatic coupling
    """

    SP = SimpleKeyword("sp")
    ENGRAD = SimpleKeyword("engrad")
    OPT = SimpleKeyword("opt")
    FREQ = SimpleKeyword("freq")
    NUMFREQ = SimpleKeyword("numfreq")
    MD = SimpleKeyword("md")
    EDA = SimpleKeyword("eda")
    AUTOFRAG = SimpleKeyword("autofrag")
    CIM = SimpleKeyword("cim")
    SOLVATOR = SimpleKeyword("solvator")
    ENMGRAD = SimpleKeyword("enmgrad")
    CALCESTHESS = SimpleKeyword("calcesthess")
    MT = SimpleKeyword("mt")
    NMSCAN = SimpleKeyword("nmscan")
    PRINTTHERMOCHEM = SimpleKeyword("printthermochem")
    PROPERTIESONLY = SimpleKeyword("propertiesonly")
    NUMNAC = SimpleKeyword("numnac")
