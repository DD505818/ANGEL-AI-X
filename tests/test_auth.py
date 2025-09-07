"""Tests for JWT authentication and IP allowlist."""
import os
import jwt
from fastapi.testclient import TestClient

os.environ["JWT_SECRET"] = "secret"
os.environ["IP_ALLOWLIST"] = "testclient"

import main

client = TestClient(main.app)

def _token() -> str:
    return jwt.encode({"sub": "tester"}, os.environ["JWT_SECRET"], algorithm="HS256")

def test_authenticated_request() -> None:
    res = client.get("/secure-ping", headers={"Authorization": f"Bearer {_token()}"})
    assert res.status_code == 200
    assert res.json()["status"] == "secure"

def test_missing_token() -> None:
    res = client.get("/secure-ping")
    assert res.status_code == 401
