from .huey_task import run_job, run_infra_job  # import các task đã register
from app.core.queue.interfaces.queue_interface import IQueue
from app.exceptions.queuejob_exception import QueueJobException

class HueyQueue(IQueue):
    def add_job(self, host_ip, func, **kwargs):
        self._run_job(host_ip, func, **kwargs)

    def add_infra_job(self, host_ip, obj, method_name, **kwargs):
        self._run_infra_job(host_ip, obj, method_name, **kwargs)
    
    def add_async_job(self, func, **kwargs):
        pass
    
    def _run_job(self, host_ip, func, **kwargs):
        try:
            run_job(host_ip, func, **kwargs)
        except Exception as e:
            raise QueueJobException(f"Failed to run job: {e}")
        
    def _run_infra_job(self, host_ip, obj, method_name, **kwargs):
        try:
            run_infra_job(obj, host_ip, method_name, **kwargs)
        except Exception as e:
            raise QueueJobException(f"Failed to run job: {e}")
    
    async def _run_async_job(self, func, **kwargs):
        pass

    def get_job(self, job_id):
        pass
    
    def del_job(self, job_id):
        pass