from app import db, ma
from marshmallow import fields

# Loan class
class Loan(db.Model):
    __tablename__ = 'loans'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    interest_rate = db.Column(db.Float, nullable=False)
    loan_term = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String, default='Pending')
    due_date = db.Column(db.Date, nullable=False)

    def __init__(self, user_id, amount, interest_rate, loan_term, status, due_date):
        self.user_id = user_id
        self.amount = amount
        self.interest_rate = interest_rate
        self.loan_term = loan_term
        self.status = status
        self.due_date = due_date

class LoanSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Loan
        load_instance = True
        sqla_session = db.session
        include_fk = True


loan_schema = LoanSchema()

# Class User
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    national_id = db.Column(db.Integer, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    loans = db.relationship('Loan', backref='user', lazy='dynamic')

    def __init__(self, first_name, last_name, national_id, password_hash):
        self.first_name = first_name
        self.last_name = last_name
        self.national_id = national_id
        self.password_hash = password_hash

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session

user_schema = UserSchema()

