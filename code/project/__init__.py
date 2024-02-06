"""\
Generic Neural Network Project
==============================

Author: Akshay Mestry <xa@mes3.dev>
Created on: Thursday, January 25 2024
Last updated on: Monday, February 05 2024

:copyright: (c) 2024 Akshay Mestry. All rights reserved.
:license: MIT, see LICENSE for more details.
"""

import getpass
import os
import platform
import time

from .types import _T
from .types import _FinalStr
from .types import _StringList

__all__: _StringList = []

# Name of the codebase or the underlying project. This variable will be
# used throughout the application or the project and its lifecycle.
# The primary log file for the entire application will be logged under
# this name. Hence this name is critical in identifying the instance
# which is calling the project level code instead of module-level.
PROJECT: _FinalStr = "project"  # type: ignore

# Current stable version of the project.
VERSION: str = "1.0.0"

# Name of the system's network where the application or the project is
# running. This name is important for identifying on which system was
# the application or the project running when comparing the log files.
SYSTEM: str = platform.node()


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

big_bang = time.time()

# This configurator object acts as the central repository for all
# configuration settings used throughout the project. It encapsulates
# configurations related to various aspects of the project, such as
# available split details, project paths and feature toggles. By
# centralizing configuration management, the project benefits from a
# single source of truth for settings, enhancing maintainability
# and scalability.
cfg = utils.Configurator(
    log=config.Log,
    path=config.Path,
    plot=config.Plot,
    profile=config.Profile(),
)

# This global logger is configured to be used across the entire project
# to ensure consistent logging practices. It facilitates tracking
# project behavior, errors, and performance metrics in a unified manner.
# The logger is set up with predefined settings such as log format,
# level, and output destinations (e.g., console, file, etc.) to
# standardize log messages, making them easier to read and analyze.
kwargs = {"name": cfg.log.name, "level": cfg.log.level, "color": cfg.log.color}
logger = logging.getLogger(__name__, **kwargs)
logger.info(
    f"Starting application: {PROJECT} v{VERSION} on {SYSTEM} with "
    f"PID {os.getpid()} (at {os.getcwd()} by {getpass.getuser()})"
)

from . import exceptions

profile = None
if profile is None:
    logger.info("No profile set, falling back to default profile: train")
    profile = cfg.profile.train
else:
    logger.info(f"Running {PROJECT} with set profile: {profile}")

logger.info(f"Logger initialized with log level: {cfg.log.level}")
logger.info(
    f"Module imports for {PROJECT}: initialization completed in "
    f"{time.time() - big_bang:.3f} secs"
)
