import os

from .base_yaml_schema import BaseYamlSchema


class BaseMeta(BaseYamlSchema):
    """
    BaseMeta class represents a base meta object with its fields, which are loaded from YAML
    file specified by data_path and validated using schema specified in meta_schema.yaml.
    """

    def __init__(self, data_path: str) -> None:
        """
        Initializes BaseMeta instance with schema and data file paths.

        Args:
        - data_path (str): path to the data file

        Returns: None
        """
        schema_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../schema/meta_schema.yaml")
        )
        super().__init__(schema_path, data_path)


class Meta(BaseMeta):
    """
    Meta class extends BaseMeta class and represents a meta object with its fields, which are
    loaded from YAML file specified by data_path and validated using schema specified in
    meta_schema.yaml.
    """

    def __init__(self, parent: object, data_path: str) -> None:
        """
        Initializes Meta instance with parent object and data file paths.

        Args:
        - parent (object): parent object
        - data_path (str): path to the data file

        Returns: None
        """
        self.parent = parent
        super().__init__(data_path)
