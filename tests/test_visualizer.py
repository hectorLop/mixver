from pathlib import Path

from mixver.config import ROOT
from mixver.storages.local_storage import LocalStorage


def test_visualizer():
    path = Path(ROOT, "tests/data")
    storage = LocalStorage(storage_path=path)
    storage.visualize()


if __name__ == "__main__":
    test_visualizer()
