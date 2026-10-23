import pytest

from opi.utils.misc import check_minimal_version
from opi.utils.orca_version import OrcaVersion


@pytest.mark.unit
@pytest.mark.parametrize(
    "version_str, prerelease",
    [
        ("6.1.1", ()),
        ("6.1.1-f.0", ("f", "0")),
        ("7.0.0-f.beta.4", ("f", "beta", "4")),
    ],
)
def test_version_from_str(version_str: str, prerelease: tuple[str, ...]):
    version = OrcaVersion.from_str(version_str)
    assert version.prerelease == prerelease
    assert check_minimal_version(version)


@pytest.mark.unit
def test_version_from_output():
    output = "                         Program Version 7.0.0-f.beta.4  -  CURRENT   -\n"
    assert OrcaVersion.from_output(output) == OrcaVersion.from_str("7.0.0-f.beta.4")


@pytest.mark.unit
def test_version_ordering():
    ordered = [
        "6.1.1-f.0",
        "6.1.1-f.1",
        "6.1.1",
        "7.0.0-f.alpha.1",
        "7.0.0-f.beta.3",
        "7.0.0-f.beta.4",
        "7.0.0-f.rc.1",
        "7.0.0-f.0",
        "7.0.1-f.0",
    ]
    versions = [OrcaVersion.from_str(v) for v in ordered]
    assert sorted(reversed(versions)) == versions
    assert all(a < b for a, b in zip(versions, versions[1:]))
    assert OrcaVersion.from_str("7.0.0-f.beta.4") <= OrcaVersion.from_str("7.0.0-f.beta.4")
    assert not OrcaVersion.from_str("7.0.0-f.beta.4") >= OrcaVersion.from_str("7.0.0-f.0")
