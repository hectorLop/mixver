import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from mixver.versioning.exceptions import ArtifactDoesNotExist
from mixver.versioning.utils import hash


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

        hashed_name = hash(name)

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
                if tag not in tags_data:
                    tags_data[tag] = {tag: {hashed_name: {new_version: filename}}}
                else:
                    tags_data[tag] = {hashed_name: {new_version: filename}}

        return filename

    def update_tags(self, name: str, tags: list[str], version: str = "") -> None:
        """
        Update the tags with a given artifact. In the case that no version is passed,
        it uses the latest version of that artifact.

        Args:
            name (str): Artifact's name.
            tags (list[str]): List of tags to be updated.
            version (str): Artifact's version. Default is empty, which means the
                latest version of the artifact will be used.
        """
        with open(Path(self.storage_path, self._version_file), "r") as file:
            version_data = json.load(file)

        hashed_name = hash(name)

        if hashed_name not in version_data:
            raise ArtifactDoesNotExist(name)

        if not version:
            versions = version_data[hashed_name].keys()
            versions = list(map(int, versions))
            version = max(versions)
        else:
            versions = version_data[hashed_name].keys()

            if not version in versions:
                raise ArtifactDoesNotExist(name)

        with open(Path(self.storage_path, self._tags_file), "r") as file:
            tags_data = json.load(file)

        for tag in tags:
            tags_data[tag] = {hashed_name: {version: f"{hashed_name}_{version}"}}

        with open(Path(self.storage_path, self._tags_file), "w") as file:
            json.dump(tags_data, file)

    def remove_artifact(self, name: str) -> None:
        """
        Remove an artifact from the registry.

        Args:
            name (str): Artifact's name.
        """
        # TODO: Remove the artifact from the versions
        with open(Path(self.storage_path, self._version_file), "r") as file:
            version_data = json.load(file)

        hashed_name = hash(name)

        if hashed_name not in version_data:
            raise ArtifactDoesNotExist(name)
        else:
            del version_data[hashed_name]

        with open(Path(self.storage_path, self._version_file), "w") as file:
            json.dump(version_data, file)

        with open(Path(self.storage_path, self._tags_file), "r") as file:
            tags_data = json.load(file)

        print(tags_data)
        for tag in tags_data.keys():
            if hashed_name in tags_data[tag]:
                del tags_data[tag][hashed_name]

        with open(Path(self.storage_path, self._tags_file), "w") as file:
            json.dump(tags_data, file)

    def get_artifact_by_version(self, name: str, version: str = "") -> str:
        """
        Retrieves an artifact by its version. If the version is empty, the
        latest version will be returned.

        Args:
            name (str): Artifact's name.
            version (str): Artifact's version. Default is empty.

        Returns:
            str: Artifact's filepath.
        """
        # TODO: Check the key is in the versions. Otherwise raise ArtifactDoesNotExist
        raise NotImplementedError

    def get_artifact_by_tag(self, name: str, tag: str) -> str:
        """
        Retrieves an artifact by its version. If the version is empty, the
        latest version will be returned.

        Args:
            name (str): Artifact's name.
            version (str): Artifact's version. Default is empty.

        Returns:
            str: Artifact's filepath.
        """
        raise NotImplementedError
