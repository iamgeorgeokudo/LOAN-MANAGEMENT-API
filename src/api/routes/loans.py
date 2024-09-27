from flask import Blueprint, request
from api.utils.responses import response_with
from api.utils import responses as resp
from api.models.loans import Loan, LoanSchema
from api.utils.database import db

loan_routes = Blueprint("loan_routes", __name__)

@loan_routes.route('/', methods=['GET'])
def get_loan_list():
    fetched = Loan.query.all()
    loan_schema = LoanSchema(many=True, only=['user_id',
    'loan_amount', 'loan_interest_rate', 'loan_term', 'loan_status', ])
    loans, error = loan_schema.dump(fetched)

    return response_with(resp.SUCCESS_200, value={"loans": loans})

@loan_routes.route('/<int:id>', methods=['GET'])
def get_loan_detail(id):
    fetched = Loan.query.get_or_404(id)
    loan_schema = LoanSchema()
    loans, error = loan_schema.dump(fetched)
    
    return response_with(resp.SUCCESS_200, value={"loans": loans})

