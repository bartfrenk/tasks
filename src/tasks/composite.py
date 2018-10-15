from graph import DirectedGraph

from .base import Task, TaskSchema



class TaskGraph(Task):

    def __init__(self, *tasks):
        self._graph = DirectedGraph()
        self._settings = None
        self._label = None
        self.__schema = None
        for task in tasks:
            self.add_task(task)

    def add_task(self, task):
        for node in self._graph.nodes:
            for name in node.schema.inputs:
                if name in task.schema.outputs:
                    self._graph.add_arc(src=task, dst=node, label=name)
            for name in node.schema.outputs:
                if name in task.schema.inputs:
                    self._graph.add_arc(src=node, dst=task, label=name)
        self._graph.add_node(task)
        self._reset_memoization()

    @property
    def label(self):
        return self._label or self.__class__.__name__

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
        if self.__schema is None:
            settings = {}
            for task in self._graph.nodes:
                settings[task.label] = task.schema.settings
            self.__schema = TaskSchema(settings, {}, {})
        return self.__schema

    def _reset_memoization(self):
        self.__schema = None

    def execute(self, settings, inputs, **context):
        pass
