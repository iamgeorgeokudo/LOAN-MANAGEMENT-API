from api.utils.database import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from datetime import datetime

class Loan(db.Model):
    __tablename__ = 'loans'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    loan_amount = db.Column(db.Float, nullable=False)
    interest_rate = db.Column(db.Float, nullable=False)
    loan_term = db.Column(db.Integer, nullable=False) # in months
    loan_status = db.Column(db.String(64), nullable=False, default='Pending')
    #due_date = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


    def __init__(self, loan_amount, interest_rate, loan_term, loan_status,user_id=None):
        self.loan_amount = loan_amount
        self.interest_rate = interest_rate
        self.loan_term = loan_term
        self.loan_status = loan_status
        self.user_id = user_id

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    
class LoanSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema):
        model = Loan
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    loan_amount = fields.Float(required=True)
    loan_interest_rate = fields.Float(required=True)
    loan_term = fields.Integer(required=True)
    loan_status = fields.String(required=True)
    user_id = fields.Integer()
    