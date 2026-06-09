import copy
import pytest
from fastapi.testclient import TestClient

from src.app import app, activities as activities_global


@pytest.fixture
def client():
    """Return a TestClient for the FastAPI app."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Deep-copy and restore the global `activities` dict around each test.

    This ensures tests are isolated and do not depend on test ordering.
    """
    snapshot = copy.deepcopy(activities_global)
    yield
    activities_global.clear()
    activities_global.update(snapshot)
