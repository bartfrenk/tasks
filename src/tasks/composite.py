from graph import DirectedGraph

from tasks.base import Task, TaskSchema, ExecutionError


class TaskGraph(Task):
    def __init__(self, *tasks):
        self._label = self.__class__.__name__
        self._graph = DirectedGraph()
        self._schema = TaskSchema.empty()
        for task in tasks:
            self.add_task(task)

    def add_task(self, task):
        self._connect_inputs(task)
        self._connect_outputs(task)
        self._extend_settings(task)
        self._graph.add_node(task)

    def _connect_inputs(self, task):
        for (name, schema) in task.schema.inputs.items():
            connected = False
            for node in self._graph.nodes:
                if name in node.schema.outputs:
                    self._graph.add_arc(src=node, dst=task, label=name)
                    del self._schema.outputs[name]
                    connected = True
            if not connected:
                self._schema.inputs[name] = schema

    def _connect_outputs(self, task):
        for (name, schema) in task.schema.outputs.items():
            connected = False
            for node in self._graph.nodes:
                if name in node.schema.inputs:
                    self._graph.add_arc(src=task, dst=node, label=name)
                    del self._schema.inputs[name]
                    connected = True
            if not connected:
                self._schema.outputs[name] = schema

    def _extend_settings(self, task):
        self._schema.settings[task.label] = task.schema.settings

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        self._label = value

    @property
    def tasks(self):
        return self._graph.nodes

    @property
    def dependencies(self):
        return self._graph.arcs

    @property
    def schema(self):
        return self._schema

    # TODO: Need to abstract over cache to allow for consumption of inputs
    def execute(self, settings, inputs, **context):
        cache = inputs
        unfinished = self._graph.nodes
        while unfinished:
            try:
                current = next(task for task in unfinished
                               if self._inputs_available(cache, task))
                task_output = self._execute_task(settings, cache, current, **context)
                cache.update(task_output)
                unfinished.remove(current)
            except StopIteration:
                raise ExecutionError("Could not execute graph")
        return cache

    @staticmethod
    def _execute_task(settings, cache, task, **context):
        task_settings = settings[task.label]
        task_inputs = select_keys(cache, task.schema.inputs.keys())
        return task.execute(task_settings, task_inputs, **context)

    @staticmethod
    def _inputs_available(cache, task):
        return all(name in cache for name in task.schema.inputs)

    def _dependencies_by_label(self, label):
        for arc in self._graph.arcs:
            if arc.label == label:
                yield arc


def select_keys(dct, keys):
    return {k: dct[k] for k in keys}
