from unittest.mock import patch

from run import app


def test_register_success():
    app.config["TESTING"] = True

    with app.test_client() as client:

        with patch(
            "app.routes.auth_routes.register_user"
        ) as mock_register:

            mock_register.return_value = (
                {"message": "User registered successfully"},
                201
            )

            response = client.post(
                "/register",
                json={
                    "email": "test@example.com",
                    "password": "Test@123"
                }
            )

            assert response.status_code == 201
            assert response.get_json()["message"] == \
                "User registered successfully"

            mock_register.assert_called_once_with(
                "test@example.com",
                "Test@123"
            )


def test_login_success():
    app.config["TESTING"] = True
    app.config["JWT_SECRET_KEY"] = "test-secret-key"

    with app.test_client() as client:

        with patch(
            "app.routes.auth_routes.login_user"
        ) as mock_login:

            mock_login.return_value = (
                {
                    "message": "Login successful",
                    "access_token": "test-jwt-token"
                },
                200
            )

            response = client.post(
                "/login",
                json={
                    "email": "test@example.com",
                    "password": "Test@123"
                }
            )

            assert response.status_code == 200
            assert response.get_json()["message"] == \
                "Login successful"

            assert "access_token" in response.get_json()

            mock_login.assert_called_once_with(
                "test@example.com",
                "Test@123"
            )
