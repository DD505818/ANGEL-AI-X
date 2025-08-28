import json
from pathlib import Path


def test_controlplane_schema_structure():
    schema_path = (
        Path(__file__).resolve().parent.parent / "config" / "controlplane.schema.json"
    )
    with schema_path.open() as f:
        schema = json.load(f)

    assert schema["title"] == "ANGEL Control-Plane Envelope v1"
    assert set(schema["required"]) == {
        "msg_id",
        "ts",
        "issuer",
        "type",
        "ttl_ms",
        "sig",
    }
    actions = schema["properties"]["type"]["enum"]
    assert {"halt", "resume", "gear_set"}.issubset(actions)
