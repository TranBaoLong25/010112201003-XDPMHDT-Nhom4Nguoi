from werkzeug.security import generate_password_hash, check_password_hash
from models.user_model import UserModel
from services.auth import encode_auth_token
from uuid import uuid4

# Danh sách lưu user tạm thời (GIẢ ĐỊNH)
# LƯU Ý: Dữ liệu bị mất khi container Docker dừng lại.
users = [] 

class UserService:
    @staticmethod
    def create_user(username, email, password, role):
        if role not in ['admin', 'staff', 'customer', 'guest']:
            return {"error": "Role không hợp lệ"}, 400
        
        # Kiểm tra username và email đã tồn tại
        if any(u.get('email') == email or u.get('username') == username for u in users):
            return {"error": "Tên đăng nhập hoặc Email đã tồn tại"}, 400
            
        hashed_pw = generate_password_hash(password)
        
        # 1. TẠO USER: Khởi tạo model và lấy dictionary
        user = UserModel(username, email, hashed_pw, role).to_dict()
        
        # 2. SỬA LỖI: Gán mật khẩu đã băm vào khóa "password" để khớp với logic check_password_hash
        user['password'] = hashed_pw 
        user['_id'] = str(uuid4())
        
        users.append(user)
        return {"message": "Tạo user thành công"}, 201

    @staticmethod
    # SỬA: Logic đã được kiểm tra và hoàn thiện để dùng username
    def login_user(username, password): 
        
        # 1. Tìm user bằng username
        user = next((u for u in users if u.get('username') == username), None)
        
        # 2. Xác thực: Dùng khóa user["password"] (chứa giá trị hash)
        # Lỗi logic đã được sửa trong hàm create_user để đảm bảo user["password"] tồn tại
        if not user or not check_password_hash(user["password"], password): 
            return ({"error": "Sai tên đăng nhập hoặc mật khẩu"}, 401)
            
        # 3. Tạo token
        token = encode_auth_token(user["_id"], user["role"])
        
        # 4. Trả về token và role (Dạng tuple cho jsonify(*args))
        user_info = {k: v for k, v in user.items() if k != "password"}
        
        return ({"token": token, "role": user_info['role'], "user": user_info}, 200)

    @staticmethod
    def get_all_users(current_user):
        if current_user["role"] != "admin":
            return {"error": "Chỉ admin được phép"}, 403
        return {"users": [ {k:v for k,v in u.items() if k != "password"} for u in users ]}, 200

    @staticmethod
    def get_user_by_id(user_id, current_user):
        user = next((u for u in users if u['_id'] == user_id), None)
        if not user:
            return {"error": "Không tìm thấy user"}, 404
        if current_user["role"] == "admin" or current_user["_id"] == user_id:
            user_info = {k: v for k, v in user.items() if k != "password"}
            return {"user": user_info}, 200
        return {"error": "Không có quyền"}, 403

    @staticmethod
    def delete_user(user_id, current_user):
        global users
        if current_user["role"] != "admin":
            return {"error": "Chỉ admin được phép xóa user"}, 403
        before = len(users)
        users = [u for u in users if u['_id'] != user_id]
        if len(users) == before:
            return {"error": "Không tìm thấy user"}, 404
        return {"message": "Xóa user thành công"}, 200

    @staticmethod
    def update_user(user_id, data, current_user):
        user = next((u for u in users if u['_id'] == user_id), None)
        if not user:
            return {"error": "Không tìm thấy user"}, 404
        if current_user["role"] != "admin" and user['_id'] != current_user["_id"]:
            return {"error": "Không có quyền"}, 403
        for k in ["username", "email", "role"]:
            if k in data:
                user[k] = data[k]
        if "password" in data:
            user["password"] = generate_password_hash(data["password"])
        return {"message": "Cập nhật user thành công"}, 200