from opi.input.simple_keywords.base import (
    SimpleKeyword,
    SimpleKeywordBox,
)

__all__ = ("Docker",)


class Docker(SimpleKeywordBox):
    """Enum to store all simple keywords of type Docker."""

    NORMALDOCK = SimpleKeyword("normaldock")
    """SimpleKeyword: Docker Methods."""
    COMPLETEDOCK = SimpleKeyword("completedock")
    """SimpleKeyword: Docker Methods."""
    DOCK_GFN_FF = SimpleKeyword("dock(gfn-ff)")
    """SimpleKeyword: Docker Methods."""
    DOCK_GFN0_XTB = SimpleKeyword("dock(gfn0-xtb)")
    """SimpleKeyword: Docker Methods."""
    DOCK_GFN1_XTB = SimpleKeyword("dock(gfn1-xtb)")
    """SimpleKeyword: Docker Methods."""
    DOCK_GFN2_XTB = SimpleKeyword("dock(gfn2-xtb)")
    """SimpleKeyword: Docker Methods."""
    DOCK_GFNFF = SimpleKeyword("dock(gfnff)")
    """SimpleKeyword: Docker Methods."""
    DOCK_XTB = SimpleKeyword("dock(xtb)")
    """SimpleKeyword: Docker Methods."""
    DOCK_XTB0 = SimpleKeyword("dock(xtb0)")
    """SimpleKeyword: Docker Methods."""
    DOCK_XTB1 = SimpleKeyword("dock(xtb1)")
    """SimpleKeyword: Docker Methods."""
    DOCKER = SimpleKeyword("docker")
    """SimpleKeyword: GOAT Methods."""
    DOCKER_GFN_FF = SimpleKeyword("docker(gfn-ff)")
    """SimpleKeyword: Docker Methods."""
    DOCKER_GFN0_XTB = SimpleKeyword("docker(gfn0-xtb)")
    """SimpleKeyword: Docker Methods."""
    DOCKER_GFN1_XTB = SimpleKeyword("docker(gfn1-xtb)")
    """SimpleKeyword: Docker Methods."""
    DOCKER_GFN2_XTB = SimpleKeyword("docker(gfn2-xtb)")
    """SimpleKeyword: Docker Methods."""
    DOCKER_GFNFF = SimpleKeyword("docker(gfnff)")
    """SimpleKeyword: Docker Methods."""
    DOCKER_XTB = SimpleKeyword("docker(xtb)")
    """SimpleKeyword: Docker Methods."""
    DOCKER_XTB0 = SimpleKeyword("docker(xtb0)")
    """SimpleKeyword: Docker Methods."""
    DOCKER_XTB1 = SimpleKeyword("docker(xtb1)")
    """SimpleKeyword: Docker Methods."""
    QUICKDOCK = SimpleKeyword("quickdock")
    """SimpleKeyword: Docker Methods."""
    SCREENDOCK = SimpleKeyword("screendock")
    """SimpleKeyword: Docker Methods."""
