from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment
import gunicorn
import psycopg2

app = Flask(__name__)
login = LoginManager(app)
login.login_view = 'index'
app.config.from_object(Config)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
moment = Moment(app)

from app import routes, models


if __name__ == '__main__':
    app.run()