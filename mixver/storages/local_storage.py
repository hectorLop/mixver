import os
import pickle
from ctypes import Union
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict

from mixver.versioning.versioner import Versioner


@dataclass(frozen=True)
class LocalStorage:
    """
    Local storage to version ML models.

    Attributes:
        _storage_path (str): Local path to use as storage.
        _versioner (Versioner): Artifacts versioning manager.
    """

    _storage_path: str
    _versioner: Versioner = field(init=False)

    def __post_init__(self) -> None:
        """
        Create the storage.
        """
        # TODO: Handle complex paths or random names
        if not os.path.isdir(self._storage_path):
            os.mkdir(self._storage_path)

        self._versioner = Versioner(storage_path=self._storage_path)

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

    def push(
        self, artifact: Any, name: str, metadata: Dict, tags: list[str] = []
    ) -> None:
        """
        Save data into the storage.
        """
        data = {
            "artifact": artifact,
            "metadata": metadata,
        }

        filename = self._versioner.add_artifact(name=name, tags=tags)

        # TODO: Check that the path is valid and ends up with a .pkl
        with open(f"{filename}.pkl", "wb") as file:
            pickle.dump(data, file)

    def pull(self, name: str, identifier: Union[str, int]) -> Dict:
        """
        Retrieve data from the storage.
        """
        if isinstance(identifier, int):
            filename = self._versioner.get_artifact_by_version(
                name=name, version=str(identifier)
            )
        elif isinstance(identifier, str):
            filename = self._versioner.get_artifact_by_tag(name=name, tag=identifier)
        else:
            message = (
                "The identifier must be an integer to identify an artifact by its version or "
                "a string to identify the artifact by its tag."
            )
            raise ValueError(message)

        with open(f"{filename}.pkl", "rb") as file:
            data = pickle.load(file)

        return data
