import glob
import os

from routestpy import DotEnvLoader
from routestpy import JsonLoader
from routestpy import TomlLoader
from routestpy import YamlLoader


class ConfigLoader:
    def __init__(self, env):
        self.env = env
        self.config_path = os.path.join(os.getcwd(), "config")

    def load(self):
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

        return loader.load(file)
