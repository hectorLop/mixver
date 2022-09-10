import json
import os
from pathlib import Path

import pytest

from mixver.config import ROOT


@pytest.fixture(scope="function")
def test_folder():
    storage_path = Path(ROOT, "prueba")
    os.makedirs(storage_path)

    artifact_name = "artifact"
    test_artifact_name = "test_artifact"
    tag_name = "tag_prueba"

    # Create the files beforehand to check if the versioner truncates them
    with open(Path(storage_path, ".versions.json"), "w", encoding="utf8") as file:
        data = {artifact_name: {"1": f"{artifact_name}_1"}}
        data[test_artifact_name] = {"1": f"{test_artifact_name}_1"}
        json.dump(data, file)

    with open(Path(storage_path, ".tags.json"), "w", encoding="utf8") as file:
        data = {tag_name: {artifact_name: {"1": f"{artifact_name}_1"}}}
        json.dump(data, file)

    return storage_path, artifact_name, tag_name
