"""\
Generic Visualization API
=========================

Author: Akshay Mestry <xa@mes3.dev>
Created on: Friday, January 26 2024
Last updated on: Friday, February 02 2024

:copyright: (c) 2024 Akshay Mestry. All rights reserved.
:license: MIT, see LICENSE for more details.
"""

from __future__ import annotations

import re
import typing as t
from collections import defaultdict as ddict
from os import path as p

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes._axes import Axes
from matplotlib.backend_bases import Event
from matplotlib.figure import Figure

from . import cfg
from . import export
from . import logger
from .types import _VT
from .utils import convert_case


@export
def ema_smoothening(scalars: list[float], weight: float = 0.75) -> list[float]:
    """Implementation of EMA smoothing used for TensorBoard.

    An exponential moving average (EMA), also known as an exponentially
    weighted moving average (EWMA), is a first-order infinite impulse
    response filter that applies weighting factors which decrease
    exponentially.

    :param scalars: List of real scalar values.
    :param weight: Weight setting for smoothening, defaults to ``0.75``.
    :returns: List of smoothen-ed scalars.

    .. seealso::

        [1] Implementation based on solution provided on StackOverflow,
            here: https://stackoverflow.com/a/49357445
        [2] Exponential Moving Average: https://shorturl.at/oEIQT
    """
    smoothed: list[float] = []
    last = scalars[0]
    for point in scalars:
        tmp = last * weight + (1 - weight) * point
        smoothed.append(tmp)
        last = tmp
    return smoothed


class CurveMeta(type):
    """A metaclass for creating classes with predefined record-keeping
    capabilities and type-naming behaviors.

    The ``CurveMeta`` class serves as a metaclass, which means it defines
    the behavior of class objects themselves, rather than instances of
    those classes. This metaclass is particularly designed to
    automatically include additional attributes in classes for
    record-keeping purposes and to enforce specific naming conventions.

    The classes created using this metaclass will have a dynamic set of
    attributes based on the splits defined in a configuration object. They
    will also have a ``type`` attribute derived from the class name.
    """

    def __new__(
        mcls, name: str, bases: tuple[type, ...], namespace: dict[str, _VT]
    ) -> type:
        """Create and return a new class with additional attributes for
        record-keeping and type identification.
        """
        cls = super().__new__(mcls, name, bases, namespace)
        cls.records: ddict = ddict(list)  # type: ignore
        for split in cfg.split:
            setattr(cls, split, cls.records[split])  # type: ignore
        cls.type = cls.__name__.lower()  # type: ignore
        return cls


@export
class Curve(metaclass=CurveMeta):
    """A class for logging and plotting records for training,
    validation, and testing splits.

    The ``Curve`` class uses a metaclass ```CurveMeta``` for automatic
    record-keeping and type-naming behaviors. It is designed to track
    and visualize data across different phases of machine learning
    model training, such as training, validation, and testing. The class
    allows for easy logging of metrics and provides functionalities to
    plot these metrics with options like smoothing and drawing
    confidence intervals.

    .. code-block:: python

        >>> class Accuracy(Curve):
        ...     pass
        ...
        >>> curve = Curve()
        >>> curve.accuracy.plot(train=0.5, validation=0.45)
        >>> curve.accuracy.simple_plot()

    :var curves: A class-level dictionary that keeps track of all
                 subclasses of ``Curve``. This allows the class to
                 maintain a registry of all curve types.

    .. seealso::

        [1] Read about Matplotlib styles and default settings, here:
            https://shorturl.at/djuMN
        [2] To see the plot configurations, read: ``config.Plot``.
        [3] To see how the derived curves are renamed from ``Curve``
            class, read: ``utils.convert_case``.
    """

    curves: t.Dict[str, type[Curve]] = {}

    def __init_subclass__(cls) -> None:
        """Register curves.

        This method is called when a class is subclassed. This allows
        the ``Curve`` class to keep a track of the derived ``curves``.
        """
        curve = convert_case(cls.__name__)
        logger.debug(f"Registering {curve}...")
        cls.curves[curve] = cls

    def __new__(cls, style: str | None = None) -> type:  # type: ignore
        """Create and return a new ``Curve`` class with curves and
        updated matplotlib settings.
        """
        for curve, instance in cls.curves.items():
            setattr(cls, curve, instance)
        cls.style = style
        if cls.style is None:
            cls.style = "default"
        logger.debug(f"Using {cls.style} style for Matplotlib plots...")
        cls.update_matplotlib_settings()
        return cls

    @classmethod
    def update_matplotlib_settings(cls) -> None:
        """Applies the specified Matplotlib style settings and updates
        Matplotlib's rcParams as per the configuration.
        """
        plt.style.use(cls.style)
        logger.debug("Updating Matplotlib rc file...")
        plt.rcParams.update(cfg.plot.params)

    @classmethod
    def log(cls, **kwargs: _VT) -> None:
        """Logs data points to the appropriate category (like ``train``,
        ``validation``, ``test``) based on the provided keyword
        arguments.

        This method facilitates the dynamic tracking of different
        metrics as the training process progresses.
        """
        for k, v in kwargs.items():
            if k in cfg.split:
                getattr(cls, k).append(v)

    @classmethod
    def confidence_interval(
        cls, y: np.ndarray, color: str, alpha: float = 0.3
    ) -> None:
        """Adds a confidence interval to a given plot.

        The interval is calculated based on the mean and standard
        deviation of the provided ``y``. This method enhances the
        plot by visually representing the variability or uncertainty in
        the data.

        :param y: Array-like or scalars to plot the confidence interval
                  against with.
        :param color: Color of the confidence interval.
        :param alpha: Alpha value or opacity of the confidence interval,
                      defaults to ``0.3``.
        """
        x = np.arange(len(y))
        ci = 0.1 * np.std(y) / np.mean(y)
        plt.fill_between(x, (y - ci), (y + ci), color=color, alpha=alpha)

    @classmethod
    def legend(cls, axs: Axes, figure: Figure, flag: bool) -> None:
        """Makes the legend of the plot interactive.

        This method allows clicking on a legend item to toggle the
        visibility of the corresponding plot line. This method enhances
        the usability of plots with multiple data series.

        :param axs: Axes instances of the plot.
        :param figure: Figure instance of the plot.
        """
        legend = axs.legend()
        legend.set_draggable(True)
        if flag:
            return
        line_map = zip(axs.get_lines(), legend.get_lines())
        map_legend_to_ax = {l: a for a, l in line_map}

        def on_pick(event: Event) -> None:
            legend_line = event.artist  # type: ignore
            try:
                ax_line = map_legend_to_ax[legend_line]
                visible = not ax_line.get_visible()
                ax_line.set_visible(visible)
            except KeyError:
                visible = False
            legend_line.set_alpha(1.0 if visible else 0.2)
            figure.canvas.draw()

        for line in legend.get_lines():
            line.set_picker(5)
            line.set_pickradius(5)
        figure.canvas.mpl_connect("pick_event", on_pick)

    @classmethod
    def simple_plot(
        cls,
        smooth: bool = True,
        title: str | None = None,
        xlabel: str = "Epochs",
        ylabel: str | None = None,
        confidence_interval: bool = False,
    ) -> None:
        """Creates a simple plot of the logged data.

        This method offers various customization options, including
        smoothing of curves, adding titles and axis labels, and the
        option to draw confidence intervals. This method provides a quick
        way to visualize the performance metrics.
        """
        if ylabel is None:
            ylabel = cls.type.title()  # type: ignore
        figure, axs = plt.subplots()
        for split, y in cls.records.items():  # type: ignore
            if not len(y):
                continue
            if smooth:
                y = ema_smoothening(y)
            y = np.array(y)
            label = f"{split} {cls.type}".title()  # type: ignore
            color = getattr(getattr(cfg.plot, split), "color")
            axs.plot(y, label=label, alpha=0.7, color=color)
            axs.set_title(title)  # type: ignore
            axs.set_xlabel(xlabel)
            axs.set_ylabel(ylabel)
            axs.tick_params(direction="inout", length=5)
            if confidence_interval:
                cls.confidence_interval(y, color)
        cls.legend(axs, figure, confidence_interval)
        plt.tight_layout()
        if title:
            cls.save(title)
        plt.show()

    @classmethod
    def save(cls, name: str | None = None) -> None:
        """Save plot as PNG."""
        if name is None:
            name = ""
        name = re.sub(r"[\W_]+", "_", name) + ".png"
        name = name.lower()
        path = p.join(cfg.path.figures, name)
        plt.savefig(path)
        logger.debug(f"Plot saved at {path!r}...")


@export
class Accuracy(Curve):
    """Record accuracies."""


@export
class Loss(Curve):
    """Record losses."""
