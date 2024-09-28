from flask import Blueprint, request
from api.utils.responses import response_with
from api.utils import responses as resp
from api.models.loans import Loan, LoanSchema
from api.utils.database import db

loan_routes = Blueprint("loan_routes", __name__)

# view all loans
@loan_routes.route('/', methods=['GET'])
def get_loan_list():
    fetched = Loan.query.all()
    loan_schema = LoanSchema(many=True, only=['user_id',
    'loan_amount', 'loan_interest_rate', 'loan_term', 'loan_status', ])
    loans, error = loan_schema.dump(fetched)

    return response_with(resp.SUCCESS_200, value={"loans": loans})

# get loan detail
@loan_routes.route('/<int:id>', methods=['GET'])
def get_loan_detail(id):
    fetched = Loan.query.get_or_404(id)
    loan_schema = LoanSchema()
    loans, error = loan_schema.dump(fetched)
    
    return response_with(resp.SUCCESS_200, value={"loans": loans})

# update loan detail

@loan_routes.route('/<int:id>', methods=['PUT'])
def update_loan_detail():
    data = request.get_json()
    get_loan = Loan.query.get_or_404(id) 
    get_loan.loan_amount = data['loan_amount']
    get_loan.loan_interest_rate = data['loan_interest_rate']
    get_loan.loan_term = data['loan_term']
    get_loan.loan_status = data['loan_status']
    db.session.add(get_loan)
    db.session.commit()
    loan_schema = LoanSchema()
    loan, error = loan_schema.dump(get_loan)
    return response_with(resp.SUCCESS_200, value={"loan": loan})

# modify loan
@loan_routes.route('/<int:id>', methods=['PATCH'])
def modify_loan_detail(id):
    data = request.get_json()
    get_loan = Loan.query.get_or_404(id)
    if data.get('loan_amount'):
        get_loan.loan_amount = data['loan_amount']
    if data.get('loan_interest_rate'):
        get_loan.loan_interest_rate = data['loan_interest_rate']
    if data.get('loan_term'):
            get_loan.loan_term = data['loan_term']
    if data.get('loan_status'):
            get_loan.loan_status = data['loan_status']
    db.session.add(get_loan)
    db.session.commit()
    loan_schema = LoanSchema()
    loan, error = loan_schema.dump(get_loan)
    return response_with(resp.SUCCESS_200, value={"loan": loan})
    

# delete loan
@loan_routes.route('/<int:id>', methods=['DELETE'])
def delete_loan(id):
    get_loan = Loan.query.get_or_404(id)
    db.session.delete(get_loan)
    db.session.commit()
    return response_with(resp.SUCCESS_204)