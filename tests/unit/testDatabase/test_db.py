import pytest
from app import create_app,db
from app.models import Employee

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"]  = True
    app.testing = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

    client = app.test_client()
    with app.app_context():
        db.create_all()
        ###### WRITE UNIT TEST ######
        emp = Employee(name = "Parth",)