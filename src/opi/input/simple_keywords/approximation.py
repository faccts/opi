from opi.input.simple_keywords.base import (
    SimpleKeyword,
    SimpleKeywordBox,
)

__all__ = ("Approximation",)


class Approximation(SimpleKeywordBox):
    """Enum to store all simple keywords of type Approximation."""

    CLUSTERALL = SimpleKeyword("clusterall")
    """SimpleKeyword: Cluster all grids."""
    COSXCLUSTERALL = SimpleKeyword("cosxclusterall")
    """SimpleKeyword: Cluster cosx grid."""
    COSJXC = SimpleKeyword("cosjxc")
    """SimpleKeyword: Fast but blurry DFT."""
    FMM = SimpleKeyword("fmm")
    """SimpleKeyword: Use FFM approximation."""
    FROZENCORE = SimpleKeyword("frozencore")
    """SimpleKeyword: Frozen core approx. in correlated WFT."""
    NOFROZENCORE = SimpleKeyword("nofrozencore")
    """SimpleKeyword: Do not use frozen core approximation."""
    RI_BUPO_J = SimpleKeyword("ri-bupo/j")
    """SimpleKeyword: Use BUPO approximation."""
    NOBUPO = SimpleKeyword("nobupo")
    """SimpleKeyword: Do not use BUPO approximation."""
    NOCOSX = SimpleKeyword("nocosx")
    """SimpleKeyword: Do not use cosx."""
    RCSINGLESFOCK = SimpleKeyword("rcsinglesfock")
    """SimpleKeyword: Use COSX for Fock like single terms in CC."""
    NORCSINGLESFOCK = SimpleKeyword("norcsinglesfock")
    """SimpleKeyword: Do not use COSX for Fock like single terms in CC."""
    RI = SimpleKeyword("ri")
    """SimpleKeyword: Use RI."""
    NORI = SimpleKeyword("nori")
    """SimpleKeyword: Do not use RI."""
    RIJCOSX = SimpleKeyword("rijcosx")
    """SimpleKeyword: Approximation for two-electron integrals."""
    NORIJCOSX = SimpleKeyword("norijcosx")
    """SimpleKeyword: Approximation for two-electron integrals."""
    RIJKSINGLESFOCK = SimpleKeyword("rijksinglesfock")
    """SimpleKeyword: Use RIJK for Fock like single terms in CC."""
    NORIJKSINGLESFOCK = SimpleKeyword("norijksinglesfock")
    """SimpleKeyword: Do not use RIJK for Fock like single terms in CC."""
    USESFITTING = SimpleKeyword("usesfitting")
    """SimpleKeyword: Use overlap fitting in cosx."""
    NOSFITTING = SimpleKeyword("nosfitting")
    """SimpleKeyword: Do not use overlap fitting in cosx."""
    SPLITRIJ = SimpleKeyword("splitrij")
    """SimpleKeyword: Approximation for two-electron integrals."""
    NOSPLITRIJ = SimpleKeyword("nosplitrij")
    """SimpleKeyword: Approximation for two-electron integrals."""
    RIAO = SimpleKeyword("riao")
    """SimpleKeyword: Approximation for two-electron integrals."""
    RICOSJ = SimpleKeyword("ricosj")
    """SimpleKeyword: Approximation for two-electron integrals."""
    RICOSJX = SimpleKeyword("ricosjx")
    """SimpleKeyword: Approximation for two-electron integrals."""
    RIJK = SimpleKeyword("rijk")
    """SimpleKeyword: Approximation for two-electron integrals."""
    RIJONX = SimpleKeyword("rijonx")
    """SimpleKeyword: Approximation for two-electron integrals."""
    RIJXC = SimpleKeyword("rijxc")
    """SimpleKeyword: Approximation for two-electron integrals."""
