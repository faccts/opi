import re
from typing import Any

from semantic_version import Version  # type: ignore[import-untyped]


class OrcaVersion(Version):  # type: ignore
    """
    Class to hold an ORCA version tag: X.Y[.Z[-f.A]]
    The "[...]" parts are optional. X, Y, Z and A are integers.
    """

    RGX_VERSION = re.compile(
        # major version
        r"(?P<major>\d+)"
        # minor version
        r"\.(?P<minor>\d+)"
        r"("
        # micro version [optional]
        r"\.(?P<micro>\d+)"
        # bugfix version [optional]
        r"(-(?P<bugfix>f\.\d+))?"
        r")?",
        re.VERBOSE | re.IGNORECASE,
    )
    RGX_OUTPUT_VERSION = re.compile(
        r"^[ \t]*Program Version[ \t]+([1-9]+\.[0-9]+(\.[0-9]+(-f.[0-9]+)?)?)",
        re.MULTILINE,
    )

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
            # > Patch level has to be a number. Cannot be None.
            patch = int(g) if (g := mmatch.group("micro")) else 0
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
            # > Remove ".x" suffix
            version = version.removesuffix(".x")
            return OrcaVersion.from_str(version)

        except (AttributeError, KeyError, ValueError) as err:
            raise ValueError("Could not determine ORCA version from JSON-property file.") from err
