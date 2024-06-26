from src.models.base import Base
from src.models.place import Place
from src.models.user import User
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Review(db.Model):
    __tablename__ = "Reviews"

    place_id = db.Column(db.String(36), primary_key=True, nullable=False)
    user_id = db.Column(db.String(36), nullable=False)
    comment = db.Column(db.String(2000))
    rating = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp(), nullable=False)

    def __repr__(self) -> str:

        return f"<Review {self.id} - '{self.comment[:25]}...'>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "place_id": self.place_id,
            "user_id": self.user_id,
            "comment": self.comment,
            "rating": self.rating,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def create(data: dict) -> "Review":
        """Create a new review"""
        from src.persistence import repo

        user: User | None = User.get(data["user_id"])

        if not user:
            raise ValueError(f"User with ID {data['user_id']} not found")

        place: Place | None = Place.get(data["place_id"])

        if not place:
            raise ValueError(f"Place with ID {data['place_id']} not found")

        new_review = Review(**data)

        repo.save(new_review)

        return new_review

    @staticmethod
    def update(review_id: str, data: dict) -> "Review | None":
        """Update an existing review"""
        from src.persistence import repo

        review = Review.get(review_id)

        if not review:
            raise ValueError("Review not found")

        for key, value in data.items():
            setattr(review, key, value)

        repo.update(review)

        return review
