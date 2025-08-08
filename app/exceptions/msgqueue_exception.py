from app.base_exception import BaseException

class MsgQueueException(BaseException):
    """Base class for all msg queue exceptions."""
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"MsgQueueException: {self.message}"