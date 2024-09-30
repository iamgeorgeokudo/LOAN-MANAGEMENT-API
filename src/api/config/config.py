import  os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI =  'sqlite:///' + os.path.join(basedir, 'prod_db.sqlite')

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'dev_db.sqlite')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI =  'sqlite://'
    SQLALCHEMY_ECHO = False
    TESTING = True
    JWT_SECRET_KEY = 'jwt-secret'
    SECRET_KEY = 'secret'
    SECURITY_PASSWORD_SALT= 'PASSWORD-SALT'
    MAIL_DEFAULT_SENDER= 'zonicahbirgen@gmail.com'
    MAIL_SERVER= 'smtp.gmail.com'
    MAIL_PORT= 465
    MAIL_USERNAME= 'zonicahbirgen@gmail.com'
    MAIL_PASSWORD= "musa2580."
    MAIL_USE_TLS= False
    MAIL_USE_SSL= True

# itsdangerous keys
SECRET_KEY = 'abc4$'
SECURITY_PASSWORD_SALT = 'abc4$'
MAIL_DEFAULT_SENDER = 'zonicahbirgen@gmail.com'
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USERNAME = 'zonicahbirgen@gmail.com'
MAIL_PASSWORD = 'musa2580.'
MAIL_USE_TLS = False
MAIL_USE_SSL = True