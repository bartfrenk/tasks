from functools import partial

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


class SimpleType:

    def __init__(self, ty, description=None):
        self.description = description
        self._ty = ty

    def check(self, data):
        if not isinstance(data, self._ty):
            raise ValidationFailure(f"Expected value of type: {self._ty}")

    @property
    def ty(self):
        return self._ty


def new_simple_type(ty):
    return partial(SimpleType, ty)

Float = new_simple_type(float)
Integer = new_simple_type(int)
String = new_simple_type(str)
DataFrame = new_simple_type(str)
