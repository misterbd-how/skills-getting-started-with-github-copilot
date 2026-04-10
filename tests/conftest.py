# Test fixtures for FastAPI backend tests
import pytest
from fastapi.testclient import TestClient
from src.app import app

@pytest.fixture(scope="module")
def client():
    """Fixture for FastAPI TestClient."""
    with TestClient(app) as c:
        yield c
