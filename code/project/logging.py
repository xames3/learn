"""\
Generic Logging API
===================

Author: Akshay Mestry <xa@mes3.dev>
Created on: Thursday, January 25 2024
Last updated on: Tuesday, February 06 2024

A robust event logging system is written in this module along with an
assortment of related functions and classes. The ability for all the
modules to participate in logging is the key benefit of having a
dedicated OR rather customizable logging API. In order to configure the
system's default logging capabilities, it offers the core abstractions.

The objects from the builtin ``logging`` module are monkey-patched to
achieve this level of modularity. This module is also in responsible
of using colours to represent the severity of the logging levels on the
terminal.

:copyright: (c) 2024 Akshay Mestry. All rights reserved.
:license: MIT, see LICENSE for more details.
"""

from __future__ import annotations

import logging
import os
import re
import sys
import typing as t
from logging.handlers import RotatingFileHandler
from os import path as p

from . import export
from .types import _VT
from .types import _ExceptionInformation
from .types import _Logger
from .types import _Path
from .types import _Record
from .types import _Regex
from .types import _Stream

ansi_escape: _Regex = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
last_record: list[str] = []


def setup_logs_dir() -> _Path:
    """Create a log directory and log all stdin-stdout I/O to it.

    By default, the logs are maintained in the ``../logs`` directory. If
    the directory has been purged or does not already exist, this
    function will re-create it.
    """
    path = p.join(os.getcwd(), "logs")
    if not p.exists(path):
        os.makedirs(path, exist_ok=True)
    return path


def use_color(choice: bool) -> str:
    """Return log format based on the choice.

    If choice is ``True``, colored log format is returned else
    non-colored format is returned.

    :param choice: Boolean value to allow colored logs.
    :returns: Colored or non-colored log format based on choice.
    """
    if choice:
        return (
            "%(gray)s%(asctime)s %(color)s%(levelname)8s%(reset)s "
            "%(gray)s%(stack)s:%(lineno)d%(reset)s : %(message)s"
        )
    return "%(asctime)s %(levelname)8s %(stack)s:%(lineno)d : %(message)s"


@export
class Formatter(logging.Formatter):
    """ANSI color scheme formatter.

    This class formats the ``record.pathname`` and ``record.exc_info``
    attributes to generate an uniform and clear log message. The class
    then adds gray hues to the log's metadata and colorizes the levels.

    :var ansi_hue_map: Mapping of hues for different logging levels.
    :var ansi_attrs: Attributes to be added to the log record.
    :param fmt: Format for the log message.
    :param datefmt: Format for the log datetime.
    """

    # See https://stackoverflow.com/a/14693789/14316408 for the RegEx
    # logic behind the ANSI escape sequence.
    ansi_hue_map: dict[int, str] = {
        99: "\x1b[38;5;45m",
        90: "\x1b[38;5;242m",
        60: "\x1b[38;5;128m",
        50: "\x1b[38;5;197m",
        40: "\x1b[38;5;204m",
        30: "\x1b[38;5;215m",
        20: "\x1b[38;5;41m",
        10: "\x1b[38;5;14m",
        00: "\x1b[0m",
    }
    ansi_attrs: tuple[str, ...] = "color", "gray", "reset"

    def __init__(self, fmt: str, datefmt: str) -> None:
        """Initialize the formatter with suitable formats."""
        self.fmt = fmt
        self.datefmt = datefmt

    def colorize(self, record: _Record) -> None:
        """Add colors to the logging levels by manipulating log records.

        This approach is on the cutting edge because it modifies the
        record object in real time. This has the potential to be a
        disadvantage. We verify if the logging stream is a ``TTY``
        interface or not to avoid memory leaks. If we are certain that
        the stream is a ``TTY``, we alter the object.

        As a result, when writing to a file, this method avoids the
        record from containing unreadable ANSI characters.

        :param record: Logged event's instance.
        """
        # The same could have been done using the ``hasattr()`` too.
        # This ``isatty`` is a special attribute which is injected by
        # the ``StreamHandler()`` class.
        if getattr(record, "isatty", False):
            hue_map = zip(("color", "gray", "reset"), (record.levelno, 90, 0))
            for hue, level in hue_map:
                setattr(record, hue, self.ansi_hue_map[level])
        else:
            for attr in self.ansi_attrs:
                setattr(record, attr, "")

    def decolorize(self, record: _Record) -> None:
        """Remove ``color``, ``gray`` and ``reset`` attributes from the
        log record.

        This method is opposite of ``colorize()`` of the same class.
        It prevents the record from writing un-readable ANSI characters
        to a non-TTY interface.

        :param record: Logged event's instance.
        """
        for attr in self.ansi_attrs:
            delattr(record, attr)

    def formatException(self, ei: _ExceptionInformation) -> str:
        r"""Format exception information as text.

        This implementation does not work directly. The log formatter
        from the standard library is required. The parent class creates
        an output string with ``\n`` which needs to be truncated and
        this method does this well.

        :param ei: Information about the captured exception.
        :returns: Formatted exception string.
        """
        func, lineno = "<module>", 0
        klass, msg, tbk = ei
        if tbk:
            func, lineno = tbk.tb_frame.f_code.co_name, tbk.tb_lineno
        func = "on" if func in ("<lambda>", "<module>") else f"in {func}() on"
        return f"{klass.__name__ if klass else klass}: {msg} line {lineno}"

    @staticmethod
    def stack(path: str, func: str) -> str:
        """Format path and function as stack.

        :param path: Path of the module which is logging the event.
        :param func: Callable object's name.
        :returns: Spring-boot style formatted path, well kinda...

        .. note::

            If called from a module, the base path of the module would
            be used else ``shell`` would be returned for the interpreter
            (stdin) based inputs.
        """
        if path == "<stdin>":
            return "shell"  # Should not return this rightaway...
        if os.name == "nt":
            path = p.splitdrive(path)[1]
        # NOTE: This presumes we work through a virtual environment.
        # This is a safe assumption as we peruse through the site-
        # packages. In case, this is not running via the virtualenv, we
        # might get a different result.
        abspath = "site-packages" if "site-packages" in path else os.getcwd()
        path = path.split(abspath)[-1]
        path = path.replace(p.sep, ".")[path[0] != ":" : -3]
        if func not in ("<module>", "<lambda>"):
            path += f".{func}"
        return path

    def format(self, record: _Record) -> str:
        """Format log record as text.

        If any exception is captured then it is formatted using
        the ``formatException()`` and replaced with the original
        message.

        :param record: Logged event's instance.
        :returns: Captured and formatted output log message.
        """
        # Update the pathname and the invoking function name using the
        # stack. This stack will be set as a record attribute which will
        # allow us to use the %(stack)s placeholder in the log format.
        setattr(record, "stack", self.stack(record.pathname, record.funcName))
        if record.exc_info:
            record.msg = self.formatException(record.exc_info)
            record.exc_info = record.exc_text = None
        self.colorize(record)
        msg = logging.Formatter(self.fmt, self.datefmt).format(record)
        # Escape the ANSI sequence here as this will render the colors
        # on the TTY but won't add them to the non-TTY interfaces, for
        # example, log file.
        record.msg = ansi_escape.sub("", str(record.msg))
        self.decolorize(record)
        return msg


@export
class StreamHandler(logging.StreamHandler[_Stream]):
    """A StreamHandler derivative.

    Custom stream handler which adds an inspection of a TTY interface to
    the stream and avoids ``tqdm`` progress bar's interruption by
    logging output to the console.
    """

    def format(self, record: _Record) -> str:
        """Add hint if the specified stream is a TTY.

        The ``hint`` here, means the boolean specification as this
        attribute helps to identify a stream's interface. This solves a
        major problem when printing un-readable ANSI sequences to a
        non-TTY interface.

        :param record: Logged event's instance.
        :returns: Formatted string for the output stream.
        """
        if hasattr(self.stream, "isatty"):
            try:
                setattr(record, "isatty", self.stream.isatty())
            except ValueError:
                setattr(record, "isatty", False)
        else:
            setattr(record, "isatty", False)
        strict = super().format(record)
        delattr(record, "isatty")
        return strict

    def emit(self, record: _Record) -> None:
        """Emit a record.

        :param record: Logged event's instance.
        """
        try:
            msg = self.format(record)
            if record.levelname == "LOOP":
                last_record.append(msg)
            else:
                self.stream.write(msg + "\n")
            self.flush()
        except RecursionError:
            raise
        except Exception:
            self.handleError(record)


class Filter:
    """Filter loop logging level."""

    def __init__(self, level: int = 99) -> None:
        """Initialize ``Filter`` with a log level."""
        self.level = level

    def filter(self, record: _Record) -> bool:
        """Determine if a record is loggable or not."""
        return record.levelno < self.level


def init(
    logger: _Logger,
    level: int | None = None,
    fmt: str | None = None,
    datefmt: str | None = None,
    color: bool = True,
    filename: str | None = None,
    max_bytes: int = 10_000_000,
    backup_count: int = 10,
    encoding: str | None = None,
    filemode: str = "a",
    handlers: list[logging.Handler] | None = None,
    stream: _Stream | None = sys.stderr,
    capture_warnings: bool = True,
) -> _Logger:
    """Configure an application level logger.

    This function initializes a logger with default configurations for
    the logging system.

    If any handlers are provided as part of input, the function
    overrides the default behaviour in favour of the provided handler.
    It is a convenience function intended for use by simple applications
    to do one-shot configuration.

    :param logger: Logger instance.
    :param level: Minimum logging level of the event, defaults
                  to ``None``.
    :param fmt: Format for the log message, defaults to ``None``.
    :param datefmt: Format for the log datetime, defaults to ``None``.
    :param color: Boolean option to whether display colored log outputs
                  on the terminal or not, defaults to ``True``.
    :param filename: Log file's absolute path, defaults to ``None``.
    :param max_bytes: Maximum size in bytes after which the rollover
                      should happen, defaults to ``10 MB``.
    :param backup_count: Maximum number of files to archive before
                         discarding, defaults to ``10``.
    :param encoding: Platform-dependent encoding for the file, defaults
                     to ``None``.
    :param filemode: Mode in which the file needs to be opened, defaults
                    to append ``a`` mode.
    :param handlers: List of various logging handlers to use, defaults
                     to ``None``.
    :param stream: IO stream, defaults to ``sys.stderr``.
    :param capture_warnings: Boolean option to whether capture the
                             warnings while logging, defaults
                             to ``True``.
    :returns: Configured logger instance.
    """
    if level is None:
        level = logging.INFO
    logger.setLevel(level)
    if handlers is None:
        handlers = []
    for handler in logger.handlers:
        logger.removeHandler(handler)
        handler.close()
    if not logger.handlers:
        if fmt is None:
            fmt = use_color(color)
        if datefmt is None:
            datefmt = "%Y-%m-%dT%H:%M:%SZ"
        formatter = Formatter(fmt, datefmt)
        stream_handler = StreamHandler(stream)
        handlers.append(stream_handler)
        if filename:
            file_handler = RotatingFileHandler(
                filename, filemode, max_bytes, backup_count, encoding
            )
            file_handler.addFilter(Filter())
            handlers.append(file_handler)
        for handler in handlers:
            logger.addHandler(handler)
            handler.setFormatter(formatter)
    logging.captureWarnings(capture_warnings)
    return logger


@export
def getLogger(module: str, **kwargs: _VT) -> _Logger:
    """Return logger instance.

    This function is supposed to be used by the modules for logging.
    The logger generated by this function is a child which reports logs
    back to the parent logger defined by the ``init()``.

    The function is most useful for the intermediate modules which want
    to perform logging at the module level as this function returns a
    child logger. Whereas the ``init`` is an application level logger.

    :param module: Module to be logged.
    :returns: Logger instance.
    """
    logger = logging.getLogger(kwargs.pop("name")).getChild(module)
    setattr(logger, "loop", lambda *args: logger.log(99, *args))
    logging.addLevelName(99, "LOOP")
    filename = p.join(setup_logs_dir(), f"{module}.log")
    return init(logger, filename=filename, **kwargs)  # type: ignore
