from flask import Blueprint, request, jsonify

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from database.db import db

from models.user_model import User

auth_bp = Blueprint(
    'auth',
    __name__
)

# REGISTER
@auth_bp.route(
    '/register',
    methods=['POST']
)
def register():

    try:

        data = request.get_json()

        existing_user = User.query.filter_by(
            email=data.get('email')
        ).first()

        if existing_user:

            return jsonify({
                "message":
                    "User already exists"
            }), 400

        hashed_password = generate_password_hash(
            data.get('password'),
            method='pbkdf2:sha256'
        )

        user = User(

            full_name=data.get(
                'full_name'
            ),

            email=data.get(
                'email'
            ),

            password=hashed_password,

            role=data.get(
                'role'
            )
        )

        db.session.add(user)

        db.session.commit()

        return jsonify({
            "message":
                "User registered successfully"
        }), 201

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# LOGIN
@auth_bp.route(
    '/login',
    methods=['POST']
)
def login():

    try:

        data = request.get_json()

        user = User.query.filter_by(
            email=data.get('email')
        ).first()

        if not user:

            return jsonify({
                "message":
                    "Invalid credentials"
            }), 401

        if not check_password_hash(
            user.password,
            data.get('password')
        ):

            return jsonify({
                "message":
                    "Invalid credentials"
            }), 401

        return jsonify({

            "message":
                "Login successful",

            "user": {

                "id": user.id,

                "full_name":
                    user.full_name,

                "email":
                    user.email,

                "role":
                    user.role
            }

        }), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# DELETE ALL USERS
@auth_bp.route(
    '/delete-all-users',
    methods=['DELETE']
)
def delete_all_users():

    try:

        User.query.delete()

        db.session.commit()

        return jsonify({
            "message":
                "All users deleted"
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500