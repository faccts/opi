from opi.input.simple_keywords.base import (
    SimpleKeyword,
    SimpleKeywordBox,
)

__all__ = ("Approximation",)


class Approximation(SimpleKeywordBox):
    """Enum to store all simple keywords of type Approximation.

    Attributes
    ----------
    CLUSTERALL : SimpleKeyword
        cluster all grids
    COSXCLUSTERALL : SimpleKeyword
        cluster cosx grid
    COSJXC : SimpleKeyword
        fast but blurry DFT
    FMM : SimpleKeyword
        Use FFM approximation
    FROZENCORE : SimpleKeyword
        Frozen core approx. in correlated WFT
    NOFROZENCORE : SimpleKeyword
        do not use frozen core approximation
    RI_BUPO_J : SimpleKeyword
        Use BUPO
    NOBUPO : SimpleKeyword
        Do not use BUPO
    NOCOSX : SimpleKeyword
        Do not use cosx
    RCSINGLESFOCK : SimpleKeyword
        Use COSX for Fock like single terms in CC
    NORCSINGLESFOCK : SimpleKeyword
        Do not use COSX for Fock like single terms in CC
    RI : SimpleKeyword
        Use RI
    NORI : SimpleKeyword
        Do not use RI
    RIJCOSX : SimpleKeyword
        Approximation for two-electron integrals
    NORIJCOSX : SimpleKeyword
        Approximation for two-electron integrals
    RIJKSINGLESFOCK : SimpleKeyword
        Use RIJK for Fock like single terms in CC
    NORIJKSINGLESFOCK : SimpleKeyword
        Do not use RIJK for Fock like single terms in CC
    USESFITTING : SimpleKeyword
        Approximation
    NOSFITTING : SimpleKeyword
        Do not use overlap fitting in cosx
    SPLITJ : SimpleKeyword
        Approximation for two-electron integrals
    SPLITRIJ : SimpleKeyword
        Approximation for two-electron integrals
    NOSPLITRIJ : SimpleKeyword
        Approximation for two-electron integrals
    RIAO : SimpleKeyword
        Approximation for two-electron integrals
    RICOSJ : SimpleKeyword
        Approximation for two-electron integrals
    RICOSJX : SimpleKeyword
        Approximation for two-electron integrals
    RIJK : SimpleKeyword
        Approximation for two-electron integrals
    RIJONX : SimpleKeyword
        Approximation for two-electron integrals
    RIJXC : SimpleKeyword
        Approximation for two-electron integrals
    """

    CLUSTERALL = SimpleKeyword("clusterall")
    COSXCLUSTERALL = SimpleKeyword("cosxclusterall")
    COSJXC = SimpleKeyword("cosjxc")
    FMM = SimpleKeyword("fmm")
    FROZENCORE = SimpleKeyword("frozencore")
    NOFROZENCORE = SimpleKeyword("nofrozencore")
    RI_BUPO_J = SimpleKeyword("ri-bupo/j")
    NOBUPO = SimpleKeyword("nobupo")
    NOCOSX = SimpleKeyword("nocosx")
    RCSINGLESFOCK = SimpleKeyword("rcsinglesfock")
    NORCSINGLESFOCK = SimpleKeyword("norcsinglesfock")
    RI = SimpleKeyword("ri")
    NORI = SimpleKeyword("nori")
    RIJCOSX = SimpleKeyword("rijcosx")
    NORIJCOSX = SimpleKeyword("norijcosx")
    RIJKSINGLESFOCK = SimpleKeyword("rijksinglesfock")
    NORIJKSINGLESFOCK = SimpleKeyword("norijksinglesfock")
    USESFITTING = SimpleKeyword("usesfitting")
    NOSFITTING = SimpleKeyword("nosfitting")
    SPLITJ = SimpleKeyword("splitj")
    SPLITRIJ = SimpleKeyword("splitrij")
    NOSPLITRIJ = SimpleKeyword("nosplitrij")
    RIAO = SimpleKeyword("riao")
    RICOSJ = SimpleKeyword("ricosj")
    RICOSJX = SimpleKeyword("ricosjx")
    RIJK = SimpleKeyword("rijk")
    RIJONX = SimpleKeyword("rijonx")
    RIJXC = SimpleKeyword("rijxc")
