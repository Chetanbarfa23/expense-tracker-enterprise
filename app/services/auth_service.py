# ======================================================
# AUTH SERVICE
# ======================================================

from flask_jwt_extended import create_access_token
import bcrypt

from app.repository.user_repository import (
    create_user,
    get_user_by_email
)

from app.repository.user_repository import (
    get_all_users as repo_get_all_users
)

from app.utils.response import (
    success_response,
    error_response
)

# ======================================================
# GET ALL USERS
# ======================================================

def get_all_users():

    users = repo_get_all_users()

    return users


# ======================================================
# REGISTER USER
# ======================================================

def register_user(email, password):

    # =====================================
    # VALIDATE EMAIL
    # =====================================

    if not email:

        return error_response(
            "Email is required"
        )

    # =====================================
    # VALIDATE PASSWORD
    # =====================================

    if not password:

        return error_response(
            "Password is required"
        )

    # =====================================
    # CHECK USER EXISTS
    # =====================================

    user = get_user_by_email(email)

    if user:

        return error_response(
            "Email already exists"
        )

    # =====================================
    # HASH PASSWORD
    # =====================================

    hashed_password = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    )

    # =====================================
    # SAVE USER
    # =====================================

    create_user(
        email,
        hashed_password.decode()
    )

    # =====================================
    # SUCCESS RESPONSE
    # =====================================

    return success_response(
        "User Registered Successfully"
    )


# ======================================================
# LOGIN USER
# ======================================================

def login_user(email, password):

    # =====================================
    # VALIDATE EMAIL
    # =====================================

    if not email:

        return error_response(
            "Email is required"
        )

    # =====================================
    # VALIDATE PASSWORD
    # =====================================

    if not password:

        return error_response(
            "Password is required"
        )

    # =====================================
    # CHECK USER EXISTS
    # =====================================

    user = get_user_by_email(email)

    if not user:

        return error_response(
            "User not found"
        )

    # =====================================
    # VERIFY PASSWORD
    # =====================================

    password_match = bcrypt.checkpw(
        password.encode(),
        user["password"].encode()
    )

    if not password_match:

        return error_response(
            "Invalid Password"
        )

    # =====================================
    # GENERATE JWT TOKEN
    # =====================================

    token = create_access_token(
        identity=str(user["id"])
    )

    # =====================================
    # SUCCESS RESPONSE
    # =====================================

    return success_response(
        "Login Successful",
        {
            "token": token
        }
    )