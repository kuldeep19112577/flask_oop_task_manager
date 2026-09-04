from flask_jwt_extended import create_access_token
from .user_service import UserService


class AuthService:
    def __init__(self):
        self.user_service = UserService()

    def login(self, email, password):
        found_user = self.user_service.find_by_email(email)
        if found_user and found_user.password == password:
            return create_access_token(identity=email)
        return None
