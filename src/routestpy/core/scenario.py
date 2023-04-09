import os
from pathlib import Path

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
        self.body = None
        self.response = None
        super().__init__(data_path)

        parameter_types = ["headers", "path_variables", "query_params"]
        for param_type in parameter_types:
            target = self.scenario["parameters"][param_type]
            keys_set = {d['key'] for d in target}
            missing_entries = [d for d in self.parent.route["parameters"][param_type] if d['key'] not in keys_set]
            target.extend(missing_entries)

        # Copy missing meta properties from Parent app meta to the route meta
        target = self.scenario["meta"]
        for key in self.parent.route["meta"]:
            if key not in target:
                target[key] = self.parent.route["meta"][key]
            elif (
                key in self.parent.route["meta"] and key in target and isinstance(self.parent.route["meta"][key], list)
            ):
                # Copy missing items from app to route
                for item in self.parent.route["meta"][key]:
                    if item not in target[key]:
                        target[key].append(item)

        self.scenario["meta"] = target

        # Copy missing hooks from Parent app hooks to the route hooks
        target = self.scenario["hooks"]
        for hook in self.parent.route["hooks"]:
            if hook not in target:
                target.append(hook)
        self.scenario["hooks"] = target

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
