from abc import ABC, abstractmethod


class ValidationError(Exception):
    pass


class Schema(ABC):
    @abstractmethod
    def check(self, data):
        pass


class Dict:
    def __init__(self, **properties):
        self.properties = properties

    def check(self, data):
        if not isinstance(data, dict):
            raise ValidationError()
        for (key, parameter) in self.properties.items():
            if not key in data:
                raise ValidationError()
            parameter.check(data[key])

    def update(self, schema):
        if not isinstance(schema, Dict):
            raise ValueError()
        self.properties.update(schema.properties)

    def __iter__(self):
        return iter(self.properties)

    def items(self):
        return self.properties.items()

    def __setitem__(self, name, value):
        self.properties[name] = value

class Parameter(Schema):
    def __init__(self, description):
        self.description = description

    @abstractmethod
    def check(self, data):
        pass

    @property
    @abstractmethod
    def python_type(self):
        pass


class NativeType(Parameter):

    __native_type = None

    def __init__(self, description, native_type):
        super(NativeType, self).__init__(description)
        self._native_type = native_type

    def check(self, data):
        if not isinstance(data, self._native_type):
            raise ValidationError()

    @property
    def python_type(self):
        return self._native_type

def Float(description):
    return NativeType(description, float)

def Int(description):
    return NativeType(description, int)

def String(description):
    return NativeType(description, str)
