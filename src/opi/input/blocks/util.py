from collections import UserDict
from functools import cache
from pathlib import Path
from types import UnionType
from typing import Annotated, Any, Literal, Self, Union, get_args, get_origin

from pydantic import BaseModel, ConfigDict, conlist, model_validator

__all__ = (
    "CaseInsensitiveLiteralModel",
    "InputString",
    "InputFilePath",
    "NumList",
    "NoCaseDict",
)


def _collect_literal_strings(annotation: Any) -> list[str]:
    """
    Collect the string values of all `Literal`s in a type annotation.

    Descends into unions and `Annotated`, but not into containers such as `list`,
    as only a plain string value is matched against the `Literal`s.

    Parameters
    ----------
    annotation : Any
        Type annotation of a pydantic field.

    Returns
    -------
    list[str]
        The string values of the `Literal`s found, in order of appearance.
    """
    origin = get_origin(annotation)
    if origin is Literal:
        return [arg for arg in get_args(annotation) if isinstance(arg, str)]
    if origin is Annotated:
        return _collect_literal_strings(get_args(annotation)[0])
    if origin is Union or origin is UnionType:
        return [value for arg in get_args(annotation) for value in _collect_literal_strings(arg)]
    return []


@cache
def _literal_lookup(model: type[BaseModel], field_name: str) -> dict[str, str]:
    """
    Map the lowercased `Literal` string values of a model field onto their exact spelling.

    Parameters
    ----------
    model : type[BaseModel]
        Model class that defines the field.
    field_name : str
        Name of the field.

    Returns
    -------
    dict[str, str]
        Lowercased `Literal` value mapped onto the `Literal` value as defined.
    """
    field = model.model_fields.get(field_name)
    if field is None:
        return {}
    return {value.lower(): value for value in _collect_literal_strings(field.annotation)}


class CaseInsensitiveLiteralModel(BaseModel):
    """
    Base model whose `Literal` fields accept string values in any casing, as ORCA does.

    A string given for a field whose annotation contains a `Literal` is mapped
    case-insensitively onto the matching `Literal` value, e.g. "Direct" onto "direct".
    Strings that match no `Literal` value are passed on unchanged, so that pydantic
    validates them against the rest of the annotation.

    The mapping is done by a model validator, so that it precedes all field validators,
    including the field-specific "before" validators of subclasses.
    """

    @model_validator(mode="before")
    @classmethod
    def normalize_literal_case(cls, data: Any) -> Any:
        """
        Map string values case-insensitively onto the matching `Literal` value of their field.

        Parameters
        ----------
        data : Any
            Input data of the model, usually a dict mapping field names onto values.

        Returns
        -------
        Any
            `data` with every string value replaced by its matching `Literal` value, if any.
        """
        if not isinstance(data, dict):
            return data
        normalized = dict(data)
        for field_name, value in data.items():
            if isinstance(field_name, str) and isinstance(value, str):
                lookup = _literal_lookup(cls, field_name)
                normalized[field_name] = lookup.get(value.lower(), value)
        return normalized


class InputFilePath(BaseModel):
    """
    Class to model file paths inside block inputs. Main purpose is to override str function.

    Attributes
    ----------
    file: Path
        Path to the file of type `Path`.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)
    file: Path

    def __str__(self) -> str:
        return '"' + str(self.file) + '"'

    @classmethod
    def from_string(cls, path: str) -> Self:
        """
        Parameters
        ----------
        path : str
        """
        return cls(file=Path(path))


class InputString(BaseModel):
    """
    Class to model strings inside block inputs. Main purpose is to override the str function.

    Attributes
    ----------
    string: str
        String to be stored.
    """

    string: str

    def __str__(self) -> str:
        return f'"{self.string}"'


class NumList(BaseModel):
    """
    Class to format integer or float lists for orca inp files

    Attributes
    ----------
    numlist : list[int] | list[float]
        Stores list of integers or floats
    """

    numlist: conlist(int) | conlist(float)  # type: ignore

    def __init__(self, numlist: list[int] | list[float]) -> None:
        super().__init__(numlist=numlist)

    def __str__(self) -> str:
        return ",".join(map(str, self.numlist))

    @classmethod
    def from_string(cls, inp: str) -> "NumList":
        """
        Converts a string of comma separated values into `NumList` instance.

        Parameters
        ----------
        inp : str
        """
        if not inp or inp.strip() == "":
            return NumList([])

        # Split and clean the string
        items = [item.strip() for item in inp.split(",") if item.strip()]

        if not items:
            return NumList([])

        # Check if any item contains a decimal point or needs float conversion
        needs_float = False
        parsed_values: list[int | float] = []

        for item in items:
            try:
                # Try to convert to float first
                float_val = float(item)

                # Check if it's actually an integer
                if float_val.is_integer() and "." not in item:
                    parsed_values.append(int(float_val))
                else:
                    parsed_values.append(float_val)
                    needs_float = True

            except ValueError:
                raise ValueError(f"Cannot convert '{item}' to a number")

        # If any float was found, convert all to float
        if needs_float:
            return NumList([float(val) for val in parsed_values])
        else:
            return NumList(parsed_values)


class NoCaseDict(UserDict[str, str]):
    """
    A dictionary whose keys are case-insensitive.
    This only applies for string-like keys.
    """

    def __getitem__(self, key: str) -> str:
        """
        Retrieve a value from the dictionary.

        Parameters
        ----------
        key: str
            Key of entry to be fetched.

        Returns
        -------
        str
            Value of entry.

        Raises
        ------
        TypeError
            If the key is not a string.

        KeyError
            If attribute with given name does not exist.

        """
        if not isinstance(key, str):
            raise TypeError(f"Key must be of type string, got {type(key)}")
        key = self._norm_key(key)
        return self.data[key]

    def __setitem__(self, key: str, value: str) -> None:
        """
        Set a value in the dictionary.

        Parameters
        ----------
        key: str
            Key of entry
        value: str
            Value of entry to be set

        Raises
        -------
        TypeError
            If key or value is not a string.

        """
        if not isinstance(key, str):
            raise TypeError(f"Key must be of type string, got {type(key)}")
        if not isinstance(value, str):
            raise TypeError(f"Value must be of type string, got {type(value)}")
        key = self._norm_key(key)
        self.data[key] = value

    def __delitem__(self, key: str) -> None:
        """
        Delete an item from the dictionary.

        Parameters
        ----------
        key: str
        Name of entry to be deleted.

        Returns
        -------
        None

        Raises
        -------
        KeyError
            If key does not exist in dictionary.

        TypeError
            If the key is not a string.

        """
        if not isinstance(key, str):
            raise TypeError(f"Key must be of type string, got {type(key)}")
        key = self._norm_key(key)
        del self.data[key]

    def __contains__(self, key: Any) -> bool:
        """
        Check if a key exists in the dictionary.

        Parameters
        ----------
        key: Any
            Key of entry

        Returns
        -------
        bool
            True if key exists in the dictionary. False otherwise.

        Raises
        ------
        TypeError
            If the key is not a string.

        """
        if not isinstance(key, str):
            raise TypeError(f"Key must be of type string, got {type(key)}")
        key = self._norm_key(key)
        return key in self.data

    def _norm_key(self, key: str, /) -> str:
        """
        Normalize key to lower case.

        Parameters
        ----------
        key: str
            Key of entry

        Returns
        -------
        str
            Normalized key.

        """
        return key.lower().strip()
