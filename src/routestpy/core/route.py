import os
from typing import List

import requests
from pathlib import Path
from .application import Application
from .base_yaml_schema import BaseYamlSchema



class BaseRoute(BaseYamlSchema):
    """
    BaseRoute class represents a base route which has scenarios and response, loaded from YAML
    file specified by data_path.
    """

    def __init__(self, data_path: Path) -> None:
        """
        Initializes BaseRoute instance with schema and data file paths.

        Args:
        - data_path (Path): path to the data file

        Returns: None
        """
        schema_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../schema/route_schema.yaml")
        )
        super().__init__(schema_path, data_path)


class Route(BaseRoute):
    """
    Route class extends BaseRoute class and represents a route with its scenarios and response,
    which are loaded from YAML file specified by data_path.
    """

    def __init__(self, parent: Application, data_path: Path) -> None:
        """
        Initializes Route instance with parent Application and data file paths.

        Args:
        - parent (Application): parent application instance
        - data_path (Path): path to the data file

        Returns: None
        """
        from .scenario import Scenario
        
        self.parent: Application = parent
        self.scenarios: List[Scenario] = []
        self.response: requests.Response = None
        super().__init__(data_path)
        print(f"Loaded Route[{self.route['info']['name']}] successfully!!")

    @classmethod
    def new_route(cls, parent: Application, data_path: Path) -> "Route":
        """
        Creates a new Route instance and populates it with data from the given data dictionary.

        Args:
        - parent (Application): parent application instance
        - data_path (str): path to the data file

        Returns:
        - Route: new Route instance populated with data from the given data dictionary
        """
        return cls(parent, data_path)
