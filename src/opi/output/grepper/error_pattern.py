# patterns.py
import re
from pathlib import Path

from opi.output.grepper.core import Grepper


class ErrorPattern:
    """
    Represents an error pattern in the ORCA output file.
    More complex error patterns derive from this class and override extract.

    Attributes
    ----------
    grep_string: str
        The string that is searched in the output file.
    message: str
        A human-readable error message of the given error pattern.
    critical: bool
        When the error is critical we will stop searching for further errors after finding it.

    """

    grep_string: str = ""
    message: str = ""
    critical: bool = False

    def __init__(
        self,
        grep_string: str = "",
        message: str = "",
        critical: bool | None = None,
    ) -> None:
        if grep_string:
            self.grep_string = grep_string
        if message:
            self.message = message
        if critical is not None:
            self.critical = critical

    def match(self, file_path: Path) -> str | None:
        grepper = Grepper(file_path)
        hit = grepper.search(self.grep_string, case_sensitive=True)
        if not hit:
            return None
        return self.extract(file_path) or self.message

    def extract(self, file_path: Path) -> str | None:
        return None


class InvalidLineError(ErrorPattern):
    """
    Triggered when ORCA encounters an invalid line in the input file.
    This typically means a line does not start with a valid ORCA input
    character such as '$', '!', '%', '*' or '['.
    """

    grep_string = "ERROR: expect a '$', '!', '%', '*' or '[' in the input"
    message = "Invalid input line in ORCA input"
    critical = True

    def extract(self, file_path: Path) -> str | None:
        grepper = Grepper(file_path)
        match = grepper.search(self.grep_string, case_sensitive=True, skip_lines=1)
        if match:
            m = re.search(r"\((.+?)\)", match[0])
            result = m.group(1) if m else None
            return f"Invalid line starting with: {result}" if result else None
        return None


class SimpleKeywordsError(ErrorPattern):
    """
    Triggered when ORCA encounters an unrecognized or duplicated keyword
    in the simple input line (the '!' line).
    """

    grep_string = "UNRECOGNIZED OR DUPLICATED KEYWORD(S) IN SIMPLE INPUT LINE"
    message = "An unrecognized or duplicated simple keyword was requested"
    critical = True

    def extract(self, file_path: Path) -> str | None:
        grepper = Grepper(file_path)
        match = grepper.search(self.grep_string, case_sensitive=True, skip_lines=1)
        return f"Unknown/duplicate simple keyword(s): {match[0]}" if match else None


class UnknownBlockError(ErrorPattern):
    """
    Triggered when ORCA encounters an unknown block name in the input file,
    i.e. a '%blockname' that ORCA does not recognize.
    """

    grep_string = "Unknown identifier"
    message = "An unknown block was requested"
    critical = True

    def extract(self, file_path: Path) -> str | None:
        grepper = Grepper(file_path)
        match = grepper.search(self.grep_string, case_sensitive=True, skip_lines=0)
        return f"Unknown block: {match[0].split()[-1]}" if match else None


class UnknownBlockKeyError(ErrorPattern):
    """
    Triggered when ORCA encounters an unknown key inside a block,
    i.e. a valid block name but an unrecognized option within it.
    """

    grep_string = "Unknown identifier in"
    message = "An unknown block option was requested"
    critical = True

    def extract(self, file_path: Path) -> str | None:
        grepper = Grepper(file_path)
        match = grepper.search(self.grep_string, case_sensitive=True, skip_lines=1)
        return f"Unknown block key: {match[0].split(':')[-1]}" if match else None


class UnknownBlockValueError(ErrorPattern):
    """
    Triggered when ORCA encounters an invalid value for a block option,
    i.e. the key is recognized but the assigned value is not valid.
    """

    grep_string = "Invalid assignment"
    message = "An invalid value was requested in a block"
    critical = True

    def extract(self, file_path: Path) -> str | None:
        grepper = Grepper(file_path)
        match = grepper.search(self.grep_string, case_sensitive=True, skip_lines=1)
        return f"Unknown block value: {match[0].split(':')[-1]}" if match else None


class NotEnoughMemoryScfError(ErrorPattern):
    """
    Triggered when there is not enough memory available for the SCF
    """

    grep_string = "Error  (ORCA_SCF): Not enough memory available!"
    message = "Not enough memory for SCF available"
    critical = True

    def extract(self, file_path: Path) -> str | None:
        grepper = Grepper(file_path)
        avail_match = grepper.search(self.grep_string, case_sensitive=True, skip_lines=1)
        est_match = grepper.search(self.grep_string, case_sensitive=True, skip_lines=2)
        if not avail_match or not est_match:
            return None
        mem_avail = avail_match[-1].split(":")[-1]
        mem_estimated = est_match[-1].split(":")[-1]
        if mem_avail and mem_estimated:
            return f"Not enough memory available for SCF. Available: {mem_avail}, Required: {mem_estimated}"
        return None
