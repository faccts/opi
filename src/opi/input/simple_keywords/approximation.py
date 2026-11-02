from opi.input.simple_keywords.base import (
    ORCAKeyword,
    SimpleKeywordBox,
)

__all__ = ("Approximation",)


class Approximation(SimpleKeywordBox):
    """Enum to store all simple keywords of type Approximation."""

    CLUSTERALL = ORCAKeyword("clusterall")
    """ORCAKeyword: Cluster all grids."""
    COSXCLUSTERALL = ORCAKeyword("cosxclusterall")
    """ORCAKeyword: Cluster cosx grid."""
    COSJXC = ORCAKeyword("cosjxc")
    """ORCAKeyword: Fast but blurry DFT."""
    FMM = ORCAKeyword("fmm")
    """ORCAKeyword: Use FFM approximation."""
    FROZENCORE = ORCAKeyword("frozencore")
    """ORCAKeyword: Frozen core approx. in correlated WFT."""
    NOFROZENCORE = ORCAKeyword("nofrozencore")
    """ORCAKeyword: Do not use frozen core approximation."""
    RI_BUPO_J = ORCAKeyword("ri-bupo/j")
    """ORCAKeyword: Use BUPO approximation."""
    NOBUPO = ORCAKeyword("nobupo")
    """ORCAKeyword: Do not use BUPO approximation."""
    NOCOSX = ORCAKeyword("nocosx")
    """ORCAKeyword: Do not use cosx."""
    RCSINGLESFOCK = ORCAKeyword("rcsinglesfock")
    """ORCAKeyword: Use COSX for Fock like single terms in CC."""
    NORCSINGLESFOCK = ORCAKeyword("norcsinglesfock")
    """ORCAKeyword: Do not use COSX for Fock like single terms in CC."""
    RI = ORCAKeyword("ri")
    """ORCAKeyword: Use RI."""
    NORI = ORCAKeyword("nori")
    """ORCAKeyword: Do not use RI."""
    RIJCOSX = ORCAKeyword("rijcosx")
    """ORCAKeyword: Approximation for two-electron integrals."""
    NORIJCOSX = ORCAKeyword("norijcosx")
    """ORCAKeyword: Approximation for two-electron integrals."""
    RIJKSINGLESFOCK = ORCAKeyword("rijksinglesfock")
    """ORCAKeyword: Use RIJK for Fock like single terms in CC."""
    NORIJKSINGLESFOCK = ORCAKeyword("norijksinglesfock")
    """ORCAKeyword: Do not use RIJK for Fock like single terms in CC."""
    USESFITTING = ORCAKeyword("usesfitting")
    """ORCAKeyword: Use overlap fitting in cosx."""
    NOSFITTING = ORCAKeyword("nosfitting")
    """ORCAKeyword: Do not use overlap fitting in cosx."""
    SPLITRIJ = ORCAKeyword("splitrij")
    """ORCAKeyword: Approximation for two-electron integrals."""
    NOSPLITRIJ = ORCAKeyword("nosplitrij")
    """ORCAKeyword: Approximation for two-electron integrals."""
    RIAO = ORCAKeyword("riao")
    """ORCAKeyword: Approximation for two-electron integrals."""
    RICOSJ = ORCAKeyword("ricosj")
    """ORCAKeyword: Approximation for two-electron integrals."""
    RICOSJX = ORCAKeyword("ricosjx")
    """ORCAKeyword: Approximation for two-electron integrals."""
    RIJK = ORCAKeyword("rijk")
    """ORCAKeyword: Approximation for two-electron integrals."""
    RIJONX = ORCAKeyword("rijonx")
    """ORCAKeyword: Approximation for two-electron integrals."""
    RIJXC = ORCAKeyword("rijxc")
    """ORCAKeyword: Approximation for two-electron integrals."""
