from abc import ABC, abstractmethod
from functools import partial
from datetime import datetime


class ValidationFailure(Exception):
    pass


def check(schema, data):
    if hasattr(schema, "check"):
        schema.check(data)
    if isinstance(schema, dict):
        for key in schema:
            if not isinstance(data, dict):
                raise ValidationFailure("Expected a dictionary")
            if not key in data:
                raise ValidationFailure(f"Expected key: {key}")
            check(schema[key], data[key])


class AtomicType(ABC):

    @abstractmethod
    def parser(self, **settings):
        pass

    @property
    @abstractmethod
    def data_type(self):
        pass

    @property
    @abstractmethod
    def description(self):
        pass

    @abstractmethod
    def check(self, data):
        if not isinstance(data, self.data_type):
            raise ValidationFailure(f"Expected value of type: {self.data_type}")


class SimpleType(AtomicType):

    def __init__(self, data_type, make_parser=None, description=None, default=None):
        self._data_type = data_type
        self._default = default
        self._make_parser = make_parser or (lambda: self._data_type)
        self._description = description

    def check(self, data):
        if not isinstance(data, self._data_type):
            raise ValidationFailure(f"Expected value of type: {self.data_type}")

    @property
    def data_type(self):
        return self._data_type

    def parser(self, **settings):
        return self._make_parser(**settings)

    @property
    def description(self):
        return self._description or ""


def datetime_parser(fmt="%Y%m%dT%H%M%S"):
    def fn(data):
        return datetime.strptime(data, fmt)
    return fn

def new_simple_type(ty, new_parser=None):
    return partial(SimpleType, ty, new_parser)

Float = new_simple_type(float)
Integer = new_simple_type(int)
String = new_simple_type(str)
Datetime = new_simple_type(datetime, datetime_parser)

DataFrame = new_simple_type(str)
Text = new_simple_type(str)

## Where to inject the parsers? Note that these parsers might have complicated
## effects if we require that the end result of a parser is an instance of
## data_type: consider the case of specifying a DataFrame by an S3 URL. In the
## latter case it is not even possible to inject the parser in the schema, since
## the base URL might depend on many things.
##
## Why, maybe they should not even be called parsers. Or they might be split up
## in a parsing bit (which belongs with the types, and is not effectful), and an
## application-dependent bit (possibly, effectful).
