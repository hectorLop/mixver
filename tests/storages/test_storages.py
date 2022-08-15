import os
import shutil

from mixver.storages.local_storage import LocalStorage


def test_local_storage_creation():
    """
    Test the creation of a LocalStorage in an exising folder.
    """
    folder = "~/Data/prueba_storage"
    os.makedirs(folder)

    storage = LocalStorage(folder)

    assert storage.storage_path == folder

    shutil.rmtree(folder)


def test_local_storage_creation_new_folder():
    """
    Test the creation of a LocalStorage in a new folder.
    """
    folder = "~/Data/prueba_storage_new"
    os.makedirs(folder)

    storage = LocalStorage(folder)

    assert storage.storage_path == folder
    assert os.path.isdir(folder)

    shutil.rmtree(folder)


def test_local_storage_push():
    """
    Test saving data into the storage.
    """
    assert False


def test_local_storage_pull():
    """
    Test retrieving data from the storage.
    """
    assert False
