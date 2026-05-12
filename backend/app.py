from flask import Flask

from flask_cors import CORS

from flask_jwt_extended import JWTManager

from dotenv import load_dotenv

import os

# LOAD ENV
load_dotenv()

# DATABASE
from database.db import db

# MODELS
from models.user_model import User
from models.student_model import Student
from models.teacher_model import Teacher
from models.attendance_model import Attendance
from models.fee_structure_model import FeeStructure
from models.bus_route_model import BusRoute

# ROUTES
from routes.auth_routes import auth_bp
from routes.student_routes import student_bp
from routes.teacher_routes import teacher_bp
from routes.attendance_routes import attendance_bp
from routes.fee_routes import fee_bp
from routes.dashboard_routes import dashboard_bp
from routes.report_routes import report_bp

app = Flask(__name__)

# CONFIG
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# INIT
db.init_app(app)

JWTManager(app)

CORS(app)

# REGISTER ROUTES
app.register_blueprint(auth_bp, url_prefix='/api/auth')

app.register_blueprint(student_bp, url_prefix='/api/students')

app.register_blueprint(teacher_bp, url_prefix='/api/teachers')

app.register_blueprint(attendance_bp, url_prefix='/api/attendance')

app.register_blueprint(fee_bp, url_prefix='/api/fees')

app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')

app.register_blueprint(report_bp, url_prefix='/api/reports')

# CREATE DATABASE
with app.app_context():

    db.create_all()

# RUN
if __name__ == '__main__':

    app.run(debug=True)