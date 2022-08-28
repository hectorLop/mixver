class ArtifactDoesNotExist(Exception):
    """
    Indicates that the requested artifact doesn't exist.

    Args:
        name (str): Artifact's name.

    Attributes:
        name (str): Artifact's attribute.
        message (str): Exception's message.
    """

    def __init__(self, name: str, is_tag: bool = False) -> None:
        self.name = name

        if is_tag:
            self.message = f"The '{name}' tag doesn't exist"
        else:
            self.message = f"The '{name}' artifact doesn't exist"

        super().__init__(self.message)
