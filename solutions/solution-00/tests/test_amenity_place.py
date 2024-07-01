import unittest
from src.models.amenity import PlaceAmenity
from unittest.mock import patch

class TestPlaceAmenityModel(unittest.TestCase):

    # Assuming you have a way to mock or inject the persistence layer (repo)
    # for testing purposes

    @patch('src.models.place_amenity.repo.save')
    def test_create_place_amenity(self, mock_save):
        """Tests creating a new PlaceAmenity object"""
        data = {"place_id": "1", "amenity_id": "2"}
        place_amenity = PlaceAmenity.create(data)
        self.assertIsNotNone(place_amenity)
        mock_save.assert_called_once()  # Verify that repo.save is called

    @patch('src.models.place_amenity.repo.get_all')
    def test_get_place_amenity(self, mock_get_all):
        """Tests getting a PlaceAmenity by place and amenity IDs"""
        place_id = "1"
        amenity_id = "2"
        mock_get_all.return_value = [PlaceAmenity(place_id, amenity_id)]
        place_amenity = PlaceAmenity.get(place_id, amenity_id)
        self.assertIsNotNone(place_amenity)
        mock_get_all.assert_called_once()  # Verify that repo.get_all is called

    @patch('src.models.place_amenity.repo.delete')
    def test_delete_place_amenity(self, mock_delete):
        """Tests deleting a PlaceAmenity object"""
        place_id = "1"
        amenity_id = "2"
        PlaceAmenity.delete(place_id, amenity_id)
        mock_delete.assert_called_once()  # Verify that repo.delete is called

