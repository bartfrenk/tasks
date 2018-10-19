from argparse import ArgumentParser

from schema import cli


def new_parser(task, *args, **kwargs):
    parser = cli.SchemaParser(ArgumentParser(*args, **kwargs))
    parser.add_schema(task.schema.settings, "settings")
    parser.add_schema(task.schema.inputs, "inputs")
    parser.add_schema(task.schema.outputs, "outputs")
    return parser
