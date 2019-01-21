import logging
import configparser
from .source import Source, SupportDepth
from .file_monitor import FileMonitor

_logger = logging.getLogger('xconfig')
if _logger.level == logging.NOTSET:
    _logger.setLevel(logging.WARN)


class INI(Source):
    def __init__(self, filename: str, read_only: bool = False, monitor: bool = False):
        super().__init__()
        self._filename = filename
        self._read_only = read_only
        self._monitor = FileMonitor(filename, self._notify_listeners) if monitor else None

    def read(self):
        cfg = configparser.ConfigParser()
        cfg.read(self._filename)
        blob = {}
        for section in cfg.sections():
            blob[section] = {}
            for key in cfg[section]:
                blob[section][key] = cfg[section][key]
        return blob

    def write(self, blob: dict, filename: str = None):
        cfg = configparser.ConfigParser()
        cfg.read_dict(blob)
        with open(filename if filename else self._filename, 'w') as configfile:
            cfg.write(configfile)

    @property
    def support_depth(self) -> SupportDepth:
        return SupportDepth.Flat
