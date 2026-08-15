import pytest

from run import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["JWT_SECRET_KEY"] = "test-secret-key"

    with app.test_client() as client:
        yield client


# Basic API tests

def test_home(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.get_json()["message"] == \
        "Expense Tracker Enterprise Running 🚀"


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"


# JWT protection tests

def test_add_expense_requires_jwt(client):
    response = client.post(
        "/add-expense",
        data={
            "amount": "500",
            "category": "Food",
            "description": "Lunch"
        }
    )

    assert response.status_code == 401


def test_get_expenses_requires_jwt(client):
    response = client.get("/expenses")

    assert response.status_code == 401


def test_update_expense_requires_jwt(client):
    response = client.put(
        "/expense/1",
        json={
            "amount": "500",
            "category": "Food",
            "description": "Lunch"
        }
    )

    assert response.status_code == 401


def test_delete_expense_requires_jwt(client):
    response = client.delete("/expense/1")

    assert response.status_code == 401
