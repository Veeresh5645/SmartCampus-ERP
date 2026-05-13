from flask import Blueprint, request, jsonify

from database.db import db

from models.expense_model import Expense

accounting_bp = Blueprint(
    'accounting',
    __name__
)


# ADD EXPENSE
@accounting_bp.route(
    '/add-expense',
    methods=['POST']
)
def add_expense():

    try:

        data = request.get_json()

        expense = Expense(

            category=data.get(
                'category'
            ),

            amount=float(
                data.get(
                    'amount',
                    0
                ) or 0
            ),

            comment=data.get(
                'comment'
            ),

            expense_date=data.get(
                'expense_date'
            )
        )

        db.session.add(expense)

        db.session.commit()

        return jsonify({

            "message":
                "Expense added successfully"

        }), 201

    except Exception as e:

        print(e)

        return jsonify({
            "error": str(e)
        }), 500


# GET EXPENSES
@accounting_bp.route(
    '/expenses',
    methods=['GET']
)
def get_expenses():

    try:

        expenses = Expense.query.all()

        output = []

        for expense in expenses:

            output.append({

                "id": expense.id,

                "category":
                    expense.category,

                "amount":
                    expense.amount,

                "comment":
                    expense.comment,

                "expense_date":
                    expense.expense_date
            })

        return jsonify(output)

    except Exception as e:

        print(e)

        return jsonify({
            "error": str(e)
        }), 500