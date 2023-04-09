import os
from typing import Optional

from .base_yaml_schema import BaseYamlSchema


class BaseInfo(BaseYamlSchema):
    """
    BaseInfo class represents a base class for information with data loaded from YAML file.
    """

    def __init__(self, data_path: str) -> None:
        """
        Initializes BaseInfo instance with schema and data file paths.

        Args:
        - data_path (str): path to the data file

        Returns: None
        """
        schema_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../schema/info_schema.yaml")
        )
        super().__init__(schema_path, data_path)


class Info(BaseInfo):
    """
    Info class extends BaseInfo class and represents information with data loaded from YAML
    file.
    """

    def __init__(self, parent: Optional[object], data_path: str) -> None:
        """
        Initializes Info instance with parent object and data file path.

        Args:
        - parent (Optional[object]): parent object if any
        - data_path (str): path to the data file

        Returns: None
        """
        super().__init__(data_path)
        self.parent = parent
