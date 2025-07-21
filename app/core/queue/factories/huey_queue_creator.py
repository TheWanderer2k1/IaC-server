from app.core.queue.abstracts.queu_creator import QueueCreator
from .huey_queue import HueyQueue

class HueyQueueCreator(QueueCreator):
    def create_queue(self):
        return HueyQueue()
    
huey_creator = HueyQueueCreator()
