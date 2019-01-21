import logging
from enum import Enum
from typing import Callable

_logger = logging.getLogger('xconfig')
if _logger.level == logging.NOTSET:
    _logger.setLevel(logging.WARN)


class SupportDepth(Enum):
    Flat = 0
    Layered = 1
    Tree = 2


class Source:
    def __init__(self):
        self._listeners: [Callable] = []

    def read(self) -> dict:
        raise NotImplementedError

    def write(self, blob: dict):
        raise NotImplementedError

    def attach_change_listener(self, listener: Callable):
        self._listeners.append(listener)

    def detach_change_listener(self, listener: Callable):
        try:
            self._listeners.remove(listener)
        except ValueError:
            pass

    @property
    def support_depth(self) -> SupportDepth:
        raise NotImplementedError

    def _notify_listeners(self):
        for listener in self._listeners:
            _logger.debug("Calling change listener {0} for source {1}.".format(listener, type(self)))
            listener()
