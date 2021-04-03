from app import create_app, db
import pytest
from testConfig import TestConfig


@pytest.fixture()
def test_client():
    app = create_app(TestConfig)
    testing_client = app.test_client()
    ctx = app.app_context()
    ctx.push()

    yield testing_client
    ctx.pop()


@pytest.fixture()
def database():
    db.create_all()
    yield db
    db.drop_all()
