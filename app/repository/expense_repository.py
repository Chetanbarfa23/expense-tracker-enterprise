from database.database import get_connection
from app.utils.logger import logger

# ==========================================
# ADD EXPENSE
# ==========================================

def add_expense(
    amount,
    category,
    description,
    user_id
):

    conn = None
    cursor = None

    try:

        # Database Connection
        conn = get_connection()

        # Create Cursor
        cursor = conn.cursor()

        # Execute SQL
        cursor.execute(
            """
            INSERT INTO expenses
            (
                amount,
                category,
                description,
                user_id
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s
            )
            """,
            (
                amount,
                category,
                description,
                user_id
            )
        )

        # Save Changes
        conn.commit()

    except Exception as e:

        logger.error(f"Database Error: {e}")

        raise
    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


# ==========================================
# GET ALL EXPENSES OF LOGGED-IN USER
# ==========================================

def get_expenses(user_id):

    conn = None
    cursor = None

    try:

        # Database Connection
        conn = get_connection()

        # Create Cursor
        cursor = conn.cursor()

        # Execute SQL
        cursor.execute(
            """
            SELECT *
            FROM expenses
            WHERE user_id = %s
            """,
            (user_id,)
        )

        # Fetch All Rows
        expenses = cursor.fetchall()

        return expenses

    except Exception as e:

        print("Database Error:", e)

        raise

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


# ==========================================
# UPDATE EXPENSE
# ==========================================

def update_expense(
    expense_id,
    amount,
    category,
    description,
    user_id
):

    conn = None
    cursor = None

    try:

        # Database Connection
        conn = get_connection()

        # Create Cursor
        cursor = conn.cursor()

        # Execute SQL
        cursor.execute(
            """
            UPDATE expenses
            SET
                amount = %s,
                category = %s,
                description = %s
            WHERE
                id = %s
                AND user_id = %s
            """,
            (
                amount,
                category,
                description,
                expense_id,
                user_id
            )
        )

        # Save Changes
        conn.commit()

    except Exception as e:

        print("Database Error:", e)

        raise

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


# ==========================================
# DELETE EXPENSE
# ==========================================

def delete_expense(
    expense_id,
    user_id
):

    conn = None
    cursor = None

    try:

        # Database Connection
        conn = get_connection()

        # Create Cursor
        cursor = conn.cursor()

        # Execute SQL
        cursor.execute(
            """
            DELETE FROM expenses
            WHERE
                id = %s
                AND user_id = %s
            """,
            (
                expense_id,
                user_id
            )
        )

        # Save Changes
        conn.commit()

    except Exception as e:

        print("Database Error:", e)

        raise

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()