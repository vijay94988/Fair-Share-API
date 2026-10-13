import os
from collections.abc import Iterator
from unittest.mock import Mock
import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("DB_NAME", "fair_share_test")
os.environ.setdefault("DB_USER", "test_user")
os.environ.setdefault("DB_PASSWORD", "test_password")

from app.dependencies import get_db_cursor
from app.main import app

@pytest.fixture
def mock_cursor() -> Mock:
    return Mock()

@pytest.fixture
def client(mock_cursor: Mock) -> Iterator[TestClient]:
    def override_get_db_cursor() -> Iterator[Mock]:
        yield mock_cursor
    app.dependency_overrides[get_db_cursor] = override_get_db_cursor
    test_client = TestClient(app)

    yield test_client

    test_client.close()
    app.dependency_overrides.clear()
