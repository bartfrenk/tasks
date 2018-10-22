class SchemaParser:
    """
    Command line argument parser that outputs data matching a schema.  The
    parser is configured by supplying it with a collection of schemas (via
    :func:`~SchemaParser.add_schema`).
    """

    def __init__(self, parser, settings=None):
        """Create an instance, based on an existing command line parser.

        :param parser: The underlying parser.  It should conform to the
            interface of :class:`~argparse.ArgumentParser`.
        """
        self.parser = parser
        self._settings = settings or {}

    def add_schema(self, schema, section=None):
        """Add schema to the argument parser.

        :param section: Add the schema parser in a separate group with this
            name.
        """

        if section:
            group = self.parser.add_argument_group(section)
        else:
            group = self.parser

        def recur(root, prefix):

            if hasattr(root, "data_type") and hasattr(root, "description"):
                settings = self._settings.get(root.data_type, {})
                group.add_argument(
                    "--{}".format(".".join(prefix)),
                    type=root.parser(**settings),
                    help=root.description,
                    metavar="<{}>".format(root.data_type.__name__))

            if isinstance(root, dict):
                for (name, child) in root.items():
                    recur(child, prefix + [name])

        recur(schema, [])

    def parse_args(self, *args, **kwargs):
        return self.parser.parse_args(*args, **kwargs)


class ModelParser:
    def __init__(self, parser):
        self.parser = parser

    def add_model(self, schema, section=None):
        if section:
            group = self.parser.add_argument_group(section)
        else:
            group = self.parser

        def recur(root, prefix):

            if hasattr(root, "data_type") and hasattr(root, "description"):
                settings = self._settings.get(root.data_type, {})
                group.add_argument(
                    "--{}".format(".".join(prefix)),
                    type=root.parser(**settings),
                    help=root.description,
                    metavar="<{}>".format(root.data_type.__name__))

            if isinstance(root, dict):
                for (name, child) in root.items():
                    recur(child, prefix + [name])

        recur(schema, [])
