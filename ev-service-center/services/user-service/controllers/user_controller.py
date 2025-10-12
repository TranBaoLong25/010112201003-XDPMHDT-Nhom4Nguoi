from flask import Blueprint, jsonify, request
from bson import ObjectId
from services.user_service import UserService

user_bp = Blueprint('user_bp', __name__)

# 🧩 Chặn favicon.ico request
@user_bp.route('/favicon.ico')
def favicon():
    return '', 204


# ------------------ ROUTES ------------------ #

@user_bp.route("/register", methods=["POST"])
def register_user():
    data = request.get_json()
    return jsonify(*UserService.create_user(
        data["username"], data["email"], data["password"], data.get("role", "customer")
    ))

@user_bp.route("/login", methods=["POST"])
def login_user():
    data = request.get_json()
    return jsonify(*UserService.login_user(data["email"], data["password"]))

@user_bp.route("/", methods=["GET"])
def get_all_users():
    return jsonify(*UserService.get_all_users())

@user_bp.route("/<user_id>", methods=["GET"])
def get_user(user_id):
    return jsonify(*UserService.get_user_by_id(user_id))

@user_bp.route("/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    return jsonify(*UserService.delete_user(user_id))
