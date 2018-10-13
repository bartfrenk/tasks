from argparse import ArgumentParser


class SchemaArgumentParser(ArgumentParser):

    def add_schema(self, schema, section=None):
        if not hasattr(schema, "properties"):
            raise ValueError("Schema should have a properties attribute")

        if section is None:
            group = self
        else:
            group = self.add_argument_group(section)

        for (name, parameter) in schema.properties.items():
            self._add_parameter(group, name, parameter)

    def _add_parameter(self, group, name, parameter):
        option = self._long_option(name)
        group.add_argument(
            option,
            type=parameter.python_type,
            help=parameter.description,
            metavar=parameter.python_type.__name__)

    def _long_option(self, name):
        # pylint: disable=no-self-use
        return "--{}".format(name)
