class ArtifactDoesNotExist(Exception):
    """
    Indicates that the requested artifact doesn't exist.

    Args:
        name (str): Artifact's name.

    Attributes:
        name (str): Artifact's attribute.
        message (str): Exception's message.
    """

    def __init__(self, name: str) -> None:
        self.name = name
        self.message = f"The '{name}' artifact doesn't exist"
        super().__init__(self.message)
