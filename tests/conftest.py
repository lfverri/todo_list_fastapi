import pytest
from fastapi.testclient import TestClient

from app.app import app


@pytest.fixture
def client():
    """Fixture to create a TestClient for the FastAPI app."""
    return TestClient(app)
