from app import create_app


def test_login():
    app = create_app()
    with app.test_client() as test_client:
        response = test_client.get("/auth/login")
        assert response.status_code == 200
        assert b"Login" in response.data
        assert b"Email" in response.data
        assert b"Password" in response.data
        assert b"remember" in response.data

