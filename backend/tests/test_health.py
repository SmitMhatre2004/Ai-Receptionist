"""Smoke tests for Phase 1: confirms the app boots and core routes respond.

Run with:  pytest
"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_returns_ok() -> None:
    response = client.get("/")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"


def test_health_check_returns_healthy() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "healthy"
    assert "env" in body
