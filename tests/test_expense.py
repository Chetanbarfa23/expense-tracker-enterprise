from unittest.mock import patch

from flask_jwt_extended import create_access_token

from run import app


app.config["TESTING"] = True
app.config["JWT_SECRET_KEY"] = "test-secret-key-that-is-at-least-32-bytes-long"

def get_test_token():
    with app.app_context():
        return create_access_token(identity="1")


def test_get_expenses_success():
    token = get_test_token()

    with app.test_client() as client:
        with patch(
            "app.routes.expense_routes.get_expenses_service"
        ) as mock_service:

            mock_service.return_value = {
                "success": True,
                "expenses": [
                    {
                        "id": 1,
                        "amount": 500,
                        "category": "Food",
                        "description": "Lunch"
                    }
                ]
            }

            response = client.get(
                "/expenses",
                headers={
                    "Authorization": f"Bearer {token}"
                }
            )

            assert response.status_code == 200
            assert response.get_json()["success"] is True

            mock_service.assert_called_once_with("1")


def test_add_expense_success():
    token = get_test_token()

    with app.test_client() as client:
        with patch(
            "app.routes.expense_routes.add_expense_service"
        ) as mock_service:

            mock_service.return_value = {
                "success": True,
                "message": "Expense added successfully"
            }

            response = client.post(
                "/add-expense",
                headers={
                    "Authorization": f"Bearer {token}"
                },
                data={
                    "amount": "500",
                    "category": "Food",
                    "description": "Lunch"
                }
            )

            assert response.status_code == 200
            assert response.get_json()["success"] is True

            mock_service.assert_called_once()


def test_update_expense_success():
    token = get_test_token()

    with app.test_client() as client:
        with patch(
            "app.routes.expense_routes.update_expense_service"
        ) as mock_service:

            mock_service.return_value = {
                "success": True,
                "message": "Expense updated successfully"
            }

            response = client.put(
                "/expense/1",
                headers={
                    "Authorization": f"Bearer {token}"
                },
                json={
                    "amount": 700,
                    "category": "Food",
                    "description": "Dinner"
                }
            )

            assert response.status_code == 200
            assert response.get_json()["success"] is True

            mock_service.assert_called_once_with(
                1,
                700,
                "Food",
                "Dinner",
                "1"
            )


def test_delete_expense_success():
    token = get_test_token()

    with app.test_client() as client:
        with patch(
            "app.routes.expense_routes.delete_expense_service"
        ) as mock_service:

            mock_service.return_value = {
                "success": True,
                "message": "Expense deleted successfully"
            }

            response = client.delete(
                "/expense/1",
                headers={
                    "Authorization": f"Bearer {token}"
                }
            )

            assert response.status_code == 200
            assert response.get_json()["success"] is True

            mock_service.assert_called_once_with(
                1,
                "1"
            )
