from app import create_app, db
import pytest
from testConfig import TestConfig


@pytest.fixture()
def test_client():
    app = create_app(TestConfig)
    with app.test_client() as client:
        with app.app_context():
            pass
        yield client

@pytest.fixture()
def database():
    db.create_all()
    yield db
    db.drop_all()

@pytest.fixture
def App():
    app = create_app(TestConfig)
    app.app_context().push()
    yield app
    app.app_context().pop()