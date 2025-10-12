# user_service.py
from werkzeug.security import generate_password_hash, check_password_hash
from config.db import db
from models.user_model import UserModel

users_collection = db["users"]

class UserService:
    @staticmethod
    def create_user(username, email, password, role="customer"):
        if users_collection.find_one({"email": email}):
            return {"error": "Email already exists"}, 400

        hashed_pw = generate_password_hash(password)
        new_user = UserModel(username, email, hashed_pw, role)
        users_collection.insert_one(new_user.to_dict())
        return {"message": "User created successfully"}, 201

    @staticmethod
    def login_user(email, password):
        user = users_collection.find_one({"email": email})
        if not user or not check_password_hash(user["password"], password):
            return {"error": "Invalid credentials"}, 401
        return {"message": "Login successful", "user": {"email": email, "role": user["role"]}}, 200

    @staticmethod
    def get_all_users():
        users = list(users_collection.find({}, {"password": 0}))
        return users, 200

    @staticmethod
    def get_user_by_id(user_id):
        from bson import ObjectId
        user = users_collection.find_one({"_id": ObjectId(user_id)}, {"password": 0})
        if not user:
            return {"error": "User not found"}, 404
        return user, 200

    @staticmethod
    def delete_user(user_id):
        from bson import ObjectId
        result = users_collection.delete_one({"_id": ObjectId(user_id)})
        if result.deleted_count == 0:
            return {"error": "User not found"}, 404
        return {"message": "User deleted successfully"}, 200
