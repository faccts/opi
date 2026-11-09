import math
import re
from typing import Any

from semantic_version import Version  # type: ignore[import-untyped]


class OrcaVersion(Version):  # type: ignore
    """
    Class to hold an ORCA version tag: X.Y[.Z[-f.[T.]A]]
    The "[...]" parts are optional. X, Y, Z and A are integers.
    T is an optional pre-release tag, e.g. "beta" in "7.0.0-f.beta.4".
    """

    RGX_VERSION = re.compile(
        # major version
        r"(?P<major>\d+)"
        # minor version
        r"\.(?P<minor>\d+)"
        r"("
        # micro version [optional]
        r"\.(?P<micro>\d+|x)"
        # bugfix version [optional]
        r"(-(?P<bugfix>f(\.[a-z]+)?\.\d+))?"
        r")?",
        re.VERBOSE | re.IGNORECASE,
    )
    RGX_OUTPUT_VERSION = re.compile(
        r"^\s*Program Version\s+([1-9]+\.\d+\.([xX]|\d+(-f(\.[a-zA-Z]+)?\.\d+)?))",
        re.MULTILINE,
    )

    def _orca_key(self) -> tuple[int, int, int, int, str, float]:
        """
        Sort key, in which pre-release versions (e.g. "f.beta.4") sort before the final release
        ("f.0") of the same version. A version without bugfix part sorts after all its bugfix releases.
        """
        match self.prerelease:
            case ("f", tag, num):
                return (self.major, self.minor, self.patch, 0, tag.lower(), int(num))
            case ("f", num):
                return (self.major, self.minor, self.patch, 1, "", int(num))
            case ():
                return (self.major, self.minor, self.patch, 1, "", math.inf)
            case _:
                raise ValueError(f"Invalid ORCA version: {self}")

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, OrcaVersion):
            return NotImplemented
        return self._orca_key() < other._orca_key()

    def __le__(self, other: object) -> bool:
        if not isinstance(other, OrcaVersion):
            return NotImplemented
        return self._orca_key() <= other._orca_key()

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, OrcaVersion):
            return NotImplemented
        return self._orca_key() > other._orca_key()

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, OrcaVersion):
            return NotImplemented
        return self._orca_key() >= other._orca_key()

    @classmethod
    def from_str(cls, version_str: str, /) -> "OrcaVersion":
        """
        Create OrcaVersion from classical version string.

        Parameters
        ----------
        version_str : str
        """
        mmatch = cls.RGX_VERSION.fullmatch(version_str)

        try:
            assert isinstance(mmatch, re.Match)

            # > Parts of version string
            major = int(mmatch.group("major"))
            minor = int(mmatch.group("minor"))
            # > Patch level has to be a number. Cannot be None or "x".
            if g := mmatch.group("micro"):
                patch = 9 if g.lower() == "x" else int(g)
            else:
                patch = 0
            prerelease = g.split(".") if (g := mmatch.group("bugfix")) else None

            return cls(
                major=major,
                minor=minor,
                patch=patch,
                prerelease=prerelease,
            )
        except (AssertionError, AttributeError, ValueError) as err:
            raise ValueError(f"Invalid ORCA version string: {version_str}") from err

    @classmethod
    def from_output(cls, output: str | bytes, /) -> "OrcaVersion":
        """
        Create OrcaVersion from ORCA output.

        Parameters
        ----------
        output : str | bytes
        """
        if isinstance(output, bytes):
            output = output.decode()
        version_str = cls.RGX_OUTPUT_VERSION.search(output)
        try:
            assert isinstance(version_str, re.Match)
            return cls.from_str(version_str.group(1))

        except (AssertionError, AttributeError):
            raise ValueError("Could not determine ORCA version from output")

    @classmethod
    def from_json(cls, json_data: dict[str, Any], /) -> "OrcaVersion":
        """
        Create OrcaVersion parse property of the JSON-property file.

        Parameters
        ----------
        json_data : dict[str | Any]
        """
        try:
            version = json_data["calculation_status"]["version"]
            return OrcaVersion.from_str(version)

        except (AttributeError, KeyError, ValueError) as err:
            raise ValueError("Could not determine ORCA version from JSON-property file.") from err
