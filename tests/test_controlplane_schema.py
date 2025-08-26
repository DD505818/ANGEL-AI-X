import json
from pathlib import Path


def test_controlplane_schema_structure():
    schema_path = Path(__file__).resolve().parent.parent / "controlplane.schema.json"
    with schema_path.open() as f:
        schema = json.load(f)

    assert schema["title"] == "ANGEL Control Plane Command"
    assert set(schema["required"]) == {"version", "timestamp", "command", "signature"}
    actions = schema["properties"]["command"]["properties"]["action"]["enum"]
    assert {"HALT", "RESUME", "GEAR"}.issubset(actions)
