import re
import typing
from typing import Any, Union, get_args, get_origin

from pydantic import BaseModel


def get_clean_type_name(t: Any) -> str:
    origin = get_origin(t)
    if origin is Union:
        args = [a for a in get_args(t) if a is not type(None)]
        return get_clean_type_name(args[0]) if args else "None"
    elif hasattr(t, "__name__"):
        return str(t.__name__)
    else:
        matches = re.findall(r"\.([^.|\]\s]+)", str(t))
        result = matches[-1] if matches else str(t)
        return result


class GetItem(BaseModel):
    """This class contains the get_item function for nearly all other classes"""

    def __getitem__(self, name: str) -> Any:
        return getattr(self, name.lower())

    def graph(self, depth: int = -1, _level: int = 0, /, *, max_list_length: int = 5) -> str:
        """ "Graph output of the populated data types"""
        if depth == 0:
            return ""

        indent = "  " * _level
        lines = []
        hints = typing.get_type_hints(type(self))

        for key, value in self.__dict__.items():
            if value is None:
                continue

            hint = hints.get(key, type(value))
            typename = get_clean_type_name(hint)
            header = f"{indent}- {key} ({typename})"

            # Nested GetItem
            if isinstance(value, GetItem):
                lines.append(header)
                lines.append(value.graph(depth - 1 if depth > 0 else -1, _level + 1))

            # List of GetItem
            elif isinstance(value, list):
                sublines = []
                for i, item in enumerate(value):
                    if isinstance(item, GetItem):
                        sublines.append(f"{indent}  - [{i}]")
                        sublines.append(item.graph(depth - 1 if depth > 0 else -1, _level + 2))
                        if len(sublines) > max_list_length:
                            sublines.append(f"{indent}  - ...\n")
                            break
                if sublines:
                    lines.append(header)
                    lines.extend(sublines)

            # Dict of GetItem
            elif isinstance(value, dict):
                sublines = []
                for k, item in value.items():
                    if isinstance(item, GetItem):
                        sublines.append(f"{indent}  - [{k}]")
                        sublines.append(item.graph(depth - 1 if depth > 0 else -1, _level + 2))
                if sublines:
                    lines.append(header)
                    lines.extend(sublines)

            # Primitive (but not None) – just print the key name
            else:
                lines.append(header)

        return "\n".join(lines)
