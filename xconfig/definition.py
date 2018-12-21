import collections.abc as abc
import datetime
import logging
import os
import time
from enum import Enum
from typing import Any, Callable
import types

_logger = logging.getLogger('xconfig')
if _logger.level == logging.NOTSET:
    _logger.setLevel(logging.WARN)


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
    def __init__(self, tag: str = None, is_root: bool = True):
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


class Definition(_RootSection):
    def __init__(self):
        super().__init__()


class Config(types.SimpleNamespace):
    def __init__(self, definition: Definition):
        self._definition = definition
        self._source = None

    @staticmethod
    def loads(self, definition: Definition, source: Source) -> Config:
        config = Config(definition)
        config.load(source)
        return config
    
    def load(self, source: Source):
        if self._source:
            self._source.detach_change_listener(self._on_source_changed)
        self._source = source
        self._source.attach_change_listener(self._on_source_changed)
        self._config = Config(self)
        _load_config(self, self._definition)
        return self._config
    
    def save(self):
        self._save_config(self, self._definition)

    def _on_source_changed(self):
        pass


def _load_config(config: Config, definition: Definition):
    pass

def _save_definition(config: Config, Definition: Definition):
    pass
