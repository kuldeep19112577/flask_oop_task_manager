from flask import Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from ..services.user_service import UserService
from ..services.auth_service import AuthService

auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")

user_service = UserService()
auth_service = AuthService()


@auth_blueprint.post("/register")
def handle_register():
    user_data = request.json
    username = user_data.get("username")
    email = user_data.get('email')
    password = user_data.get('password')
    role = user_data.get('role')
    new_user = user_service.create_user(username, email, password, role)
    return {"message": "User creation successful"}, 201


@auth_blueprint.post("/login")
def handle_login():
    email = request.json.get('email')
    password = request.json.get('password')
    token = auth_service.login(email, password)

    if not token:
        return "Invalid credentials", 400

    return {
        "token": token,
        "email":email,
        "status":"Login Successful"
    }, 201


@auth_blueprint.get("/me")
@jwt_required()
def handle_me():
    email = get_jwt_identity()
    found_user = user_service.find_by_email(email)

    if not found_user:
        return "Hacker situation", 400

    user = found_user.get_dictionary()
    del user['password']
    return user
