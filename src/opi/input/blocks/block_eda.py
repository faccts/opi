from pydantic import field_validator

from opi.input.blocks import Block, InputFilePath

__all__ = ("BlockEda",)


class BlockEda(Block):
    """Class to model %eda block in ORCA"""

    _name: str = "eda"
    frag1_c: int | None = None
    frag2_c: int | None = None
    frag1_m: int | None = None
    frag2_m: int | None = None
    frag1_sf: bool | None = None
    frag2_sf: bool | None = None
    printinfo: bool | None = None
    frag2_fs: bool | None = None
    frag1: InputFilePath | None = None
    frag2: InputFilePath | None = None
    frag1_methodfile: InputFilePath | None = None
    frag2_methodfile: InputFilePath | None = None

    @field_validator("frag1", "frag2", "frag1_methodfile", "frag2_methodfile", mode="before")
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
