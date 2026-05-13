from flask import Flask
from flask_cors import CORS

from dotenv import load_dotenv

import os

from database.db import db

# LOAD ENV VARIABLES
load_dotenv()

# APP
app = Flask(__name__)

CORS(app)

# DATABASE CONFIG
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'sqlite:///school_erp.db'
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# INIT DATABASE
db.init_app(app)

# IMPORT MODELS
from models.user_model import User
from models.student_model import Student
from models.teacher_model import Teacher
from models.fee_structure_model import FeeStructure
from models.bus_route_model import BusRoute
from models.fee_payment_model import FeePayment
from models.expense_model import Expense
from models.teacher_attendance_model import TeacherAttendance
from models.salary_record_model import SalaryRecord
from models.working_day_model import WorkingDay

# IMPORT ROUTES
from routes.auth_routes import auth_bp
from routes.student_routes import student_bp
from routes.teacher_routes import teacher_bp
from routes.fee_routes import fee_bp
from routes.accounting_routes import accounting_bp
from routes.payroll_routes import payroll_bp

# REGISTER BLUEPRINTS
app.register_blueprint(
    auth_bp,
    url_prefix='/api/auth'
)

app.register_blueprint(
    student_bp,
    url_prefix='/api/students'
)

app.register_blueprint(
    teacher_bp,
    url_prefix='/api/teachers'
)

app.register_blueprint(
    fee_bp,
    url_prefix='/api/fees'
)

app.register_blueprint(
    accounting_bp,
    url_prefix='/api/accounting'
)

app.register_blueprint(
    payroll_bp,
    url_prefix='/api/payroll'
)

# CREATE DATABASE TABLES
with app.app_context():

    db.create_all()

# RUN APP
if __name__ == '__main__':

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(
        host='0.0.0.0',
        port=port
    )