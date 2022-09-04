import os
import pickle
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Union

from mixver.versioning.versioner import Versioner


@dataclass
class LocalStorage:
    """
    Local storage to version ML models.

    Attributes:
        storage_path (str): Local path to use as storage.
        _versioner (Versioner): Artifacts versioning manager.
    """

    storage_path: str
    _versioner: Versioner = field(init=False)

    def __post_init__(self) -> None:
        """
        Create the storage.
        """
        # TODO: Handle complex paths or random names
        if not os.path.isdir(self.storage_path):
            os.mkdir(self.storage_path)

        self._versioner = Versioner(storage_path=self.storage_path)

    def _create_storage(self) -> str:
        """
        Assign a folder to be used as the local storage.

        Args:
            path (str): Storage path.
        """
        # TODO: Handle complex paths or random names
        if not os.path.isdir(self.storage_path):
            os.mkdir(self.storage_path)

    def push(
        self, artifact: Any, name: str, metadata: Dict, tags: list[str] = []
    ) -> str:
        """
        Save data into the storage.
        """
        data = {
            "artifact": artifact,
            "metadata": metadata,
        }

        filename = self._versioner.add_artifact(name=name, tags=tags)

        with open(Path(self.storage_path, f"{filename}.pkl"), "wb") as file:
            pickle.dump(data, file)

        return filename

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

        with open(Path(self.storage_path, f"{filename}.pkl"), "rb") as file:
            data = pickle.load(file)

        return data
