from pathlib import Path
import yaml


class Settings:
    def __init__(self, path: Path):
        with open(path) as f:
            self.raw = yaml.safe_load(f)

    def __getitem__(self, item):
        return self.raw[item]
