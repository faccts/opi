import json
from abc import ABC
from pathlib import Path
from typing import Any, Self

from opi.output.models.base.get_item import GetItem
from opi.utils.misc import dict_to_lower


class JSONLoadable(GetItem, ABC):
    """
    Superclass providing utility methods for loading objects from JSON data or files.
    """

    @classmethod
    def from_json(cls, json_data: dict[str, Any]) -> Self:
        """
        Create object from JSON data

        Parameters
        ----------
        json_data : dict[str,Any]
            JSON data

        Returns
        -------
        JSONLoadable
            Object created from JSON data

        Raises
        ------
        TypeError
            If the JSON data is not a dictionary.

        """
        data = dict_to_lower(json_data)
        if not isinstance(data, dict):
            raise TypeError("Data is not a dictionary")

        return cls(**data)

    @classmethod
    def from_json_file(cls, json_file: Path | str) -> Self:
        """
        Creates an object from a JSON file.

        Parameters
        ----------
        json_file: Path | str
            Path to the JSON file

        Returns
        -------
        JSONLoadable
            Object created from JSON file

        Raises
        ------
        TypeError
            Raised if `dict_to_lower()` does not return a dictionary.
        ValueError
            Raised if the JSON data is invalid.
        FileNotFoundError
            Raised if `json_file` does not point to a file.

        """
        if isinstance(json_file, str):
            json_file = Path(json_file)
        try:
            with open(json_file, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"File {json_file} not found")
        except json.decoder.JSONDecodeError:
            raise ValueError(f"Invalid JSON: {json_file}")

        return cls.from_json(data)
