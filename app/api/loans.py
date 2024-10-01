from flask import request, jsonify
from app import db
from . import api
from ..models import Loan, loan_schema
from datetime import datetime
from marshmallow import ValidationError

# Create loan
@api.route('/loan', methods=['POST'])
def create_loan():
     # Get the data from the request
    data = request.get_json()

    # Extract individual fields
    user_id = data.get('user_id')
    amount = data.get('amount')
    interest_rate = data.get('interest_rate')
    loan_term = data.get('loan_term')
    status = data.get('status', 'Pending')  # Default to 'Pending' if not provided
    due_date_str = data.get('due_date')

    # Convert due_date to datetime
    try:
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format, expected YYYY-MM-DD'}), 400

    # Validate required fields
    if not user_id or not amount or not interest_rate or not loan_term or not due_date:
        return jsonify({'error': 'Missing required fields'}), 400

    # Create a new Loan object
    new_loan = Loan(user_id=user_id, amount=amount, interest_rate=interest_rate, loan_term=loan_term, status=status, due_date=due_date)

    # Add the new loan to the session
    db.session.add(new_loan)
    db.session.commit()

    # Return the newly created loan as a response
    return loan_schema.jsonify(new_loan), 201

# Get all loans
@api.route('/loan', methods=['GET'])
def get_loans():
    all_loans = Loan.query.all()
    result = loan_schema.dump(all_loans,many=True)
    return jsonify(result), 200


# Get Single loan for a user
@api.route('/loan/<int:id>', methods=['GET'])
def get_loan(id):

    loan = Loan.query.get(id)

    # If loan is not found, return a 404 error
    if not loan:
        return jsonify({'error': 'Loan not found'}), 404

    # Serialize the loan data
    result = loan_schema.dump(loan)

    # Return the loan as a JSON response
    return jsonify(result), 200

# update loan
@api.route('/users/<int:user_id>/loans/<int:loan_id>', methods=['PUT'])
def update_loan(user_id, loan_id):
    # Query the database for the specific loan
    loan = Loan.query.filter_by(user_id=user_id, id=loan_id).first()

    # If loan is not found, return a 404 error
    if not loan:
        return jsonify({'error': 'Loan not found'}), 404

    # Get the data from the request
    data = request.get_json()

    # Update loan fields if present in the request
    loan.amount = data.get('amount', loan.amount)
    loan.interest_rate = data.get('interest_rate', loan.interest_rate)
    loan.loan_term = data.get('loan_term', loan.loan_term)
    loan.status = data.get('status', loan.status)

    # Handle due_date with date conversion
    due_date_str = data.get('due_date')
    if due_date_str:
        try:
            loan.due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid date format, expected YYYY-MM-DD'}), 400

    # Commit the changes to the database
    db.session.commit()

    # Serialize and return the updated loan
    return loan_schema.jsonify(loan), 200

# Delete loan
@api.route('/users/<int:user_id>/loans/<int:loan_id>', methods=['DELETE'])
def delete_loan(user_id, loan_id):
    # Query the database for the specific loan
    loan = Loan.query.filter_by(user_id=user_id, id=loan_id).first()

    # If loan is not found, return a 404 error
    if not loan:
        return jsonify({'error': 'Loan not found'}), 404

    # Delete the loan from the database
    db.session.delete(loan)
    db.session.commit()

    # Return a success message
    return jsonify({'message': f'Loan {loan_id} for user {user_id} has been deleted'}), 200

# Total repayment
# Total Repayment=Loan Amount+(Loan Amount×Interest Rate×Loan Term)
@api.route('/users/<int:user_id>/loans/<int:loan_id>/repayment', methods=['GET'])
def calculate_total_repayment(user_id, loan_id):
    # Query the database for the specific loan
    loan = Loan.query.filter_by(user_id=user_id, id=loan_id).first()

    # If loan is not found, return a 404 error
    if not loan:
        return jsonify({'error': 'Loan not found'}), 404

    # Calculate the total repayment using the simple interest formula
    total_repayment = loan.amount + (loan.amount * loan.interest_rate * loan.loan_term)

    # Return the total repayment amount as a JSON response
    return jsonify({
        'loan_id': loan_id,
        'user_id': user_id,
        'amount': loan.amount,
        'interest_rate': loan.interest_rate,
        'loan_term': loan.loan_term,
        'total_repayment': total_repayment
    }), 200

# Monthly repayment
@api.route('/users/<int:user_id>/loans/<int:loan_id>/monthly-repayment', methods=['GET'])
def calculate_monthly_repayment(user_id, loan_id):
    # Query the database for the specific loan
    loan = Loan.query.filter_by(user_id=user_id, id=loan_id).first()

    # If loan is not found, return a 404 error
    if not loan:
        return jsonify({'error': 'Loan not found'}), 404

    # Calculate total repayment using the simple interest formula
    total_repayment = loan.amount + (loan.amount * loan.interest_rate * (loan.loan_term / 12))  # assuming loan_term is in months

    # Calculate the monthly repayment
    monthly_repayment = total_repayment / loan.loan_term

    # Return the monthly repayment amount as a JSON response
    return jsonify({
        'loan_id': loan_id,
        'user_id': user_id,
        'amount': loan.amount,
        'interest_rate': loan.interest_rate,
        'loan_term': loan.loan_term,
        'total_repayment': total_repayment,
        'monthly_repayment': monthly_repayment
    }), 200


