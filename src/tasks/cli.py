from argparse import ArgumentParser


def new_parser(task_schema, *args, **kwargs):
    parser = ArgumentParser(*args, **kwargs)
    _add_schema_to_group(parser, "settings", task_schema.settings)
    _add_schema_to_group(parser, "inputs", task_schema.inputs)
    _add_schema_to_group(parser, "outputs", task_schema.outputs)
    return parser


def _add_schema_to_group(parser, group_name, schema):
    group = parser.add_argument_group(group_name)

    def recur(schema_, prefix):

        if hasattr(schema_, "ty") and hasattr(schema_, "description"):
            group.add_argument(
                "--{}".format(".".join(prefix)),
                type=schema_.ty,
                help=schema_.description,
                metavar="<{}>".format(schema_.ty.__name__))
        if isinstance(schema_, dict):
            for (name, nested_schema) in schema_.items():
                recur(nested_schema, prefix + [name])

    recur(schema, [])
    return group
