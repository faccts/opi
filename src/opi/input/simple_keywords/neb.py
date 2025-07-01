from opi.input.simple_keywords.base import (
    SimpleKeyword,
    SimpleKeywordBox,
)

__all__ = ("Neb",)


class Neb(SimpleKeywordBox):
    """Enum to store all simple keywords of type Neb.

    Attributes
    ----------
    NEB : SimpleKeyword
        NEB for finding minimal energy pathways (and transition states)
    NEB_CI : SimpleKeyword
        NEB for finding minimal energy pathways (and transition states)
    NEB_IDPP : SimpleKeyword
        NEB for finding minimal energy pathways (and transition states)
    NEB_MMFTS : SimpleKeyword
        NEB for finding minimal energy pathways (and transition states)
    NEB_TS : SimpleKeyword
        NEB for finding minimal energy pathways (and transition states)
    FAST_NEB_TS : SimpleKeyword
        NEB for finding minimal energy pathways (and transition states)
    LOOSE_NEB_TS : SimpleKeyword
        NEB for finding minimal energy pathways (and transition states)
    TIGHT_NEB_TS : SimpleKeyword
        NEB for finding minimal energy pathways (and transition states)
    ZOOM_NEB : SimpleKeyword
        NEB for finding minimal energy pathways (and transition states)
    ZOOM_NEB_CI : SimpleKeyword
        NEB for finding minimal energy pathways (and transition states)
    ZOOM_NEB_TS : SimpleKeyword
        NEB for finding minimal energy pathways (and transition states)
    FLAT_NEB_TS : SimpleKeyword
        NEB for finding minimal energy pathways (and transition states)
    IRC : SimpleKeyword
        internal reaction coordinate
    SCANTS : SimpleKeyword
        scan for transition state
    """

    NEB = SimpleKeyword("neb")
    NEB_CI = SimpleKeyword("neb-ci")
    NEB_IDPP = SimpleKeyword("neb-idpp")
    NEB_MMFTS = SimpleKeyword("neb-mmfts")
    NEB_TS = SimpleKeyword("neb-ts")
    FAST_NEB_TS = SimpleKeyword("fast-neb-ts")
    LOOSE_NEB_TS = SimpleKeyword("loose-neb-ts")
    TIGHT_NEB_TS = SimpleKeyword("tight-neb-ts")
    ZOOM_NEB = SimpleKeyword("zoom-neb")
    ZOOM_NEB_CI = SimpleKeyword("zoom-neb-ci")
    ZOOM_NEB_TS = SimpleKeyword("zoom-neb-ts")
    FLAT_NEB_TS = SimpleKeyword("flat-neb-ts")
    IRC = SimpleKeyword("irc")
    SCANTS = SimpleKeyword("scants")
