from abc import ABC, abstractmethod

class IQueue(ABC):
    @abstractmethod
    def add_job(self, func, **kwargs):
        pass

    @abstractmethod
    def _run_job(self, func, **kwargs):
        pass

    @abstractmethod
    def get_job(self, job_id):
        pass

    @abstractmethod
    def del_job(self, job_id):
        pass