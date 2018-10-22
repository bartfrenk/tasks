from typing import get_type_hints


def settings(task):
    return get_type_hints(task)["settings"]


def inputs(task):
    return get_type_hints(task)["inputs"]


def outputs(task):
    return get_type_hints(task)["return"]
