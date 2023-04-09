import os
from pathlib import Path
from typing import Optional

import requests

from .base_yaml_schema import BaseYamlSchema
from .route import Route


class BaseScenario(BaseYamlSchema):
    """
    BaseScenario class represents a scenario with its request body, response, and other
    metadata loaded from a YAML file.
    """

    def __init__(self, data_path: Path) -> None:
        """
        Initializes BaseScenario instance with schema and data file paths.

        Args:
        - data_path (str): path to the data file

        Returns: None
        """
        schema_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../schema/scenario_schema.yaml"))
        super().__init__(schema_path, data_path)


class Scenario(BaseScenario):
    """
    Scenario class extends BaseScenario class and represents a scenario with its
    request body, response, and other metadata loaded from a YAML file.
    """

    def __init__(self, parent: Route, data_path: Path) -> None:
        """
        Initializes Scenario instance with parent route and data file paths.

        Args:
        - parent (Route): parent route instance
        - data_path (str): path to the data file

        Returns: None
        """
        self.parent = parent
        self.body: Optional[dict] = None
        self.response: Optional[requests.Response] = None
        super().__init__(data_path)

    @classmethod
    def create_new_scenario(cls, parent: Route, data_path: Path) -> "Scenario":
        """
        Creates a new Scenario instance with parent route and data file paths.

        Args:
        - parent (Route): parent route instance
        - data_path (str): path to the data file

        Returns:
        - scenario (Scenario): a new instance of the Scenario class
        """
        return cls(parent=parent, data_path=data_path)
