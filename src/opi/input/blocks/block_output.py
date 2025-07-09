from opi.input.blocks import Block

__all__ = ("BlockOutput",)


class BlockOutput(Block):
    """Class to model the %output block in ORCA"""

    _name: str = "output"
    # > options
    jsonpropfile: bool | None = None  # If True, generate JSON property file
    jsongbwfile: bool | None = None  # If True, generate JSON gbw file
