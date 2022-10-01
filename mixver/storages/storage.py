from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from mixver.versioning.versioner import Versioner


@dataclass
class Storage(ABC):
    """
    Storage interface.
    """

    _versioner: Versioner = field(init=False)

    @abstractmethod
    def push(
        self, artifact: Any, name: str, metadata: Dict, tags: Optional[list[str]] = None
    ) -> str:
        """
        Save data into the storage.
        """

    @abstractmethod
    def pull(self, tag: str = "", name: str = "", version: str = "") -> Dict:
        """
        Retrieve data from the storage.
        """

    @abstractmethod
    def visualize(self):
        """
        Visualize the tags and their associated artifacts.
        """
