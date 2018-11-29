import os
import time
import datetime
import logging
import types
import collections.abc as abc
import configparser
from enum import Enum
from watchdog.observers import Observer as WatchdogObserver
from watchdog.events import FileSystemEventHandler

_logger = logging.getLogger('xconfig')
if _logger.level == logging.NOTSET:
    _logger.setLevel(logging.WARN)


class INI:
    @staticmethod
    def read(filename):
        cfg = configparser.ConfigParser()
        cfg.read(filename)
        blob = {}
        for section in cfg.sections():
            blob[section] = {}
            for key in cfg[section]:
                blob[section][key] = cfg[section][key]
        return blob

    @staticmethod
    def write(blob, filename):
        cfg = configparser.ConfigParser()
        cfg.read_dict(blob)
        with open(filename, 'w') as configfile:
            cfg.write(configfile)

    @staticmethod
    def supports_layers():
        return False


class _Entry:
    def __init__(self, tag):
        self._tag = tag

    @property
    def tag(self):
        return self._tag

    @tag.setter
    def tag(self, value):
        self._tag = value


class ValueType:
    pass


class Boolean(ValueType):
    pass


class String(ValueType):
    pass


class Number(ValueType):
    pass


class Option(_Entry):
    def __init__(self, tag, value_type, default=None, required=False, hidden=False, help=None):
        if not tag:
            raise ValueError("tag must be valid and not None")
        super().__init__(tag)
        if not value_type:
            raise ValueError("value_type must be valid and not None")
        self._value_type = value_type
        self._default = default
        self._required = required
        self._hidden = hidden
        self._help = help

    @property
    def value_type(self):
        return self._value_type

    @value_type.setter
    def value_type(self, value):
        self._value_type = value

    @property
    def default_value(self):
        return self._default

    @default_value.setter
    def default_value(self, value):
        self._default = value

    @property
    def required(self):
        return self._required

    @required.setter
    def required(self, value):
        self._required = value

    @property
    def hidden(self):
        return self._hidden

    @hidden.setter
    def hidden(self, value):
        self._hidden = value

    @property
    def help(self):
        return self._help

    @help.setter
    def help(self, value):
        self._help = value


class _RootSection(_Entry, abc.MutableSequence):
    def __init__(self, tag=None, is_root=True):
        _Entry.__init__(self, tag)
        abc.MutableSequence.__init__(self)
        self._is_root = is_root
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

    @property
    def is_root(self):
        return self.is_root


class Section(_RootSection):
    def __init__(self, tag):
        if not tag:
            raise ValueError("tag must be valid and not None")
        super().__init__(tag)


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

    def load(self, file_name=None, file_type=INI, monitor_file=False):
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
