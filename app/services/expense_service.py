from app.services.s3_service import upload_file_to_s3

from app.repository.expense_repository import (
    add_expense,
    get_expenses,
    update_expense,
    delete_expense
)


# ==========================================
# ADD EXPENSE
# ==========================================

def add_expense_service(
    amount,
    category,
    description,
    receipt,
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

    # --------------------------------------
    # Upload Receipt to Amazon S3
    # --------------------------------------

    receipt_url = None

    if receipt:
        receipt_url = upload_file_to_s3(receipt)

    # --------------------------------------
    # Save Expense in Database
    # --------------------------------------

    add_expense(
        amount,
        category,
        description,
        receipt_url,
        user_id
    )

    # --------------------------------------
    # Success Response
    # --------------------------------------

    return {
        "success": True,
        "message": "Expense Added Successfully"
    }


# ==========================================
# GET ALL EXPENSES
# ==========================================

def get_expenses_service(user_id):

    expenses = get_expenses(user_id)

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

    if not amount:
        return {
            "success": False,
            "message": "Amount is required"
        }

    if not category:
        return {
            "success": False,
            "message": "Category is required"
        }

    update_expense(
        expense_id,
        amount,
        category,
        description,
        user_id
    )

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