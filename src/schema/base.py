"""
Wrapper for the pydantic library.  Adds minimal functionality, and tweaks settings to
our use case.
"""

# YAPF does not yet support 3.6 type hint syntax
# Local Variables:
# eval: (yapf-mode -1)
# End:

import pydantic
# pylint: disable=unused-import
from pydantic import ValidationError

from utils.conversions import snake_to_camel

__all__ = ["fields", "BaseConfig", "BaseModel", "Schema"]


def fields(model):
    return model.__fields__


class BaseConfig(pydantic.BaseConfig):
    allow_population_by_alias = True
    derive_alias = snake_to_camel
    validate_all = True
    arbitrary_types_allowed = True

    @classmethod
    def get_field_schema(cls, name):
        field_config = cls.fields.get(name) or {}

        if 'alias' not in field_config and callable(cls.derive_alias):
            field_config['alias'] = cls.derive_alias(name)

        return field_config


class BaseModel(pydantic.BaseModel):
    Config = BaseConfig


class Schema(pydantic.Schema):
    def __init__(self, **kwargs):
        if "default" not in kwargs:
            super().__init__(None, **kwargs)
        else:
            super().__init__(**kwargs)


class BoolError(pydantic.errors.PydanticTypeError):
    msg_template = 'value is not a valid bool'


def _bool_validator(v) -> bool:
    if isinstance(v, bool):
        return v
    raise BoolError()


def _set_strict_validators():
    # pylint: disable=protected-access
    alist_replace(pydantic.validators._VALIDATORS, bool, [_bool_validator])


def alist_replace(alist, key, value):
    for (i, (k, _)) in enumerate(alist):
        if key == k:
            alist[i] = (key, value)


_set_strict_validators()
