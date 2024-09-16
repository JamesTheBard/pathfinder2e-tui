import jsonschema.exceptions
from validation.validate import Validator
import jsonschema

if __name__ == "__main__":
    v = Validator("characters/info.yaml")
    try:
        v.validate()
    except jsonschema.exceptions.ValidationError as e:
        print(f"Validation Error at '{'/'.join(e.path)}': {e.message}")
        