"""\
L.E.A.R.N Utilities API
=======================

Author: Akshay Mestry <xa@mes3.dev>
Created on: Friday, January 26 2024
Last updated on: Friday, February 02 2024

:copyright: (c) 2024 Akshay Mestry. All rights reserved.
:license: MIT, see LICENSE for more details.
"""

from __future__ import annotations

import re

from . import export
from .types import _VT
from .types import _Any


@export
class Configurator(dict):
    """A dictionary-like class that functions as a configurator, allowing
    keys to be accessed as attributes.

    This class extends the standard Python dictionary to provide a more
    convenient way to handle configuration parameters. It allows access
    to dictionary keys using attribute notation, which can be more
    readable and concise, especially when dealing with nested
    configurations.

    The class is designed to be flexible and easy to use for various
    configuration needs in software applications. The ``Configurator``
    class can handle nested dictionaries by converting them
    into ``Configurator`` instances, enabling attribute-like access at
    multiple levels.

    .. warning::

        This class overrides the ``__setattr__`` and ``__delattr__``
        methods to behave like ``dict.__setitem__`` and
        ``dict.__delitem__``, respectively. This means that attributes
        can be set and deleted just like dictionary keys, and these
        changes will be reflected in the dictionary data structure.
    """

    def __init__(self, **kwargs: _VT) -> None:
        """Initialize ``Configurator`` with config parameters."""
        super().__init__(**kwargs)
        for k, v in kwargs.items():
            self[k] = Configurator(**v) if isinstance(v, dict) else v

    def __getattr__(self, attr: str) -> _Any:
        """Overrides the default attribute access method and returns key
        as attribute.
        """
        if attr in self:
            return self[attr]
        raise AttributeError(f"Couldn't find attribute: {attr!r}")

    __setattr__ = dict.__setitem__  # type: ignore
    __delattr__ = dict.__delitem__  # type: ignore


@export
class AttrDict(dict):
    """A dictionary subclass that enables attribute-style access to its
    key-value pairs.

    The ``AttrDict`` class extends the standard Python dictionary,
    allowing users to access the dictionary's keys as if they were
    attributes. This feature enhances code readability and convenience
    in accessing data, especially in settings where dot notation is
    preferred over bracket notation for key access.
    
    The class retains all the functionality of a standard Python
    dictionary and is compatible with its methods.

    .. note::

        While ``AttrDict`` provides a convenient way to access key
        values, care should be taken not to confuse keys with the
        dictionary's native methods and attributes.
    """

    def __getattr__(self, attr: str) -> _Any:
        """Overrides the default attribute access method and returns
        key as attribute.
        """
        if attr in self:
            return self[attr]
        raise AttributeError(f"Couldn't find attribute: {attr!r}")


@export
def convert_case(name: str) -> str:
    """Convert ``PascalCase`` class names to ``SnakeCase``.

    :param name: Name of the class in PascalCase.
    :returns: Name conformed to SnakeCase.
    """
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()
