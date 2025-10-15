import jwt
import datetime

SECRET_KEY = "your_jwt_secret"

def encode_auth_token(user_id, role):
    try:
        # Tính thời gian hết hạn
        expiration = datetime.datetime.utcnow() + datetime.timedelta(days=1)
        
        payload = {
            # Dùng timestamp số nguyên (int) cho tính ổn định của JWT
            'exp': int(expiration.timestamp()), 
            'iat': int(datetime.datetime.utcnow().timestamp()),
            'sub': str(user_id),  # Đảm bảo user_id là string
            'role': str(role)      # Đảm bảo role là string
        }
        return jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    except Exception as e:
        # Nếu vẫn gặp lỗi, hàm sẽ trả về None
        return None

def decode_auth_token(auth_token):
    try:
        payload = jwt.decode(auth_token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None