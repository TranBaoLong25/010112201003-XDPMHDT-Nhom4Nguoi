# user_model.py
class UserModel:
    def __init__(self, username, email, password, role="customer"):
        self.username = username
        self.email = email
        self.password = password  # Mã hóa ở tầng service
        self.role = role

    def to_dict(self):
        return {
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "role": self.role
        }
