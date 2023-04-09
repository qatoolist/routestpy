import os

from dotenv import load_dotenv

from routestpy import Config


class DotEnvLoader:
    def load(self, file):
        load_dotenv(file)
        config_dict = os.environ
        return self._create_config(config_dict)

    def _create_config(self, config_dict):
        config = Config()
        for key, value in config_dict.items():
            setattr(config, key, value)
        return config
