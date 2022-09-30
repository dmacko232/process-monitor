from typing import List, Tuple
import json
import os

def save_json(data: List[Tuple[float, int, int]], out_path: str) -> None:
    """Saves data to json. If path doesnt exist throws exception."""

    out_dirname = os.path.dirname(out_path)
    if out_dirname: # dont create in case its empty string
        os.makedirs(os.path.dirname(out_path), exist_ok=True) # create dir if needed
    with open(out_path, "w") as out_handle:
        json.dump(data, out_handle, indent=2)
