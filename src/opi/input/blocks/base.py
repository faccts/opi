from abc import ABC
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, field_validator

from opi.input.blocks.util import InputFilePath, NoCaseDict
from opi.input.simple_keywords import SimpleKeyword

__all__ = ["Block"]


class Block(BaseModel, ABC):
    """
    Base Class for Block.
    Each ORCA input block is defined in the module block_<block_name>.py
    Every class defined for a block is derived from this base Block class ,
    which defines attributes, methods and properties shared by all blocks.

    Attributes
    ----------
        aftercoord: bool
            Indicates whether the block is positioned after a coordinate transformation.
        _name: str
            Internal name identifier for the block.
        _arbitrary: dict[str, str]
            A dictionary storing arbitrary key-value options for the ORCA input that are not implemented natively.
            Both key and value are stored as strings.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)
    _name: str
    aftercoord: bool = False
    _arbitrary: NoCaseDict = NoCaseDict()

    def add_option(self, name: str, val: str) -> None:
        """
        Add arbitrary attributes to this block.

        Parameters
        ----------
        name : str
        Key value of arbitrary attribute.

        val : str
        Value of arbitrary attribute.

        Raises
        ------
        TypeError
            if name or val are not of type string.

        KeyError
            if attribute of same name is already defined.
        """
        if self.has_option(name):
            raise KeyError(f"Attribute {name} already defined")
        self._arbitrary.__setitem__(name, val)

    def modify_option(self, name: str, val: str) -> None:
        """
        Modify an arbitrary attribute of this block.
        If an attribute with this name already exists, the attribute will be overwritten.
        If the attribute doesn't exist yet, a new attribute will be created.

        Parameters
        ----------
        name: str
            Name of arbitrary attribute.
        val: str
            Value of arbitrary attribute.

        Raises
        ------
        TypeError
            If name or val are not of type string.

        """
        self._arbitrary.__setitem__(name, val)

    def remove_option(self, name: str) -> None:
        """
        Remove arbitrary attribute from this block.

        Parameters
        ----------
        name: str
            Name of arbitrary attribute to remove

        Raises
        -------
        KeyError
            if no attribute with that name exists
        TypeError
            if name is not of type string
        """
        self._arbitrary.__delitem__(name)

    def clear_options(self) -> None:
        """
        Clear all arbitrary attributes from this block.
        """
        self._arbitrary.clear()

    def has_option(self, name: str) -> bool:
        """
        Check if an arbitrary attribute with the given name exists.

        Parameters
        ----------
        name: str
            Name of the attribute.

        Returns
        -------
        bool
            True if the attribute with the given name exists, False otherwise.

        Raises
        ------
        TypeError
            if name is not of type string
        """
        return self._arbitrary.__contains__(name)

    def get_option(self, name: str) -> str | None:
        """
        Get the value of an arbitrary attribute.

        Parameters
        ----------
        name: str
            Name of the attribute.

        Returns
        -------
        str or None
            The value of the attribute if it exists, else None.

        Raises
        ------
        KeyError
            if no attribute with that name exists
        TypeError
            if name is not of type string
        """
        return self._arbitrary.__getitem__(name)

    def format_orca(self) -> str:
        """
        Method to convert a Block instance into string for the ORCA input file.
        Returns the string representation of the respective class it is called by.
        """
        s = f"%{self.name}\n"
        for key, value in self._arbitrary.items():  # print arbitrary key value pairs first
            s += f"    {key} {value.lower()}\n"
        for (
            key,
            value,
        ) in self.__dict__.items():  # iterate through all key value pairs defined in the block
            if value is not None:
                if key == "aftercoord":  # skip aftercoord
                    continue
                elif isinstance(value, SimpleKeyword):
                    s += f'    {key} "{str(value).lower()}"\n'  # add quotations if value is of type SimpleKeyword
                else:
                    s += f"    {key} {str(value).lower()}\n"  # print key value pairs
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
