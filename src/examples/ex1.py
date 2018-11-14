from schema.base import read_schema
from schema.cli import SchemaParser

def main(path):
    schema = read_schema(path)
    parser = SchemaParser(schema)
    return parser.parse()


if __name__ == "__main__":
    main("../res/schema.yaml")

