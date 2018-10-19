import logging
from abc import ABC, abstractmethod
import schema


class ExecutionException(Exception):
    pass


class Channel(ABC):
    """Interface for the communication mechanism between tasks."""
    @abstractmethod
    def put(self, name, data, consumers):
        pass

    @abstractmethod
    def take(self, name, consumer=None):
        """Attempts to take the named data from the channel for the consumer.

        :raises KeyError: When the channel does not contain the named data for the consumer.
        """
        pass

    @abstractmethod
    def has(self, name, consumer=None):
        """
        Check whether the channel has named data to be used by the consumer.
        Set consumer to None to just check whether the named data exists in the
        channel.
        """
        pass

    def select(self, names, consumer=None):
        """Take named data from the channel for the specified consumer.  Does
        not change the state of the channel when consumer is set to None.

        :returns: A dict mapping names to their associated data.
        """
        result = {}
        for name in names:
            try:
                result[name] = self.take(name, consumer)
            except KeyError:
                pass
        return result

    def __contains__(self, name):
        return self.has(name)

class InMemoryChannel(Channel):

    def __init__(self):
        self._data = {}

    def put(self, name, data, consumers):
        self._data[name] = {"data": data, "consumers": consumers}

    def has(self, name, consumer=None):
        return "consumers" in self._data.get(name, {}) and \
            (consumer is None or consumer in self._data[name]["consumers"])

    def take(self, name, consumer=None):
        if not self.has(name, consumer):
            raise KeyError(f"Channel does not contain {name} for {consumer}")
        data = self._data[name]["data"]
        if consumer is not None:
            self._data[name]["consumers"].remove(consumer)
            if not self._data[name]["consumers"]:
                del self._data[name]
        return data

    def __repr__(self):
        return f"<{self.__class__.__name__}({repr(self._data)})>"

class Executor(ABC):
    """Interface for executors."""

    @abstractmethod
    def execute(self, task, settings, inputs, **context):
        pass

log = logging.getLogger(__name__)

class SequentialExecutor(Executor):
    """Executor that runs the subtasks of a task in sequence."""

    def __init__(self, channel):
        """Create an instance.

        :param channel: Abstraction over shared data.  Stores outputs, and
            allows tasks to retrieve inputs.
        """
        self._channel = channel
        self._pending = []

    def execute(self, task, settings, inputs, **context):
        log.info("Starting execution of task %s", task)
        schema.check(task.schema.inputs, inputs)
        schema.check(task.schema.settings, settings)

        # TODO: This requires subtasks to be a list. It is preferred that
        # subtasks is an iterator, to allow for generating subtasks on the fly.
        # Note: Might be difficult since we need to get all consumers of a piece
        # of named data.
        self._pending = task.subtasks.copy()
        self._add_to_channel(inputs)

        while True:
            subtask = self._next_subtask()
            if subtask is None:
                return self._channel.select(task.schema.outputs.keys())
            log.info("Selected %s for execution", subtask)
            outputs = self._run(subtask, settings, **context)
            self._add_to_channel(outputs)
            self._pending.remove(subtask)

    def _add_to_channel(self, outputs):
        """Add all outputs to channel."""
        for (name, data) in outputs.items():
            consumers = self._get_consumers(name, data)
            self._channel.put(name, data, consumers)

    def _next_subtask(self):
        """Return the next subtask to execute."""

        def inputs_in_channel(subtask):
            for name in subtask.schema.inputs:
                if name not in self._channel:
                    return False
            return True

        if not self._pending:
            return None
        try:
            return next(filter(inputs_in_channel, self._pending))
        except StopIteration:
            log.error("Pending tasks: %s", self._pending)
            log.error("Data in channel: %s", self._channel)
            raise ExecutionException("No pending task is ready")

    def _run(self, subtask, settings, **context):
        names = subtask.schema.inputs.keys()
        inputs = self._channel.select(names, subtask)

        return subtask.run(settings[subtask.label], inputs, **context)

    def _get_consumers(self, name, _data):
        """Return a list of all consumers of the named data."""

        def is_consumer(subtask):
            return name in subtask.schema.inputs

        return list(filter(is_consumer, self._pending))
