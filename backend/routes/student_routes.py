from flask import Blueprint, request, jsonify

from database.db import db

from models.student_model import Student

student_bp = Blueprint(
    'students',
    __name__
)

# GET ALL STUDENTS
@student_bp.route(
    '/all',
    methods=['GET']
)
def get_students():

    students = Student.query.all()

    output = []

    for student in students:

        output.append({

            "id": student.id,

            "full_name": student.full_name,

            "admission_number":
                student.admission_number
        })

    return jsonify(output)


# ADD STUDENT
@student_bp.route(
    '/add',
    methods=['POST']
)
def add_student():

    data = request.get_json()

    print(data)

    student = Student(

        full_name=data.get(
            'full_name'
        ),

        admission_number=data.get(
            'admission_number'
        )
    )

    db.session.add(student)

    db.session.commit()

    return jsonify({

        "message":
            "Student added successfully"

    }), 201