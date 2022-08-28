import json
import os
import shutil
from pathlib import Path

import pytest

from mixver.config import ROOT
from mixver.versioning.exceptions import ArtifactDoesNotExist
from mixver.versioning.utils import hash
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


def test_versioner_existant_storage(test_folder):
    """
    Test the versioner on a existant storage.
    """
    storage_path, expected_name, tag_name = test_folder

    versioner = Versioner(storage_path=storage_path)

    # Check that the versioner hasn't truncated the existing files
    with open(Path(storage_path, ".versions.json"), "r") as file:
        data = json.load(file)
        assert expected_name in data.keys()
        assert list(data[expected_name].keys())[0] == "1"
        assert data[expected_name]["1"] == f"{expected_name}_1"

    with open(Path(storage_path, ".tags.json"), "r") as file:
        data = json.load(file)
        assert list(data.keys())[0] == tag_name
        assert list(data[tag_name].keys())[0] == expected_name
        assert data[tag_name][expected_name] == {"1": f"{expected_name}_1"}

    shutil.rmtree(storage_path)


def test_versioner_add_new_artifact(test_folder):
    """
    Test adding a new artifact
    """
    storage_path, _, _ = test_folder

    versioner = Versioner(storage_path=storage_path)
    filename = versioner.add_artifact("artifact2")
    hashed_name, version = filename.split("_")

    assert hashed_name == hash("artifact2")
    assert version == "1"

    with open(Path(storage_path, ".versions.json"), "r") as file:
        data = json.load(file)

        assert hashed_name in data
        assert version in data[hashed_name]
        assert data[hashed_name][version] == filename

    shutil.rmtree(storage_path)


def test_versioner_add_existing_artifact(test_folder):
    """
    Test adding a new artifact
    """
    storage_path, expected_name, _ = test_folder

    versioner = Versioner(storage_path=storage_path)
    filename = versioner.add_artifact("artifact")
    hashed_name, version = filename.split("_")

    assert hashed_name == expected_name
    assert version == "2"

    with open(Path(storage_path, ".versions.json"), "r") as file:
        data = json.load(file)

        assert hashed_name in data
        assert version in data[hashed_name]
        assert data[hashed_name][version] == filename

    shutil.rmtree(storage_path)


def test_update_tags(test_folder):
    """
    Test updating the tags of an existing artifact.
    """
    storage_path, _, tag_name = test_folder

    versioner = Versioner(storage_path=storage_path)
    versioner.update_tags(name="test_artifact", tags=[tag_name])
    expected_name = hash("test_artifact")

    with open(Path(storage_path, ".tags.json"), "r") as file:
        data = json.load(file)

        assert tag_name in data
        assert expected_name in data[tag_name]
        assert "1" in data[tag_name][expected_name]
        assert data[tag_name][expected_name] == {"1": f"{expected_name}_1"}

    shutil.rmtree(storage_path)


def test_update_tags_artifact_not_exist(test_folder):
    """
    Test the exception raises when the artifact doesn't exist.
    """
    storage_path, _, tag_name = test_folder

    versioner = Versioner(storage_path=storage_path)

    with pytest.raises(ArtifactDoesNotExist):
        versioner.update_tags(name="not_exist_artifact", tags=[tag_name])

    shutil.rmtree(storage_path)


def test_update_tags_artifact_version_not_exist(test_folder):
    """
    Test the exception raises when the artifact version doesn't exist.
    """
    storage_path, _, tag_name = test_folder

    versioner = Versioner(storage_path=storage_path)

    with pytest.raises(ArtifactDoesNotExist):
        versioner.update_tags(name="test_artifact", tags=[tag_name], version="14")

    shutil.rmtree(storage_path)
