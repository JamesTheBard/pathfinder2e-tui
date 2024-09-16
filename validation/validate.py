import json
import yaml
from pathlib import Path

class Validator:

    def __init__(self, character_sheet: str | Path):
        self.character_sheet = Path(character_sheet)
        self.schema_file = Path("validation/schema.json")

    def validate(self):
        pass

    def load_data(self):
        self.schema = json.load(self.schema_file.read_text())
        self.data = yaml.safe_load(self.character_sheet)
