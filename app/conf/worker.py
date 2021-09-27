"""Uvicorn Worker Configuration"""
from multiprocessing import cpu_count


class UviCornWorker:
    """A class to configure the uvicorn to run multiple processes"""

    web_concurrency: int = cpu_count() - 1


worker = UviCornWorker()
