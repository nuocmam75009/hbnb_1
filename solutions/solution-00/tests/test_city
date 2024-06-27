import unittest
from src.models.city import City
from unittest.mock import patch
from src.models.country import Country
from django.db import IntegrityError

# Patching Country model and persistence layer (repo)
@patch('src.models.city.Country.get')
@patch('src.models.city.repo.save')
@patch('src.models.city.repo.update')
class TestCityModel(unittest.TestCase):

    def test_create_city_valid_data(self, mock_repo_update, mock_repo_save, mock_country_get):
        # Tests creating a new City object with valid data"""
        data = {"name": "New York", "country_code": "US"}
        mock_country_get.return_value = Country()  # Simulate successful country lookup
        city = City.create(data)
        self.assertIsNotNone(city)
        self.assertEqual(city.name, data["name"])
        self.assertEqual(city.country_code, data["country_code"])
        mock_repo_save.assert_called_once()  # Verify repo.save is called

    def test_create_city_invalid_country(self, mock_repo_update, mock_repo_save, mock_country_get):
        # Tests creating a City object with an invalid country code"""
        data = {"name": "New York", "country_code": "XX"}
        mock_country_get.return_value = None  # Simulate unsuccessful country lookup
        with self.assertRaises(ValueError):
            City.create(data)
        mock_repo_save.assert_not_called()  # Verify repo.save is not called

    def test_update_city(self, mock_repo_update, mock_repo_save, mock_country_get):
        # Tests updating an existing City object
        data = {"name": "New City Name"}
        city = City(name="Old Name", country_code="US")
        updated_city = City.update(str(city.id), data)
        self.assertEqual(updated_city.name, data["name"])
        mock_repo_update.assert_called_once()  # Verify repo.update is called

    def test_update_city_error(self, mock_repo_update, mock_country_get):
            # Tests updating a City object with a database error"""
            data = {"name": "New City Name"}
            city = City(name="Old Name", country_code="US")
            mock_repo_update.side_effect = IntegrityError  # Simulate database integrity error

            with self.assertRaises(ValueError) as e:
                City.update(str(city.id), data)
            self.assertIn("Error updating city", str(e.exception))
            mock_repo_update.assert_called_once()  # Verify repo.update is called
