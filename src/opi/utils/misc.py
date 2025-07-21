import os
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence, cast

from opi import ORCA_MINIMAL_VERSION
from opi.utils.orca_version import OrcaVersion

FLOAT_REGEX: str = r"[+-]?((\d+(\.\d*)?)|(\.\d+))"


def eprint(*msgs: Sequence[Any], **kwargs: Mapping[str, Any]) -> None:
    """
    Print to directly to STDERR.

    Parameters
    ----------
    *msgs : Sequence[Any]

    **kwargs : Mapping[str | Any]
    """
    print(*msgs, file=sys.stderr, **kwargs)  # type: ignore


def add_to_env(
    variable: str,
    value: str,
    /,
    *,
    prepend: bool = False,
    env: dict[str, str] | os._Environ[str] | None = None,
) -> None:
    """
    Parameters
    ----------
    variable : str
    value : str
    prepend : bool, default: False
    env : dict[str | str] | os._Environ[str] | None, default: None
    """
    if not isinstance(variable, str):
        raise TypeError(f"'variable' parameter is not a string, but: {type(variable)}")
    if not isinstance(value, str):
        raise TypeError(f"'value' parameter is not a string, but: {type(value)}")

    # > Get env
    if env is None:
        env = os.environ

    # > Get current values
    current_values = env.get(variable, "").split(os.pathsep)
    # > Check if values is already at desired end of the list
    desired_pos = 0 if prepend else -1
    try:
        do_add = current_values[desired_pos] != value
    except IndexError:
        do_add = True

    # > Add value if not present
    if do_add:
        insert_pos = 0 if prepend else len(current_values)
        current_values.insert(insert_pos, value)
        env[variable] = os.pathsep.join(current_values)


def get_filesize(file: Path, /) -> int | None:
    """
    Get size of file.
    Return None if path is not a file or does not exist.

    Parameters
    ----------
    file : Path
        Path to file
    """
    if file.is_file():
        return file.stat().st_size
    return None


def delete_empty_file(file: Path, /) -> bool:
    """
    Check if given file exists. If it exists and it is empty delete it.

    Parameter
    ----------
    file: Path
        Path to file.

    Parameters
    ----------
    file : Path
    """
    if not isinstance(file, Path):
        raise TypeError(f"`file` is not a Path, but: {type(file)}")

    if file.is_file() and get_filesize(file) == 0:
        file.unlink()
        return True
    return False


def lowercase(data: dict[str, Any], /) -> None:
    """
    Recursively modifies the given dictionary in place so that all keys are lowercase.

    Parameters
    ----------
    data : dict[str | Any]
        The dictionary to modify
    """

    # > Recursion termination criteria
    if not isinstance(data, dict):
        return

    # > Need to cache keys, otherwise Python complains: "RuntimeError: dictionary keys changed during iteration"
    keys = list(data.keys())

    # > Loop over keys
    for key in keys:
        # > Get value and remove from dictionary.
        value = data.pop(key)
        # > If `value` is a dictionary recurse into dictionary
        if isinstance(value, dict):
            lowercase(value)
        # > If value is a list, check if any items are dictionaries and recurse into thees.
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    lowercase(item)
        # > Update key.
        key_lower = key.lower()
        data[key_lower] = value


def get_package_name() -> str:
    """
    Get the name of this package.
    The name is derived from the import path to the current module.
    """
    pkg_name, __, __ = __name__.partition(".")
    return pkg_name


def is_linux() -> bool:
    """
    Return if current OS is Linux.
    """
    return sys.platform == "linux"


def is_windows() -> bool:
    """
    Return if current OS is Windows.
    """
    return sys.platform == "windows"


def is_mac() -> bool:
    """
    Return if current OS is Mac OS X.
    """
    return sys.platform == "darwin"


def check_minimal_version(version: OrcaVersion, /) -> bool:
    """
    Check if the given ORCA version fits to minimal required version.

    Parameters
    ----------
    version : OrcaVersion
    """
    return cast(bool, version >= ORCA_MINIMAL_VERSION)
