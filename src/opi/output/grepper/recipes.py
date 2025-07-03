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
