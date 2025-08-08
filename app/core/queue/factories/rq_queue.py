from rq import Queue
from rq.job import Job
from redis import Redis
from app.config import settings
from app.core.queue.interfaces.queue_interface import IQueue

class RQQueue(IQueue):
    def __init__(self):
        self.redis_conn = Redis(**settings.redis_conn)
        self.queue = Queue(connection=self.redis_conn)

    def add_job(self, func, **kwargs):
        job = self.queue.enqueue(self._run_job, func, **kwargs)
        return job
    
    def add_async_job(self, func, **kwargs):
        job = self.queue.enqueue(self._run_async_job, func, **kwargs)
        return job

    def _run_job(self, func, **kwargs):
        try:
            result = func(**kwargs)
            # gọi webhook báo kết quả
            print(result)
        except Exception as e:
            # gọi webhook báo exception
            print(e)
            raise Exception(e)
    
    async def _run_async_job(self, func, **kwargs):
        try:
            result = await func(**kwargs)
            # gọi webhook báo kết quả
            print(result)
        except Exception as e:
            # gọi webhook báo exception
            print(e)
            raise Exception(e)

    def get_job(self, job_id):
        return Job.fetch(job_id, self.redis_conn)

    def del_job(self, job_id):
        job = self.get_job(job_id)
        job.delete()