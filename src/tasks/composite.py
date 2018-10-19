from graph import DirectedGraph

from tasks.base import Task, TaskSchema


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
        if task.schema.settings:
            self._schema.settings[task.label] = task.schema.settings

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        self._label = value

    @property
    def subtasks(self):
        return self._graph.nodes

    @property
    def dependencies(self):
        return self._graph.arcs

    @property
    def schema(self):
        return self._schema

    def __repr__(self):
        return f"<{self._label}>"
