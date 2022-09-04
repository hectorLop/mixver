import json
import os
from dataclasses import dataclass, field
from pathlib import Path

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

        if name in version_data:
            versions = version_data[name].keys()
            versions = list(map(int, versions))
            new_version = max(versions) + 1
        else:
            new_version = 1
            version_data[name] = {}

        filename = f"{name}_{new_version}"
        version_data[name][new_version] = filename

        with open(Path(self.storage_path, self._version_file), "w") as file:
            json.dump(version_data, file)

        if tags:
            with open(Path(self.storage_path, self._tags_file), "r") as file:
                try:
                    tags_data = json.load(file)
                except json.decoder.JSONDecodeError:
                    tags_data = {}

            for tag in tags:
                if tag not in tags_data:
                    tags_data[tag] = {name: {new_version: filename}}
                else:
                    tags_data[tag] = {name: {new_version: filename}}

            with open(Path(self.storage_path, self._tags_file), "w") as file:
                json.dump(tags_data, file)

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

        if name not in version_data:
            raise ArtifactDoesNotExist(name)

        if not version:
            versions = version_data[name].keys()
            versions = list(map(int, versions))
            version = max(versions)
        else:
            versions = version_data[name].keys()

            if not version in versions:
                raise ArtifactDoesNotExist(name)

        with open(Path(self.storage_path, self._tags_file), "r") as file:
            tags_data = json.load(file)

        for tag in tags:
            tags_data[tag] = {name: {version: f"{name}_{version}"}}

        with open(Path(self.storage_path, self._tags_file), "w") as file:
            json.dump(tags_data, file)

    def remove_artifact(self, name: str) -> None:
        """
        Remove an artifact from the registry.

        Args:
            name (str): Artifact's name.
        """
        with open(Path(self.storage_path, self._version_file), "r") as file:
            version_data = json.load(file)

        if name not in version_data:
            raise ArtifactDoesNotExist(name)
        else:
            del version_data[name]

        with open(Path(self.storage_path, self._version_file), "w") as file:
            json.dump(version_data, file)

        with open(Path(self.storage_path, self._tags_file), "r") as file:
            tags_data = json.load(file)

        for tag in tags_data.keys():
            if name in tags_data[tag]:
                del tags_data[tag][name]

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
        try:
            with open(Path(self.storage_path, self._version_file), "r") as file:
                version_data = json.load(file)
        except:
            raise EmptyRegistry()

        if name not in version_data:
            raise ArtifactDoesNotExist(name)

        if not version:
            versions = version_data[name].keys()
            versions = list(map(int, versions))
            version = str(max(versions))
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
            with open(Path(self.storage_path, self._tags_file), "r") as file:
                tags_data = json.load(file)
        except:
            raise EmptyTags()

        if tag not in tags_data:
            raise ArtifactDoesNotExist(tag, is_tag=True)

        name = list(tags_data[tag].keys())[0]
        filename = list(tags_data[tag][name].values())[0]

        return filename
