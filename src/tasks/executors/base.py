from abc import ABC, abstractmethod


class ExecutionException(Exception):
    pass


class Executor(ABC):
    """Interface for executors."""

    @abstractmethod
    def execute(self, task, settings, inputs, **context):
        pass
