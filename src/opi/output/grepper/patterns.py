from opi.output.grepper.error_pattern import (
    ErrorPattern,
    InvalidLineError,
    SimpleKeywordsError,
    UnknownBlockError,
    UnknownBlockKeyError,
    UnknownBlockValueError,
)

# > Success strings
TERMINATED_NORMALLY = "****ORCA TERMINATED NORMALLY****"
SCF_CONVERGED = "SUCCESS"
GEOMETRY_CONVERGED = "HURRAY"
CC_CONVERGED = "The Coupled-Cluster iterations have converged"

# > Has strings
HAS_GEOMETRY_OPT = "Geometry Optimization Run"
HAS_SCF = "SCF SETTINGS"
HAS_ABORTING = "aborting"

# > Error patterns in order of priority.
# > Critical errors are listed first and will stop scanning when matched.
# > Non-critical errors are listed after and will all be reported.
ERROR_PATTERNS: list[ErrorPattern] = [
    # > Critical input errors - stop scanning on first match
    InvalidLineError(),
    SimpleKeywordsError(),
    UnknownBlockValueError(),
    UnknownBlockKeyError(),
    UnknownBlockError(),
    ErrorPattern(
        "You must have a [COORDS] ... [END] block in your input",
        "No coordinates in the ORCA input.",
        critical=True,
    ),
    # > Non-critical convergence errors - all reported
    ErrorPattern(
        "Error (SHARK/CP-SCF Solver): Unfortunately, the calculation did not converge.",
        "CP-SCF did not converge",
        critical=True,
    ),
    ErrorPattern(
        "The Coupled-Cluster iterations have NOT converged",
        "Coupled-Cluster did not converge",
        critical=True,
    ),
    ErrorPattern("CIS/TDA-DFT did not converge", "CIS/TDA-DFT did not converge"),
    ErrorPattern("SCF NOT CONVERGED", "SCF did not converge", critical=True),
    ErrorPattern(
        "The optimization did not converge",
        "Geometry optimization did not converge",
        critical=False,
    ),
    # > Unspecific errors - these could potentially be dropped
    ErrorPattern("ABORTING THE RUN", "ORCA aborted the run"),
    ErrorPattern("ERROR", "ORCA encountered an error"),
]
