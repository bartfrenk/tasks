from abc import ABC, abstractmethod


class Channel(ABC):
    """Interface for the communication mechanism between tasks."""

    @abstractmethod
    def put(self, name, data, consumers):
        pass

    @abstractmethod
    def take(self, name, consumer=None):
        """Attempts to take the named data from the channel for the consumer.

        :raises KeyError: When the channel does not contain the named data for the consumer.
        """
        pass

    @abstractmethod
    def has(self, name, consumer=None):
        """
        Check whether the channel has named data to be used by the consumer.
        Set consumer to None to just check whether the named data exists in the
        channel.
        """
        pass

    def select(self, names, consumer=None):
        """Take named data from the channel for the specified consumer.  Does
        not change the state of the channel when consumer is set to None.

        :returns: A dict mapping names to their associated data.
        """
        result = {}
        for name in names:
            try:
                result[name] = self.take(name, consumer)
            except KeyError:
                pass
        return result

    def __contains__(self, name):
        return self.has(name)
