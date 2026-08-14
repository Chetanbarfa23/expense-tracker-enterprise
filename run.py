# =====================================================
# IMPORTS
# =====================================================

from flask import Flask
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager

import os

from app.routes.auth_routes import auth
from app.routes.expense_routes import expense
from database.database import get_connection


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

app.register_blueprint(auth)
app.register_blueprint(expense)


# =====================================================
# HOME ROUTE
# =====================================================

@app.route("/")
def home():

    return {
        "message": "Expense Tracker Enterprise Running 🚀"
    }, 200


# =====================================================
# HEALTH CHECK ROUTE
# Used by Kubernetes Readiness & Liveness Probes
# =====================================================

@app.route("/health")
def health():

    return {
        "status": "healthy"
    }, 200


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
    }, 200


# =====================================================
# RUN FLASK SERVER
# =====================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )