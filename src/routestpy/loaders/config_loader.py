import glob
import os
from pathlib import Path
from types import SimpleNamespace

from routestpy import DotEnvLoader
from routestpy import JsonLoader
from routestpy import TomlLoader
from routestpy import YamlLoader


class ConfigLoader:
    def __init__(self, env=None):
        if env is None:
            env = os.getenv("ENV_VAR_NAME", default="prod")
        self.env = env
        self.config_path = Path.cwd() / "config"

    def load(self) -> SimpleNamespace:
        files = glob.glob(os.path.join(self.config_path, f"{self.env}.*"))
        if len(files) != 1:
            raise Exception(f"Invalid number of config files for {self.env} environment")

        file = files[0]
        extension = file.split(".")[-1]

        if extension == "json":
            loader = JsonLoader()
        elif extension == "yaml":
            loader = YamlLoader()
        elif extension == "toml":
            loader = TomlLoader()
        elif extension == "env":
            loader = DotEnvLoader()
        else:
            raise Exception(f"Invalid config file format: {extension}")

        return self.convert_dict_to_namespace(loader.load(file))

    def convert_dict_to_namespace(self, d):
        """
        Recursively converts all nested dictionaries to SimpleNamespace objects.
        """
        if isinstance(d, dict):
            for key, value in d.items():
                d[key] = self.convert_dict_to_namespace(value)
            return SimpleNamespace(**d)
        elif isinstance(d, list):
            return [self.convert_dict_to_namespace(item) for item in d]
        else:
            return d
