""" Another way to run the app"""

from src import create_app
from flask_sqlalchemy import SQLAlchemy, create_engine
from flask import Flask
from sqlalchemy.orm import sessionmaker
from flask_jwt_extended import JWTManager
import secrets
from src import create_app
from flask_sqlalchemy import SQLAlchemy, create_engine
from flask import Flask
from sqlalchemy.orm import sessionmaker
from flask_jwt_extended import JWTManager
import secrets

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///development.db'
db = SQLAlchemy(app)

app = create_app()

app.config['JWT_SECRET_KEY'] = secrets.token_urlsafe(16)
print(app.config['JWT_SECRET_KEY'])
jwt = JWTManager(app)

if __name__ == "__main__":
    app.run()