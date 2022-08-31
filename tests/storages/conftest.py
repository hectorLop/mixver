import os
from pathlib import Path

import pytest

from mixver.config import ROOT


@pytest.fixture(scope="function")
def storage_folder():
    storage_path = Path(ROOT, "storage")
    os.makedirs(storage_path)

    return storage_path
