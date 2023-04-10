import json


class JsonLoader:
    def load(self, file) -> dict:
        with open(file) as f:
            config_dict = json.load(f)
            return config_dict
