import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    ## localhost
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir,
                                                                                            'app.db')
    ## pythonanywhere.com
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://<user>:<pws>@Rygor.mysql.pythonanywhere-services.com/Rygor$app'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
