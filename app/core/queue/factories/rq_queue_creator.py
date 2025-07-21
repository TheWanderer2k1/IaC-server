from app.core.queue.abstracts.queu_creator import QueueCreator
from .rq_queue import RQQueue

class RQQueueCreator(QueueCreator):
    def create_queue(self):
        return RQQueue()
    
rq_creator = RQQueueCreator()
