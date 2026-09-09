import re
import typing
import warnings
from abc import ABC
from types import UnionType
from typing import Any, ClassVar, get_args, get_origin

from pydantic import BaseModel, ValidationError, ValidationInfo, model_validator
from pydantic.functional_validators import ModelWrapValidatorHandler


def get_clean_type_name(t: Any) -> str:
    """Get the type name of an object and returns it as a string."""
    # > Get the unsubscripted version of the type
    origin = get_origin(t)
    # > If the type is a Union we have to dissect it
    # > typically it will be Union[Something | None] so we do not want the None part
    if origin is UnionType:
        # > Generate a list of the types in the Union
        args = [a for a in get_args(t) if a is not type(None)]
        # > recursively call the function on the first argument
        return get_clean_type_name(args[0]) if args else "None"
    # > If the single type has a name we return it
    elif hasattr(t, "__name__"):
        return str(t.__name__)
    # > If no name is available we converty the type to a string
    # > and try to make the output pretty (only print the class name)
    else:
        matches = re.findall(r"\.([^.|\]\s]+)", str(t))
        result = matches[-1] if matches else str(t).split("|")[0].strip()
        return result


class GetItem(BaseModel, ABC):
    """
    This class contains the `get_item` function and is the ABC of the output model classes.

    Attributes
    -----------
    strict: bool, default = True
        Default boolean if no explicit context is given. If True, pydantic validation will raise a `ValidationError`,
        if False, the field which caused the validation to fail will be dropped and return to the default Value, which
        is typically `None`.
    """

    strict: ClassVar[bool] = (
        True  # > Annotated but with ClassVar so that it is not treated as a Pydantic field
    )

    @model_validator(mode="wrap")
    @classmethod
    def _drop_invalid_fields(
        cls,
        data: Any,
        handler: ModelWrapValidatorHandler["GetItem"],
        info: ValidationInfo,
    ) -> "GetItem":
        # > First try to run core Pydantic validation
        try:
            return handler(data)
        except ValidationError as e:
            # > In strict mode (the default) we don't recover - just raise
            if (info.context or {}).get("strict", cls.strict):
                raise
            # > data to validate should always be a dict since we load it from JSON - defensive check
            if not isinstance(data, dict):
                raise
            # > Identify the top-level fields that triggered the ValidationError
            bad_keys = {str(error["loc"][0]) for error in e.errors() if error["loc"]}
            # > Nothing actionable to drop - re-raise the original error
            if not bad_keys:
                raise
            # > Rebuild the input without the offending fields - each dropped field
            # > falls back to its own default on revalidation - typically None
            cleaned = {k: v for k, v in data.items() if str(k) not in bad_keys}
            # > Revalidate - this re-raises if a dropped field was actually required
            result = handler(cleaned)
            # > Let the caller know which fields were dropped
            warnings.warn(f"{cls.__name__}: dropped fields due to validation errors: {bad_keys}")
            return result

    def __getitem__(self, name: str) -> Any:
        return getattr(self, name.lower())

    def graph(self, depth: int = -1, level: int = 0, /, *, max_list_length: int = 5) -> str:
        """
        Graph output for populated models (derived classes of GetItem). Loops over all attributes and returns their names
        together with their types as string. If an attribute is a derived class of GetItem, this function is called
        recursively on it with increased `level` resulting in increased indentation.

        Parameters
        ----------
        depth : int, default = -1
            Integer to determine the depth to which the graph should be shown. With the default -1 the depth is without
            limit.
        level : int, default = 0
            Level of indentation, increases with recursive calls. Default is the starting indentation (no indentation).
        max_list_length : int, default = 5
            Maximum number of items to show from lists in the graph (since most of the lists in the output contain repetitive
            elements)

        Returns
        ----------
        str
            Graph output for populated models (derived classes of GetItem) as formatted string.
        """
        # > if depth reaches zero empty string is returned
        if depth == 0:
            return ""

        # > determine the indentation to use from current level
        indent = "  " * level
        lines = []
        # > get type hints for current model
        hints = typing.get_type_hints(type(self))

        # > loop over all attributes of current model
        for key, value in self.__dict__.items():
            # > if the attribute is None we report that
            if value is None:
                lines.append(f"{indent}- {key} (None)")
                continue

            hint = hints.get(key, type(value))
            typename = get_clean_type_name(hint)
            header = f"{indent}- {key} ({typename})"

            # Nested GetItem
            if isinstance(value, GetItem):
                lines.append(header)
                lines.append(value.graph(depth - 1 if depth > 0 else -1, level + 1))

            # List of GetItem
            elif isinstance(value, list):
                sublines = []
                counter = 0
                for i, item in enumerate(value):
                    if isinstance(item, GetItem):
                        sublines.append(f"{indent}  - [{i}]")
                        counter += 1
                        sublines.append(item.graph(depth - 1 if depth > 0 else -1, level + 2))
                        if counter > max_list_length:
                            sublines.append(f"{indent}  - ...\n")
                            break
                lines.append(header)
                lines.extend(sublines)

            # Dict of GetItem
            elif isinstance(value, dict):
                sublines = []
                for k, item in value.items():
                    if isinstance(item, GetItem):
                        sublines.append(f"{indent}  - [{k}]")
                        sublines.append(item.graph(depth - 1 if depth > 0 else -1, level + 2))
                if sublines:
                    lines.append(header)
                    lines.extend(sublines)

            # Primitive (but not None) – just add the key name
            else:
                lines.append(header)

        return "\n".join(lines)

    def __eq__(self, other: Any) -> bool:
        """
        For GetItems to be equal they must have the same attributes with exactly the same values.
        """
        if type(self) is not type(other):
            return False
        return bool(self.__dict__ == other.__dict__)
