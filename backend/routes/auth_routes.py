from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from flask_bcrypt import Bcrypt

from database.db import db
from models.user_model import User

auth_bp = Blueprint('auth', __name__)

bcrypt = Bcrypt()

# ADMIN REGISTRATION
@auth_bp.route('/register', methods=['POST'])
def register():

    data = request.get_json()

    full_name = data.get('full_name')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({
            "message": "User already exists"
        }), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    new_user = User(
        full_name=full_name,
        email=email,
        password=hashed_password,
        role=role
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "User registered successfully"
    }), 201


# LOGIN
@auth_bp.route('/login', methods=['POST'])
def login():

    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({
            "message": "Invalid email or password"
        }), 401

    is_password_correct = bcrypt.check_password_hash(
        user.password,
        password
    )

    if not is_password_correct:
        return jsonify({
            "message": "Invalid email or password"
        }), 401

    access_token = create_access_token(identity={
        "id": user.id,
        "role": user.role,
        "email": user.email
    })

    return jsonify({
        "message": "Login successful",
        "token": access_token,
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "role": user.role
        }
    }), 200