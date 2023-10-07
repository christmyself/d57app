import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY' ,'hard to guess string')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #MAIL_SERVER = os.environ.get('MAIL_SERVER','smtp.office365.com')
    MAIL_SERVER = os.environ.get('MAIL_SERVER','smtp.exmail.qq.com')
    #MAIL_PORT = os.environ.get('MAIL_PORT',587)
    MAIL_PORT = os.environ.get('MAIL_PORT',465)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME','zhangchi@d57.games')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD','1q2w3e4r')
    D57_MAIL_SUBJECT_PREFIX = '[D57-Team]'
    D57_MAIL_SENDER = 'D57 Team <zhangchi@d57.games>'
    D57_ADMIN = os.environ.get('D57_ADMIN')

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
#    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL','mysql+pymysql://root:1q2w3e4r@localhost:3306/d57app-dev')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite://'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL','mysql+pymysql://root:1q2w3e4r@localhost:3306/d57app')
#    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
class DockerConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # 把日志输出到stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'docker': DockerConfig,

    'default': ProductionConfig
}
