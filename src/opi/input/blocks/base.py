from abc import ABC
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, field_validator

from opi.input.blocks.util import InputFilePath
from opi.input.simple_keywords import SimpleKeyword

__all__ = "Block"


class Block(BaseModel, ABC):
    """
    Base Class for Block.
    Each ORCA input block is defined in the module block_<block_name>.py
    Every class defined for a block is derived from this base Block class ,
    which defines attributes, methods and properties shared by all blocks.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)
    _name: str
    aftercoord: bool = False

    def format_orca(self) -> str:
        """
        Method to convert a Block instance into string for the ORCA input file.
        Returns the string representation of the respective class it is called by.
        """
        s = f"%{self.name}\n"
        for key, value in self.__dict__.items():
            if value is not None:
                if key == "aftercoord":
                    continue
                elif isinstance(value, SimpleKeyword):
                    s += f'    {key} "{str(value).lower()}"\n'
                else:
                    s += f"    {key} {str(value).lower()}\n"
        s += "end"

        return s

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        """
        Parameters
        ----------
        name : str
        """
        raise AttributeError("*Block.name* is a read-only property!")

    @field_validator("*", mode="before")
    @classmethod
    def init_inputpath(cls, inp: Any) -> Any:
        if isinstance(inp, Path):
            return InputFilePath(file=inp)
        else:
            return inp
