from abc import abstractmethod, ABC

import schema as s


class Task(ABC):
    @abstractmethod
    def execute(self, settings, inputs, **context):
        pass

    @property
    @abstractmethod
    def schema(self):
        pass

    @property
    @abstractmethod
    def label(self):
        pass

    def __call__(self, settings, inputs):
        self.execute(settings, inputs)


class SimpleTask(Task):
    def __init__(self, schema, execute, label=None):
        self._execute = execute
        self._schema = schema
        self._label = label or str(execute)

    @property
    def schema(self):
        return self._schema

    @property
    def label(self):
        return self._label

    def execute(self, settings, inputs, **context):
        s.check(self.schema.settings, settings)
        s.check(self.schema.inputs, inputs)
        return self._execute(settings, inputs, **context)

    def __repr__(self):
        return "<{}({})>".format(self.__class__.__name__,
                                 self._execute.__name__)


class TaskSchema:
    def __init__(self, settings, inputs, outputs):
        if not isinstance(settings, dict):
            raise ValueError("Expected 'settings' to be a dict")
        if not isinstance(inputs, dict):
            raise ValueError("Expected 'inputs' to be a dict")
        if not isinstance(outputs, dict):
            raise ValueError("Expected 'outputs' to be a dict")

        self.settings = settings
        self.inputs = inputs
        self.outputs = outputs

    @classmethod
    def empty(cls):
        return cls({}, {}, {})

    def check_inputs(self, data):
        self._check_data(self.inputs, data)

    def check_outputs(self, data):
        self._check_data(self.outputs, data)

    def check_settings(self, data):
        self._check_data(self.settings, data)

    def append(self, task_schema, key=None):
        attrs = ["settings", "inputs", "outputs"]
        for attr in attrs:
            if key:
                getattr(self, attr)[key] = getattr(task_schema, attr)
            else:
                getattr(self, attr).update(getattr(task_schema, attr))

    @classmethod
    def _check_data(cls, schema, data):
        s.check(schema, data)


def task(settings, inputs, outputs):
    def decorator(execute):
        schema = TaskSchema(settings, inputs, outputs)
        label = execute.__name__
        return SimpleTask(schema, execute, label)

    return decorator
