import toml


class TomlLoader:
    def load(self, file) -> dict:
        with open(file) as f:
            config_dict = toml.load(f)
            return config_dict
