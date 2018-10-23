"""
Wrapper for the pydantic library.  Adds minimal functionality, and tweaks settings to
our use case.
"""

# YAPF does not yet support 3.6 type hint syntax
# Local Variables:
# eval: (yapf-mode -1)
# End:

from typing import Dict, Optional

import pydantic
from pydantic import ValidationError

from utils.conversions import snake_to_camel
from utils import alist

__all__ = ["fields", "BaseConfig", "BaseModel", "Schema", "ValidationError"]


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


class Setting(BaseModel):
    hello: int


class Config(BaseModel):
    sett: Setting
    hello: int


def fields(model: BaseModel) -> Dict[str, pydantic.fields.Field]:
    return model.__fields__


def get_nested_attrs(x, attrs, default=None):
    head, *rest = attrs
    if not rest:
        return getattr(x, head, default)
    if not hasattr(x, head):
        return default
    return get_nested_attrs(getattr(x, head), rest, default)


def description(field: pydantic.fields.Field) -> Optional[str]:
    extra = get_nested_attrs(field, ["_schema", "extra"])
    if not isinstance(extra, dict):
        return None
    return extra.get("description")


def is_model(v) -> bool:
    return isinstance(v, BaseModel)


class BoolError(pydantic.errors.PydanticTypeError):
    msg_template = 'value is not a valid bool'


def _bool_validator(v) -> bool:
    if isinstance(v, bool):
        return v
    raise BoolError()


def _set_strict_validators():
    # pylint: disable=protected-access
    alist.update(pydantic.validators._VALIDATORS, bool, [_bool_validator])


_set_strict_validators()
