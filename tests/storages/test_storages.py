import os
import pickle
import shutil
from pathlib import Path

from mixver.config import ROOT
from mixver.storages.local_storage import LocalStorage


class MockArtifact:
    name: str = "LinearRegression"


def test_local_storage_creation():
    """
    Test the creation of a LocalStorage in an exising folder.
    """
    folder = Path(ROOT, "prueba_storage")
    os.makedirs(folder)

    storage = LocalStorage(folder)

    assert storage.storage_path == folder

    shutil.rmtree(folder)


def test_local_storage_creation_new_folder():
    """
    Test the creation of a LocalStorage in a new folder.
    """
    folder = Path(ROOT, "prueba_storage_new")
    os.makedirs(folder)

    storage = LocalStorage(folder)

    assert storage.storage_path == folder
    assert os.path.isdir(folder)

    shutil.rmtree(folder)


def test_local_storage_push():
    """
    Test saving data into the storage.
    """
    folder = Path(ROOT, "prueba_storage")
    os.makedirs(folder)

    storage = LocalStorage(folder)
    artifact_path = Path(folder, "artifact.pkl")
    storage.push(artifact=MockArtifact(), path=artifact_path, metadata={"score": 0.9})

    assert os.path.isfile(artifact_path)

    with open(artifact_path, "rb") as file:
        artifact = pickle.load(file)

    assert artifact["artifact"].name == "LinearRegression"
    assert artifact["metadata"]["score"] == 0.9

    shutil.rmtree(folder)


def test_local_storage_pull():
    """
    Test retrieving data from the storage.
    """
    folder = Path(ROOT, "prueba_storage")
    os.makedirs(folder)

    storage = LocalStorage(folder)
    artifact_path = Path(folder, "artifact.pkl")
    data = {
        "artifact": MockArtifact(),
        "metadata": {"score": 0.9},
    }

    with open(artifact_path, "wb") as file:
        pickle.dump(data, file)

    saved_artifact = storage.pull("artifact.pkl")

    assert saved_artifact["artifact"].name == "LinearRegression"
    assert saved_artifact["metadata"]["score"] == 0.9

    shutil.rmtree(folder)
