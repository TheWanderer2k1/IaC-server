from .huey_task import run_job  # import các task đã register
from app.core.queue.interfaces.queue_interface import IQueue
from app.exceptions.queuejob_exception import QueueJobException

class HueyQueue(IQueue):
    def add_job(self, func, **kwargs):
        self._run_job(func, **kwargs)
    
    def add_async_job(self, func, **kwargs):
        pass
    
    def _run_job(self, func, **kwargs):
        try:
            run_job(func, **kwargs)
        except Exception as e:
            raise QueueJobException(f"Failed to run job: {e}")
    
    async def _run_async_job(self, func, **kwargs):
        pass

    def get_job(self, job_id):
        pass
    
    def del_job(self, job_id):
        pass