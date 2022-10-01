from dataclasses import dataclass

from mixver.storages.storage import Storage


@dataclass
class AWSStorage(Storage):
    """
    This class represents the AWS storage to version
    artifacts.
    """

    bucket: str
