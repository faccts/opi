from opi.input.simple_keywords.base import (
    SimpleKeyword,
    SimpleKeywordBox,
)

__all__ = ("BasisOption",)


class BasisOption(SimpleKeywordBox):
    """Enum to store all simple keywords of type BasisOption."""

    ANOBASIS = SimpleKeyword("anobasis")
    """SimpleKeyword: Modifies a selected basis."""
    DECONTRACT = SimpleKeyword("decontract")
    """SimpleKeyword: Modifies a selected basis."""
    DECONTRACTAUX = SimpleKeyword("decontractaux")
    """SimpleKeyword: Modifies a selected basis."""
    DECONTRACTAUXC = SimpleKeyword("decontractauxc")
    """SimpleKeyword: Modifies a selected basis."""
    DECONTRACTAUXJ = SimpleKeyword("decontractauxj")
    """SimpleKeyword: Modifies a selected basis."""
    DECONTRACTAUXJK = SimpleKeyword("decontractauxjk")
    """SimpleKeyword: Modifies a selected basis."""
    DECONTRACTBAS = SimpleKeyword("decontractbas")
    """SimpleKeyword: Modifies a selected basis."""
    DECONTRACTCABS = SimpleKeyword("decontractcabs")
    """SimpleKeyword: Modifies a selected basis."""
    NOANOBASIS = SimpleKeyword("noanobasis")
    """SimpleKeyword: Modifies a selected basis."""
    NODECONTRACT = SimpleKeyword("nodecontract")
    """SimpleKeyword: Modifies a selected basis."""
    NODECONTRACTAUX = SimpleKeyword("nodecontractaux")
    """SimpleKeyword: Modifies a selected basis."""
    NODECONTRACTAUXC = SimpleKeyword("nodecontractauxc")
    """SimpleKeyword: Modifies a selected basis."""
    NODECONTRACTAUXJ = SimpleKeyword("nodecontractauxj")
    """SimpleKeyword: Modifies a selected basis."""
    NODECONTRACTAUXJK = SimpleKeyword("nodecontractauxjk")
    """SimpleKeyword: Modifies a selected basis."""
    NODECONTRACTBAS = SimpleKeyword("nodecontractbas")
    """SimpleKeyword: Modifies a selected basis."""
    NODECONTRACTCABS = SimpleKeyword("nodecontractcabs")
    """SimpleKeyword: Modifies a selected basis."""
    NOUNCONTRACT = SimpleKeyword("nouncontract")
    """SimpleKeyword: Modifies a selected basis."""
    NOUNCONTRACTAUX = SimpleKeyword("nouncontractaux")
    """SimpleKeyword: Modifies a selected basis."""
    NOUNCONTRACTAUXC = SimpleKeyword("nouncontractauxc")
    """SimpleKeyword: Modifies a selected basis."""
    NOUNCONTRACTAUXJ = SimpleKeyword("nouncontractauxj")
    """SimpleKeyword: Modifies a selected basis."""
    NOUNCONTRACTAUXJK = SimpleKeyword("nouncontractauxjk")
    """SimpleKeyword: Modifies a selected basis."""
    NOUNCONTRACTBAS = SimpleKeyword("nouncontractbas")
    """SimpleKeyword: Modifies a selected basis."""
    NOUNCONTRACTCABS = SimpleKeyword("nouncontractcabs")
    """SimpleKeyword: Modifies a selected basis."""
    UNCONTRACT = SimpleKeyword("uncontract")
    """SimpleKeyword: Modifies a selected basis."""
    UNCONTRACTAUX = SimpleKeyword("uncontractaux")
    """SimpleKeyword: Modifies a selected basis."""
    UNCONTRACTAUXC = SimpleKeyword("uncontractauxc")
    """SimpleKeyword: Modifies a selected basis."""
    UNCONTRACTAUXJ = SimpleKeyword("uncontractauxj")
    """SimpleKeyword: Modifies a selected basis."""
    UNCONTRACTAUXJK = SimpleKeyword("uncontractauxjk")
    """SimpleKeyword: Modifies a selected basis."""
    UNCONTRACTBAS = SimpleKeyword("uncontractbas")
    """SimpleKeyword: Modifies a selected basis."""
    UNCONTRACTCABS = SimpleKeyword("uncontractcabs")
    """SimpleKeyword: Modifies a selected basis."""
