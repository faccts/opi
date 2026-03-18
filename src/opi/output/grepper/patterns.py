from opi.output.grepper.error_pattern import ErrorPattern, _extract_keyword

# > Success strings
TERMINATED_NORMALLY = "****ORCA TERMINATED NORMALLY****"
SCF_CONVERGED = "SUCCESS"
GEOMETRY_CONVERGED = "HURRAY"
CC_CONVERGED = "The Coupled-Cluster iterations have converged"

# > Has strings
HAS_GEOMETRY_OPT = "Geometry Optimization Run"
HAS_SCF = "SCF SETTINGS"
HAS_ABORTING = "aborting"

# > List of known error patterns
# > In decreasing order of priority
ERROR_PATTERNS: list[ErrorPattern] = [
    ErrorPattern(
        "ERROR: expect a '$', '!', '%', '*' or '[' in the input", "Invalid input line in ORCA input"
    ),
    ErrorPattern(
        "UNRECOGNIZED OR DUPLICATED KEYWORD(S) IN SIMPLE INPUT LINE",
        "An unrecognized or duplicated simple keyword was requested",
        extractor=_extract_keyword,
    ),
    ErrorPattern("Unknown identifier in", "An unknown block option was requested"),
    ErrorPattern("Invalid assignment", "An invalid value was requested in a block"),
    ErrorPattern(
        "The Coupled-Cluster iterations have NOT converged", "Coupled-Cluster did not converge"
    ),
    ErrorPattern("CIS/TDA-DFT did not converge", "CIS/TDA-DFT did not converge"),
    ErrorPattern("SCF NOT CONVERGED", "SCF did not converge"),
    ErrorPattern("The optimization did not converge", "Geometry optimization did not converge"),
    ErrorPattern("ABORTING THE RUN", "ORCA aborted the run"),
    ErrorPattern("ERROR", "ORCA encountered an error"),
]
