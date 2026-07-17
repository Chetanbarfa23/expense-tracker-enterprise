# =====================================================
# IMPORTS
# =====================================================

from flask import Flask
from dotenv import load_dotenv
from app.routes.expense_routes import expense
from database.database import get_connection

from flask_jwt_extended import JWTManager

# Import Blueprint
from app.routes.auth_routes import auth

import os

# =====================================================
# LOAD ENVIRONMENT VARIABLES
# =====================================================

load_dotenv()


# =====================================================
# CREATE FLASK APPLICATION
# =====================================================

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app)



# =====================================================
# REGISTER BLUEPRINTS
# =====================================================

# Register all routes with Flask.
# Without this line, Flask will not know
# about /users or /register APIs.

app.register_blueprint(auth)

app.register_blueprint(expense)
# =====================================================
# HOME ROUTE
# =====================================================

@app.route("/")
def home():

    return {
        "message": "Expense Tracker Enterprise Running 🚀"
    }


# =====================================================
# DATABASE CONNECTION TEST
# =====================================================

@app.route("/test-db")
def test_db():

    # Get MySQL Connection
    conn = get_connection()

    # Create Cursor
    cursor = conn.cursor()

    # Execute Test Query
    cursor.execute("SELECT 1")

    # Get Result
    result = cursor.fetchone()

    # Close Resources
    cursor.close()
    conn.close()

    # Return Response
    return {
        "db": result
    }


# =====================================================
# RUN FLASK SERVER
# =====================================================

# =====================================================
# RUN FLASK SERVER
# =====================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )