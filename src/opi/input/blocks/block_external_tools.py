from pydantic import field_validator

from opi.input.blocks.base import Block, InputFilePath

__all__ = ("BlockExternalTools")

# > There is already another %methods block for dispersion, 
#   but they should not be used at the same time.
class BlockExternalTools(Block):
    """Class to model %method block in ORCA"""

    _name: str = "method"
    ProgExt: InputFilePath | None = None # Path to wrapper script
    Ext_Params: str | None = None # Arbitrary optional command line arguments


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