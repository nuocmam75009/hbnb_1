import unittest
from src.models.amenity import Amenity

class TestAmenityModel(unittest.TestCase):

    def test_create_amenity(self):
        """Tests creating a new Amenity object"""
        data = {"name": "Wi-Fi"}
        amenity = Amenity.create(data)
        self.assertIsNotNone(amenity)
        self.assertEqual(amenity.name, data["name"])

    def test_amenity_to_dict(self):
        """Tests converting Amenity object to dictionary"""
        data = {"name": "Wi-Fi"}
        amenity = Amenity(**data)
        amenity_dict = amenity.to_dict()
        self.assertEqual(amenity_dict["name"], data["name"])
        # You can add further assertions to validate other fields in the dictionary

