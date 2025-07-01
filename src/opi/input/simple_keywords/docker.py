from opi.input.simple_keywords.base import (
    SimpleKeyword,
    SimpleKeywordBox,
)

__all__ = ("Docker",)


class Docker(SimpleKeywordBox):
    """Enum to store all simple keywords of type Docker.

    Attributes
    ----------
    NORMALDOCK : SimpleKeyword
        Docker Methods
    COMPLETEDOCK : SimpleKeyword
        Docker Methods
    DOCK_GFN_FF : SimpleKeyword
        Docker Methods
    DOCK_GFN0_XTB : SimpleKeyword
        Docker Methods
    DOCK_GFN1_XTB : SimpleKeyword
        Docker Methods
    DOCK_GFN2_XTB : SimpleKeyword
        Docker Methods
    DOCK_GFNFF : SimpleKeyword
        Docker Methods
    DOCK_XTB : SimpleKeyword
        Docker Methods
    DOCK_XTB0 : SimpleKeyword
        Docker Methods
    DOCK_XTB1 : SimpleKeyword
        Docker Methods
    DOCKER : SimpleKeyword
        GOAT Methods
    DOCKER_GFN_FF : SimpleKeyword
        Docker Methods
    DOCKER_GFN0_XTB : SimpleKeyword
        Docker Methods
    DOCKER_GFN1_XTB : SimpleKeyword
        Docker Methods
    DOCKER_GFN2_XTB : SimpleKeyword
        Docker Methods
    DOCKER_GFNFF : SimpleKeyword
        Docker Methods
    DOCKER_XTB : SimpleKeyword
        Docker Methods
    DOCKER_XTB0 : SimpleKeyword
        Docker Methods
    DOCKER_XTB1 : SimpleKeyword
        Docker Methods
    QUICKDOCK : SimpleKeyword
        Docker Methods
    SCREENDOCK : SimpleKeyword
        Docker Methods
    """

    NORMALDOCK = SimpleKeyword("normaldock")
    COMPLETEDOCK = SimpleKeyword("completedock")
    DOCK_GFN_FF = SimpleKeyword("dock(gfn-ff)")
    DOCK_GFN0_XTB = SimpleKeyword("dock(gfn0-xtb)")
    DOCK_GFN1_XTB = SimpleKeyword("dock(gfn1-xtb)")
    DOCK_GFN2_XTB = SimpleKeyword("dock(gfn2-xtb)")
    DOCK_GFNFF = SimpleKeyword("dock(gfnff)")
    DOCK_XTB = SimpleKeyword("dock(xtb)")
    DOCK_XTB0 = SimpleKeyword("dock(xtb0)")
    DOCK_XTB1 = SimpleKeyword("dock(xtb1)")
    DOCKER = SimpleKeyword("docker")
    DOCKER_GFN_FF = SimpleKeyword("docker(gfn-ff)")
    DOCKER_GFN0_XTB = SimpleKeyword("docker(gfn0-xtb)")
    DOCKER_GFN1_XTB = SimpleKeyword("docker(gfn1-xtb)")
    DOCKER_GFN2_XTB = SimpleKeyword("docker(gfn2-xtb)")
    DOCKER_GFNFF = SimpleKeyword("docker(gfnff)")
    DOCKER_XTB = SimpleKeyword("docker(xtb)")
    DOCKER_XTB0 = SimpleKeyword("docker(xtb0)")
    DOCKER_XTB1 = SimpleKeyword("docker(xtb1)")
    QUICKDOCK = SimpleKeyword("quickdock")
    SCREENDOCK = SimpleKeyword("screendock")
