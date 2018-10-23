from schema.base import BaseModel, Schema, ValidationError
from schema.cli import SchemaParser



class Settings(BaseModel):
    number_of_cv_folds: int
    split_dataset: bool = Schema(
        description="Split the dataset into training and validation?")
    training_fraction: float
    hello: int = 0


# try:
#     settings = Settings(number_of_cv_folds=0.1, split_dataset="asda", training_fraction=0.5)
# except ValidationError as exc:
#     import pdb; pdb.set_trace()
#     print(exc)


# s = Settings.parse_obj({"number_of_cv_folds": 1,
#                         "training_fraction": 0.5,
#                         "split_dataset": True,
#                         "hello": False})


if __name__ == "__main__":
    parser = SchemaParser(by_alias=False)
    parser.add_schema(Settings)
    try:
        s = parser.parse_schemas()
        print(s)
    except ValidationError as exc:
        print(exc)
