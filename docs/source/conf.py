"""\
L.E.A.R.N Sphinx Configuration
==============================

Author: Akshay "XA" Mestry <xa@mes3.dev>
Created on: Wednesday, April 12 2023
Last updated on: Thursday, May 11 2023

This file contains the configuration settings for building the L.E.A.R.N
documentation using Sphinx, a popular Python documentation tool. Sphinx
is a powerful documentation generator that makes it easy to create high
quality technical documentation for technical projects.

This configuration file is used to specify the Sphinx documentation
build process. It tells Sphinx where to find the source files for the
documentation, what output format to generate, and other options that
control how the documentation is built.

Usage::

    To use this configuration file, copy it to the root directory of
    Sphinx project, in this case the ``docs`` directory and customize
    the settings as needed. You can then run the Sphinx build process by
    running the command:

        ``sphinx-build -W -b html SOURCE-DIR OUTPUT-DIR``

For more information on configuring Sphinx and building documentation,
see the official Sphinx documentation here: https://www.sphinx-doc.org/en/master/usage/configuration.html
"""

from __future__ import annotations

import importlib
import sys
import typing as t
from os import path as p

from sphinx.locale import __
from sphinx.registry import *

if t.TYPE_CHECKING:
    from types import ModuleType

    from sphinx.application import Sphinx

this = p.dirname(__file__)

MODULE_NAME: str = "learn"
EXTENSION_PATH: str = p.join(this, "_extensions/sphinx/ext/learn/__init__.py")


def build_module() -> ModuleType:
    """Build the learn extension from ``_extensions`` directory."""
    spec = importlib.util.spec_from_file_location(MODULE_NAME, EXTENSION_PATH)
    module = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
    sys.modules[MODULE_NAME] = module
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


def load_learn_extension(self, app: Sphinx, extname: str) -> None:
    """Monkey-patched ``SphinxComponentRegistry.load_extension``."""
    if extname in app.extensions:
        return
    if extname in EXTENSION_BLACKLIST:
        logger.warning(
            __(
                f"the extension {extname} was already merged with Sphinx since "
                f"version {EXTENSION_BLACKLIST[extname]}; this extension is"
                " ignored."
            )
        )
        return
    prefix = __(f"while setting up extension {extname}:")
    with prefixed_warnings(prefix):
        try:
            if extname == "sphinx.ext.learn":
                mod = build_module()
            else:
                mod = import_module(extname)
        except ImportError as err:
            logger.verbose(__("Original exception:\n") + traceback.format_exc())
            raise ExtensionError(
                __(f"Could not import extension {extname}"), err
            ) from err

        setup = getattr(mod, "setup", None)
        if setup is None:
            logger.warning(
                __(
                    f"extension {extname} has no setup() function; is it"
                    " really a Sphinx extension module?"
                ),
            )
            metadata: dict[str, t.Any] = {}
        else:
            try:
                metadata = setup(app)
            except VersionRequirementError as err:
                raise VersionRequirementError(
                    __(
                        f"The {extname} extension used by this project needs "
                        f"at least Sphinx v{err}; it therefore cannot be built"
                        " with this version."
                    )
                ) from err

        if metadata is None:
            metadata = {}
        elif not isinstance(metadata, dict):
            logger.warning(
                __(
                    f"extension {extname} returned an unsupported object from"
                    " its setup() function; it should return None or a"
                    " metadata dictionary"
                ),
            )
            metadata = {}
        app.extensions[extname] = Extension(extname, mod, **metadata)


SphinxComponentRegistry.load_extension = load_learn_extension  # type: ignore[method-assign]


class LearnProject(t.NamedTuple):
    """Configuration and metadata about the project."""

    # Project metadata
    author: str = 'Akshay "XA" Mestry'
    copyright: str = '2023, Akshay "XA" Mestry. All rights reserved'
    default_language: str = "en"
    main_title: str = "Learning & Exploring AI and its Real-world Networks"
    release: str = "1.0.0"
    short_title: str = "L.E.A.R.N"
    url: str = "https://github.com/xames3/learn"

    # Theme metadata
    theme: str = "sphinx_book_theme"


_project = LearnProject()

# Project information
# ===================
# This involves the metadata about the project like the name, copyright
# and release details.
author = _project.author
copyright = _project.copyright
project = _project.main_title
release = _project.release

# General configurations
# ======================
# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.githubpages",
    "sphinx.ext.imgmath",
    "sphinx.ext.intersphinx",
    "sphinx.ext.learn",
    "sphinx.ext.mathjax",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx_favicon",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# NOTE: This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    "_build",
    ".DS_Store",
    "Thumbs.db",
]

# HTML output options
# ====================
# The theme to use for HTML and HTML help pages along with page-wide
# settings.
favicons = [
    "favicon-16x16.png",
    "favicon-32x32.png",
    "logo.svg",
]
html_context = {"default_mode": "light"}
html_show_sourcelink = False
html_theme = _project.theme
html_title = _project.short_title
html_theme_options = {
    "article_header_end": ["search-button"],
    "logo": {"image_light": "_static/logo.png", "alt_text": "Home"},
    "navigation_with_keys": True,
    "repository_url": _project.url,
    "search_bar_text": "Search on L.E.A.R.N...",
    "secondary_sidebar_items": [],
    "show_prev_next": False,
}
language = _project.default_language

# Add any paths that contain custom static files (such as style sheets)
# here, relative to this directory. They are copied after the builtin
# static files, so a file named "default.css" will overwrite the builtin
# "default.css".
html_static_path = ["_static"]
html_css_files = [
    "css/defaults.css",
    "css/style.css",
]

# Miscellaneous options
# =====================
# Extra configurations that are used throughout the build process.
todo_include_todos = True
intersphinx_mapping = {
    "Sphinx": ("https://www.sphinx-doc.org/en/stable/", None),
    "matplotlib": ("https://matplotlib.org/stable/", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "pandas": ("https://pandas.pydata.org/docs/", None),
    "python": ("https://docs.python.org/3", None),
    "scikit-learn": ("https://scikit-learn.org/stable/", None),
    "scipy": ("https://docs.scipy.org/doc/scipy/reference/", None),
}
