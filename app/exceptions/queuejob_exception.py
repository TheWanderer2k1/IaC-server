from app.base_exception import BaseException

class QueueJobException(BaseException):
    """Base class for all queue job exceptions."""
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"QueueJobException: {self.message}"