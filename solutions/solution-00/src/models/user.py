from src.models.base import Base
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from flask import jsonify

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "Users"

    id = db.Column(db.String(36), primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)  # Ensure secure storage
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp(), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

#  Modify login process to include role information in the JWT.
def login(self) -> str:
        additional_claims = {"is_admin": self.is_admin}
        access_token = create_access_token(identity=self.id, additional_claims=additional_claims)
        return jsonify(access_token=access_token)


def set_password(self, password: str) -> str:
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

def check_password(self, password: str) -> str:
        return bcrypt.check_password_hash(self.password_hash, password)

def __repr__(self) -> str:

    return f"<User {self.id} ({self.email})>"

def to_dict(self) -> dict:
        #Dictionary representation of the object
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

@staticmethod
def create(user: dict) -> "User":
        """Create a new user"""
        from src.persistence import repo

        users: list["User"] = User.get_all()

        for u in users:
            if u.email == user["email"]:
                raise ValueError("User already exists")

        new_user = User(**user)

        repo.save(new_user)

        return new_user

@staticmethod
def update(user_id: str, data: dict) -> "User | None":
        """Update an existing user"""
        from src.persistence import repo

        user: User | None = User.get(user_id)

        if not user:
            return None

        if "email" in data:
            user.email = data["email"]
        if "first_name" in data:
            user.first_name = data["first_name"]
        if "last_name" in data:
            user.last_name = data["last_name"]

        repo.update(user)

        return user
