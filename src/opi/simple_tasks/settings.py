import types as builtin_types
import typing
from typing import Any

from pydantic import BaseModel, ConfigDict, field_validator, model_validator
from pydantic_core.core_schema import ValidationInfo

from opi.input import Input
from opi.input.blocks import BlockABC
from opi.input.simple_keywords import SimpleKeyword, SimpleKeywordBox, SolvationModel, Solvent
from opi.input.simple_keywords.solvation_model import SolvationModelAndSolvent


class Settings(BaseModel):
    """
    Base Pydantic model for all OPI task and method settings.

    Subclasses declare typed fields whose annotations encode how each value
    maps to an ORCA input: a single-element metadata tuple means a simple
    keyword, a two-element tuple ``(block_name, attr)`` means a block option.
    ``map_to_input`` reads those annotations at runtime to populate an
    ``Input`` object automatically.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True, validate_assignment=True)
    _name: str

    def __or__(self, other: "Settings") -> "Settings":
        """
        Merge two ``Settings`` objects of the same type.

        Fields explicitly set on ``other`` take precedence; fields that were
        not set on ``other`` keep their value from ``self``.

        Parameters
        ----------
        other : Settings
            Settings object whose set fields override those of ``self``.

        Returns
        -------
        Settings
            New instance of the same type containing the merged fields.
        """
        if type(self) is not type(other):
            return NotImplemented

        combined_data = {**self.model_dump(), **other.model_dump(exclude_unset=True)}
        return self.__class__(**combined_data)

    def map_to_input(self) -> Input:
        """
        Function to map all information held in `Settings` class to an `Input` class object. The function receives an
        `Input` object , which may or may not be already populated, after which the function uses the type hints of
        every field defined in the class to either fetch a `SimpleKeyword` from the appropriate Enum, and adds it to
        `Input.simple_keywords`, or initializes the appropriate block with the attribute set to user defined value, and
        adds it to `Input.blocks`.

        The modified `Input` object is then returned.


        Returns
        -------
        Input
            Modified `Input` object.
        """
        # initialize an empty input object which will reflect the input options selected by the user
        input_object = Input()

        # include_extras=True preserves Annotated metadata, which encodes how each field maps to ORCA input
        hints = typing.get_type_hints(self.__class__, include_extras=True)

        for field_name, field_type in hints.items():
            value = getattr(self, field_name)
            if value is None:
                continue

            metadata = self._get_field_metadata(field_type)

            match metadata:
                case (validator,):
                    # Single-element metadata: field maps to a simple keyword
                    if issubclass(validator, Solvent):
                        # Solvent is handled indirectly via SolvationModel; skip standalone
                        continue

                    new_keyword = self._get_simple_keyword(validator, value)
                    if new_keyword:
                        input_object.add_simple_keywords(new_keyword)

                case (validator, key):
                    # Two-element metadata: field maps to an attribute on a block
                    block_type = self._get_block_class(field_name, validator)
                    block_instant = block_type(**{key: value})

                    # `get_block()` returns None for a block that has not been added yet.
                    existing_block = input_object.get_block(block_type)
                    if existing_block is None:
                        input_object.add_blocks(block_instant)
                    else:
                        # Merge with any existing block of this type so no other attributes are lost
                        new_block = block_instant | existing_block
                        input_object.add_blocks(new_block, overwrite=True)

        return input_object

    def __str__(self) -> str:
        """
        String representation of `Settings`. Mostly for debugging purposes.

        Returns
        -------
        str
            String representation of `Settings`.

        """
        lines = [f"{self._name.title()} Settings:"]
        for field_name, value in self.model_dump().items():
            lines.append(f"  {field_name}: {value}")
        return "\n".join(lines)

    @staticmethod
    def _get_block_class(field_name: str, block_name: Any) -> type["BlockABC"]:
        """
        Resolve the ORCA block name a field is annotated with into its `BlockABC` subclass.

        Parameters
        ----------
        field_name: str
            Name of the field, used for the error message only.
        block_name: Any
            Name of the ORCA block, as taken from the metadata of the field annotation.

        Returns
        -------
        type[BlockABC]
            The `BlockABC` subclass that implements the block.

        Raises
        ------
        ValueError
            If `block_name` is not the name of an ORCA block that OPI implements.
        """
        block_class = BlockABC.get_block_class(block_name) if isinstance(block_name, str) else None
        if block_class is None:
            raise ValueError(
                f"'{field_name}' is annotated with {block_name!r}, "
                "which is not the name of an ORCA block implemented by OPI."
            )

        return block_class

    @staticmethod
    def _get_field_metadata(hint: Any) -> tuple[Any, ...]:
        """
        Function to return the metadata of the type annotation of a field.
        The type hints are first retrieved after which the metadata is extracted and then returned.

        Parameters
        ----------
        hint: Type hint / annotation of field

        Returns
        -------
        tuple
            Tuple of metadata about the field.

        """
        origin = typing.get_origin(hint)
        args = typing.get_args(hint)
        # Optional[X] and X | None both produce a Union; unwrap to reach the inner type
        is_union = origin is typing.Union or isinstance(hint, builtin_types.UnionType)
        if is_union:
            non_none_args = [arg for arg in args if arg is not type(None)]
            if non_none_args:
                return Settings._get_field_metadata(non_none_args[0])
        # For Annotated[T, m1, m2, ...], get_args returns (T, m1, m2, ...); skip T at index 0
        return args[1:] if len(args) > 1 else ()

    @staticmethod
    def _resolve_field_value(
        field_name: str, value: Any, metadata: tuple[type["SimpleKeywordBox"]] | tuple[str, str]
    ) -> Any:
        """
        Function to translate user input into OPI compatible types. This is done using the metadata of the type
        annotation associated with the field. There are two cases:

        Case 1
        ------
        Metadata has only one value. In this case the field is a simple keyword. Here the class associated with the input
        option (eg: `Dft`) ,  will be checked to see if the user-given input option exists , and if it does , returns
        the enum member associated with the input option.

        Example
        =======
        simple_keyword_attribute: typing.Annotated[SimpleKeyword, Dft]

        In this case the metadata is the class Dft, which signifies that the expected simple keyword must be from the
        Dft enum.

        Case 2
        ------
        Metadata has two values, validator class and key. In this case the field is a block option. The associated block
        class is first fetched, and then the attribute of the block is set to the user-given input option. This is then
        validated by the block itself using Pydantic features. The validation function of the block translates user input
        to OPI compatible types, which is then returned.

        Example
        =======
        block_option: typing.Annotated[int, "scf", "maxiter"]

        In this case the metadata is ("scf", "maxiter"). The first value indicates the ORCA block the value belongs to,
        while the second value indicates which field from the Block class correlates to this block option.


        Parameters
        ----------
        field_name: str
            Name of the field, used for error messages only.
        value: Any
            User input value.
        metadata: tuple
            Tuple of metadata about the field.

        Returns
        -------
        Any
            User input value translated to OPI compatible types.

        """
        match metadata:
            case (validator,):
                # Case 1: Simple keyword — look up value as a member of the validator enum
                # Solvent is not resolved here; it is paired with SolvationModel later in _get_simple_keyword
                if isinstance(validator, type) and issubclass(validator, Solvent):
                    return value
                if not isinstance(validator, type) or not issubclass(validator, SimpleKeywordBox):
                    raise TypeError(f"Expected SimpleKeywordBox subclass, got {validator}")
                # Find simple keyword using the validator given
                return validator.find_keyword(value)

            case (validator, key):
                # Case 2: Block option — run value through Pydantic block validation to get the translated type
                if not isinstance(key, str):
                    raise TypeError(f"Expected str key, got {type(key)}")

                block_cls = Settings._get_block_class(field_name, validator)
                instance = block_cls.model_validate({key: value})
                return getattr(instance, str(key))

            case _:
                # No metadata: field needs no translation
                return value

    def _get_simple_keyword(
        self,
        validator: type[SimpleKeywordBox],
        value: str | SimpleKeyword | SolvationModelAndSolvent,
    ) -> SimpleKeyword:
        """
        Resolve a field value to a ``SimpleKeyword``.

        For ``SolvationModel`` fields the current ``solvent`` attribute is
        combined with the model to produce a ``SolvationModelAndSolvent``
        keyword; all other fields are looked up directly in their enum.

        Parameters
        ----------
        validator : type[SimpleKeywordBox]
            The enum class that owns the keyword (e.g. ``Dft``, ``BasisSet``).
        value : str or SimpleKeyword or SolvationModelAndSolvent
            Raw user-supplied value.

        Returns
        -------
        SimpleKeyword
            Resolved keyword ready to pass to ``Input.add_simple_keywords``.

        Raises
        ------
        ValueError
            If ``validator`` is ``SolvationModel`` but ``solvent`` is not set.
        TypeError
            If ``value`` is not a ``SolvationModelAndSolvent`` when required.
        """
        if validator == SolvationModel:
            # SolvationModel needs a solvent to form a compound keyword; read it from the Solvent field
            solvent_value = getattr(self, "solvent", None)
            if solvent_value is None:
                raise ValueError("A solvation model was requested without a solvent.")
            solvent = Solvent(Solvent.find_keyword(str(solvent_value)))
            if not isinstance(value, SolvationModelAndSolvent):
                raise TypeError("Wrong type for solvent or solvation model")

            # value is a SolvationModelAndSolvent callable; calling it with solvent produces the keyword
            new_keyword = value(solvent)
        elif isinstance(value, SimpleKeyword):
            # Field validation already resolved this to a SimpleKeyword; avoid re-deriving it,
            # since re-running find_keyword() bypasses subclass fallbacks (e.g. DftSettings'
            # dispersion-correction handling) and can reject an already-valid value.
            new_keyword = value
        else:
            # Fallback for values that were never resolved to a SimpleKeyword
            new_keyword = validator.find_keyword(value)

        return new_keyword

    @field_validator("*", mode="before")
    @classmethod
    def validate_fields(cls, value: Any, info: ValidationInfo) -> Any:
        """
        This field validator handles validation upon reassignment of values of class attributes.

        This validator is applied to all fields and is executed prior to Pydantics internal validation, which is useful
        for handling reassignment of values or custom preprocessing logic.

        The method does the following:
        1. Retrieves type hints, including metadata and checks whether current field has corresponding type hint.
        2. Extracts field specific metadata from type hint.
        3. Resolves incoming value using metadata.

        Parameters
        ----------
        value: Any
            User input value.
        info: ValidationInfo
            Object containing contextual information about field being validated.

        Returns
        -------
        Any
            User input value processed and converted to OPI compatible types.
        """
        if value is None:
            return value

        hints = typing.get_type_hints(cls, include_extras=True)

        if info.field_name not in hints:
            return value

        hint = hints[info.field_name]
        metadata = cls._get_field_metadata(hint)
        return cls._resolve_field_value(info.field_name, value, metadata)

    @model_validator(mode="after")
    def cross_validate(self) -> "Settings":
        """
        Function to process and validate user input, this validator handles validation upon model initialization. Since
        `self.validate_field()` already exists, this function will be reserved only for cross validation between fields.

        Returns
        -------
        Settings
            Cross-validated instance of `Settings` class

        """
        return self
