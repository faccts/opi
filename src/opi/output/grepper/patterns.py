"""
Contains patterns for ORCA health checks and error checking capabilities.
At the end of the file the list of ErrorPatterns is found that is used to generate the output of `get_error_messages`.
"""

from opi.output.grepper.error_pattern import (
    ErrorPattern,
    ErrorTerminationError,
    InvalidLineError,
    MdciPairsError,
    MissingBasisError,
    MissingSharedLibraryError,
    MpiProcessAbortError,
    MultiplicityError,
    NotEnoughMemoryScfError,
    SimpleKeywordsError,
    UnknownBlockError,
    UnknownBlockKeyError,
    UnknownBlockValueError,
    ZeroDistanceError,
)

# > Success strings - String that indicate something finished with success
TERMINATED_NORMALLY = "****ORCA TERMINATED NORMALLY****"
SCF_CONVERGED = "SUCCESS"
GEOMETRY_CONVERGED = "HURRAY"
NEB_CONVERGED = "H U R R A Y"
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
NO_VIRTUALS_ERROR = ErrorPattern(
    "Cannot do Coupled Cluster calculations without virtuals",
    "No virtual orbitals available for the coupled-cluster calculation. Choose a larger basis set",
    critical=True,
)
MOINP_GEOMETRY_ERROR = ErrorPattern(
    "Error: Input geometry does not match current geometry",
    "The geometry of the orbitals read in with `moinp` does not match the current geometry",
    critical=True,
)
# > Open MPI and dynamic linker messages are written to stderr and never reach the ".out" file.
MPIRUN_NOT_FOUND_ERROR = ErrorPattern(
    "mpirun: not found",
    "Could not find `mpirun`. Check your Open MPI installation",
    critical=True,
    stderr=True,
)
MPI_SLOTS_ERROR = ErrorPattern(
    "There are not enough slots available in the system",
    "Not enough Open MPI slots available for the requested number of processes",
    critical=True,
    stderr=True,
)
ABORTING_ERROR = ErrorPattern("aborting the run", "ORCA aborted the run", case_sensitive=False)
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
    MultiplicityError(),  # critical
    ZeroDistanceError(),  # critical
    MissingBasisError(),  # critical
    # > Critical convergence errors
    CPSCF_NOT_CONVERGED_ERROR,  # critical
    CC_NOT_CONVERGED_ERROR,  # critical
    SCF_NOT_CONVERGED_ERROR,  # critical
    # > Memory errors
    NotEnoughMemoryScfError(),  # critical
    TRIPLES_OOM_ERROR,  # critical
    OOM_ERROR,  # critical
    # > Critical setup errors of correlated methods
    NO_VIRTUALS_ERROR,  # critical
    MdciPairsError(),  # critical
    # > Orbitals read in with `moinp` do not fit the calculation
    MOINP_GEOMETRY_ERROR,  # critical
    # > Open MPI and dynamic linker errors, searched in the ".err" file
    MPIRUN_NOT_FOUND_ERROR,  # critical
    MissingSharedLibraryError(),  # critical
    MPI_SLOTS_ERROR,  # critical
    # > non-critical convergence errors. Checked before the generic error termination below,
    # > which is less specific.
    OPT_NOT_CONVERGED_ERROR,  # non-critical: scan continues
    CIS_TDA_NOT_CONVERGED_ERROR,  # non-critical: scan continues
    # > Any module that terminates not normally. Reported before the MPI process abort below,
    # > as it names the failing ORCA module, while the abort gives the signal as the cause.
    ErrorTerminationError(),  # non-critical: scan continues
    # > MPI process killed by a signal
    MpiProcessAbortError(),  # critical
    # > Unspecific errors
    ABORTING_ERROR,  # non-critical: scan continues
    GENERIC_ERROR,  # non-critical: scan continues
]
