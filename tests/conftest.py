"""Shared test fixtures and configuration"""
import copy
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Provide a TestClient for the FastAPI app"""
    return TestClient(app)


@pytest.fixture
def sample_activities():
    """
    Provide a copy of sample activities for testing.
    Uses deep copy to prevent state pollution between tests.
    """
    return copy.deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities(sample_activities, monkeypatch):
    """
    Reset activities to sample state before each test.
    This ensures tests don't interfere with each other.
    """
    monkeypatch.setattr("src.app.activities", sample_activities)
