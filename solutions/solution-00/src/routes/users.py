# Routes for users endpoints.

from flask import Blueprint
from flask import request, jsonify
from werkzeug.security import check_password_hash
import jwt
from datetime import datetime, timedelta
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from hbnb import app, config


jwt = JWTManager(app)


from src.controllers.users import (
    create_user,
    delete_user,
    get_user_by_id,
    get_users,
    update_user,
    get_user_by_email,
)

users_bp = Blueprint("users", __name__, url_prefix="/users")

@users_bp.route("/", methods=["GET"])
@jwt_required()
def get_users():
    return get_users()

@users_bp.route("/", methods=["POST"])
@jwt_required()
def create_user():
    return create_user()

@users_bp.route("/<user_id>", methods=["GET"])
@jwt_required()
def get_user_by_id(user_id):
    return get_user_by_id(user_id)

@users_bp.route("/<user_id>", methods=["PUT"])
@jwt_required()
def update_user(user_id):
    return update_user(user_id)

@users_bp.route("/<user_id>", methods=["DELETE"])
@jwt_required()
def delete_user(user_id):
    return delete_user(user_id)



@users_bp.route("/login", methods=["POST"])
def login():
    email = request.json.get("email")
    password = request.json.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = get_user_by_email(email)

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid email or password"}), 401

    token = jwt.encode(
        {
            "user_id": user.id,
            "exp": datetime.now(datetime.UTC) + timedelta(hours=1)
        },
        "JWT_SECRET_KEY",
        algorithm="HS256"
    )
    return jsonify({"token": token.decode("utf-8")}), 200
