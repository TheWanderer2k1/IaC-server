from app.config import logger

class BaseException(Exception):
    """
    Base class for all custom exceptions in the application.
    """
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
        logger.error(f"{self.__class__.__name__}: {self.message}")

    def __str__(self):
        return f"{self.__class__.__name__}: {self.message}"