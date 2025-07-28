from typing import Any

from pydantic import BaseModel


class GetItem(BaseModel):
    """This class contains the get_item function for nearly all other classes"""

    def __getitem__(self, name: str) -> Any:
        return getattr(self, name.lower())

    def graph(self, depth: int = -1, _level: int = 0) -> str:
        """ "Graph output of the populated data types"""
        if depth == 0:
            return ""

        indent = "  " * _level
        lines = []

        for key, value in self.__dict__.items():
            if value is None:
                continue

            # Nested GetItem
            if isinstance(value, GetItem):
                lines.append(f"{indent}- {key}")
                lines.append(value.graph(depth - 1 if depth > 0 else -1, _level + 1))

            # List of GetItem
            elif isinstance(value, list):
                sublines = []
                for i, item in enumerate(value):
                    if isinstance(item, GetItem):
                        sublines.append(f"{indent}  - [{i}]")
                        sublines.append(item.graph(depth - 1 if depth > 0 else -1, _level + 2))
                if sublines:
                    lines.append(f"{indent}- {key}")
                    lines.extend(sublines)

            # Dict of GetItem
            elif isinstance(value, dict):
                sublines = []
                for k, item in value.items():
                    if isinstance(item, GetItem):
                        sublines.append(f"{indent}  - [{k}]")
                        sublines.append(item.graph(depth - 1 if depth > 0 else -1, _level + 2))
                if sublines:
                    lines.append(f"{indent}- {key}")
                    lines.extend(sublines)

            # Primitive (but not None) – just print the key name
            else:
                lines.append(f"{indent}- {key}")

        return "\n".join(lines)
