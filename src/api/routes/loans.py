from flask import Blueprint, request
from api.utils.responses import response_with
from api.utils import responses as resp
from api.models.loans import Loan, LoanSchema
from api.utils.database import db

loan_routes = Blueprint("loan_routes", __name__)