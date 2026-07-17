# ==========================================================
# USER REPOSITORY
# ==========================================================
#
# Repository Layer Responsibilities:
#
# ✔ Connect to MySQL
# ✔ Execute SQL Queries
# ✔ Return Database Results
#
# Repository NEVER:
# ✘ Validates Data
# ✘ Generates JWT
# ✘ Hashes Password
# ✘ Returns JSON
#
# Repository only knows SQL.
#
# ==========================================================

from database.database import get_connection


# ==========================================================
# GET ALL USERS
# ==========================================================
#
# Returns:
# List of all users from the users table.
#
# SQL:
# SELECT * FROM users;
#
# ==========================================================

def get_all_users():

    # Create Database Connection
    conn = get_connection()

    # Create Cursor
    cursor = conn.cursor()

    # Execute SQL Query
    cursor.execute(
        """
        SELECT *
        FROM users
        """
    )

    # Fetch All Records
    users = cursor.fetchall()

    # Close Resources
    cursor.close()
    conn.close()

    # Return Python List
    return users


# ==========================================================
# GET USER BY EMAIL
# ==========================================================
#
# Parameter:
# email
#
# Returns:
# One user if email exists
# Otherwise returns None
#
# SQL:
#
# SELECT *
# FROM users
# WHERE email = ?
#
# ==========================================================

def get_user_by_email(email):

    # Create Database Connection
    conn = get_connection()

    # Create Cursor
    cursor = conn.cursor()

    # Execute SQL Query
    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE email = %s
        """,
        (email,)
    )

    # Fetch Single Record
    user = cursor.fetchone()

    # Close Resources
    cursor.close()
    conn.close()

    # Return User
    return user


# ==========================================================
# CREATE USER
# ==========================================================
#
# Parameters:
# email
# password
#
# SQL:
#
# INSERT INTO users
# (email,password)
# VALUES
# (%s,%s)
#
# commit() is required because
# INSERT permanently changes the database.
#
# ==========================================================

def create_user(email, password):

    # Create Database Connection
    conn = get_connection()

    # Create Cursor
    cursor = conn.cursor()

    # Execute INSERT Query
    cursor.execute(
        """
        INSERT INTO users
        (
            email,
            password
        )
        VALUES
        (
            %s,
            %s
        )
        """,
        (email, password)
    )
              
    # Save Changes Permanently
    conn.commit()

    # Close Resources
    cursor.close()
    conn.close()