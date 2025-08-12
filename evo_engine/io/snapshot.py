
import json
from dataclasses import asdict, is_dataclass
from typing import Any

def _coerce(obj: Any):
    if is_dataclass(obj):
        return asdict(obj)
    if isinstance(obj, (list, tuple)):
        return [ _coerce(x) for x in obj ]
    if isinstance(obj, dict):
        return {k:_coerce(v) for k,v in obj.items()}
    return obj

def write_snapshot(snapshot, path: str) -> None:
    with open(path, "w") as f:
        json.dump(_coerce(snapshot), f, indent=2)

def read_snapshot(path: str):
    with open(path, "r") as f:
        return json.load(f)
