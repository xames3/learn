"""\
Generic Neural Network Project
==============================

Author: Akshay Mestry <xa@mes3.dev>
Created on: Thursday, January 25 2024
Last updated on: Friday, February 02 2024

:copyright: (c) 2024 Akshay Mestry. All rights reserved.
:license: MIT, see LICENSE for more details.
"""

from .types import _T
from .types import _FinalStr
from .types import _StringList

__all__: _StringList = []

# Name of the codebase or the underlying project. This variable will be
# used throughout the application or the project and its lifecycle.
PROJECT: _FinalStr = "project"  # type: ignore


def export(defn: _T) -> _T:
    """Export callables.

    This implementation serves as a decorator function for lifting
    callable definitions out of the ``globals()`` dictionary and bringing
    them to top level without manipulating the ``__all__`` variable.

    .. code-block:: python

        from . import export

        @export
        def spam():
            ...

        @export
        class Foo:
            ...

    :param defn: Callable definitions, either function or class that
                 needs to be exported to top level.
    :returns: Exported callable definition.
    """
    globals()[defn.__name__] = defn
    __all__.append(defn.__name__)
    return defn


from . import config
from . import logging
from . import utils

# This global logger is configured to be used across the entire project
# to ensure consistent logging practices. It facilitates tracking
# project behavior, errors, and performance metrics in a unified manner.
# The logger is set up with predefined settings such as log format,
# level, and output destinations (e.g., console, file, etc.) to
# standardize log messages, making them easier to read and analyze.
logger = logging.getLogger(__name__)

# This configurator object acts as the central repository for all
# configuration settings used throughout the project. It encapsulates
# configurations related to various aspects of the project, such as
# available split details, project paths and feature toggles. By
# centralizing configuration management, the project benefits from a
# single source of truth for settings, enhancing maintainability
# and scalability.
logger.debug("Loading configurator instance...")
cfg = utils.Configurator(
    path=config.Path,
    plot=config.Plot,
    split=config.Split(),
)
