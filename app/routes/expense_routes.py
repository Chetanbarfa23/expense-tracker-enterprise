from flask import Blueprint, request

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)
from app.services.expense_service import (
    add_expense_service,
    get_expenses_service,
    update_expense_service,
    delete_expense_service
)

expense = Blueprint(
    "expense",
    __name__
)


@expense.route(
    "/add-expense",
    methods=["POST"]
)
@jwt_required()

def add_expense():

    data = request.get_json()

    amount = data.get("amount")

    category = data.get("category")

    description = data.get("description")

    user_id = get_jwt_identity()

    result = add_expense_service(
        amount,
        category,
        description,
        user_id
    )

    return result

# ==========================================
# GET ALL EXPENSES
# ==========================================

@expense.route(
    "/expenses",
    methods=["GET"]
)
@jwt_required()

def get_expenses():

    # Get Logged-in User ID
    user_id = get_jwt_identity()

    # Call Service
    result = get_expenses_service(user_id)

    # Return Response
    return result


# ==========================================
# UPDATE EXPENSE
# ==========================================

@expense.route(
    "/expense/<int:expense_id>",
    methods=["PUT"]
)
@jwt_required()

def update_expense(expense_id):

    # Read JSON Data
    data = request.get_json()

    # Read Fields
    amount = data.get("amount")
    category = data.get("category")
    description = data.get("description")

    # Logged-in User
    user_id = get_jwt_identity()

    # Call Service
    result = update_expense_service(
        expense_id,
        amount,
        category,
        description,
        user_id
    )

    # Return Response
    return result


# ==========================================
# DELETE EXPENSE
# ==========================================

@expense.route(
    "/expense/<int:expense_id>",
    methods=["DELETE"]
)
@jwt_required()

def delete_expense(expense_id):

    # Logged-in User
    user_id = get_jwt_identity()

    # Call Service
    result = delete_expense_service(
        expense_id,
        user_id
    )

    # Return Response
    return result