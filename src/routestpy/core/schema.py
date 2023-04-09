from pathlib import Path
from typing import Any

import jsonschema
import pykwalify.core
import yaml
from jsonschema import validators
from jsonschema.exceptions import ValidationError


class BaseBodySchema:
    """
    BaseBodySchema class represents a base schema for HTTP request and response bodies.
    """

    def __init__(self, schema_path: Path) -> None:
        """
        Initializes BaseBodySchema instance with schema file path.

        Args:
        - schema_path (str): path to the schema file

        Returns: None
        """
        if not isinstance(schema_path, Path):
            raise TypeError("schema_path must be a Path")

        if not schema_path.exists():
            raise ValueError("schema_path is not a valid file path or URL")

        # Load the schema from a file or URL
        try:
            with open(schema_path) as f:
                schema_data = yaml.safe_load(f)
        except (FileNotFoundError, OSError):
            raise ValueError("Failed to load schema file")

        # Validate the schema
        try:
            pykwalify.core.Core(source_data=schema_data, schema_data=schema_data).validate()
        except pykwalify.errors.SchemaError as e:
            raise ValueError(f"Invalid schema: {e}")

        resolver = jsonschema.RefResolver(base_uri=schema_path, referrer=schema_data)
        self.schema = jsonschema.validators.extend(
            validators.Draft7Validator,
            validators=[jsonschema.validators.RefResolver(self.schema, resolver=resolver)],
        )
        self.data_path: Path = None
        self.data: Any = {}

        # Add dynamic properties to the class based on the schema
        for prop, val in self.schema.schema["properties"].items():
            setattr(self, prop, None)

    @property
    def data_path(self) -> Path:
        return self._data_path

    @data_path.setter
    def data_path(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("data_path must be a string")
        path = Path(value)
        if not path.exists():
            raise ValueError("data_path is not a valid file path or URL")

        # Load the data from a file or URL
        try:
            with open(value) as f:
                self.data = yaml.safe_load(f)
        except (FileNotFoundError, OSError):
            raise ValueError("Failed to load data file")

        # Validate the data against the schema
        try:
            self.schema.validate(self.data)
        except jsonschema.exceptions.ValidationError:
            raise ValueError("Data file does not match schema")

        # Set property values from the data file
        for prop, val in self.data.items():
            if hasattr(self, prop):
                setattr(self, prop, val)

        self._data_path = value

    def validate(self) -> None:
        """
        Validates the stored data against the schema.

        Args: None

        Returns: None
        """
        # Validate the stored data against the schema
        try:
            self.schema.validate(self.data)
        except ValidationError as e:
            raise ValueError(str(e))


class BodySchema(BaseBodySchema):
    """
    BodySchema class extends BaseBodySchema class and represents a schema for HTTP request and response bodies.
    """
