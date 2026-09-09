"""Module for defining exception types raised by OPI."""

from typing import Sequence


class OpiError(Exception):
    """Base class for all OPI based errors."""

    pass


class OpiExecutionError(OpiError):
    """Base class for errors raised while executing binary applications."""

    pass


class OrcaMmError(OpiExecutionError):
    """Raised when an `orca_mm` command reports an error."""

    def __init__(self, command: str, arguments: Sequence[str], error: str):
        """
        Parameters
        ----------
        command : str
            `orca_mm` subcommand that was executed.
        arguments : Sequence[str]
            Command-line arguments passed to `orca_mm`.
        error : str
            Error output captured from `orca_mm` STDERR.
        """
        fmt_arguments = " ".join(arguments)
        message = (
            f"Failed running command: 'orca_mm -{command} {fmt_arguments}'.\n"
            f"orca_mm failed with the following error:\n{error.strip()}"
        )
        super().__init__(message)
