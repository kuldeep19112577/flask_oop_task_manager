from uuid import uuid4
from ..models.user import User


user_database = []


class UserService:
    def create_user(self, username, email, password, role):
        new_user = User(
            id=str(uuid4()),
            username=username,
            email=email,
            password=password,
            role=role
        )
        user_database.append(new_user)
        return new_user

    def find_by_email(self, email):
        found_list = list(filter(lambda x: x.email == email, user_database))
        return found_list[0] if found_list else None

    def find_by_id(self, user_id):
        found_list = list(filter(lambda x: x.id == user_id, user_database))
        return found_list[0] if found_list else None
