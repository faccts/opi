from opi.input.simple_keywords.base import (
    ORCAKeyword,
    SimpleKeywordBox,
)

__all__ = ("Docker",)


class Docker(SimpleKeywordBox):
    """Enum to store all simple keywords of type Docker."""

    NORMALDOCK = ORCAKeyword("normaldock")
    """ORCAKeyword: Docker Methods."""
    COMPLETEDOCK = ORCAKeyword("completedock")
    """ORCAKeyword: Docker Methods."""
    DOCK_GFN_FF = ORCAKeyword("dock(gfn-ff)")
    """ORCAKeyword: Docker Methods."""
    DOCK_GFN0_XTB = ORCAKeyword("dock(gfn0-xtb)")
    """ORCAKeyword: Docker Methods."""
    DOCK_GFN1_XTB = ORCAKeyword("dock(gfn1-xtb)")
    """ORCAKeyword: Docker Methods."""
    DOCK_GFN2_XTB = ORCAKeyword("dock(gfn2-xtb)")
    """ORCAKeyword: Docker Methods."""
    DOCK_GFNFF = ORCAKeyword("dock(gfnff)")
    """ORCAKeyword: Docker Methods."""
    DOCK_XTB = ORCAKeyword("dock(xtb)")
    """ORCAKeyword: Docker Methods."""
    DOCK_XTB0 = ORCAKeyword("dock(xtb0)")
    """ORCAKeyword: Docker Methods."""
    DOCK_XTB1 = ORCAKeyword("dock(xtb1)")
    """ORCAKeyword: Docker Methods."""
    DOCKER = ORCAKeyword("docker")
    """ORCAKeyword: GOAT Methods."""
    DOCKER_GFN_FF = ORCAKeyword("docker(gfn-ff)")
    """ORCAKeyword: Docker Methods."""
    DOCKER_GFN0_XTB = ORCAKeyword("docker(gfn0-xtb)")
    """ORCAKeyword: Docker Methods."""
    DOCKER_GFN1_XTB = ORCAKeyword("docker(gfn1-xtb)")
    """ORCAKeyword: Docker Methods."""
    DOCKER_GFN2_XTB = ORCAKeyword("docker(gfn2-xtb)")
    """ORCAKeyword: Docker Methods."""
    DOCKER_GFNFF = ORCAKeyword("docker(gfnff)")
    """ORCAKeyword: Docker Methods."""
    DOCKER_XTB = ORCAKeyword("docker(xtb)")
    """ORCAKeyword: Docker Methods."""
    DOCKER_XTB0 = ORCAKeyword("docker(xtb0)")
    """ORCAKeyword: Docker Methods."""
    DOCKER_XTB1 = ORCAKeyword("docker(xtb1)")
    """ORCAKeyword: Docker Methods."""
    QUICKDOCK = ORCAKeyword("quickdock")
    """ORCAKeyword: Docker Methods."""
    SCREENDOCK = ORCAKeyword("screendock")
    """ORCAKeyword: Docker Methods."""
