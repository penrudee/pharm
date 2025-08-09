from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
login = LoginManager()

migrate = Migrate(app, db)


# db.init_app(app)
login.init_app(app)
login.login_view = 'login'

# from app import routes
# app.register_blueprint(routes.bp)
    
# with app.app_context():
#     db.create_all()
from app import routes,models
