# Initialize flask app
import os
import logging
import sys
import api.utils.responses as resp
from flask import Flask,jsonify
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint
from flask_jwt_extended import JWTManager
from api.utils.database import db, ma
from api.utils.responses import response_with
from api.utils.email import mail
from api.config.config import ProductionConfig, TestingConfig, DevelopmentConfig 
from api.routes.users import user_routes
from api.routes.loans import loan_routes


app = Flask(__name__)

if os.environ.get('WORK_ENV') == 'PROD':
    app_config = ProductionConfig

elif os.environ.get('WORK_ENV') == 'TEST':
    app_config = TestingConfig

else:
    app_config = DevelopmentConfig

app.config.from_object(app_config)

db.init_app(app)
ma.init_app(app)
jwt = JWTManager(app)
mail.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(user_routes, url_prefix='/api/users')
app.register_blueprint(loan_routes, url_prefix='/api/loans')

#GLOBAL HTTP CONFIGURATIONS
@app.after_request
def add_header(response):
    return response
    
@app.errorhandler(400)
def bad_request(e):
    logging.error(e)
    return response_with(resp.BAD_REQUEST_400)
    
@app.errorhandler(500)
def server_error(e):
    logging.error(e)
    return response_with(resp.SERVER_ERROR_500)
    
@app.errorhandler(404)
def not_found(e):
    logging.error(e)
    return response_with(resp. SERVER_ERROR_404)

    db.__init__(app)

    with app.app_context():
        db.create_all()
    
    return app


# Serves API specs
@app.route("/api/spec")
def spec():
    swag = swagger(app, prefix='/api')
    swag['info']['base'] = "http://localhost:5000"
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "PEZIKA Loan Management API"
    return jsonify(swag)

# Initiate swagger ui
swaggerui_blueprint = get_swaggerui_blueprint('/api/docs', '/api/spec', config={'app_name': "PEZIKA Loan Management API"})
app.register_blueprint(swaggerui_blueprint, url_prefix='/api/docs')


if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0", use_reloader=False)