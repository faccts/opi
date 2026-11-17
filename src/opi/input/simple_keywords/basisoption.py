from opi.input.simple_keywords.base import (
    ORCAKeyword,
    SimpleKeywordBox,
)

__all__ = ("BasisOption",)


class BasisOption(SimpleKeywordBox):
    """Enum to store all simple keywords of type BasisOption."""

    ANOBASIS = ORCAKeyword("anobasis")
    """ORCAKeyword: Modifies a selected basis."""
    DECONTRACT = ORCAKeyword("decontract")
    """ORCAKeyword: Modifies a selected basis."""
    DECONTRACTAUX = ORCAKeyword("decontractaux")
    """ORCAKeyword: Modifies a selected basis."""
    DECONTRACTAUXC = ORCAKeyword("decontractauxc")
    """ORCAKeyword: Modifies a selected basis."""
    DECONTRACTAUXJ = ORCAKeyword("decontractauxj")
    """ORCAKeyword: Modifies a selected basis."""
    DECONTRACTAUXJK = ORCAKeyword("decontractauxjk")
    """ORCAKeyword: Modifies a selected basis."""
    DECONTRACTBAS = ORCAKeyword("decontractbas")
    """ORCAKeyword: Modifies a selected basis."""
    DECONTRACTCABS = ORCAKeyword("decontractcabs")
    """ORCAKeyword: Modifies a selected basis."""
    NOANOBASIS = ORCAKeyword("noanobasis")
    """ORCAKeyword: Modifies a selected basis."""
    NODECONTRACT = ORCAKeyword("nodecontract")
    """ORCAKeyword: Modifies a selected basis."""
    NODECONTRACTAUX = ORCAKeyword("nodecontractaux")
    """ORCAKeyword: Modifies a selected basis."""
    NODECONTRACTAUXC = ORCAKeyword("nodecontractauxc")
    """ORCAKeyword: Modifies a selected basis."""
    NODECONTRACTAUXJ = ORCAKeyword("nodecontractauxj")
    """ORCAKeyword: Modifies a selected basis."""
    NODECONTRACTAUXJK = ORCAKeyword("nodecontractauxjk")
    """ORCAKeyword: Modifies a selected basis."""
    NODECONTRACTBAS = ORCAKeyword("nodecontractbas")
    """ORCAKeyword: Modifies a selected basis."""
    NODECONTRACTCABS = ORCAKeyword("nodecontractcabs")
    """ORCAKeyword: Modifies a selected basis."""
    NOUNCONTRACT = ORCAKeyword("nouncontract")
    """ORCAKeyword: Modifies a selected basis."""
    NOUNCONTRACTAUX = ORCAKeyword("nouncontractaux")
    """ORCAKeyword: Modifies a selected basis."""
    NOUNCONTRACTAUXC = ORCAKeyword("nouncontractauxc")
    """ORCAKeyword: Modifies a selected basis."""
    NOUNCONTRACTAUXJ = ORCAKeyword("nouncontractauxj")
    """ORCAKeyword: Modifies a selected basis."""
    NOUNCONTRACTAUXJK = ORCAKeyword("nouncontractauxjk")
    """ORCAKeyword: Modifies a selected basis."""
    NOUNCONTRACTBAS = ORCAKeyword("nouncontractbas")
    """ORCAKeyword: Modifies a selected basis."""
    NOUNCONTRACTCABS = ORCAKeyword("nouncontractcabs")
    """ORCAKeyword: Modifies a selected basis."""
    UNCONTRACT = ORCAKeyword("uncontract")
    """ORCAKeyword: Modifies a selected basis."""
    UNCONTRACTAUX = ORCAKeyword("uncontractaux")
    """ORCAKeyword: Modifies a selected basis."""
    UNCONTRACTAUXC = ORCAKeyword("uncontractauxc")
    """ORCAKeyword: Modifies a selected basis."""
    UNCONTRACTAUXJ = ORCAKeyword("uncontractauxj")
    """ORCAKeyword: Modifies a selected basis."""
    UNCONTRACTAUXJK = ORCAKeyword("uncontractauxjk")
    """ORCAKeyword: Modifies a selected basis."""
    UNCONTRACTBAS = ORCAKeyword("uncontractbas")
    """ORCAKeyword: Modifies a selected basis."""
    UNCONTRACTCABS = ORCAKeyword("uncontractcabs")
    """ORCAKeyword: Modifies a selected basis."""
