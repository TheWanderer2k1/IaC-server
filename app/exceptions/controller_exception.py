class ControllerException(Exception):
    """Base class for all controller exceptions."""
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"ControllerException: {self.message}"