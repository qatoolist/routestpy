import os
from pathlib import Path
from typing import List
from typing import Optional
import requests

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
        from .scenario import Scenario
        
        schema_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../schema/route_schema.yaml"))
        super().__init__(schema_path, data_path)
        self.response: Optional[requests.Response] = None
        self.scenarios: List[Scenario] = []



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

        super().__init__(data_path)
        self.parent: Application = parent

        parameter_types = ["headers", "path_variables", "query_params"]
        for param_type in parameter_types:
            target = self.route["parameters"][param_type]
            keys_set = set([d['key'] for d in target])
            missing_entries = [d for d in self.parent.app["parameters"][param_type] if d['key'] not in keys_set]
            target.extend(missing_entries)
            self.route["parameters"][param_type] = target

        # Copy missing meta properties from Parent app meta to the route meta
        target = self.route["meta"]
        for key, value in self.parent.app["meta"].items():
            if key not in target:
                target[key] = value
            elif isinstance(value, list):
                # Copy missing items from app to route
                target[key] = list(set(target[key] + value))

        self.route["meta"] = target

        # Copy missing hooks from Parent app hooks to the route hooks
        route_hooks = self.route["hooks"]
        for hook in self.parent.app["hooks"]:
            if hook not in route_hooks:
                route_hooks.append(hook)
        self.route["hooks"] = route_hooks

        
        for sc in self.route['scenarios']:
            s = Scenario.create_new_scenario(self, self.data_path.parent.joinpath(sc[2:]))
            self.scenarios.append(s)

    
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
