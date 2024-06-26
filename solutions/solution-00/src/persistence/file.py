"""
This module exports a Repository that persists data in a JSON file
"""

from datetime import datetime
import json
from src.models.base import Base
from src.persistence.repository import Repository
from utils.constants import FILE_STORAGE_FILENAME


class FileRepository(Repository):
    # File Repository with conditional persistence logic

    def __init__(self, storage_type: str = 'file') -> None:
        # Initialize repo with optional storage type
        # Default: file-based
        self.storage_type = storage_type
        self.__data = {}

        if self.storage_type == "file":
            self.reload()

    def _save_to_file(self):
        # Helper method to save data to JSON (file-based storage)
        serialized = {
            k: [v.to_dict() for v in l if type(v) is not dict]
            for k, l in self.__data.items()
        }

        with open(FILE_STORAGE_FILENAME, "w") as file:
            json.dump(serialized, file)

    def _save_to_db(self, data: Base, session):
        # Saves obj to the DB for DB storage
        session.add(data)
        session.commit()

    def get_all(self, model_name: str):
        """Get all objects of a given model"""
        if self.storage_type == "file":
            return self.__data.get(model_name, [])
        elif self.storage_type == "database":
            raise NotImplementedError("Database retrieval not implemented")
        else:
            raise ValueError("Invalid storage type: {}".format(self.storage_type))

    def get(self, model_name: str, obj_id: str):
        # Get object by ID
        if self.storage_type == "file":
            for obj in self.getall(model_name):
                if obj.id == obj_id:
                    return obj
                return None
        elif self.storage_type == "database":
            # Delegate to DB retrieval logic by Id
            raise NotImplementedError("Database retrieval not implemented.")
        else:
            raise ValueError("Invalid storage type {}".format(self.storage_type


                                                              ))
    def reload(self):
        # Reloads the data from the file (only for filebased)
        if self.storage_type == "file":
            file_data = {}
            try:
                with open(FILE_STORAGE_FILENAME, "r") as file:
                    file_data = json.load(file)
            except FileNotFoundError:
                pass
            self.__data = file_data


        from src.models.amenity import Amenity, PlaceAmenity
        from src.models.city import City
        from src.models.country import Country
        from src.models.place import Place
        from src.models.review import Review
        from src.models.user import User

        models = {
            "amenity": Amenity,
            "city": City,
            "country": Country,
            "place": Place,
            "placeamenity": PlaceAmenity,
            "review": Review,
            "user": User,
        }

        for model, data in file_data.items():
            for item in data:
                instance: Base = models[model](**item)

                if "created_at" in item:
                    instance.created_at = datetime.fromisoformat(
                        item["created_at"]
                    )
                if "updated_at" in item:
                    instance.updated_at = datetime.fromisoformat(
                        item["updated_at"]
                    )

                self.save(data=instance, save_to_file=False)

    def save(self, data: Base, save_to_file=True):
        # Save an object to the repository
        model: str = data.__class__.__name__.lower()

        if model not in self.__data:
            self.__data[model] = []

        self.__data[model].append(data)

        if self.storage_type == "file" and save_to_file:
            self._save_to_file()
        elif self.storage_type == "database":
            raise NotImplementedError("Database storage not implemented.")
        else:
            raise ValueError("Invalid storage type: {}".format(self.storage_type))

    def update(self, obj: Base):
        # Update an object in the repository"""
        cls = obj.__class__.__name__.lower()

        for i, o in enumerate(self.__data[cls]):
            if o.id == obj.id:
                obj.updated_at = datetime.now()
                self.__data[cls][i] = obj

                if self.storage_type == "file":
                    self._save_to_file()
                elif self.storage_type == "database":
                    raise NotImplementedError("Database storage not implemented.")
                return obj
            return

    def delete(self, obj: Base):
        # Delete an object from the repository

        class_name = obj.__class__.__name__.lower()

        if obj not in self.__data[class_name]:
            return False
        self.__data[class_name].remove(obj)

        if self.storage_type == "file":
            self._save_to_file()
        elif self.storage_type == "database":
            raise NotImplementedError("Database storage not implemented.")
            return obj
        return
