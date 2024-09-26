from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from flask_bootstrap import Bootstrap
from config import config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
ma = Marshmallow()
bootstrap = Bootstrap()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    ma.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)
    
    # application blueprints

    # from .main import main as main_blueprint
    # app.register_blueprint(main_blueprint)

    from .loans import loans  as loans_blueprint
    app.register_blueprint(loans_blueprint)

    from .auth import auth  as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    

    from .utils import utils as utils_blueprint
    app.register_blueprint(utils_blueprint)

     
    return app

# with create_app('development').app_context():
#     db.create_all()
#     db.session.commit()
#     db.session.close()
#     print('Database created successfully')