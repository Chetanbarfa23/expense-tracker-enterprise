from app.repository.expense_repository import (
    add_expense,
    get_expenses,
    update_expense,
    delete_expense
)
def add_expense_service(
    amount,
    category,
    description,
    user_id
):

    # Validate Amount
    if not amount:

        return {
            "success": False,
            "message": "Amount is required"
        }

    # Validate Category
    if not category:

        return {
            "success": False,
            "message": "Category is required"
        }

    # Save Expense
    add_expense(
        amount,
        category,
        description,
        user_id
    )

    # Success Response
    return {
        "success": True,
        "message": "Expense Added Successfully"
    }

# ==========================================
# GET ALL EXPENSES
# ==========================================

def get_expenses_service(user_id):

    # Get Expenses From Repository
    expenses = get_expenses(user_id)

    # Return Response
    return {
        "success": True,
        "expenses": expenses
    }

# ==========================================
# UPDATE EXPENSE
# ==========================================

def update_expense_service(
    expense_id,
    amount,
    category,
    description,
    user_id
):

    # Validate Amount
    if not amount:

        return {
            "success": False,
            "message": "Amount is required"
        }

    # Validate Category
    if not category:

        return {
            "success": False,
            "message": "Category is required"
        }

    # Update Expense
    update_expense(
        expense_id,
        amount,
        category,
        description,
        user_id
    )

    # Success Response
    return {
        "success": True,
        "message": "Expense Updated Successfully"
    }


# ==========================================
# DELETE EXPENSE
# ==========================================

def delete_expense_service(
    expense_id,
    user_id
):

    delete_expense(
        expense_id,
        user_id
    )

    return {
        "success": True,
        "message": "Expense Deleted Successfully"
    }