import logging

import schema

from tasks.executors.base import Executor, ExecutionException

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

        return subtask.run(settings.get(subtask.label, {}), inputs, **context)

    def _get_consumers(self, name, _data):
        """Return a list of all consumers of the named data."""

        def is_consumer(subtask):
            return name in subtask.schema.inputs

        return list(filter(is_consumer, self._pending))
