from opi.input.simple_keywords.base import (
    SimpleKeyword,
    SimpleKeywordBox,
)

__all__ = ("BasisOption",)


class BasisOption(SimpleKeywordBox):
    """Enum to store all simple keywords of type BasisOption.

    Attributes
    ----------
    ANOBASIS : SimpleKeyword
        Modifies a selected basis
    DECONTRACT : SimpleKeyword
        Modifies a selected basis
    DECONTRACTAUX : SimpleKeyword
        Modifies a selected basis
    DECONTRACTAUXC : SimpleKeyword
        Modifies a selected basis
    DECONTRACTAUXJ : SimpleKeyword
        Modifies a selected basis
    DECONTRACTAUXJK : SimpleKeyword
        Modifies a selected basis
    DECONTRACTBAS : SimpleKeyword
        Modifies a selected basis
    DECONTRACTCABS : SimpleKeyword
        Modifies a selected basis
    NOANOBASIS : SimpleKeyword
        Modifies a selected basis
    NODECONTRACT : SimpleKeyword
        Modifies a selected basis
    NODECONTRACTAUX : SimpleKeyword
        Modifies a selected basis
    NODECONTRACTAUXC : SimpleKeyword
        Modifies a selected basis
    NODECONTRACTAUXJ : SimpleKeyword
        Modifies a selected basis
    NODECONTRACTAUXJK : SimpleKeyword
        Modifies a selected basis
    NODECONTRACTBAS : SimpleKeyword
        Modifies a selected basis
    NODECONTRACTCABS : SimpleKeyword
        Modifies a selected basis
    NOUNCONTRACT : SimpleKeyword
        Modifies a selected basis
    NOUNCONTRACTAUX : SimpleKeyword
        Modifies a selected basis
    NOUNCONTRACTAUXC : SimpleKeyword
        Modifies a selected basis
    NOUNCONTRACTAUXJ : SimpleKeyword
        Modifies a selected basis
    NOUNCONTRACTAUXJK : SimpleKeyword
        Modifies a selected basis
    NOUNCONTRACTBAS : SimpleKeyword
        Modifies a selected basis
    NOUNCONTRACTCABS : SimpleKeyword
        Modifies a selected basis
    UNCONTRACT : SimpleKeyword
        Modifies a selected basis
    UNCONTRACTAUX : SimpleKeyword
        Modifies a selected basis
    UNCONTRACTAUXC : SimpleKeyword
        Modifies a selected basis
    UNCONTRACTAUXJ : SimpleKeyword
        Modifies a selected basis
    UNCONTRACTAUXJK : SimpleKeyword
        Modifies a selected basis
    UNCONTRACTBAS : SimpleKeyword
        Modifies a selected basis
    UNCONTRACTCABS : SimpleKeyword
        Modifies a selected basis
    """

    ANOBASIS = SimpleKeyword("anobasis")
    DECONTRACT = SimpleKeyword("decontract")
    DECONTRACTAUX = SimpleKeyword("decontractaux")
    DECONTRACTAUXC = SimpleKeyword("decontractauxc")
    DECONTRACTAUXJ = SimpleKeyword("decontractauxj")
    DECONTRACTAUXJK = SimpleKeyword("decontractauxjk")
    DECONTRACTBAS = SimpleKeyword("decontractbas")
    DECONTRACTCABS = SimpleKeyword("decontractcabs")
    NOANOBASIS = SimpleKeyword("noanobasis")
    NODECONTRACT = SimpleKeyword("nodecontract")
    NODECONTRACTAUX = SimpleKeyword("nodecontractaux")
    NODECONTRACTAUXC = SimpleKeyword("nodecontractauxc")
    NODECONTRACTAUXJ = SimpleKeyword("nodecontractauxj")
    NODECONTRACTAUXJK = SimpleKeyword("nodecontractauxjk")
    NODECONTRACTBAS = SimpleKeyword("nodecontractbas")
    NODECONTRACTCABS = SimpleKeyword("nodecontractcabs")
    NOUNCONTRACT = SimpleKeyword("nouncontract")
    NOUNCONTRACTAUX = SimpleKeyword("nouncontractaux")
    NOUNCONTRACTAUXC = SimpleKeyword("nouncontractauxc")
    NOUNCONTRACTAUXJ = SimpleKeyword("nouncontractauxj")
    NOUNCONTRACTAUXJK = SimpleKeyword("nouncontractauxjk")
    NOUNCONTRACTBAS = SimpleKeyword("nouncontractbas")
    NOUNCONTRACTCABS = SimpleKeyword("nouncontractcabs")
    UNCONTRACT = SimpleKeyword("uncontract")
    UNCONTRACTAUX = SimpleKeyword("uncontractaux")
    UNCONTRACTAUXC = SimpleKeyword("uncontractauxc")
    UNCONTRACTAUXJ = SimpleKeyword("uncontractauxj")
    UNCONTRACTAUXJK = SimpleKeyword("uncontractauxjk")
    UNCONTRACTBAS = SimpleKeyword("uncontractbas")
    UNCONTRACTCABS = SimpleKeyword("uncontractcabs")
