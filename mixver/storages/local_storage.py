import os


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

    def push(self) -> None:
        """
        Save data into the storage.
        """

    def pull(self) -> None:
        """
        Retrieve data from the storage.
        """
