envelope_schema = {
  "type": "object",
  "required": ["msg_id","ts","issuer","type","scope","targets","ttl_ms","hysteresis_s","options","sig"],
  "properties": {
    "msg_id": {"type":"string"},
    "ts": {"type":"integer"},
    "issuer": {"type":"string"},
    "type": {"type":"string", "enum":["halt","resume","cancel_all","gear_set","gear_restore"]},
    "scope": {"type":"string"},
    "targets": {"type":"array","items":{"type":"string"}},
    "ttl_ms": {"type":"integer","minimum":1},
    "hysteresis_s": {"type":"integer","minimum":0},
    "options": {"type":"object"},
    "sig": {"type":"string"}
  },
  "additionalProperties": False
}
