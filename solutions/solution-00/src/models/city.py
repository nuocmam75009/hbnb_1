from src.models.base import Base
from src.models.country import Country
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from src.models.country import Country

db = SQLAlchemy()

class City(db.Model):
    __tablename__ = 'Cities'

    name = db.Column(db.String(255), nullable=False)
    code = db.Column(db.String(2), primary_key=True, nullable=False)
    country_code = db.Column(db.Integer, ForeignKey(Country.id), nullable=False)

    country = db.relationship("Country", backref="cities")

    def __init__(self, name: str, country_code: str, **kw) -> None:

        super().__init__(**kw)

        self.name = name
        self.country_code = country_code

    def __repr__(self) -> str:

        return f"<City {self.id} ({self.name})>"

    def to_dict(self) -> dict:
        # Dictionary representation of the object"""
        return {
            "id": self.id,
            "name": self.name,
            "country_code": self.country_code,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def create(data: dict) -> "City":
        # Create a new city
        from src.persistence import repo

        country = Country.get(data["country_code"])

        if not country:
            raise ValueError("Country not found")

        city = City(**data)

        repo.save(city)

        return city

    @staticmethod
    def update(city_id: str, data: dict) -> "City":
        # Update an existing city"""
        from src.persistence import repo

        city = City.get(city_id)

        if not city:
            raise ValueError("City not found")

        for key, value in data.items():
            setattr(city, key, value)

        repo.update(city)

        return city
