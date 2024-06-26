""" Another way to run the app"""

from src import create_app
from flask_sqlalchemy import SQLAlchemy
from flask import Flask


app = create_app()

if __name__ == "__main__":
    app.run()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///development.db'
db = SQLAlchemy(app)