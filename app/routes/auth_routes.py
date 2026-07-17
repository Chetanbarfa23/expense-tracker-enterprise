from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.services.auth_service import (
    get_all_users,
    register_user,
    login_user
)

auth = Blueprint(
    "auth",
    __name__
)

# ==========================================
# GET ALL USERS
# ==========================================

@auth.route("/users", methods=["GET"])
def get_users():

    users = get_all_users()

    return {
        "success": True,
        "users": users
    }


# ==========================================
# REGISTER USER
# ==========================================

@auth.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    email = data.get("email")

    password = data.get("password")

    result = register_user(
        email,
        password
    )

    return result

@auth.route("/login", methods=["POST"])
def login():

    # Read JSON Data
    data = request.get_json()

    # Get Email
    email = data.get("email")

    # Get Password
    password = data.get("password")

    # Call Service
    result = login_user(
        email,
        password
    )

    # Return Response
    return result


