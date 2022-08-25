import yaml

config = None
file_path = "config.yaml"


def __init__(self):
    self.file_path = "config.yaml"
    self.config = None


# config should only need to be called once then can be retrieved by any file.
def get_config_all(self):
    if not self.config:
        init_config(self)

    return self.config


def get_config(self, section):
    if not self.config:
        init_config(self)

    return self.config.get(section)


def init_config(self):
    with open(self.file_path, "r") as f:
        self.config = yaml.safe_load(f)
