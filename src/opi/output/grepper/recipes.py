from pathlib import Path

from opi.output.grepper.core import Grepper


def has_string_in_file(file_name: Path, search_for: str, /, *, strict: bool = True) -> bool:
    """
    Searches the output_file for a string and returns True if found otherwise False.
    The string needs to be given in the correct casing

    Parameters
    ----------
    file_name : Path
        Path to the output file
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
    Searches the output_file for a string and returns a float from the line of this string.

    Parameters
    ----------
    file_name : Path
        Path to the output file
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

    return has_string_in_file(file_name, "****ORCA TERMINATED NORMALLY****")


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
    return has_string_in_file(file_name, "aborting")


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
    return has_string_in_file(file_name, "Geometry Optimization Run")


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
    return has_string_in_file(file_name, "HURRAY")


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
    return has_string_in_file(file_name, "SCF SETTINGS")


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
    return has_string_in_file(file_name, "SUCCESS")
