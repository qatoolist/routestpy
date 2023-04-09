import os
from typing import Any
from typing import Dict
from typing import List
from pathlib import Path
from .base_yaml_schema import BaseYamlSchema
from typing import List

class BaseApplication(BaseYamlSchema):
    """
    BaseApplication class represents a base application with its routes, environment,
    host, config, params, hooks, and register, which are loaded from a YAML file
    specified by data_path.
    """

    def __init__(self, app_yaml_path: str) -> None:
        """
        Initializes BaseApplication instance with schema and data file paths.

        Args:
        - data_path (str): Path to the data file.

        Returns: None
        """
        from .route import Route
        
        schema_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../schema/app_schema.yaml")
        )
        print(f"App Schema Path : {schema_path}")
        self.routes: List[Route] = []
        self.environment: str = ""  # Represents the environment of the application.
        self.host: str = ""  # Represents the host on which the application is running.
        self.config: Dict[
            str, Any
        ] = {}  # Represents the configuration parameters of the application.
        self.params: Dict[str, Any] = {}  # Represents the input parameters of the application.
        self.hooks: Dict[str, Any] = {}  # Represents the hooks of the application.
        self.register: Dict[
            str, Any
        ] = {}  # Represents the registered components of the application.
        super().__init__(schema_path, app_yaml_path)

    def find_routes(self, base_path: Path) -> List[Path]:
        """
        Scans all the directories within base_path and returns a list of directories
        whose name ends with "_route" and contain at least one "route.yaml" file.

        Args:
            base_path (Path): The base path to scan for routes.

        Returns:
            List[str]: A list of directory paths that are valid routes.
        """
        routes = []
        for dir_path in base_path.iterdir():
            if dir_path.is_dir() and dir_path.name.endswith("_route"):
                # Check if the directory contains a route.yaml file
                route_yaml = dir_path.joinpath("route.yaml")
                if not route_yaml.exists():
                    continue
                routes.append(dir_path)
        return routes


class Application(BaseApplication):
    """
    Application class extends BaseApplication class and represents an application with its
    routes, environment, host, config, params, hooks, and register, which are loaded from a YAML
    file specified by data_path.
    """ 

    def __init__(self, project_path: Path) -> None:
        """
        Initializes Application instance with data file paths.

        Args:
        - data_path (Path): Path to the data file.

        Returns: None
        """
        from .route import Route
        
        APP_YAML_PATH = project_path.joinpath('app', 'app.yaml')
        super().__init__(APP_YAML_PATH)
        self.project_path = Path(project_path)
        self.app_yaml_path = Path(APP_YAML_PATH)
        self.app_routes_path = self.project_path.joinpath('routes')
        
        print(f"Project Path : {self.project_path}")
        print(f"App yaml Path : {self.app_yaml_path}")
        print(f"Routes Path : {self.app_routes_path}")
        routes_list = self.find_routes(self.app_routes_path)
        
        for route_path in routes_list:
            route_yaml = route_path.joinpath('route.yaml')
            self.routes.append(Route.new_route(self, route_yaml))
        
        print(f"App name {self.app['name']}")
        print(f"Available Routes {routes_list}")


    @classmethod
    def create_application(cls, project_path: str) -> "Application":
        """
        Creates an Application instance with the specified data file.

        Args:
        - data_path (str): Path to the data file.

        Returns:
        An Application instance.
        """
        return cls(Path(project_path))
