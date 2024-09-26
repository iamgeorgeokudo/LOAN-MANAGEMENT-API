from flask import Blueprint

loans = Blueprint('loans', __name__)

from . import views