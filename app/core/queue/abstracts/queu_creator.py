from abc import ABC, abstractmethod
from app.core.queue.interfaces.queue_interface import IQueue

class QueueCreator(ABC):
    @abstractmethod
    def create_queue(self) -> IQueue:
        pass