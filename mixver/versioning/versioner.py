import os
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class Versioner:
    """
    Class that manages the artifacts versioning
    """

    storage_path: str
    _version_file: str = field(default=".versions.json", init=False)
    _tags_file: str = field(default=".tags.json", init=False)

    def __post_init__(self):
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
