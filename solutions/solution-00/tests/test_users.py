import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from unittest.mock import patch
from src.models.user import User

class TestUserModel(unittest.TestCase):
    def test_create_user_valid_data(self):
        # Tests creating a new User object with valid data
        data = {
            "email": "test@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "password": "password123",
            "is_admin": False
        }
        with patch("src.models.user.User.get_all") as mock_get_all, \
             patch("src.models.user.repo.save") as mock_repo_save:
            mock_get_all.return_value = []
            user = User.create(data)
            self.assertIsNotNone(user)
            self.assertEqual(user.email, data["email"])
            self.assertEqual(user.first_name, data["first_name"])
            self.assertEqual(user.last_name, data["last_name"])
            self.assertEqual(user.password, data["password"])
            self.assertEqual(user.is_admin, data["is_admin"])
            mock_repo_save.assert_called_once()

    def test_create_user_existing_email(self):
        # Tests creating a User object with an existing email
        data = {
            "email": "test@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "password": "password123",
            "is_admin": False
        }
        existing_user = User(email="test@example.com")
        with patch("src.models.user.User.get_all") as mock_get_all:
            mock_get_all.return_value = [existing_user]
            with self.assertRaises(ValueError):
                User.create(data)

    def test_update_user(self):
        # Tests updating an existing User object
        user_id = "123"
        data = {
            "email": "updated@example.com",
            "first_name": "Jane",
            "last_name": "Smith"
        }
        user = User(email="test@example.com", first_name="John", last_name="Doe")
        with patch("src.models.user.User.get") as mock_get, \
             patch("src.models.user.repo.update") as mock_repo_update:
            mock_get.return_value = user
            updated_user = User.update(user_id, data)
            self.assertEqual(updated_user.email, data["email"])
            self.assertEqual(updated_user.first_name, data["first_name"])
            self.assertEqual(updated_user.last_name, data["last_name"])
            mock_repo_update.assert_called_once()

    def test_update_user_not_found(self):
        # Tests updating a User object that does not exist
        user_id = "123"
        data = {
            "email": "updated@example.com",
            "first_name": "Jane",
            "last_name": "Smith"
        }
        with patch("src.models.user.User.get") as mock_get:
            mock_get.return_value = None
            updated_user = User.update(user_id, data)
            self.assertIsNone(updated_user)


if __name__ == "__main__":
    unittest.main()