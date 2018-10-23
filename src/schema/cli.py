"""
Create command line argument parsers from a list of schemas.
"""

import argparse
from typing import Mapping, Any

from structures.tree import Tree

from schema.base import fields, description


class SchemaParser:
    def __init__(self, parser=None, by_alias=True):
        self.parser = parser or argparse.ArgumentParser()
        self._by_alias = by_alias
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
                    group.add_argument(
                        "--{}".format(".".join(prefix)),
                        help=description(root),
                        type=_get_field_parser(root),
                        metavar="<{}>".format(root.type_.__name__))

            if hasattr(root, "fields"):
                for (name, child) in fields(root).items():
                    if self._by_alias:
                        recur(child, prefix + [child.alias])
                    else:
                        recur(child, prefix + [name])

        recur(schema, [])
        self._schemas.append(schema)

    def parse(self, args=None):
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

    def _make_instance(self, schema, tree):
        data = {}
        for (name, child) in fields(schema).items():
            key = child.alias if self._by_alias else name
            if hasattr(child.type_, "fields"):
                data[key] = self._make_instance(child.type_, tree[key])
            else:
                data[key] = tree[key]
        return schema(**data)


_TYPE_PARSERS: Mapping[Any, Any] = {}


def _get_field_parser(field):
    return _TYPE_PARSERS.get(field.type_, field.type_)
