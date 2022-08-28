class ArtifactNotExist(Exception):
    def __init__(self, name: str) -> None:
        self.name = name
        self.message = f"The '{name}' artifact doesn't exist"
        super().__init__(self.message)
