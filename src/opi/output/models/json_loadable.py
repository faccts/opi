import json
from abc import ABC
from pathlib import Path
from typing import Any, Self

from opi.output.models.base.get_item import GetItem
from opi.utils.misc import dict_to_lower


class JSONLoadable(GetItem, ABC):
    """
    Superclass providing utility methods for loading objects from JSON data or files and for
    dumping them back into JSON data or files.
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

    def to_json(self, *, exclude_none: bool = True) -> dict[str, Any]:
        """
        Dump object into JSON data. Fields are dumped under the key they were read from.
        This is the inverse operation of `from_json()`.

        Only the gbw models declare ORCA's spelling of their keys (as `serialization_alias`), so
        that a dumped gbw-JSON file can be read by `orca_2json`. The property models are dumped
        under the lowercase keys that OPI reads them with, which ORCA does not accept.

        Parameters
        ----------
        exclude_none : bool, default: True
            Omit fields that are `None`.

        Returns
        -------
        dict[str,Any]
            JSON data of the object.
        """
        # > Dumping in JSON mode, so that the data is JSON-serializable
        return self.model_dump(mode="json", by_alias=True, exclude_none=exclude_none)

    def to_json_file(
        self,
        json_file: Path | str,
        /,
        *,
        indent: int | None = 2,
        exclude_none: bool = True,
    ) -> Path:
        """
        Dump object into a JSON file. This is the inverse operation of `from_json_file()`.

        Parameters
        ----------
        json_file: Path | str
            Path to the JSON file to be written.
        indent : int | None, default: 2
            Indentation of the JSON file. `None` writes the most compact representation.
        exclude_none : bool, default: True
            Omit fields that are `None`.

        Returns
        -------
        Path
            Path to the written JSON file.
        """
        json_file = Path(json_file)
        json_file.write_text(json.dumps(self.to_json(exclude_none=exclude_none), indent=indent))
        return json_file
