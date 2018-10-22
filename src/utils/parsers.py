from datetime import datetime


def datetime_parser(fmt="%Y%m%dT%H%M%S"):
    def fn(data):
        return datetime.strptime(data, fmt)

    return fn
