import json
import os
from dataclasses import dataclass, field
from json.decoder import JSONDecodeError
from pathlib import Path
from typing import Optional

from mixver.versioning.exceptions import ArtifactDoesNotExist, EmptyRegistry, EmptyTags


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
            with open(version_filepath, "a", encoding="utf8"):
                pass

        if not os.path.isfile(tags_filepath):
            with open(tags_filepath, "a", encoding="utf8"):
                pass

    def _get_last_version(self, versions_data: dict, name: str) -> int:
        versions = versions_data[name].keys()
        versions = list(map(int, versions))
        return max(versions)

    def _read_file(self, filename: str) -> dict:
        with open(Path(self.storage_path, filename), "r", encoding="utf8") as file:
            try:
                data = json.load(file)
            except json.decoder.JSONDecodeError:
                data = {}

        return data

    def _modify_tags_data(self, tags: list[str], name: str, version: int):
        tags_data = self._read_file(self._tags_file)

        for tag in tags:
            tags_data[tag] = {name: {str(version): f"{name}_{version}"}}

        with open(
            Path(self.storage_path, self._tags_file), "w", encoding="utf8"
        ) as file:
            json.dump(tags_data, file)

    def add_artifact(self, name: str, tags: Optional[list[str]] = None) -> str:
        """
        Add an artifact to the system. In the case that the artifact already
        exists, its version will be upgraded.

        Args:
            name (str): Artifact's name.
            tags (list[str]): Artifact's tags. Default is []

        Returns:
            str: Artifact's filename.
        """
        version_data = self._read_file(self._version_file)

        if name in version_data:
            new_version = self._get_last_version(version_data, name) + 1
        else:
            new_version = 1
            version_data[name] = {}

        filename = f"{name}_{new_version}"
        version_data[name][new_version] = filename

        with open(
            Path(self.storage_path, self._version_file), "w", encoding="utf8"
        ) as file:
            json.dump(version_data, file)

        if tags:
            self._modify_tags_data(tags=tags, name=name, version=new_version)

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
        with open(
            Path(self.storage_path, self._version_file), "r", encoding="utf8"
        ) as file:
            version_data = json.load(file)

        if name not in version_data:
            raise ArtifactDoesNotExist(name)

        if not version:
            version = self._get_last_version(version_data, name)
        else:
            versions = version_data[name].keys()

            if not version in versions:
                raise ArtifactDoesNotExist(name)

        self._modify_tags_data(tags=tags, name=name, version=version)

    def remove_artifact(self, name: str) -> None:
        """
        Remove an artifact from the registry.

        Args:
            name (str): Artifact's name.
        """
        with open(
            Path(self.storage_path, self._version_file), "r", encoding="utf8"
        ) as file:
            version_data = json.load(file)

        if name not in version_data:
            raise ArtifactDoesNotExist(name)

        del version_data[name]

        with open(
            Path(self.storage_path, self._version_file), "w", encoding="utf8"
        ) as file:
            json.dump(version_data, file)

        with open(
            Path(self.storage_path, self._tags_file), "r", encoding="utf8"
        ) as file:
            tags_data = json.load(file)

        for tag in tags_data.keys():
            if name in tags_data[tag]:
                del tags_data[tag][name]

        with open(
            Path(self.storage_path, self._tags_file), "w", encoding="utf8"
        ) as file:
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
        with open(
            Path(self.storage_path, self._version_file), "r", encoding="utf8"
        ) as file:
            try:
                version_data = json.load(file)
            except JSONDecodeError as exc:
                raise EmptyRegistry() from exc

        if name not in version_data:
            raise ArtifactDoesNotExist(name)

        if not version:
            version = str(self._get_last_version(version_data, name))
        else:
            versions = version_data[name].keys()

            if not version in versions:
                raise ArtifactDoesNotExist(name)

        filename = version_data[name][version]

        return filename

    def get_artifact_by_tag(self, tag: str) -> str:
        """
        Retrieves an artifact by its version. If the version is empty, the
        latest version will be returned.

        Args:
            tag (str): Tag assigned to the desired artifact.

        Returns:
            str: Artifact's filepath.
        """
        try:
            with open(
                Path(self.storage_path, self._tags_file), "r", encoding="utf8"
            ) as file:
                tags_data = json.load(file)
        except Exception as exc:
            raise EmptyTags() from exc

        if tag not in tags_data:
            raise ArtifactDoesNotExist(tag, is_tag=True)

        name = list(tags_data[tag].keys())[0]
        filename = list(tags_data[tag][name].values())[0]

        return filename
