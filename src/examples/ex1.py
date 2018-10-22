from typing import List
from pydantic import BaseModel, ValidationError, conint

class Location(BaseModel):
    lat = 0.1
    lng = 10.1

class Model(BaseModel):
    is_required: float
    is_true: bool
    gt_int: conint(gt=42)
    list_of_ints: List[int] = None
    a_float: float = None
    recursive_model: Location = None
    x: int

data = dict(
    list_of_ints=['1', 2, 'bad'],
    is_true="asdsad",
    a_float='not a float',
    recursive_model={'lat': 4.2, 'lng': 'New York'},
    gt_int=21,
    x=0.1
)

try:
    Model(**data)
except ValidationError as e:
    print(e)
