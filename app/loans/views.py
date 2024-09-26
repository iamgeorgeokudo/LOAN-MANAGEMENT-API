from flask import request, jsonify
from flask_jwt_extended import jwt_required
from . import loans
from ..models import Loan, db, loan_schema, loans_schema
from ..utils.helpers import calculate_monthly_repayment, calculate_total_repayment

#create loan
@loans.route('/loan', methods=['POST'])
#@jwt_required()
def create_loan():
    data = request.get_json()
    
    new_loan = Loan(

        borrower_name=data['borrower_name'],
        loan_amount=data['loan_amount'],
        interest_rate=data['interest_rate'],
        loan_term=data['loan_term'],
        loan_status=data['loan_status']
        )

    db.session.add(new_loan)
    db.session.commit()

    return loan_schema.jsonify(new_loan), 201

# get all loans
@loans.route('/get_loans', methods=['GET'])
#@jwt_required()
def get_loans():
    loans = Loan.query.all()
    result = loans_schema.dump(loans)
    return jsonify(result), 200

# get single loan
@loans.route('/get_loan/<int:id>', methods=['GET'])
#@jwt_required()
def get_loan(id):
    loan = Loan.query.get_or_404(id)
    return loan_schema.jsonify(loan), 200

#update loan
@loans.route('/update_loan/<int:id>', methods=['PUT'])
#@jwt_required()
def update_loan(id):
    loan = Loan.query.get_or_404(id)
    
    borrower_name = request.json['borrower_name']
    loan_amount = request.json['loan_amount']
    interest_rate = request.json['interest_rate']
    loan_term = request.json['loan_term']
    loan_status = request.json['loan_status']

    loan.borrower_name = borrower_name
    loan.loan_amount = loan_amount
    loan.interest_rate = interest_rate
    loan.loan_term = loan_term
    loan.loan_status = loan_status

    db.session.commit()

    return loan_schema.jsonify(loan_schema), 200

# delete loan
@loans.route('/delete_loan/<int:id>', methods=['DELETE'])
#@jwt_required()
def delete_loan(id):
    loan = Loan.query.get_or_404(id)
    db.session.delete(loan)
    db.session.commit()

    return loan_schema.jsonify(loan), 200

# calculate monthly repaymenet
@loans.route('/loan/<int:id>/calculate_repayment', methods=['GET'])
@jwt_required()
def calculate_loan(id):
    loan = Loan.query.get_or_404(id)
    total_repayment = calculate_total_repayment(loan.loan_amount, loan.interest_rate, loan.loan_term)
    monthly_repayment = calculate_monthly_repayment(loan.loan_amount, loan.interest_rate, loan.loan_term)
    return jsonify({
        'total_repayment': total_repayment, 
        'monthly_repayment':monthly_repayment
        }), 200

# update_status
@loans.route('/loan/<int:id>/status', methods=['PUT'])
@jwt_required()
def update_loan_status(id):
    loan = Loan.query.get_or_404(id)
    data = request.get_json()
    loan.loan_status = data['loan_status']
    db.session.commit()
    return jsonify(loan.to_dict()), 200