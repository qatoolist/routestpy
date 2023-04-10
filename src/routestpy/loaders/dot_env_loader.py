import os

from dotenv import load_dotenv


class DotEnvLoader:
    def load(self, file):
        load_dotenv(file)
        config_dict = os.environ
        return config_dict
