import os
import pickle
import shutil
from pathlib import Path

import pytest

from mixver.config import ROOT
from mixver.storages.local_storage import LocalStorage


class MockArtifact:
    name: str = "LinearRegression"


def test_local_storage_creation(storage_folder):
    """
    Test the creation of a LocalStorage in an exising folder.
    """
    # folder = Path(ROOT, "prueba_storage")
    # os.makedirs(folder)
    folder = storage_folder

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


def test_local_storage_push(storage_folder):
    """
    Test saving data into the storage.
    """
    folder = storage_folder

    storage = LocalStorage(folder)
    name = "artifact"
    filename = storage.push(artifact=MockArtifact(), name=name, metadata={"score": 0.9})

    expected_path = Path(folder, f"{filename}.pkl")
    assert os.path.isfile(expected_path)

    with open(expected_path, "rb") as file:
        artifact = pickle.load(file)

    assert artifact["artifact"].name == "LinearRegression"
    assert artifact["metadata"]["score"] == 0.9

    shutil.rmtree(folder)


def test_local_storage_pull(storage_folder):
    """
    Test retrieving data from the storage.
    """
    folder = storage_folder

    storage = LocalStorage(folder)
    data = {
        "artifact": MockArtifact(),
        "metadata": {"score": 0.9},
    }

    with open(Path(folder, f"artifact.pkl"), "wb") as file:
        pickle.dump(data, file)

    # FIXME: Currently, this test is adding an artifact to the folder but the versions
    # file is empty. Therefore, there is an error reading an empty JSON.
    saved_artifact = storage.pull("artifact", identifier=1)

    assert saved_artifact["artifact"].name == "LinearRegression"
    assert saved_artifact["metadata"]["score"] == 0.9

    shutil.rmtree(folder)
