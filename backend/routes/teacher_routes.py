from flask import Blueprint, request, jsonify

from database.db import db

from models.teacher_model import Teacher

teacher_bp = Blueprint('teacher', __name__)

# ADD TEACHER
@teacher_bp.route('/add', methods=['POST'])
def add_teacher():

    data = request.get_json()

    salary = float(data.get('salary', 0))

    teacher = Teacher(
        full_name=data.get('full_name'),
        subject=data.get('subject'),
        salary=salary,
        paid_salary=0,
        remaining_salary=salary
    )

    db.session.add(teacher)

    db.session.commit()

    return jsonify({
        "message": "Teacher added successfully"
    }), 201


# GET TEACHERS
@teacher_bp.route('/all', methods=['GET'])
def get_teachers():

    teachers = Teacher.query.all()

    output = []

    for teacher in teachers:

        output.append({
            "id": teacher.id,
            "full_name": teacher.full_name,
            "subject": teacher.subject,
            "salary": teacher.salary,
            "paid_salary": teacher.paid_salary,
            "remaining_salary": teacher.remaining_salary
        })

    return jsonify(output), 200


# PAY SALARY
@teacher_bp.route('/pay-salary/<int:id>', methods=['PUT'])
def pay_salary(id):

    teacher = Teacher.query.get(id)

    if not teacher:

        return jsonify({
            "message": "Teacher not found"
        }), 404

    data = request.get_json()

    amount = float(data.get('amount', 0))

    teacher.paid_salary += amount

    teacher.remaining_salary -= amount

    db.session.commit()

    return jsonify({
        "message": "Salary updated successfully"
    }), 200