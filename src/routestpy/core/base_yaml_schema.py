import json
from pathlib import Path

import jsonschema
import yaml
from jsonschema.exceptions import ValidationError


class BaseYamlSchema:
    """
    A base class for loading YAML data and validating it against a schema.

    Attributes:
        schema_data (dict): The resolved schema data used for validating the data.
        schema (jsonschema.Draft7Validator): A JSONSchema validator object.
        data (dict): The YAML data object to be validated.
        resolved_data (dict): The resolved YAML data object with all `$ref` keys resolved.
    """

    def __init__(self, schema_path: Path, data_path: Path) -> None:
        """
        Initializes a BaseYamlSchema instance with a schema file path and a data file path.

        Args:
            schema_path (str): The path to the schema file.
            data_path (str): The path to the data file.

        Raises:
            ValueError: If the schema or data path is invalid.
        """

        schema_path = Path(schema_path)
        data_path = Path(data_path)
        self.data_path = data_path

        if not schema_path.exists():
            raise ValueError(f"Invalid schema path: {schema_path}")

        self.schema = self.load_schema(schema_path)
        self.is_valid_schema(self.schema)

        if not data_path.exists():
            raise ValueError(f"Invalid data path: {data_path}")

        self.data = self.load_data(data_path)
        self.is_valid_data(self.data, self.schema)

        # Add dynamic properties to the class based on the schema
        for prop, val in self.schema["properties"].items():
            setattr(self, prop, None)

        # Set property values from the data file
        for prop, val in self.data.items():
            if hasattr(self, prop):
                setattr(self, prop, val)

    def load_schema(self, schema_path: Path) -> dict:
        """
        Loads the schema from the given schema path and resolves all `$ref` keys.

        Args:
            schema_path (Path): The path to the schema file.

        Returns:
            dict: The resolved schema data.

        Raises:
            ValueError: If the schema is invalid.
        """
        with open(schema_path) as f:
            schema_data = yaml.safe_load(f)

        return self.resolve_schema_ref(schema_path.parent, schema_data)

    def load_data(self, data_path: Path) -> dict:
        """
        Loads the YAML data from the given data path and resolves all `$ref` keys.

        Args:
            data_path (Path): The path to the data file.

        Returns:
            dict: The YAML data object to be validated.
        """
        with open(data_path) as f:
            data = yaml.safe_load(f)

        return self.resolve_data_ref(data_path.parent, data)

    def resolve_schema_ref(self, base_path: Path, schema: dict) -> dict:
        """
        Recursively resolves all `$ref` keys in a JSON/YAML schema.

        Args:
            base_path (Path): The base path to resolve relative paths.
            schema (dict): The schema to resolve.

        Returns:
            dict: The resolved schema.

        Raises:
            ValueError: If the file extension of the `$ref` path is not supported.
        """
        if not isinstance(schema, dict):
            return schema
        for key, value in schema.items():
            if key == "$ref":
                ref_path = value
                if ref_path.startswith("./"):
                    ref_path = str(Path(base_path).joinpath(ref_path).resolve())
                with open(ref_path) as f:
                    if ref_path.endswith(".json"):
                        ref_schema = json.load(f)
                    elif ref_path.endswith(".yaml") or ref_path.endswith(".yml"):
                        ref_schema = yaml.safe_load(f)
                    else:
                        raise ValueError("Invalid file extension: " + ref_path)
                    return self.resolve_schema_ref(Path(ref_path).parent, ref_schema)
            elif isinstance(value, dict):
                schema[key] = self.resolve_schema_ref(base_path, value)
        return schema

    def resolve_data_ref(self, base_path: Path, data: dict) -> dict:
        """
        Recursively resolves all `$ref` keys in a JSON/YAML data.

        Args:
            base_path (Path): The base path to resolve relative paths.
            data (dict): The data to resolve.

        Returns:
            dict: The resolved data.

        Raises:
            ValueError: If the file extension of the `$ref` path is not supported.
        """
        if not isinstance(data, dict):
            return data
        for key, value in data.items():
            if key == "$ref":
                ref_path = value
                if ref_path.startswith("./"):
                    ref_path = str(Path(base_path).joinpath(ref_path).resolve())
                with open(ref_path) as f:
                    if ref_path.endswith(".json"):
                        ref_data = json.load(f)
                    elif ref_path.endswith(".yaml") or ref_path.endswith(".yml"):
                        ref_data = yaml.safe_load(f)
                    else:
                        raise ValueError("Invalid file extension: " + ref_path)
                    return self.resolve_data_ref(Path(ref_path).parent, ref_data)
            elif isinstance(value, dict):
                data[key] = self.resolve_data_ref(base_path, value)
        return data

    def is_valid_schema(self, schema_data: dict) -> bool:
        """
        Validates the stored data against the schema.

        Raises:
            ValueError: If the data is invalid.
        """
        # Validate the stored data against the schema
        validator = jsonschema.Draft7Validator(schema_data)
        try:
            validator.check_schema(schema_data)
            print("The schema is valid")
            return True
        except jsonschema.exceptions.SchemaError as e:
            print("The schema is invalid:", e)
            return False

    def is_valid_data(self, data: dict, schema: dict) -> bool:
        """
        Validates the stored data against the schema.

        Raises:
            ValueError: If the data is invalid.
        """
        # Validate the stored data against the schema
        try:
            jsonschema.validate(data, schema)
        except ValidationError as e:
            raise ValueError(f"Invalid data: {str(e)}")
