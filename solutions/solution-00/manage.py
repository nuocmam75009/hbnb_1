""" Entry point for the application. """

from flask.cli import FlaskGroup
from src import create_app


cli = FlaskGroup(create_app=create_app)


if __name__ == "__main__":
    cli()
