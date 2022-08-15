import os
import pickle
from pathlib import Path
from typing import Any, Dict


class LocalStorage:
    """
    Local storage to version ML models.

    Args:
        storage_path (str): Local path to use as storage.

    Attributes:
        _storage_path (str): Local path to use as storage.
    """

    def __init__(self, storage_path: str) -> None:
        self._storage_path = storage_path
        self._create_storage()

    @property
    def storage_path(self):
        """Getter for _storage_path."""
        return self._storage_path

    def _create_storage(self) -> str:
        """
        Assign a folder to be used as the local storage.

        Args:
            path (str): Storage path.
        """
        # TODO: Handle complex paths or random names
        if not os.path.isdir(self._storage_path):
            os.mkdir(self._storage_path)

    def push(self, artifact: Any, path: str, metadata: Dict) -> None:
        """
        Save data into the storage.
        """
        data = {
            "artifact": artifact,
            "metadata": metadata,
        }
        # TODO: Check that the path is valid and ends up with a .pkl
        with open(path, "wb") as file:
            pickle.dump(data, file)

    def pull(self, name: str) -> Dict:
        """
        Retrieve data from the storage.
        """
        path = Path(self._storage_path, name)

        with open(path, "rb") as file:
            data = pickle.load(file)

        return data
