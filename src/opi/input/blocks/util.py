from pathlib import Path
from typing import Self

from pydantic import BaseModel, ConfigDict, conlist

__all__ = ("InputString", "InputFilePath", "IntGroup", "NumList")


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


class IntGroup(BaseModel):
    """
    Class to format a collection of integers for the ORCA inp file

    Attributes
    ----------
    values : list[int | tuple[int, int]]
        Stores list of integers or pairs of integers
    """

    values: list[int | tuple[int, int]]

    def __str__(self) -> str:
        parts = []
        for v in self.values:
            # check if v is an integer and append to parts
            if isinstance(v, int):
                parts.append(str(v))
            else:
                # if v is not an integer it should be a range(e.g 1:10)
                # in this case we parse the string and save the lower and upper bounds as a tuple
                assert len(v) == 2
                parts.append(f"{v[0]}:{v[1]}")
        return f"{{ {' '.join(parts)} }}"

    @classmethod
    def init(cls, inp: str | list[int | tuple[int, int]] | list[int]) -> Self:
        """
        Initialize `IntGroup` from a string or list.

        Parameters
        ----------
        inp : str | list[int | tuple[int, int]]
            String format example: "{1 2 3:5 10}" or list of ints/tuples.
            Ranges like '4:10' are converted to (4, 10).
            Curly braces in strings are optional and stripped.

        Returns
        -------
        IntGroup
            An object of `IntGroup`.
        """
        if isinstance(inp, list):
            return cls(values=inp)
        else:
            # > Removing optional leading and trailing curly braces and redundant whitespaces for streamlined processing.
            cleaned_string = inp.strip().removeprefix("{").removesuffix("}").strip()

            # Handle empty set case
            if not cleaned_string:
                return cls(values=[])

            # Split by whitespace and convert to integers or tuples depending on format
            # parse the string for values which can either be integers or ranges (e.g 1:12)
            # in the case of ranges save the lower and upper limit as a tuple
            integers: list[int | tuple[int, int]] = []
            for item in cleaned_string.split():
                if ":" in item:
                    parts = item.split(":")
                    assert len(parts) == 2
                    startindex = int(parts[0])
                    endindex = int(parts[1])
                    if endindex < startindex:
                        raise ValueError(
                            f"Invalid range given, lower limit {startindex}, upper limit {endindex}"
                        )
                    integers.append((startindex, endindex))
                else:
                    integers.append(int(item))

            return cls(values=integers)
