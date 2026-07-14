from pathlib import Path

from opi.output.grepper.core import Grepper
from opi.output.grepper.patterns import (
    CASSCF_CONVERGED,
    CC_CONVERGED,
    ERROR_PATTERNS,
    GEOMETRY_CONVERGED,
    HAS_ABORTING,
    HAS_FREQ,
    HAS_GEOMETRY_OPT,
    HAS_SCF,
    SCF_CONVERGED,
    TERMINATED_NORMALLY,
)


def get_error_messages(file_name: Path) -> list[str]:
    """Return all errors from the output files until a critical error is found."""
    hits: list[str] = []
    for pattern in ERROR_PATTERNS:
        msg = pattern.extract(file_name)
        if msg:
            hits.append(msg)
            if pattern.critical:
                break
    return hits if hits else []


def get_error_message(file_name: Path) -> str:
    """Return the most important extracted error message."""
    messages = get_error_messages(file_name)
    return next(iter(messages or []), "")


def has_string_in_file(file_name: Path, search_for: str, /, *, strict: bool = True) -> bool:
    """
    Searches the output_file for a string and returns True if found otherwise False.
    The string needs to be given in the correct casing

    Parameters
    ----------
    file_name : Path
        Path to the file that should be searched.
    search_for : str
        string that function searches in function
    strict : bool, default: False
        True: Raise "FileNotFoundError" exception if `file_name` does not exist.
        False: Return just False if `file_name` does not exist.

    Raises
    -------
    FileNotFoundError
        If `file_name` does not exist and `strict` is set to True.

    Returns
    -------
    bool
        True if *search_for* was found, else False
    """
    try:
        grepper = Grepper(file_name)
        results = grepper.search(
            search_for,
            fallback=[False],
            kind=bool,
            case_sensitive=True,
        )
        return bool(results[0])

    except FileNotFoundError:
        if strict:
            raise
        else:
            return False


def get_float_from_line(
    file_name: Path, search_for: str, index: int, field: int = -1, /, *, strict: bool = True
) -> float | None:
    """
    Searches `file_name` for a string and returns a float from the line of this string.

    Parameters
    ----------
    file_name : Path
        Path to the file that should be searched.
    search_for : str
        string that function searches in file.
    index : int
        index of occurrence that should be returned.
    field: int
        field in line that should be returned
    strict : bool, default: False
        True: Raise "FileNotFoundError" exception if `file_name` does not exist or
        "ValueError" or "TypeError" if conversion of the result to float fails.
        False: Return just None if `file_name` does not exist or conversion to float fails.

    Raises
    -------
    FileNotFoundError
        If `strict` is True and `file_name` does not exist.
    ValueError
        If `strict` is True and the result is a string that cannot be converted to float.
    TypeError
        If `strict` is True and the result is of a type that cannot be converted to float.
    IndexError
        If `strict` is True and index is not available in the results.

    Returns
    -------
    float | None
        The float value if it could be retrieved, or None if not and `strict` is False.
    """
    try:
        grepper = Grepper(file_name)
        results = grepper.search(
            search_for,
            fallback=[None],
            kind=float,
            field=field,
            case_sensitive=True,
        )
        return float(results[index])

    except (FileNotFoundError, TypeError, ValueError, IndexError):
        if strict:
            raise
        else:
            return None


def get_lines_from_block(
    file_name: Path, search_for: str, /, *, index: int = -1, offset: int = 0
) -> list[str]:
    """
    Searches `file_name` for a string indicating a block and return all lines until an empty line is found.

    Parameters
    ----------
    file_name : Path
        Path to the file that should be searched.
    search_for : str
        string that function searches in file.
    index : int, default: -1
        which occurrence of the string should be used.
    offset : int, default: 0
        line offset from the line of the found string.

    Returns
    ----------
    list[str]
        Returns a list of lines as strings

    """
    lines = []
    skip_lines = offset
    # > Obtain the block by repeatedly calling the grepper and increasing the number of lines to skip, until the line
    # > obtained is empty.
    while True:
        try:
            grepper = Grepper(file_name)
            results = grepper.search(
                search_for,
                fallback=[None],
                case_sensitive=True,
                skip_lines=skip_lines,
            )
            if results[index]:
                lines.append(results[index])
                skip_lines += 1
            else:
                break
        except (FileNotFoundError, TypeError, ValueError, IndexError):
            break
    return lines


def has_terminated_normally(file_name: Path, /) -> bool:
    """
    Check if `file_name` contains the string ****ORCA TERMINATED NORMALLY****

    Parameters
    ----------
    file_name : Path
        Text file in which to look for the string.

    Returns
    -------
    bool: True if string is present, else False.
    """

    return has_string_in_file(file_name, TERMINATED_NORMALLY)


def has_aborted_run(file_name: Path, /) -> bool:
    """
    The string 'aborting' from the message '...aborting the run'

    Parameter
    ---------
    file_name: Path
        Name of the output file

    Returns
    -------
    bool
    """
    return has_string_in_file(file_name, HAS_ABORTING)


def has_frequency_calculation(file_name: Path, /) -> bool:
    """
    Searches for the message 'VIBRATIONAL FREQUENCIES' to indicate that a frequency calculation
    (FREQ or NUMFREQ) was performed.

    Parameter
    ---------
    file_name: Path
        Name of the output file

    Returns
    -------
    bool
        True if expression is found in file else False
    """
    return has_string_in_file(file_name, HAS_FREQ)


def has_geometry_optimization(file_name: Path, /) -> bool:
    """
    Searches for the message 'Geometry Optimization Run' to indicate that a geometry optimization is performed.

    Parameter
    ---------
    file_name: Path
        Name of the output file

    Returns
    -------
    bool
        True if expression is found in file else False
    """
    return has_string_in_file(file_name, HAS_GEOMETRY_OPT)


def has_geometry_optimization_converged(file_name: Path, /) -> bool:
    """
    Searches for the message 'HURRAY' to indicate that a geometry optimization has converged.

    Parameter
    ---------
    file_name: Path
        Name of the output file

    Returns
    -------
    bool
        True if expression is found in file else False
    """
    return has_string_in_file(file_name, GEOMETRY_CONVERGED)


def has_scf(file_name: Path, /) -> bool:
    """
    Searches for the message 'SCF SETTINGS' to indicate that an SCF is used.

    Parameter
    ---------
    file_name: Path
        Name of the output file

    Returns
    -------
    bool
        True if expression is found in file else False
    """
    return has_string_in_file(file_name, HAS_SCF)


def has_scf_converged(file_name: Path, /) -> bool:
    """
    Searches for the message 'SUCCESS' as indicator that the SCF converged.

    Parameter
    ---------
    file_name: Path
        Name of the output file

    Returns
    -------
    bool
        True if expression is found in file else False
    """
    return has_string_in_file(file_name, SCF_CONVERGED)


def has_casscf_converged(file_name: Path, /) -> bool:
    """
    Searches for the message '---- THE CAS-SCF GRADIENT HAS CONVERGED ----' as indicator that the CAS-SCF converged.

    Parameter
    ---------
    file_name: Path
        Name of the output file

    Returns
    -------
    bool
        True if expression is found in file else False
    """
    return has_string_in_file(file_name, CASSCF_CONVERGED)


def has_cc_converged(file_name: Path, /) -> bool:
    """
    Searches for the message 'The Coupled-Cluster iterations have converged' as indicator that the CC converged.

    Parameter
    ---------
    file_name: Path
        Name of the output file

    Returns
    -------
    bool
        True if expression is found in file else False
    """
    return has_string_in_file(file_name, CC_CONVERGED)
