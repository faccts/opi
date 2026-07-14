"""
Contains patterns for ORCA health checks and error checking capabilities.
At the end of the file the list of ErrorPatterns is found that is used to generate the output of `get_error_messages`.
"""

from opi.output.grepper.error_pattern import (
    ErrorPattern,
    InvalidLineError,
    NotEnoughMemoryScfError,
    SimpleKeywordsError,
    UnknownBlockError,
    UnknownBlockKeyError,
    UnknownBlockValueError,
)

# > Success strings - String that indicate something finished with success
TERMINATED_NORMALLY = "****ORCA TERMINATED NORMALLY****"
SCF_CONVERGED = "SUCCESS"
GEOMETRY_CONVERGED = "HURRAY"
CC_CONVERGED = "The Coupled-Cluster iterations have converged"
CASSCF_CONVERGED = "---- THE CAS-SCF GRADIENT HAS CONVERGED ----"

# > Has strings - Strings that indicate something was requested
HAS_GEOMETRY_OPT = "Geometry Optimization Run"
HAS_SCF = "SCF SETTINGS"
HAS_FREQ = "VIBRATIONAL FREQUENCIES"
HAS_ABORTING = "aborting"

# > Named error pattern instances
NO_COORDS_ERROR = ErrorPattern(
    "You must have a [COORDS] ... [END] block in your input",
    "No coordinates in the ORCA input.",
    critical=True,
)
CPSCF_NOT_CONVERGED_ERROR = ErrorPattern(
    "Error (SHARK/CP-SCF Solver): Unfortunately, the calculation did not converge.",
    "CP-SCF did not converge",
    critical=True,
)
CC_NOT_CONVERGED_ERROR = ErrorPattern(
    "The Coupled-Cluster iterations have NOT converged",
    "Coupled-Cluster did not converge",
    critical=True,
)
CIS_TDA_NOT_CONVERGED_ERROR = ErrorPattern(
    "CIS/TDA-DFT did not converge",
    "CIS/TDA-DFT did not converge",
)
SCF_NOT_CONVERGED_ERROR = ErrorPattern(
    "SCF NOT CONVERGED",
    "SCF did not converge",
    critical=True,
)
OPT_NOT_CONVERGED_ERROR = ErrorPattern(
    "The optimization did not converge",
    "Geometry optimization did not converge",
    critical=False,
)
TRIPLES_OOM_ERROR = ErrorPattern(
    "Error (ORCA_MDCI): not enough memory for computing triples",
    "Not enough memory for triples calculation",
    critical=True,
)
OOM_ERROR = ErrorPattern(
    "ERROR - OUT OF MEMORY !!!",
    "Calculation ran out of memory",
    critical=True,
)
MDCI_ERROR = ErrorPattern(
    "ORCA finished by error termination in MDCI",
    "Error in MDCI part of the calculation",
    critical=True,
)
MP2_ERROR = ErrorPattern(
    "ORCA finished by error termination in MP2",
    "Error in MP2 part of the calculation",
    critical=True,
)
MPI_ERROR = ErrorPattern(
    "-" * 74,
    "Potentially an Open MPI related error occurred.",
    critical=False,
)
ABORTING_ERROR = ErrorPattern("ABORTING THE RUN", "ORCA aborted the run")
GENERIC_ERROR = ErrorPattern("ERROR", "ORCA encountered an error")

# > Error patterns in order of priority.
# > Critical errors will stop scanning when matched.
# > Non-critical errors will just be added and reported.
ERROR_PATTERNS: list[ErrorPattern] = [
    # > Critical input errors — stop scanning on first match
    InvalidLineError(),  # critical
    SimpleKeywordsError(),  # critical
    UnknownBlockValueError(),  # critical
    UnknownBlockKeyError(),  # critical
    UnknownBlockError(),  # critical
    NO_COORDS_ERROR,  # critical
    # > Critical convergence errors
    CPSCF_NOT_CONVERGED_ERROR,  # critical
    CC_NOT_CONVERGED_ERROR,  # critical
    SCF_NOT_CONVERGED_ERROR,  # critical
    # > Memory errors
    NotEnoughMemoryScfError(),  # critical
    TRIPLES_OOM_ERROR,  # critical
    OOM_ERROR,  # critical
    # > Module terminates not normally
    MDCI_ERROR,  # critical
    MP2_ERROR,  # critical
    # > non-critical convergence errors
    OPT_NOT_CONVERGED_ERROR,  # non-critical: scan continues
    CIS_TDA_NOT_CONVERGED_ERROR,  # non-critical: scan continues
    # > Potentially MPI related error
    MPI_ERROR,  # non-critical: scan continues
    # > Unspecific errors
    ABORTING_ERROR,  # non-critical: scan continues
    GENERIC_ERROR,  # non-critical: scan continues
]
