
from app.conf import codes
from os import SEEK_CUR
from threading import Thread
from typing import Tuple, List
from app.db.session import ManagedSession

class Worker():
    
    def __init__(self,*, worker_count: int = codes.DEFAULT_WORKER_COUNT) -> None:
        self.worker_count = worker_count
        self.active_workers: list[Thread] = []
        self.job_list: List[Tuple(list,dict)] = []
        
    
    def start(self):
        while len(self.job_list):
            target,arg,kwarg  = self.job_list.pop(0)
            
            worker: Thread = Thread(target=target,args=arg,kwargs=kwarg)
            self.active_workers.append(worker)
            worker.start()
                
            if len(self.active_workers) == self.worker_count or not len(self.job_list):
                for worker in self.active_workers:
                    worker.join()
                self.active_workers.clear()
    

    
    def add_job(self,target: callable,args: list = [],kwargs: dict = {}):
        self.job_list.append((target,args,kwargs))

   