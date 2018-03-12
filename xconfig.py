import os
import time
import datetime
import logging
import types
import collections.abc as abc
from enum import Enum
from watchdog.observers import Observer as WatchdogObserver
from watchdog.events import FileSystemEventHandler

_logger = logging.getLogger('xconfig')
if _logger.level == logging.NOTSET:
    _logger.setLevel(logging.WARN)


class FileType(Enum):
    INI = 'INI'
    Json = 'JSON'


class _Entry:
    def __init__(self, tag):
        self._tag = tag

    @property
    def tag(self):
        return self._tag


class Boolean:
    pass


class String:
    pass


class Number:
    pass


class Option(_Entry):
    def __init__(self, tag, value_type, default=None, required=False, force_write=False, help=None):
        super().__init__(tag)
        self._value_type = value_type
        self._default = default
        self._required = required
        self._force_write = force_write
        self._help = help

    @property
    def value_type(self):
        return self._value_type

    @property
    def default_value(self):
        return self._default

    @property
    def is_required(self):
        return self._required

    @property
    def force_write(self):
        return self._force_write

    @property
    def help(self):
        return self._help


class _RootSection(_Entry, abc.MutableSequence):
    def __init__(self, tag=None):
        _Entry.__init__(self, tag)
        abc.MutableSequence.__init__(self)
        self._entries = []

    def __setitem__(self, index, value):
        self._entries[index] = value

    def __getitem__(self, index):
        return self._entries[index]

    def __len__(self):
        return len(self._entries)

    def __delitem__(self, index):
        del self._entries[index]

    def insert(self, index, value):
        self._entries.insert(index, value)


class Section(_RootSection):
    def __init__(self, tag):
        if tag is None:
            raise ValueError("tag must be valid and non None")
        super(tag)


class _Monitor(FileSystemEventHandler):
    def __init__(self, definition, file_type, config, file):
        self._definition = definition
        self._file_type = file_type
        self._config = config
        self._file = file
        self._path = os.path.dirname(os.path.abspath(file))
        self._observer = WatchdogObserver()
        self._observer.schedule(self, path=self._path, recursive=False)
        self._observer.start()
        self._last_event_time = datetime.datetime.now()

    def on_modified(self, event):
        if event.event_type == 'modified' and event.src_path == self._file:
            if not self._within_event_threshold():
                _logger.info('File change detected.  Reloading config {0}'.format(self._file))
                self._definition.reload(self._file, self._file_type, self._config)

    def _within_event_threshold(self):
        current_time = datetime.datetime.now()
        span = current_time - self._last_event_time
        within_threshold = span < datetime.timedelta(seconds=1)
        self._last_event_time = current_time
        return within_threshold


class Config(types.SimpleNamespace):
    pass


class Definition(_RootSection):
    _monitors = []

    def __init__(self):
        super(Definition, self).__init__()

    def load(self, file_name=None, file_type=FileType.INI, monitor_file=False):
        config = "Test"
        if monitor_file:
            self._monitors.append(_Monitor(self, file_type, config, file_name))
        return config

    def reload(self, file_name, file_type, config):
        _logger.info('Reloading...{0}, Filetype: {1}'.format(file_name, file_type))

    def generate_default(self):
        pass

    def save(self, config, file_name=None):
        pass


if __name__ == '__main__':
    definition = Definition()
    config = definition.load(r"C:\Temp\config\xconfig.cfg", monitor_file=True)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    exit()
