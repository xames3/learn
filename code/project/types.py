"""\
Generic Project Types
=====================

Author: Akshay Mestry <xa@mes3.dev>
Created on: Friday, February 02 2024
Last updated on: Friday, February 02 2024

:copyright: (c) 2024 Akshay Mestry. All rights reserved.
:license: MIT, see LICENSE for more details.
"""

from __future__ import annotations

import logging
import os
import types
import typing as t

import matplotlib.typing

_T = t.TypeVar("_T", bound=t.Callable[..., t.Any])
_VT = t.TypeVar("_VT")
_Path = t.Union[str, os.PathLike[str]]
_Regex = t.Pattern[str]
_ColorType = matplotlib.typing.ColorType
_FinalStr = t.Final[str]
_StringList = list[str]
_Any = t.Any
_Logger = logging.Logger
_Record = logging.LogRecord
_Stream = t.IO[str]
_ExceptionInformation = (
    tuple[type, BaseException, types.TracebackType | None] | tuple[None, ...]
)
