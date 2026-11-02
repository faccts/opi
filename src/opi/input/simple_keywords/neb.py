from opi.input.simple_keywords.base import (
    ORCAKeyword,
    SimpleKeywordBox,
)

__all__ = ("Neb",)


class Neb(SimpleKeywordBox):
    """Enum to store all simple keywords of type Neb."""

    NEB = ORCAKeyword("neb")
    """ORCAKeyword: NEB for finding minimal energy pathways (and transition states)."""
    NEB_CI = ORCAKeyword("neb-ci")
    """ORCAKeyword: NEB for finding minimal energy pathways (and transition states)."""
    NEB_IDPP = ORCAKeyword("neb-idpp")
    """ORCAKeyword: NEB for finding minimal energy pathways (and transition states)."""
    NEB_MMFTS = ORCAKeyword("neb-mmfts")
    """ORCAKeyword: NEB for finding minimal energy pathways (and transition states)."""
    NEB_TS = ORCAKeyword("neb-ts")
    """ORCAKeyword: NEB for finding minimal energy pathways (and transition states)."""
    FAST_NEB_TS = ORCAKeyword("fast-neb-ts")
    """ORCAKeyword: NEB for finding minimal energy pathways (and transition states)."""
    LOOSE_NEB_TS = ORCAKeyword("loose-neb-ts")
    """ORCAKeyword: NEB for finding minimal energy pathways (and transition states)."""
    TIGHT_NEB_TS = ORCAKeyword("tight-neb-ts")
    """ORCAKeyword: NEB for finding minimal energy pathways (and transition states)."""
    ZOOM_NEB = ORCAKeyword("zoom-neb")
    """ORCAKeyword: NEB for finding minimal energy pathways (and transition states)."""
    ZOOM_NEB_CI = ORCAKeyword("zoom-neb-ci")
    """ORCAKeyword: NEB for finding minimal energy pathways (and transition states)."""
    ZOOM_NEB_TS = ORCAKeyword("zoom-neb-ts")
    """ORCAKeyword: NEB for finding minimal energy pathways (and transition states)."""
    FLAT_NEB_TS = ORCAKeyword("flat-neb-ts")
    """ORCAKeyword: NEB for finding minimal energy pathways (and transition states)."""
    IRC = ORCAKeyword("irc")
    """ORCAKeyword: internal reaction coordinate."""
    SCANTS = ORCAKeyword("scants")
    """ORCAKeyword: scan for transition state."""
