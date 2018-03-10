import os
import time
import datetime
import logging
import types
from enum import Enum
from watchdog.observers import Observer as WatchdogObserver
from watchdog.events import FileSystemEventHandler

_logger = logging.getLogger('xconfig')
if _logger.level == logging.NOTSET:
    _logger.setLevel(logging.WARN)


class FileType(Enum):
    INI = 'INI'
    Json = 'JSON'


class Entry(object):
    def __init__(self, tag, default=None, required=False, force_write=False, help=None, store_as=None):
        self._tag = tag
        self._default = default
        self._required = required
        self._force_write = force_write
        self._help = help
        self._store_as = store_as


class _RootSection(object):
    def __init__(self):
        self._entries = []

    def append(self, entry):
        assert entry is not None
        self._entries.append(entry)


class Section(_RootSection):
    def __init__(self, name):
        self._name = name


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
