from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from . import db, ma

# Role class
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    users = db.relationship('User', backref='role', lazy='dynamic')

# User class
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(64), nullable=False)
    public_id = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(13), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# Loan Class
class Loan(db.Model):
    __tablename__ = 'loans'
    id = db.Column(db.Integer, primary_key=True)
    borrower_name = db.Column(db.String(100), db.ForeignKey('users.fullname'), nullable=False)
    #user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    loan_amount = db.Column(db.Float, nullable=False)
    interest_rate = db.Column(db.Float, nullable=False)
    loan_term = db.Column(db.Integer, nullable=False) # in months
    loan_status = db.Column(db.String(64), nullable=False, default='Pending')
 
    

    def __init__(self, borrower_name, loan_amount, interest_rate, loan_term, loan_status):
        self.borrower_name = borrower_name
        self.loan_amount = loan_amount
        self.interest_rate = interest_rate
        self.loan_term = loan_term
        self.loan_status = loan_status

# Loan Schema
class LoanSchema(ma.Schema):
    class Meta:
        fields = ('id', 'borrower_name', 'loan_amount', 'interest_rate', 'loan_term', 'loan_status')
        
# Init schema
loan_schema = LoanSchema()
loans_schema = LoanSchema(many=True)


