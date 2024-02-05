"""\
Generic Project Configurations
=============================

Author: Akshay Mestry <xa@mes3.dev>
Created on: Friday, January 26 2024
Last updated on: Friday, February 02 2024

:copyright: (c) 2024 Akshay Mestry. All rights reserved.
:license: MIT, see LICENSE for more details.
"""

from __future__ import annotations

import typing as t
from os import path as p

import matplotlib.colors as mcolors

from . import export
from .types import _Path
from .utils import AttrDict


@export
class Split(t.NamedTuple):
    """Container class for representing dataset splits in a ML context.

    This class is a ``NamedTuple`` used to define and access the
    standard dataset splits commonly used in machine learning: training,
    validation, and test sets. Each field in the tuple represents a
    dataset split and is initialized with default split names.

    .. code-block:: python

        >>> split = Split()
        >>> split.train
        "train"
        >>>

    :var train: The name identifier for the training dataset split. This
                split is typically used for training the machine
                learning model. It's the largest portion of the dataset
                and is used to fit the model parameters. Defaults to
                ``train``.
    :var validation: The name identifier for the validation dataset
                     split. This split is used for tuning the
                     hyperparameters of the model and for providing an
                     unbiased evaluation of a model fit during the
                     training phase. It's a subset of the dataset used
                     to provide an unbiased evaluation of a model fit on
                     the training dataset while tuning model
                     hyperparameters. Defaults to ``validation``.
    :var test: The name identifier for the test dataset split. This split
               is used for providing an unbiased evaluation of a final
               model fit on the training dataset. It's a subset of the
               dataset used to assess the performance of the final model
               after the model has gone through initial vetting by the
               validation set. Defaults to ``test``.

    .. note::

        The default names for the splits are set as ``train``,
        ``validation``, and ``test``, but these can be overridden if
        different naming conventions are preferred or required.
    """

    train: str = "train"
    validation: str = "validation"
    test: str = "test"


@export
class Path:
    """Utility class for managing directory paths within the project
    structure.

    This class provides convenient access to common directories used in
    data science and machine learning projects, such as models, figures,
    and data (both raw and processed). It centralizes the paths to
    different project directories, ensuring consistency and ease of
    maintenance. Each attribute in the class represents a specific
    directory path and is initialized to a default location relative to
    the project's root directory.

    :var models: Absolute path to the directory where machine learning
                 models are saved. Defaults to ``./models`` directory
                 relative to the project root. This directory is
                 intended for storing trained model files.
    :var figures: Absolute path to the directory for storing graphical
                 figures, such as plots and charts generated during
                 analysis or model evaluation. Defaults to ``./figures``
                 directory relative to the project root.
    :var data: Absolute path to the main data directory of the project.
               This directory is intended as the primary location for
               all data used in the project. Defaults to ``./data``
               directory relative to the project root.
    :var raw: Absolute path to the directory for storing raw data files.
              Raw data is data that has not been processed or altered
              from its original state. Defaults to ``./data/raw``
              directory, indicating that it is a subdirectory of the
              main data directory.
    :var processed: Absolute path to the directory for storing processed
                    data. Processed data is data that has been
                    transformed or formatted for analysis or modeling.
                    Defaults to ``./data/processed`` directory,
                    indicating that it is a subdirectory of the main
                    data directory.

    .. note::

        The default paths are set as relative paths from the project's
        root directory, but they can be modified as needed to fit
        different project structures or directory naming conventions.
    """

    models: _Path = p.abspath("./models")
    figures: _Path = p.abspath("./figures")
    data: _Path = p.abspath("./data")
    raw: _Path = p.abspath("./data/raw")
    processed: _Path = p.abspath("./data/processed")


@export
class Plot:
    """Configuration class for Matplotlib plot customizations.

    This class provides a structured way to define and access common plot
    customizations, such as color schemes, plot parameters, and styles
    for different aspects of data visualization.

    It utilizes ``utils.AttrDict`` for easier attribute access and
    modification. The class primarily focuses on customizing aspects of
    Matplotlib plots, including color settings for different plot
    elements, global plot parameters, and predefined styles for
    consistency across different plots.

    :var colors: A dictionary of color names mapped to their respective
                 RGB values from Matplotlib's ``TABLEAU_COLORS``. This
                 attribute provides a convenient way to access commonly
                 used colors for plot elements.
    :var params: A dictionary containing global parameters for
                 Matplotlib plots. These parameters are used to configure
                 aspects like margin settings, figure layout, and
                 resolution.
    :var style: A string representing the style template to be used for
                Matplotlib plots. This attribute allows for the quick
                application of a predefined style across multiple plots.
    :var train: An ``AttrDict`` containing labels and color
                customizations specific to training data plots. This
                includes settings for accuracy and loss plots, as well as
                the default color to represent training data.
    :var validation: An ``AttrDict`` similar to ``train``, but specific
                     to validation data plots. It contains labels and
                     color settings for accuracy and loss plots related
                     to validation data.
    :var test: An ``AttrDict`` for test data plots, containing labels
               and color settings for accuracy and loss plots in the
               context of testing data.

    .. note::

        The ``colors``, ``params``, ``style``, ``train``, ``test``, and
        ``validation`` attributes are initialized with default values
        but can be modified to fit different visualization requirements or
        preferences.
    """

    colors: AttrDict = AttrDict(
        {
            "blue": mcolors.TABLEAU_COLORS["tab:blue"],
            "brown": mcolors.TABLEAU_COLORS["tab:brown"],
            "cyan": mcolors.TABLEAU_COLORS["tab:cyan"],
            "gray": mcolors.TABLEAU_COLORS["tab:gray"],
            "green": mcolors.TABLEAU_COLORS["tab:green"],
            "olive": mcolors.TABLEAU_COLORS["tab:olive"],
            "orange": mcolors.TABLEAU_COLORS["tab:orange"],
            "pink": mcolors.TABLEAU_COLORS["tab:pink"],
            "purple": mcolors.TABLEAU_COLORS["tab:purple"],
            "red": mcolors.TABLEAU_COLORS["tab:red"],
        }
    )
    params: dict[str, t.Any] = {
        "axes.edgecolor": "#b0b0b0",
        "axes.grid.axis": "y",
        "axes.grid": True,
        "axes.xmargin": 0,
        "axes.ymargin": 0,
        "figure.autolayout": True,
        "figure.dpi": 200,
        "font.family": "serif",
        "font.serif": ["Monaco"],
        "font.size": 7.0,
        "grid.alpha": 0.2,
        "legend.fancybox": True,
        "xtick.color": "#b0b0b0",
        "xtick.labelcolor": "black",
        "ytick.color": "#b0b0b0",
        "ytick.labelcolor": "black",
    }
    style: str = "seaborn-v0_8-whitegrid"
    train: AttrDict = AttrDict(
        {
            "accuracy": "Training Accuracy",
            "loss": "Training Loss",
            "color": colors.blue,
        }
    )
    validation: AttrDict = AttrDict(
        {
            "accuracy": "Validation Accuracy",
            "loss": "Validation Loss",
            "color": colors.red,
        }
    )
    test: AttrDict = AttrDict(
        {
            "accuracy": "Testing Accuracy",
            "loss": "Testing Loss",
            "color": colors.green,
        }
    )
