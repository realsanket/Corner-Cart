import pytest
from fastapi.testclient import TestClient

from app.shared.store import get_services


@pytest.fixture()
def services():
    get_services.cache_clear()
    yield get_services()
    get_services.cache_clear()


@pytest.fixture()
def api(services):
    from app.api.main import app

    return TestClient(app)


@pytest.fixture()
def web(services):
    from app.web.main import app

    return TestClient(app)
