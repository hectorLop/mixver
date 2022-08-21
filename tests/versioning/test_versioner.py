import json
import os
import shutil
from pathlib import Path

import pytest

from mixver.config import ROOT
from mixver.versioning.versioner import Versioner


def test_versioner_new_storage():
    """
    Test the versioner on a new storage.
    """
    storage_path = Path(ROOT, "prueba_versioner")
    os.makedirs(storage_path)

    versioner = Versioner(storage_path=storage_path)

    assert os.path.isfile(Path(storage_path, ".versions.json"))
    assert os.path.isfile(Path(storage_path, ".tags.json"))

    shutil.rmtree(storage_path)


def test_versioner_existant_storage():
    """
    Test the versioner on a existant storage.
    """
    storage_path = Path(ROOT, "prueba_versioner")
    os.makedirs(storage_path)

    # Create the files beforehand to check if the versioner truncates them
    with open(Path(storage_path, ".versions.json"), "w") as file:
        data = {"key": 1}
        json.dump(data, file)
    with open(Path(storage_path, ".tags.json"), "w") as file:
        data = {"key": 1}
        json.dump(data, file)

    versioner = Versioner(storage_path=storage_path)

    # Check that the versioner hasn't truncated the existing files
    with open(Path(storage_path, ".versions.json"), "r") as file:
        data = json.load(file)
        assert data["key"] == 1
    with open(Path(storage_path, ".tags.json"), "r") as file:
        data = json.load(file)
        assert data["key"] == 1

    shutil.rmtree(storage_path)


def test_versioner_add_new_artifact():
    """
    Test adding a new artifact
    """
    storage_path = Path(ROOT, "prueba_versioner")
    os.makedirs(storage_path)

    versioner = Versioner(storage_path=storage_path)
    filename = versioner.add_artifact("artifact")

    hashed_name, version = filename.split("_")

    assert hashed_name == str(hash("artifact"))
    assert version == "1"

    with open(Path(storage_path, ".versions.json"), "r") as file:
        data = json.load(file)

        assert hashed_name in data
        assert version in data[hashed_name]
        assert data[hashed_name][version] == filename

    shutil.rmtree(storage_path)


def test_versioner_add_existing_artifact():
    """
    Test adding a new artifact
    """
    storage_path = Path(ROOT, "prueba_versioner")
    os.makedirs(storage_path)

    versioner = Versioner(storage_path=storage_path)
    expected_hashed_name = str(hash("artifact"))
    old_version = "1"
    data = {
        expected_hashed_name: {old_version: f"{expected_hashed_name}_{old_version}"}
    }

    with open(Path(storage_path, ".versions.json"), "w") as file:
        json.dump(data, file)

    filename = versioner.add_artifact("artifact")

    hashed_name, version = filename.split("_")

    assert hashed_name == expected_hashed_name
    assert version == "2"

    with open(Path(storage_path, ".versions.json"), "r") as file:
        data = json.load(file)

        assert hashed_name in data
        assert version in data[hashed_name]
        assert data[hashed_name][version] == filename

    shutil.rmtree(storage_path)
