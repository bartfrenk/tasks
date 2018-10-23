from schema.base import BaseModel, Schema, ValidationError
from schema.cli import SchemaParser



class Settings(BaseModel):
    number_of_cv_folds: int
    split_dataset: bool = Schema(
        description="Split the dataset into training and validation?")
    training_fraction: float
    hello: int = 0


if __name__ == "__main__":
    parser = SchemaParser(by_alias=False)
    parser.add_schema(Settings)
    try:
        s = parser.parse()
        print(s)
    except ValidationError as exc:
        print(exc)
