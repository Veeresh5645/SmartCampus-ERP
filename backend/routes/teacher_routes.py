from flask import Blueprint, request, jsonify

from database.db import db

from models.teacher_model import Teacher

teacher_bp = Blueprint(
    'teachers',
    __name__
)

# GET ALL TEACHERS
@teacher_bp.route(
    '/all',
    methods=['GET']
)
def get_teachers():

    teachers = Teacher.query.all()

    output = []

    for teacher in teachers:

        output.append({

            "id": teacher.id,

            "full_name":
                teacher.full_name,

            "email":
                teacher.email,

            "phone":
                teacher.phone,

            "subject":
                teacher.subject,

            "salary":
                teacher.salary
        })

    return jsonify(output)


# ADD TEACHER
@teacher_bp.route(
    '/add',
    methods=['POST']
)
def add_teacher():

    data = request.get_json()

    teacher = Teacher(

        full_name=data.get(
            'full_name'
        ),

        email=data.get(
            'email'
        ),

        phone=data.get(
            'phone'
        ),

        subject=data.get(
            'subject'
        ),

        salary=int(
            data.get(
                'salary',
                0
            ) or 0
        )
    )

    db.session.add(teacher)

    db.session.commit()

    return jsonify({

        "message":
            "Teacher added successfully"

    }), 201