import inspect
from pathlib import Path
from typing import Any, Set, get_args, get_origin

import pytest
from pydantic import BaseModel

from opi.output.core import Output
from opi.output.models.json.gbw.gbw_results import GbwResults
from opi.output.models.json.property.property_results import PropertyResults


class TestOutputAttributes:
    """
    Test suite for verifying completeness of Output attribute loading.

    This test class checks whether all attributes defined in `GbwResults` and `PropertyResults` models
    are correctly loaded when parsing JSON files. IT validates that the object structure matches
    the expected structure by comparing declared model attributes against the actually populated
    attributes from test data.

    The check is done by:
    1. Collecting all attributes from `GbwResults` and `PropertyResults`.
    2. Loading JSON test files to create `Output` objects.
    3. Tracking which attributes get populated.
    4. Asserting all expected attributes have been loaded at least once.

    """

    @pytest.mark.unit
    @pytest.mark.output
    def test_attributes(self, tmp_path: Path, json_dir: Path, json_file_list: list[Path]):
        """Test to check if all exisiting attributes in `Output` side get loaded into an `Output()` object.
        All output attributes are collected first and then through loading various json files , we remove
        attributes that load correctly.

        The test asserts at the end whether all attributes have been loaded correctly.

        Parameters
        ----------
        tmp_path : Path
            Temporary directory to save json files of the same basename to.
        """
        created = set()
        # set of attributes to ignore for now
        ignore = {
            "git",
            "efg_tensor",
            "GbwResults.orca_header.date",
            "PropertyResults.geometries.energy.root.totalnumofroots",
            "PropertyResults.geometries.vdw_correction.vdw_atomic",
            "PropertyResults.geometries.energy.root.numofmultiplicities",
            "PropertyResults.geometries.energy.root.corrdt",
            "PropertyResults.geometries.energy.root.casscfenergies",
            "PropertyResults.geometries.energy.root.corrst",
            "PropertyResults.geometries.energy.root.corrds",
            "GbwResults.molecule.td_dft.xy",
            "PropertyResults.geometries.energy.root.corrss",
        }
        # collect all attributes from GbwResults and PropertyResults
        gbw_attr = self.get_all_attributes(GbwResults, prefix="GbwResults")
        prop_attr = self.get_all_attributes(PropertyResults, prefix="PropertyResults")
        output_attr = {
            attr
            for attr in gbw_attr.union(prop_attr)
            if not any(ign.lower() in attr.lower() for ign in ignore)
        }
        for file in json_file_list:
            basename = file.stem
            basename = basename.split(".", 1)[0]

            if basename in created:
                continue

            created.add(basename)

            # create output object specific to given basename/task
            output_object = self.make_output_object(basename, json_file_list)
            # collect all loaded attributes
            object_prop_attr = self.collect_non_none_attrs(output_object.results_properties)
            object_gbw_attr = self.collect_non_none_attrs(output_object.results_gbw)

            object_attr = object_gbw_attr.union(object_prop_attr)
            # remove loaded attributes from set
            output_attr = output_attr - object_attr

            continue

        assert not output_attr

    def get_all_attributes(
        self, model: type[BaseModel], visited: Set[type] = None, prefix: str = ""
    ) -> Set[str]:
        """
        Recursively get all attribute names from a Pydantic model, including nested custom types.
        Attribute names include their parent class prefix (e.g., "A.attr1.attr2").

        Parameters
        ----------
        model: Type[BaseModel]
            The Pydantic model class to extract attributes from
        visited: Set
            Set of already visited types to avoid infinite recursion
        prefix: str
            Current prefix for nested attributes (e.g., "A.attr1.")

        Returns
        -------
        Set
            Set of all attribute names with parent prefixes (e.g., {"attr1", "A.attr1.attr2"})
        """
        if visited is None:
            visited = set()

        # Avoid infinite recursion for self-referential models
        if model in visited:
            return set()
        visited.add(model)

        attributes = set()

        # Iterate through all fields in the model
        for field_name, field_info in model.model_fields.items():
            # Add the field name with current prefix
            full_name = f"{prefix}.{field_name}" if prefix else field_name
            attributes.add(full_name)

            # Get the field type
            field_type = field_info.annotation

            # Create prefix for nested attributes - continue the chain
            nested_prefix = f"{prefix}.{field_name}" if prefix else f"{model.__name__}{field_name}"

            # Handle Optional, List, Dict, etc.
            origin = get_origin(field_type)
            if origin is not None:
                # For generic types, get the actual type arguments
                type_args = get_args(field_type)
                for arg in type_args:
                    # Recursively check if the type argument is a Pydantic model
                    if inspect.isclass(arg) and issubclass(arg, BaseModel):
                        nested_attrs = self.get_all_attributes(arg, visited.copy(), nested_prefix)
                        attributes.update(nested_attrs)
                    # Handle nested generics (e.g., List[Optional[Model]])
                    elif get_origin(arg) is not None:
                        inner_args = get_args(arg)
                        for inner_arg in inner_args:
                            if inspect.isclass(inner_arg) and issubclass(inner_arg, BaseModel):
                                nested_attrs = self.get_all_attributes(
                                    inner_arg, visited.copy(), nested_prefix
                                )
                                attributes.update(nested_attrs)
            # Handle direct Pydantic models
            elif inspect.isclass(field_type) and issubclass(field_type, BaseModel):
                nested_attrs = self.get_all_attributes(field_type, visited.copy(), nested_prefix)
                attributes.update(nested_attrs)

        return attributes

    def collect_non_none_attrs(
        self,
        obj: Any,
        *,
        depth: int = -1,
        prefix: str | None = None,
        _visited=None,
    ) -> Set[str]:
        """
        Collect a set of attribute paths whose values are not None.
        - Accepts a single object or a list of objects
        - Recursively traverses objects with __dict__

        Parameters
        ----------
        obj: Any
            Object to collect attributes from.
        depth: int
            Depth of recursion.
        prefix: str
            Optional prefix to add to attribute names.
        _visited: Set
            Set of already visited attributes to avoid infinite recursion

        Returns
        --------
        Set of all non-none attributes in the object

        """
        if obj is None or depth == 0:
            return set()

        if _visited is None:
            _visited = set()

        result = set()

        # ----------------------------
        # Case 1: top-level list input
        # ----------------------------
        if isinstance(obj, list):
            for item in obj:
                if item is None:
                    continue

                result |= self.collect_non_none_attrs(
                    item,
                    depth=depth,
                    prefix=prefix,
                    _visited=_visited,
                )
            return result

        # ----------------------------
        # Cycle detection
        # ----------------------------
        if id(obj) in _visited:
            return set()
        _visited.add(id(obj))

        # ----------------------------
        # Non-object primitives
        # ----------------------------
        if not hasattr(obj, "__dict__"):
            return set()

        base = prefix or obj.__class__.__name__

        for key, value in obj.__dict__.items():
            if value is None:
                continue

            path = f"{base}.{key}"
            result.add(path)

            # Nested object
            if hasattr(value, "__dict__"):
                result |= self.collect_non_none_attrs(
                    value,
                    depth=depth - 1 if depth > 0 else -1,
                    prefix=path,
                    _visited=_visited,
                )

            elif isinstance(value, list):
                for item in value:
                    if item is None:
                        continue

                    if hasattr(item, "__dict__"):
                        result |= self.collect_non_none_attrs(
                            item,
                            depth=depth - 1 if depth > 0 else -1,
                            prefix=path,
                            _visited=_visited,
                        )

            elif isinstance(value, dict):
                for item in value.values():
                    if item is None:
                        continue

                    if hasattr(item, "__dict__"):
                        result |= self.collect_non_none_attrs(
                            item,
                            depth=depth - 1 if depth > 0 else -1,
                            prefix=path,
                            _visited=_visited,
                        )

        return result

    def make_output_object(self, basename: str, json_file_list: list[Path]) -> Output:
        """
        Create output object and parse json files of a specific basename.

        Parameters
        ----------
        basename
            Name of json files to parse
        json_file_list
            List of json files to parse

        Returns
        -------
        Output
            Output object with parsed json files

        """
        # Look for basename.* in JSON_DIR
        json_files = [path for path in json_file_list if basename in path.name]

        # Separate GBW json and property json
        gbw_json = next(
            f for f in json_files if f.suffix == ".json" and not f.name.endswith(".property.json")
        )
        property_json = next(f for f in json_files if f.name.endswith(".property.json"))

        output_object = Output(
            basename=basename,
            version_check=False,
        )
        output_object.gbw_json_files = [gbw_json]
        output_object.property_json_file = property_json
        output_object.parse()

        return output_object
