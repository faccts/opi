import re
from pathlib import Path

from opi.output.grepper.core import Grepper


class ErrorPattern:
    """
    Represents an error pattern in the ORCA output file.
    More complex error patterns derive from this class and override the `extract` method.

    Attributes
    ----------
    grep_string: str
        The string that is searched in the output file.
    message: str
        A human-readable error message of the given error pattern.
    critical: bool
        When the error is critical we will stop searching for further errors after finding it.
        Critical errors are errors after which ORCA will abort.
    stderr: bool
        Search the ".err" file instead of the ".out" file.
        Messages of the MPI launcher and of the dynamic linker never reach the ORCA output file.
    case_sensitive: bool
        Whether `grep_string` is matched case-sensitively.

    """

    grep_string: str = ""
    message: str = ""
    critical: bool = False
    stderr: bool = False
    case_sensitive: bool = True

    def __init__(
        self,
        grep_string: str = "",
        message: str = "",
        critical: bool | None = None,
        *,
        stderr: bool | None = None,
        case_sensitive: bool | None = None,
    ) -> None:
        self.grep_string = grep_string if grep_string else type(self).grep_string
        self.message = message if message else type(self).message
        self.critical = critical if critical is not None else type(self).critical
        self.stderr = stderr if stderr is not None else type(self).stderr
        self.case_sensitive = (
            case_sensitive if case_sensitive is not None else type(self).case_sensitive
        )

    def extract(self, file_path: Path) -> str:
        """
        Search for `grep_string` in `file_path` and return `message` when found,
        or an empty string when absent. Override in subclasses to compose a more
        specific error message from the surrounding output lines.
        """
        grepper = Grepper(file_path)
        return (
            self.message
            if grepper.search(self.grep_string, case_sensitive=self.case_sensitive)
            else ""
        )


class InvalidLineError(ErrorPattern):
    """
    Triggered when ORCA encounters an invalid line in the input file.
    This typically means a line does not start with a valid ORCA input
    character such as '$', '!', '%', '*' or '['.
    """

    grep_string = "ERROR: expect a '$', '!', '%', '*' or '[' in the input"
    message = "Invalid input line in ORCA input"
    critical = True

    def extract(self, file_path: Path) -> str:
        grepper = Grepper(file_path)
        match = grepper.search(self.grep_string, case_sensitive=True, skip_lines=1)
        if match:
            m = re.search(r"\((.+?)\)", match[0])
            result = m.group(1) if m else None
            return f"Invalid line starting with: {result}" if result else self.message
        return ""


class SimpleKeywordsError(ErrorPattern):
    """
    Triggered when ORCA encounters an unrecognized or duplicated keyword
    in the simple input line (the '!' line).
    """

    grep_string = "UNRECOGNIZED OR DUPLICATED KEYWORD(S) IN SIMPLE INPUT LINE"
    message = "An unrecognized or duplicated simple keyword was requested"
    critical = True

    def extract(self, file_path: Path) -> str:
        grepper = Grepper(file_path)
        match = grepper.search(self.grep_string, case_sensitive=True, skip_lines=1)
        return f"Unknown/duplicate simple keyword(s): {match[0]}" if match else ""


class UnknownBlockError(ErrorPattern):
    """
    Triggered when ORCA encounters an unknown block name in the input file,
    i.e. a '%blockname' that ORCA does not recognize.
    """

    grep_string = "Unknown identifier"
    message = "An unknown block was requested"
    critical = True

    def extract(self, file_path: Path) -> str:
        grepper = Grepper(file_path)
        match = grepper.search(self.grep_string, case_sensitive=True, skip_lines=0)
        return f"Unknown block: {match[0].split()[-1]}" if match else ""


class UnknownBlockKeyError(ErrorPattern):
    """
    Triggered when ORCA encounters an unknown key inside a block,
    i.e. a valid block name but an unrecognized option within it.
    """

    grep_string = "Unknown identifier in"
    message = "An unknown block option was requested"
    critical = True

    def extract(self, file_path: Path) -> str:
        grepper = Grepper(file_path)
        match = grepper.search(self.grep_string, case_sensitive=True, skip_lines=1)
        return f"Unknown block key: {match[0].split(':')[-1]}" if match else ""


class UnknownBlockValueError(ErrorPattern):
    """
    Triggered when ORCA encounters an invalid value for a block option,
    i.e. the key is recognized but the assigned value is not valid.
    """

    grep_string = "Invalid assignment"
    message = "An invalid value was requested in a block"
    critical = True

    def extract(self, file_path: Path) -> str:
        grepper = Grepper(file_path)
        match = grepper.search(self.grep_string, case_sensitive=True, skip_lines=1)
        return f"Unknown block value: {match[0].split(':')[-1]}" if match else ""


class NotEnoughMemoryScfError(ErrorPattern):
    """
    Triggered when there is not enough memory available for the SCF
    """

    grep_string = "Error  (ORCA_SCF): Not enough memory available!"
    message = "Not enough memory for SCF available"
    critical = True

    def extract(self, file_path: Path) -> str:
        grepper = Grepper(file_path)
        avail_match = grepper.search(self.grep_string, case_sensitive=True, skip_lines=1)
        if not avail_match:
            return ""
        est_match = grepper.search(self.grep_string, case_sensitive=True, skip_lines=2)
        if not est_match:
            return self.message
        mem_avail = avail_match[-1].split(":")[-1]
        mem_estimated = est_match[-1].split(":")[-1]
        if mem_avail and mem_estimated:
            return f"Not enough memory available for SCF. Available: {mem_avail}, Required: {mem_estimated}"
        return self.message


class MultiplicityError(ErrorPattern):
    """
    Triggered when the requested multiplicity cannot be realized with the number of electrons,
    i.e. both are even or both are odd.
    """

    grep_string = "and number of electrons ("
    message = "The multiplicity is impossible for the given number of electrons"
    critical = True

    def extract(self, file_path: Path) -> str:
        grepper = Grepper(file_path)
        match = grepper.search(self.grep_string, case_sensitive=True)
        if not match:
            return ""
        numbers = re.findall(r"\((\d+)\)", match[0])
        if len(numbers) != 2:
            return self.message
        multiplicity, nelectrons = numbers
        return (
            f"Impossible combination of multiplicity ({multiplicity}) "
            f"and number of electrons ({nelectrons})"
        )


class ZeroDistanceError(ErrorPattern):
    """
    Triggered when two atoms of the input structure sit on top of each other, which makes the
    conversion of the Cartesian coordinates into internal coordinates fail.
    """

    grep_string = "Zero distance between atoms"
    message = "Two atoms of the input structure sit on top of each other"
    critical = True

    def extract(self, file_path: Path) -> str:
        grepper = Grepper(file_path)
        match = grepper.search(self.grep_string, case_sensitive=True)
        if not match:
            return ""
        m = re.search(r"Zero distance between atoms (\d+) and (\d+)", match[0])
        if not m:
            return self.message
        return f"Zero distance between atoms {m.group(1)} and {m.group(2)} of the input structure"


class MissingBasisError(ErrorPattern):
    """
    Triggered when no basis set is available for one of the elements of the structure.
    """

    grep_string = "The basis set was either not assigned or not available for this element"
    message = "No basis set assigned or available for one of the elements"
    critical = True

    def extract(self, file_path: Path) -> str:
        grepper = Grepper(file_path)
        if not grepper.search(self.grep_string, case_sensitive=True):
            return ""
        # > The preceding box names the atom and the kind of basis set that is missing.
        atom_match = Grepper(file_path).search(
            "basis functions on atom number", case_sensitive=True
        )
        if not atom_match:
            return self.message
        m = re.search(
            r"There are no\s+(\S+)\s+basis functions on atom number\s+(\d+)\s+\((\S+)\)",
            atom_match[-1],
        )
        if not m:
            return self.message
        kind, atom, element = m.groups()
        return f"No {kind} basis functions on atom {atom} ({element})"


class MdciPairsError(ErrorPattern):
    """
    Triggered when the MDCI module has fewer electron pairs to correlate than processes to
    distribute them over. With zero pairs the actual cause is a system with too few electrons
    to correlate, which ORCA reports through the very same message.
    """

    grep_string = "Error (ORCA_MDCI): Number of processes ("
    message = "Number of processes in the parallel calculation exceeds the number of pairs"
    critical = True

    def extract(self, file_path: Path) -> str:
        grepper = Grepper(file_path)
        match = grepper.search(self.grep_string, case_sensitive=True)
        if not match:
            return ""
        numbers = re.findall(r"\((\d+)\)", match[0])
        if len(numbers) != 2:
            return self.message
        nprocs, npairs = numbers
        if npairs == "0":
            return (
                "No electron pairs to correlate: the system has too few electrons "
                "for a correlated calculation"
            )
        return (
            f"Number of processes ({nprocs}) in the parallel calculation "
            f"exceeds the number of pairs ({npairs})"
        )


class MissingSharedLibraryError(ErrorPattern):
    """
    Triggered when the dynamic linker cannot load a shared library required by an ORCA binary,
    for example `libmpi.so` of a missing or mismatching Open MPI installation.
    The linker writes to stderr, hence the ".err" file is searched.
    """

    grep_string = "error while loading shared libraries"
    message = "A shared library required by ORCA could not be loaded"
    critical = True
    stderr = True

    def extract(self, file_path: Path) -> str:
        grepper = Grepper(file_path)
        match = grepper.search(self.grep_string, case_sensitive=True)
        if not match:
            return ""
        m = re.search(r"error while loading shared libraries:\s*([^:]+):", match[0])
        if not m:
            return self.message
        return (
            f"Could not load the shared library {m.group(1).strip()} required by ORCA. "
            "Check your ORCA and Open MPI installation"
        )


class ErrorTerminationError(ErrorPattern):
    """
    Triggered when an ORCA module terminates with an error, i.e. the catch-all for module
    failures that no more specific pattern above has already explained.
    """

    grep_string = "ORCA finished by error termination in"
    message = "ORCA finished by error termination"
    critical = True

    def extract(self, file_path: Path) -> str:
        grepper = Grepper(file_path)
        match = grepper.search(self.grep_string, case_sensitive=True)
        if not match:
            return ""
        module = match[0].split()[-1]
        return f"Error in {module} part of the calculation" if module else self.message
