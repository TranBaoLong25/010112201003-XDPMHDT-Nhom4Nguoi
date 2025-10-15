from flask import Blueprint, jsonify, request
from services.user_service import UserService, users
from services.auth import decode_auth_token

user_bp = Blueprint('user_bp', __name__)

def get_current_user():
    # ... (Hàm get_current_user và các hàm khác giữ nguyên)
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None
    token = auth_header.split(" ")[1]
    payload = decode_auth_token(token)
    if not payload:
        return None
    user = next((u for u in users if u['_id'] == payload["sub"]), None)
    return user

@user_bp.route('/favicon.ico')
def favicon():
    return '', 204

@user_bp.route("/register", methods=["POST"])
def register_user():
    data = request.get_json()
    return jsonify(*UserService.create_user(
        data["username"], data["email"], data["password"], data.get("role", "customer")
    ))

@user_bp.route("/login", methods=["POST"])
def login_user():
    data = request.get_json()
    # SỬA LỖI KEYERROR: Đã thay data["email"] bằng data["username"]
    result, status = UserService.login_user(data["username"], data["password"])
    return jsonify(result), status


# --- ĐOẠN ĐÃ SỬA ĐỂ KHẮC PHỤC LỖI TypeError ---
@user_bp.route("/", methods=["GET"])
def get_all_users():
    current_user = get_current_user()
    
    # SỬA LỖI: Kiểm tra nếu user là None (chưa đăng nhập/token lỗi)
    if current_user is None:
        # Trả về lỗi 401 Unauthorized (Không được phép)
        return jsonify({"message": "Unauthorized access. Token is missing or invalid."}), 401 

    # Nếu user đã hợp lệ, gọi Service để thực hiện logic nghiệp vụ
    return jsonify(*UserService.get_all_users(current_user))
# ----------------------------------------------------

# ... (các hàm còn lại như cũ)

@user_bp.route("/<user_id>", methods=["GET"])
def get_user(user_id):
    current_user = get_current_user()
    if current_user is None:
        return jsonify({"message": "Unauthorized access. Token is missing or invalid."}), 401
    return jsonify(*UserService.get_user_by_id(user_id, current_user))

@user_bp.route("/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    current_user = get_current_user()
    if current_user is None:
        return jsonify({"message": "Unauthorized access. Token is missing or invalid."}), 401
    return jsonify(*UserService.delete_user(user_id, current_user))

@user_bp.route("/<user_id>", methods=["PUT"])
def update_user(user_id):
    current_user = get_current_user()
    if current_user is None:
        return jsonify({"message": "Unauthorized access. Token is missing or invalid."}), 401
    data = request.get_json()
    return jsonify(*UserService.update_user(user_id, data, current_user))
# ======================= LẤY THÔNG TIN USER HIỆN TẠI ======================= #
@user_bp.route("/summary", methods=["GET"])
def get_summary():
    """Trả thông tin user hiện tại dựa vào token"""
    current_user = get_current_user()
    if current_user is None:
        return jsonify({"message": "Phiên đã hết hạn."}), 401

    return jsonify({
        "username": current_user["username"],
        "email": current_user["email"],
        "role": current_user["role"]
    }), 200
