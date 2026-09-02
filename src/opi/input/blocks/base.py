from abc import ABC
from pathlib import Path
from typing import Any, ClassVar

from pydantic import BaseModel, ConfigDict, field_validator

from opi.input.blocks.util import InputFilePath, NoCaseDict
from opi.input.simple_keywords import SimpleKeyword, Solvent

__all__ = ["BlockABC"]


class BlockABC(BaseModel, ABC):
    """
    Base Class for Block.
    Each ORCA input block is defined in the module block_<block_name>.py
    Every class defined for a block is derived from this base BlockABC class ,
    which defines attributes, methods and properties shared by all blocks.

    This class is abstract and cannot be instantiated: it models no ORCA block of its own.
    Every subclass must name the ORCA block it models, either by defining `_name` at class level
    (as the implemented blocks do, e.g. `_name: str = "scf"`) or by assigning `self._name` during
    initialization (as `Block` does for blocks that are named at runtime).

    Attributes
    ----------
        aftercoord: bool
            Indicates whether the block is positioned after a coordinate transformation.
        _name: str
            Internal name identifier for the block.
        _arbitrary: dict[str, str]
            A dictionary storing arbitrary key-value options for the ORCA input that are not implemented natively.
            Both key and value are stored as strings.
        _registry: ClassVar[dict[str, type[BlockABC]]]
            Registry that maps the name of an ORCA block to the `BlockABC` subclass implementing it.
            Only subclasses with a class-level `_name` are registered, so subclasses that receive
            their name at runtime (like `Block`) are absent.
            Used to recognize that a runtime-named block refers to an already implemented block.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)
    _name: str
    aftercoord: bool = False
    _arbitrary: NoCaseDict = NoCaseDict()

    # > Registry of the subclasses of `BlockABC`.
    # > Being a `ClassVar`, it is a single object shared by the whole class hierarchy.
    # > It is filled by `__pydantic_init_subclass__()`, hence it only contains the
    # > subclasses whose defining module has been imported.
    _registry: ClassVar[dict[str, type["BlockABC"]]] = {}

    def __init__(self, /, **data: Any) -> None:
        """
        Initialize a block.

        Parameters
        ----------
        **data : Any
            Fields of the block, passed on to pydantic.

        Raises
        ------
        TypeError
            If `BlockABC` itself is instantiated.
        """
        # > `ABC` alone does not prevent instantiation, as `BlockABC` defines no abstract method.
        # > Without this guard, a bare `BlockABC` would be a block without a name, and every
        # > access to `BlockABC.name` would fail with an `AttributeError`.
        if type(self) is BlockABC:
            raise TypeError(
                "'BlockABC' is abstract and models no ORCA block: use the class of the block, "
                "e.g. 'BlockScf', or 'Block' for a block that OPI does not implement."
            )
        super().__init__(**data)

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        """
        Register a subclass of `BlockABC` in `BlockABC._registry` under its block name. The registry allows OPI to keep track of all blocks
        that are natively implemented in OPI. so that there is no collision when the user attempts to initialize an arbitrary block.
        Called by pydantic once a subclass has been fully initialized.

        Parameters
        ----------
        **kwargs : Any
            Class keyword arguments, passed on to pydantic.
        """
        super().__pydantic_init_subclass__(**kwargs)
        name = cls.get_block_name()
        # > Subclasses without a class-level `_name` are named at runtime and cannot be registered.
        if name is not None:
            # > The first registration wins, so a subclass cannot displace the block class it derives from.
            BlockABC._registry.setdefault(name, cls)

    @staticmethod
    def normalize_name(name: str) -> str:
        """
        Normalize the name of an ORCA block, so that the same block is always referred to by the
        same name. Strips surrounding whitespace and the leading '%', and lowers the case.

        Parameters
        ----------
        name : str
            Name of an ORCA block, e.g. "%SCF".

        Returns
        -------
        str
            The normalized name, e.g. "scf".
        """
        return name.strip().removeprefix("%").strip().lower()

    @classmethod
    def get_block_name(cls) -> str | None:
        """
        Get the ORCA block name defined by this class.

        Returns
        -------
        str | None
            The class-level block name, or None if the class does not define one, or defines one
            that is empty once normalized.
        """
        name = getattr(cls.__private_attributes__.get("_name"), "default", None)
        if not isinstance(name, str):
            return None
        # > Normalize before testing for emptiness: a name such as "%" is non-empty as written,
        # > but `normalize_name()` strips it down to "".
        return BlockABC.normalize_name(name) or None

    @classmethod
    def get_block_class(cls, name: str) -> type["BlockABC"] | None:
        """
        Get the `BlockABC` subclass that implements the given ORCA block name.

        Parameters
        ----------
        name : str
            Name of the ORCA block, case-insensitive.

        Returns
        -------
        type[BlockABC] | None
            The `BlockABC` subclass for that name, or None if no subclass implements it.
        """
        return BlockABC._registry.get(BlockABC.normalize_name(name))

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
        Method to convert a BlockABC instance into string for the ORCA input file.
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
                elif isinstance(value, SimpleKeyword | Solvent):
                    s += f'    {key} "{str(value).lower()}"\n'  # add quotations if value is of type SimpleKeyword
                else:
                    s += f"    {key} {value}\n"  # print key value pairs as they are
        s += "end"

        return s

    def __or__(self, other: "BlockABC") -> "BlockABC":
        """
        Merges two instances of `BlockABC` that model the same ORCA block. If a common attribute or
        arbitrary option exists in both `self` and `other`, the value in `other` will be given
        precedence. Neither operand is modified.

        Note that the `aftercoord` value will also be overridden, even if the `self` block explicitly sets aftercoord to True,
        the `other` block will override it to False as that is the default option.

        Parameters
        ----------
        other: BlockABC
            Instance of `BlockABC` to be merged into `self`

        Returns
        -------
        BlockABC
            New instance of `BlockABC` with attributes and arbitrary options of `self` and `other`.

        Raises
        ------
        ValueError
            If `self` and `other` model different ORCA blocks, as the merged block could only
            carry one of the two names.
        """
        if not isinstance(other, BlockABC):
            return NotImplemented
        if self.name != other.name:
            raise ValueError(
                f"Cannot merge blocks that model different ORCA blocks: "
                f"'%{self.name}' and '%{other.name}'."
            )

        # > Merge by copying `self` and overlaying `other`, rather than by revalidating a dump of
        # > both: the block name and the arbitrary options live on private attributes, which
        # > `model_dump()` does not include.
        new_block = self.model_copy(deep=True)
        # > `__dict__` holds the field values as they are, so nested blocks and arbitrary types
        # > (e.g. `SimpleKeyword`) are carried over untouched instead of being serialized.
        for key, value in other.__dict__.items():
            if value is not None:
                setattr(new_block, key, value)
        new_block._arbitrary = NoCaseDict({**self._arbitrary, **other._arbitrary})
        return new_block

    @property
    def name(self) -> str:
        """
        Name of the ORCA block modelled by this block.

        Returns
        -------
        str
            The name of the ORCA block, as defined by `_name`.

        Raises
        ------
        AttributeError
            If the subclass neither defines `_name` at class level nor assigns it during
            initialization, as such a block cannot be written to the ORCA input.
        """
        name = getattr(self, "_name", None)
        name = BlockABC.normalize_name(name) if isinstance(name, str) else None
        if not name:
            raise AttributeError(
                f"'{type(self).__name__}' does not define the name of an ORCA block: "
                "subclasses of 'BlockABC' must set the private attribute '_name'."
            )
        return name

    @name.setter
    def name(self, name: str) -> None:
        """
        Parameters
        ----------
        name : str
        """
        raise AttributeError("*BlockABC.name* is a read-only property!")

    @field_validator("*", mode="before")
    @classmethod
    def init_inputpath(cls, inp: Any) -> Any:
        if isinstance(inp, Path):
            return InputFilePath(file=inp)
        else:
            return inp

    @classmethod
    def get_subclass_by_name(cls, name: str) -> type["BlockABC"]:
        """
        Look up a ``Block`` subclass by its class name or ORCA block name.

        Matching is case-insensitive and checks both the Python class name
        (e.g. ``"BlockScf"``) and the ORCA block name returned by the
        subclass's ``name`` property (e.g. ``"scf"``).

        Parameters
        ----------
        name : str
            Class name or ORCA block name of the desired subclass.

        Returns
        -------
        type[BlockABC]
            The matching subclass.

        Raises
        ------
        ValueError
            If no subclass matches ``name``.
        """
        # Search for `BlockABC` class by OPI name
        opi_block_name_matches = {sub.__name__.lower(): sub for sub in cls.__subclasses__()}
        # Search for `BlockABC` class by ORCA block name
        orca_block_name_matches = {sub.name.lower(): sub for sub in cls.__subclasses__()}
        # Collect matches across both criteria
        all_matches = opi_block_name_matches.get(name.lower()) or orca_block_name_matches.get(
            name.lower()
        )

        # If no match is found, raise ValueError
        if all_matches is None:
            raise ValueError(
                f"No Block subclass found with name {name!r}. Available: {list(opi_block_name_matches.keys())}"
            )

        return all_matches
