from opi.input.blocks import Block

__all__ = ("BlockXtb",)


class BlockXtb(Block):
    """Class to model %xtb block in ORCA"""

    _name: str = "xtb"
    xtbversion: int | None = None
    etemp: float | None = None
    doalpb: bool | None = None
    doddcosmo: bool | None = None
    docpcmx: bool | None = None
    epsilon: float | None = None
    ceh: bool | None = None
    accuracy: float | None = None
    acc: float | None = None
    maxcore: int | None = None
    nprocs: int | None = None
    randomseed: bool | None = None
    bhess: bool | None = None
