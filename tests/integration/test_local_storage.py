import json
import os
import shutil
from pathlib import Path

import pytest

from mixver.config import ROOT
from mixver.storages.local_storage import LocalStorage


class MLModel:
    model_name: str = "LogisticRegression"


def test_local_storage():
    folder = Path(ROOT, "prueba_storage")
    os.makedirs(folder)

    storage = LocalStorage(storage_path=folder)
    model = MLModel()
    metadata = {"accuracy": 0.78}
    name = "test_model"
    tags = ["latest", "validation"]
    expected_filename = Path(folder, "test_model_1.pkl")

    filename = storage.push(artifact=model, name=name, metadata=metadata, tags=tags)
    actual_filepath = Path(folder, f"{filename}.pkl")

    assert os.path.isfile(actual_filepath)
    assert actual_filepath == expected_filename

    with open(Path(folder, ".versions.json"), "r") as file:
        versions_data = json.load(file)

        assert name in versions_data
        assert versions_data[name] == {"1": f"{name}_1"}

    with open(Path(folder, ".tags.json"), "r") as file:
        tags_data = json.load(file)

        for tag in tags:
            assert tag in tags_data
            assert tags_data[tag] == {name: {"1": f"{name}_1"}}

    for identifier in [1, "latest", "validation"]:
        artifact = storage.pull(name=name, identifier=identifier)
        assert isinstance(artifact["artifact"], MLModel)
        assert artifact["metadata"] == metadata

    shutil.rmtree(folder)
