from api.utils.database import db, ma
from passlib.hash import pbkdf2_sha256 as sha256
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from api.models.loans import LoanSchema

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True,)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    email = db.Column(db.String(30), unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    isVerified = db.Column(db.Boolean, default=False, nullable=False)
    loans = db.relationship('Loan', backref='User',
    cascade="all, delete-orphan")
    

    def __init__(self, first_name, last_name, email, password_hash, loans=[]):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password_hash = password_hash
        self.loans = loans

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email = email).first()
    
    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)
    
    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)
    
class UserSchema(SQLAlchemyAutoSchema):
    class Meta():
            model = User
            sqla_session = db.session

    id = fields.Number(dump_only=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.String(required=True)
    password_hash = fields.String(required=True)
    loans = fields.Nested(LoanSchema, many=True, only=['loan_amount',
    'loan_interest_rate',
    'loan_term',
    'loan_status'                                          
    ])

    
class UserSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema):
        model =User
        sql_session = db.session
    
    id = fields.Number(dump_only=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.String(required=True)
    password_hash = fields.String(required=True)