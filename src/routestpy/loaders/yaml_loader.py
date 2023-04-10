import yaml


class YamlLoader:
    def load(self, file):
        with open(file) as f:
            config_dict = yaml.safe_load(f)
            return config_dict
