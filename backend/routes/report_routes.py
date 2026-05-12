from flask import Blueprint, Response

from models.student_model import Student

import csv

report_bp = Blueprint('report', __name__)

@report_bp.route('/students-csv', methods=['GET'])
def export_students_csv():

    students = Student.query.all()

    def generate():

        data = csv.writer()

        yield ','.join([
            'Name',
            'Admission Number',
            'Class',
            'Pending Fees'
        ]) + '\n'

        for student in students:

            yield ','.join([
                student.full_name,
                student.admission_number,
                student.current_class,
                str(student.remaining_amount)
            ]) + '\n'

    return Response(
        generate(),
        mimetype='text/csv',
        headers={
            "Content-Disposition":
            "attachment;filename=students_report.csv"
        }
    )