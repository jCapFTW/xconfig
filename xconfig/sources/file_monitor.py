from watchdog.observers import Observer as WatchdogObserver
from watchdog.events import FileSystemEventHandler
from typing import Callable
import os
import datetime
import logging


_logger = logging.getLogger('xconfig')
if _logger.level == logging.NOTSET:
    _logger.setLevel(logging.WARN)


class FileMonitor(FileSystemEventHandler):
    def __init__(self, file: str, listener: Callable):
        self._file = file
        self._listener = listener
        self._path = os.path.dirname(os.path.abspath(file))
        self._observer = WatchdogObserver()
        self._observer.schedule(self, path=self._path, recursive=False)
        self._observer.start()
        self._last_event_time = datetime.datetime.now()

    def on_modified(self, event):
        if event.event_type == 'modified' and event.src_path == self._file:
            if not self._within_event_threshold():
                _logger.debug('File change detected for file: {0}'.format(self._file))
                self._listener()

    def _within_event_threshold(self):
        '''This funciton is needed because of ghost repetitive events for the same modify call.'''
        current_time = datetime.datetime.now()
        span = current_time - self._last_event_time
        within_threshold = span < datetime.timedelta(milliseconds=50)
        self._last_event_time = current_time
        return within_threshold
