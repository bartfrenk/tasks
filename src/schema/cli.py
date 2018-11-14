from argparse import ArgumentParser
from structures.tree import Tree


def register_property_parser(type_, parser):
    _PROPERTY_PARSERS[type_] = parser


class SchemaParser:
    def __init__(self, schema):
        self._check_schema(schema)
        self._schema = schema
        self._parser = self._make_arg_parser(schema["data"])

    def parse(self, args=None):
        arguments = vars(self._parser.parse_args(args))
        return self._make_tree(arguments)

    @classmethod
    def _make_tree(cls, arguments):
        tree = Tree()
        for (name, value) in arguments.items():
            tree[name.split(".")] = value
        return tree

    def _check_schema(self, schema):
        pass  # TODO: check this against a JSON spec

    def _make_arg_parser(self, data):

        parser = ArgumentParser()

        def recur(prefix, root):
            if isinstance(root, dict):
                if "name" in root and "type" in root:
                    opt = self._make_opt(prefix, root)
                    parser.add_argument(opt, **self._make_argument(root))
                else:
                    for (name, child) in root.items():
                        recur(prefix + [name], child)
            if isinstance(root, list):
                for child in root:
                    recur(prefix, child)

        recur([], data)

        return parser

    def _make_opt(self, prefix, root):
        # pylint: disable=no-self-use
        # TODO: Change - to _
        opt = ".".join(prefix + [root["name"]])
        return f"--{opt}"

    def _make_argument(self, root):
        return {
            "help": root.get("description"),
            "type": self._make_property_parser(root),
            "metavar": "<{}>".format(root["type"])
        }

    def _make_property_parser(self, root):
        # pylint: disable=no-self-use
        type_ = root["type"]
        if type_ in _PROPERTY_PARSERS:
            return _PROPERTY_PARSERS[type_]
        raise ValueError(f"No property parser registered for {type_}")

    def __repr__(self):
        return "<{}({})>".format(self.__class__.__name__,
                                 self._schema["meta"]["id"])


_PROPERTY_PARSERS = {"int": int, "float": float, "str": lambda x: x}
