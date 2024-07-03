# Version: 1.0
from src import create_app
from flask_sqlalchemy import SQLAlchemy, create_engine
from flask import Flask
from flask_jwt_extended import JWTManager
import secrets
from dotenv import load_dotenv, dotenv_values
import os

load_dotenv()

app = Flask(__name__)
app = create_app()

# Set up a default secured SECRET_KEY if not provided by env
app.config.setdefault('SECRET_KEY', secrets.token_urlsafe(32))

# Config DB
app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///development.db'
db = SQLAlchemy(app)

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URL'])
db = SQLAlchemy(app, engine=engine)
app.config['DEBUG'] = False

# Config JWT
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', secrets.token_urlsafe(32))
jwt = JWTManager(app)

if __name__ == "__main__":
    app.run()
