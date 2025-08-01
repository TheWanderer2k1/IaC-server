from app.base_exception import BaseException

class InfraOperationException(BaseException):
    """
    Custom exception for infrastructure operation errors.
    This exception is raised when an operation on the infrastructure fails.
    """
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"InfraOperationException: {self.message}"