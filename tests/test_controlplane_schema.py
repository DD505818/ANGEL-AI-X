import json
from pathlib import Path

import pytest


def test_controlplane_schema_structure() -> None:
    schema_path = Path(__file__).resolve().parents[1] / "config" / "controlplane.schema.json"
    if not schema_path.exists():
        pytest.skip("controlplane.schema.json missing")
    with schema_path.open() as f:
        schema = json.load(f)

    assert schema["title"] == "ANGEL Control-Plane Envelope v1"
    assert set(schema["required"]) == {"msg_id", "ts", "issuer", "type", "ttl_ms", "sig"}
    actions = schema["properties"]["type"]["enum"]
    assert {"halt", "resume", "cancel_all"}.issubset(actions)
