from backend.oms.idempotency import make_client_key, new_uuid_key


def test_make_client_key_deterministic():
    k1 = make_client_key("BTCUSD", "BUY", 1.0, 20000.0, 123456)
    k2 = make_client_key("BTCUSD", "BUY", 1.0, 20000.0, 123456)
    assert k1 == k2


def test_new_uuid_key_prefix():
    key = new_uuid_key()
    assert key.startswith("ANGEL:")
