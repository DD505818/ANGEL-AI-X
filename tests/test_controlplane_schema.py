import json
from pathlib import Path

import pytest


def test_controlplane_schema_structure() -> None:
    """Validate the control-plane command schema."""
    schema_path = (
        Path(__file__).resolve().parent.parent / "config" / "controlplane.schema.json"
    )

    if not schema_path.is_file():
        pytest.skip("control-plane schema missing; skipping structure test")

    with schema_path.open() as f:
        schema = json.load(f)

    assert schema["title"] == "ANGEL Control-Plane Envelope v1"

    required_fields = {"msg_id", "ts", "issuer", "type", "ttl_ms", "sig"}
    assert required_fields.issubset(set(schema["required"]))

    actions = set(schema["properties"]["type"]["enum"])
    assert {"halt", "resume", "gear_set"}.issubset(actions)
