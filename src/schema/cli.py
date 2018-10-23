from typing import Mapping, Any

from structures.tree import Tree

from schema.base import fields


class SchemaParser:
    def __init__(self, parser):
        self.parser = parser
        self._schemas = []

    def add_schema(self, schema, section=None):
        if section:
            group = self.parser.add_argument_group(section)
        else:
            group = self.parser

        def recur(root, prefix):
            if hasattr(root, "type_"):
                if hasattr(root.type_, "fields"):
                    recur(root.type_, prefix)
                else:
                    # TODO: add description field
                    group.add_argument(
                        "--{}".format(".".join(prefix)),
                        type=_get_type_parser(root.type_),
                        metavar="<{}>".format(root.type_.__name__))


            if hasattr(root, "fields"):
                for (name, child) in fields(root).items():
                    recur(child, prefix + [name])

        recur(schema, [])
        self._schemas.append(schema)

    def parse_schemas(self, args=None):
        """
        :raises ValidationError:
        """
        arguments = vars(self.parser.parse_args(args))
        tree = self._make_tree(arguments)
        objects = []
        for schema in self._schemas:
            objects.append(self._make_instance(schema, tree))
        return objects

    @classmethod
    def _make_tree(cls, arguments):
        tree = Tree()
        for (name, value) in arguments.items():
            tree[name.split(".")] = value
        return tree

    @classmethod
    def _make_instance(cls, schema, tree):
        data = {}
        for (name, child) in fields(schema).items():
            if hasattr(child.type_, "fields"):
                data[name] = cls._make_instance(child.type_, tree[name])
            else:
                data[name] = tree[name]
        return schema(**data)


_TYPE_PARSERS: Mapping[Any, Any] = {}


def _get_type_parser(type_):
    return _TYPE_PARSERS.get(type_, type_)
