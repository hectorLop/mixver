import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class Versioner:
    """
    Class that manages the artifacts versioning

    Attributes:
        storage_path (str): Path where to create the version and tag files.
        _version_file (str): Version filename.
        _tags_file (str): Tags filename.
    """

    storage_path: str
    _version_file: str = field(default=".versions.json", init=False)
    _tags_file: str = field(default=".tags.json", init=False)

    def __post_init__(self) -> None:
        """
        The post initilizer checks if the storage path already contains
        the versions and tags file. Otherwise, they are created.
        """
        version_filepath = Path(self.storage_path, self._version_file)
        tags_filepath = Path(self.storage_path, self._tags_file)

        if not os.path.isfile(version_filepath):
            open(version_filepath, "a").close()

        if not os.path.isfile(tags_filepath):
            open(tags_filepath, "a").close()

    def add_artifact(self, name: str, tags: list[str] = []) -> str:
        """
        Add an artifact to the system. In the case that the artifact already
        exists, its version will be upgraded.

        Args:
            name (str): Artifact's name.
            tags (list[str]): Artifact's tags. Default is []

        Returns:
            str: Artifact's filename.
        """

        with open(Path(self.storage_path, self._version_file), "r") as file:
            try:
                version_data = json.load(file)
            except json.decoder.JSONDecodeError:
                version_data = {}

        hashed_name = str(hash(name))

        if hashed_name in version_data:
            versions = version_data[hashed_name].keys()
            versions = list(map(int, versions))
            new_version = max(versions) + 1
        else:
            new_version = 1
            version_data[hashed_name] = {}

        filename = f"{hashed_name}_{new_version}"
        version_data[hashed_name][new_version] = filename

        with open(Path(self.storage_path, self._version_file), "w") as file:
            json.dump(version_data, file)

        if tags:
            with open(self._tags_file, "r") as file:
                tags_data = json.load(file)

            for tag in tags:
                if tag not in data:
                    tags_data[tag] = {tag: {hashed_name: {new_version: filename}}}
                else:
                    tags_data[tag] = {hashed_name: {new_version: filename}}

        return filename

    def update(self):
        pass

    def remove(self):
        pass

    def get(self):
        pass