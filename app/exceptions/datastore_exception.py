from app.base_exception import BaseException

class DatastoreOperationException(BaseException):
    """
    Custom exception for datastore operation errors.
    This exception is raised when an operation on the datastore fails.
    """
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"DatastoreOperationException: {self.message}"