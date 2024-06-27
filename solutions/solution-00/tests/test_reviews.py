import unittest
from unittest.mock import patch
from src.models.review import Review
from src.models.place import Place
from src.models.user import User

class TestReviewModel(unittest.TestCase):
    def test_create_review_valid_data(self):
        # Tests creating a new Review object with valid data
        data = {
            "place_id": "123",
            "user_id": "456",
            "comment": "Great place!",
            "rating": 4.5
        }
        with patch("src.models.review.User.get") as mock_user_get, \
             patch("src.models.review.Place.get") as mock_place_get, \
             patch("src.models.review.repo.save") as mock_repo_save:
            mock_user_get.return_value = User()
            mock_place_get.return_value = Place()
            review = Review.create(data)
            self.assertIsNotNone(review)
            self.assertEqual(review.place_id, data["place_id"])
            self.assertEqual(review.user_id, data["user_id"])
            self.assertEqual(review.comment, data["comment"])
            self.assertEqual(review.rating, data["rating"])
            mock_repo_save.assert_called_once()

    def test_create_review_invalid_user(self):
        # Tests creating a Review object with an invalid user ID
        data = {
            "place_id": "123",
            "user_id": "456",
            "comment": "Great place!",
            "rating": 4.5
        }
        with patch("src.models.review.User.get") as mock_user_get:
            mock_user_get.return_value = None
            with self.assertRaises(ValueError):
                Review.create(data)

    def test_create_review_invalid_place(self):
        # Tests creating a Review object with an invalid place ID
        data = {
            "place_id": "123",
            "user_id": "456",
            "comment": "Great place!",
            "rating": 4.5
        }
        with patch("src.models.review.User.get") as mock_user_get, \
             patch("src.models.review.Place.get") as mock_place_get:
            mock_user_get.return_value = User()
            mock_place_get.return_value = None
            with self.assertRaises(ValueError):
                Review.create(data)

    def test_update_review(self):
        # Tests updating an existing Review object
        review_id = "789"
        data = {
            "comment": "Updated comment",
            "rating": 3.5
        }
        review = Review(place_id="123", user_id="456", comment="Great place!", rating=4.5)
        with patch("src.models.review.Review.get") as mock_review_get, \
             patch("src.models.review.repo.update") as mock_repo_update:
            mock_review_get.return_value = review
            updated_review = Review.update(review_id, data)
            self.assertEqual(updated_review.comment, data["comment"])
            self.assertEqual(updated_review.rating, data["rating"])
            mock_repo_update.assert_called_once()

    def test_update_review_not_found(self):
        # Tests updating a Review object that does not exist
        review_id = "789"
        data = {
            "comment": "Updated comment",
            "rating": 3.5
        }
        with patch("src.models.review.Review.get") as mock_review_get:
            mock_review_get.return_value = None
            with self.assertRaises(ValueError):
                Review.update(review_id, data)