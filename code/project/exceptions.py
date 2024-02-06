"""\
Generic Exceptions
==================

Author: Akshay Mestry <xa@mes3.dev>
Created on: Sunday, February 04 2024
Last updated on: Sunday, February 04 2024

:copyright: (c) 2024 Akshay Mestry. All rights reserved.
:license: MIT, see LICENSE for more details.
"""

import typing as t

from . import export
from . import logger


class ProjectExecutionError(Exception):
    """Base class for all errors raised by the project."""

    explanation: str

    def __init__(self, description: t.Optional[str] = None) -> None:
        """Initialize exception with error description."""
        if description:
            self.explanation = description
        logger.exception(self.explanation)
        super().__init__(self.explanation)


@export
class OutputFormatError(ProjectExecutionError):
    """Error to be raised when the output format is not supported."""
