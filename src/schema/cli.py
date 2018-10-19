# TODO: inheritance might be actually better here (not sure)
class SchemaParser:
    """
    Command line argument parser that outputs data matching a schema.  The
    parser is configured by supplying it with a collection of schemas (via
    :func:`~SchemaParser.add_schema`).
    """

    def __init__(self, parser):
        """Create an instance, based on an existing command line parser.

        :param parser: The underlying parser.  It should conform to the
            interface of :class:`~argparse.ArgumentParser`.
        """
        self._parser = parser

    def add_schema(self, schema, section=None):
        """Add schema to the argument parser.

        :param section: Add the schema parser in a separate group with this
            name.
        """
        if section:
            group = self._parser.add_argument_group(section)
        else:
            group = self._parser

        def recur(schema_, prefix):

            if hasattr(schema_, "ty") and hasattr(schema_, "description"):
                group.add_argument("--{}".format(".".join(prefix)),
                                   type=schema_.ty,
                                   help=schema_.description,
                                   metavar="<{}>".format(schema_.ty.__name__))
            if isinstance(schema_, dict):
                for (name, nested_schema) in schema_.items():
                    recur(nested_schema, prefix + [name])

        recur(schema, [])

    def parse_args(self, *args, **kwargs):
        return self._parser.parse_args(*args, **kwargs)
