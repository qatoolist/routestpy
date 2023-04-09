import toml

from routestpy.core.config import Config


class TomlLoader:
    def load(self, file):
        with open(file) as f:
            config_dict = toml.load(f)
            return self._create_config(config_dict)

    def _create_config(self, config_dict):
        config = Config()
        for key, value in config_dict.items():
            setattr(config, key, value)
        return config
