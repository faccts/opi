from opi.input.blocks import Block

__all__ = ("BlockRocis",)


class BlockRocis(Block):
    """Class to model %rocis block in ORCA"""

    _name: str = "rocis"

    # > General Keywords
    nroots: int | None = None
    maxdim: int | None = None
    maxiter: int | None = None
    etol: float | None = None
    rtol: float | None = None
    nguessmat: int | None = None
    # > Output Keywords
    docd: bool | None = None
