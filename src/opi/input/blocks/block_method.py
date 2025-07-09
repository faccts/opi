from pydantic import field_validator

from opi.input.blocks import Block, InputFilePath

__all__ = ("BlockMethod",)


class BlockMethod(Block):
    """Class to model %method block in ORCA"""

    _name: str = "Method"

    # > Options DFT-D
    d3s6: float | None = None
    d3a1: float | None = None
    d3s8: float | None = None
    d3a2: float | None = None

    # > Options for Extopt
    ProgExt: InputFilePath | None = None  # Path to wrapper script
    Ext_Params: str | None = None  # Arbitrary optional command line arguments


    @field_validator("ProgExt", mode="before")
    @classmethod
    def path_from_string(cls, path: str | InputFilePath) -> InputFilePath:
        """
        Parameters
        ----------
        path : str | InputFilePath
        """
        if isinstance(path, str):
            return InputFilePath.from_string(path)
        else:
            return path
