"""Tests for health check endpoint."""
from __future__ import annotations

import importlib

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def app(monkeypatch) -> "FastAPI":
    """Provide FastAPI app with required env vars configured."""
    monkeypatch.setenv("JWT_SECRET", "test-secret")
    monkeypatch.setenv("REDIS_URL", "redis://localhost:6379")
    monkeypatch.setenv("PG_DSN", "postgresql://user:pass@localhost:5432/db")
    module = importlib.import_module("backend.main")
    importlib.reload(module)
    return module.app


def test_healthz_returns_status_ok(app) -> None:
    """Health endpoint should return expected status payload."""
    client = TestClient(app)
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
