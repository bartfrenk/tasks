import logging

from tasks.channels.base import Channel


log = logging.getLogger(__name__)


class InMemoryChannel(Channel):

    def __init__(self):
        self._data = {}

    def put(self, name, data, consumers):
        log.info("Storing %s for consumers %s", name, consumers)
        self._data[name] = {"data": data, "consumers": consumers}

    def has(self, name, consumer=None):
        return "consumers" in self._data.get(name, {}) and \
            (consumer is None or consumer in self._data[name]["consumers"])

    def take(self, name, consumer=None):
        if not self.has(name, consumer):
            raise KeyError(f"Channel does not contain {name} for {consumer}")
        data = self._data[name]["data"]
        if consumer is not None:
            log.info("Data %s consumed by %s", name, consumer)
            self._data[name]["consumers"].remove(consumer)
            if not self._data[name]["consumers"]:
                del self._data[name]
        else:
            log.info("Retrieving data %s", name)
        return data

    def __repr__(self):
        return f"<{self.__class__.__name__}({repr(self._data)})>"
