from app.config import run_job  # import các task đã register
from app.core.queue.interfaces.queue_interface import IQueue

class HueyQueue(IQueue):
    def add_job(self, func, **kwargs):
        self._run_job(func, **kwargs)
    
    def add_async_job(self, func, **kwargs):
        pass
    
    def _run_job(self, func, **kwargs):
        try:
            result = run_job(func, **kwargs)
            # gọi webhook báo kết quả
            print(result)
        except Exception as e:
            # gọi webhook báo exception
            print(e)
            raise Exception(e)
    
    async def _run_async_job(self, func, **kwargs):
        pass

    def get_job(self, job_id):
        pass
    
    def del_job(self, job_id):
        pass