import unittest
from src.models.country import Country
from unittest.mock import patch

if __name__ == '__main__':
    unittest.main()


# Patching persistence layer (repo)
@patch('src.models.country.repo.get_all')
@patch('src.models.country.repo.save')
class TestCountryModel(unittest.TestCase):

    def test_get_all_countries(self, mock_repo_get_all, mock_repo_save):
        # Tests retrieving all countries
        expected_countries = [Country(name="France", code="FR"), Country(name="USA", code="US")]
        mock_repo_get_all.return_value = expected_countries
        countries = Country.get_all()
        self.assertEqual(countries, expected_countries)
        mock_repo_get_all.assert_called_once()  # Verify repo.get_all is called

    def test_get_country_by_code(self, mock_repo_get_all, mock_repo_save):
        # Tests retrieving a country by its code
        mock_repo_get_all.return_value = [Country(name="France", code="FR"), Country(name="USA", code="US")]
        country = Country.get("US")
        self.assertIsNotNone(country)
        self.assertEqual(country.code, "US")

    def test_get_country_by_nonexistent_code(self, mock_repo_get_all, mock_repo_save):
        # Tests retrieving a country with a non-existent code
        mock_repo_get_all.return_value = [Country(name="France", code="FR"), Country(name="USA", code="US")]
        country = Country.get("XX")
        self.assertIsNone(country)

    def test_create_country(self, mock_repo_get_all, mock_repo_save):
        # Tests creating a new country
        country_data = {"name": "Canada", "code": "CA"}
        mock_repo_save.return_value = True  # Simulate successful save
        country = Country.create(**country_data)
        self.assertIsNotNone(country)
        self.assertEqual(country.name, country_data["name"])
        self.assertEqual(country.code, country_data["code"])
        mock_repo_save.assert_called_once_with(country)  # Verify repo.save is called with the Country object
