import yaml

def parse_schema(text):
    return yaml.load(text)

def read_schema(path):
    with open(path, 'r') as handle:
        return yaml.load(handle.read())
