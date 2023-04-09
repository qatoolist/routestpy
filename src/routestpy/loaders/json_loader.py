import json

from routestpy.core.config import Config


class JsonLoader:
    def load(self, file):
        with open(file) as f:
            config_dict = json.load(f)
            return self._create_config(config_dict)

    def _create_config(self, config_dict):
        config = Config()
        for key, value in config_dict.items():
            setattr(config, key, value)
        return config
