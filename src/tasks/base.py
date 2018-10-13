from abc import abstractmethod, ABC

from tasks.cli import SchemaArgumentParser
from tasks.schema import Dict


class Task(ABC):
    """Interface for tasks."""

    @property
    @abstractmethod
    def settings_schema(self):
        pass

    @property
    @abstractmethod
    def inputs_schema(self):
        pass

    @property
    @abstractmethod
    def outputs_schema(self):
        """Schema for the return value of the task."""
        pass

    @property
    @abstractmethod
    def settings(self):
        pass

    @abstractmethod
    def execute(self, inputs):
        pass

    def __call__(self, inputs):
        self.settings_schema.check(self.settings)
        self.inputs_schema.check(inputs)
        return self.execute(inputs)


# TODO: metaclass to force subclasses to fill in the static __attributes
class Node(Task):
    """Class to derive atomic tasks from.  Provides a declarative mechanism for
    specifying the types of settings, inputs, and outputs.  The mechanism aims
    to be concise and intuitive.
    """

    _settings_schema = None
    _inputs_schema = None
    _outputs_schema = None

    def __init__(self):
        self._settings = None

    @property
    def settings_schema(self):
        return self._settings_schema

    @property
    def outputs_schema(self):
        return self._outputs_schema

    @property
    def inputs_schema(self):
        return self._inputs_schema

    @property
    def settings(self):
        return self._settings

    @settings.setter
    def settings(self, settings):
        self.settings_schema.check(settings)
        self._settings = settings

    @abstractmethod
    def execute(self, inputs):
        pass


class TaskArgumentParser(SchemaArgumentParser):
    def __init__(self, task, *args, **kwargs):
        self._task = task
        super().__init__(*args, **kwargs)
        self.add_schema(task.settings_schema, "settings")
        self.add_schema(task.inputs_schema, "inputs")
        self.add_schema(task.outputs_schema, "outputs")

    def parse_args(self, args=None, namespace=None):
        parsed = vars(super().parse_args(args, namespace))
        result = {'settings': {}, 'inputs': {}, 'outputs': {}}

        for name in self._task.settings_schema:
            result['settings'][name] = parsed[name]
        for name in self._task.inputs_schema:
            result['inputs'][name] = parsed[name]
        for name in self._task.outputs_schema:
            result['outputs'][name] = parsed[name]

        return result


class Graph(Task):
    def __init__(self, *nodes):
        self._nodes = []
        self._arcs = []
        for node in nodes:
            self.add_node(node)
        self._cache = {}

    def execute(self, inputs):
        pass

    def add_node(self, new_node, add_arcs=True):
        if add_arcs:
            self._add_arcs_by_io_name(new_node)
        self._nodes.append(new_node)

    @property
    def outputs_schema(self):
        # TODO: memoize and reset when adding new nodes
        # TODO: construction could be more efficient
        result = Dict()
        for node in self._nodes:
            for (name, parameter) in node.outputs_schema.items():
                if not self._is_connected_to_input(name, node):
                    result[name] = parameter
        return result

    @property
    def inputs_schema(self):
        # TODO: memoize and reset when adding new nodes
        # TODO: construction could be more efficient
        result = Dict()
        for node in self._nodes:
            for (name, parameter) in node.inputs_schema.items():
                if not self._is_connected_to_output(name, node):
                    result[name] = parameter
        return result

    @property
    def settings_schema(self):
        # TODO: memoize and reset when adding new nodes
        result = Dict()
        for node in self._nodes:
            result.update(node.settings_schema)
        return result

    @property
    def settings(self):
        result = {}
        for node in self._nodes:
            result.update(node.settings)
        return result

    def _add_arcs_by_io_name(self, new_node):
        # TODO: only add arcs between input and output when the type matches
        for node in self._nodes:
            for input_name in new_node.inputs_schema:
                if input_name in node.outputs_schema:
                    self._arcs.append((node, new_node, input_name))
            for output_name in new_node.outputs_schema:
                if output_name in node.inputs_schema:
                    self._arcs.append((node, new_node, output_name))

    def _is_connected_to_input(self, output_name, node):
        for (src, _, name) in self._arcs:
            if src == node and name == output_name:
                return True
        return False

    def _is_connected_to_output(self, input_name, node):
        for (_, dest, name) in self._arcs:
            if dest == node and name == input_name:
                return True
        return False


def command_line_app(task):
    parser = TaskArgumentParser(task)
    args = parser.parse_args()
    task.settings = args['settings']
    print(task(args['inputs']))
