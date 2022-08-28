import hashlib


def hash(string: str) -> str:
    encoded_data = hashlib.md5(string.encode())
    return encoded_data.hexdigest()
