import importlib.metadata

from opi.utils.orca_version import OrcaVersion

__all__ = ["ORCA_MINIMAL_VERSION"]

# // OPI VERSION
try:
    __version__ = importlib.metadata.version(__name__)
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.0.0"  # Fallback for development mode

# // ORCA VERSION
ORCA_MINIMAL_VERSION = OrcaVersion.from_str("6.1.0-f.0")
