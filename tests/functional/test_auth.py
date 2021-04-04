from app.auth.forms import LoginForm
from flask import Flask
from app.models import Employee


def test_login(test_client):
    emp = Employee(name="Parth", email="pmjindal@gmail.com")
    emp.set_password("1103")

    form = LoginForm(email=emp.email, password="1103")

    with test_client.session_transaction() as sess:
        sess['email'] = 'pmjindal@gmail.com'
        sess['password'] = '1103'
        response = test_client.post(
            "/auth/login/", data=form.data, follow_redirects=True)
    assert response.status_code == 200
