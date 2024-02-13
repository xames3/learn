"""\
L.E.A.R.N Sphinx Configuration
==============================

Author: Akshay Mestry <xa@mes3.dev>
Created on: Wednesday, April 12 2023
Last updated on: Monday, February 12 2024

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

        ``sphinx-build -EWaq -b html SOURCE-DIR OUTPUT-DIR``

For more information on configuring Sphinx and building documentation,
see the official Sphinx documentation here: https://shorturl.at/iwBZ5

.. versionadded:: 1.0.1
    Support for adding external links using ``_urls.txt`` and HTML tags
    using ``raw-html`` docutils role.

.. versionchanged:: 1.0.1
    Section numbering now skip the chapter title while enumerating.

.. versionadded:: 1.0.6
    Sphinx theme version to the footer alongside the copyright.

:copyright: (c) 2024 Akshay Mestry. All rights reserved.
:license: MIT, see LICENSE for more details.
"""

from __future__ import annotations

import importlib
import subprocess
import sys
import typing as t
import warnings
from os import path as p

from docutils import nodes
from docutils.transforms import Transform
from docutils.transforms import parts
from docutils.writers import _html_base
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.locale import __
from sphinx.registry import *

if t.TYPE_CHECKING:
    from types import ModuleType

    from sphinx.application import Sphinx

this = p.dirname(__file__)

MODULE_NAME: str = "learn"
EXTENSION_PATH: str = p.join(this, "_extensions/sphinx/ext/learn/__init__.py")
RAW_LINKS_PATH: str = p.join(this, "_extensions/_urls.txt")


def build_module() -> ModuleType:
    """Build the learn extension from ``_extensions`` directory."""
    spec = importlib.util.spec_from_file_location(MODULE_NAME, EXTENSION_PATH)
    module = importlib.util.module_from_spec(spec)  # type: ignore
    sys.modules[MODULE_NAME] = module
    spec.loader.exec_module(module)  # type: ignore
    return module


def load_extension(self, app: Sphinx, extname: str) -> None:
    """Monkey-patched ``SphinxComponentRegistry.load_extension``."""
    if extname in app.extensions:
        return
    if extname in EXTENSION_BLACKLIST:
        logger.warning(
            __(
                f"the extension {extname} was already merged with Sphinx "
                f"since version {EXTENSION_BLACKLIST[extname]}; this extension"
                " is ignored."
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
            logger.verbose(
                __("Original exception:\n") + traceback.format_exc()
            )
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


class NoTitleSectNum(Transform):
    """Automatically assigns numbers to the titles of document sections
    except the main title.

    .. versionadded:: 1.0.1
        Section numbering now skip the chapter title while enumerating.
    """

    def update_section_numbers(
        self, node: nodes.section, prefix: tuple = (), depth: int = 0
    ) -> None:
        """Add and update section title numbering recursively.

        :param node: Doctree node element.
        :param prefix: Tuple of string(s) to be prefixed, defaults to
                      ``()``.
        :param depth: Depth to recursively iterate over the section
                      titles, defaults to ``0``.
        """
        depth += 1
        if prefix:
            sectnum = 1
        else:
            sectnum = self.startvalue
        for child in node:
            if isinstance(child, nodes.section):
                numbers = prefix + (str(sectnum),)
                title = child[0]
                generated = nodes.generated(
                    "",
                    (
                        self.prefix
                        + ".".join(numbers[1:])
                        + self.suffix
                        + "\u00a0" * 3
                    ),
                    classes=["sectnum"],
                )
                title.insert(0, generated)
                title["auto"] = 1
                if depth < self.maxdepth:
                    self.update_section_numbers(child, numbers, depth)
                sectnum += 1


class MoreSpacedHTMLTranslator(nodes.NodeVisitor):
    """More spaced section number translator.

    .. versionadded:: 1.0.1
        Section numbering now skip the chapter title while enumerating.
    """

    def padding(self, node: nodes.generated) -> None:
        """Add padding to the section numbering.

        :param node: Doctree node element.
        :raises nodes.SkipNode
        """
        if "sectnum" in node["classes"]:
            sectnum = node.astext().rstrip(" ")
            section = self.encode(sectnum) if len(sectnum) != 3 else ""
            self.body.append(f'<span class="sectnum">{section}</span>')
            raise nodes.SkipNode


SphinxComponentRegistry.load_extension = load_extension  # type: ignore
StandaloneHTMLBuilder.supported_image_types = [
    "image/svg+xml",
    "image/gif",
    "image/png",
    "image/jpeg",
]
_html_base.HTMLTranslator.visit_generated = MoreSpacedHTMLTranslator.padding
parts.SectNum.update_section_numbers = NoTitleSectNum.update_section_numbers


class LearnProject(t.NamedTuple):
    """Configuration and metadata about the project."""

    # Project metadata
    author: str = "Akshay Mestry"
    copyright: str = "2024, Akshay Mestry"
    default_language: str = "en"
    main_title: str = "Learning the Essence of AI, Research, and Notations"
    release: str = build_module().__version__
    short_title: str = "Home"
    theme: str = "sphinx_book_theme"
    url: str = "https://github.com/xames3/learn"

    announcement: str = ""


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
# extensions coming with Sphinx (named ``sphinx.ext.*``) or your custom
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
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx_favicon",
    "sphinxcontrib.jquery",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# NOTE: This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    "_build",
    "_urls.txt",
    ".DS_Store",
    "Thumbs.db",
]

# HTML output options
# ====================
# The theme to use for HTML and HTML help pages along with page-wide
# settings.
favicons = [
    "img/favicon-16x16.png",
    "img/favicon-32x32.png",
]
html_context = {"default_mode": "light"}
html_show_sourcelink = False
html_theme = _project.theme
html_title = _project.short_title
html_theme_options = {
    "article_header_end": ["search-button"],
    "navigation_with_keys": True,
    "repository_url": _project.url,
    "secondary_sidebar_items": [],
    "show_prev_next": False,
    "footer_start": ["copyright"],
    "footer_center": ["theme-version"],
    "footer_end": ["last-updated"],
}
language = _project.default_language

# Add any paths that contain custom static files (such as style sheets)
# here, relative to this directory. They are copied after the builtin
# static files, so a file named ``default.css`` will overwrite the builtin
# ``default.css``.
html_static_path = ["_static"]
html_css_files = [
    "css/defaults.css",
    "css/learn.css",
]
html_js_files = [
    "js/learn.js",
]

# If not None, the timestamp is inserted at every page bottom, using the
# given strftime format.
git_cmd = [
    "git",
    "log",
    "--pretty=format:%cd",
    "--date=format:%b %d, %Y",
    "-n1",
]
try:
    html_last_updated_fmt = subprocess.check_output(git_cmd).decode("utf-8")
except Exception:
    warnings.warn("Couldn't retrieve last updated time from git logs [check]")
    html_last_updated_fmt = None

# Miscellaneous options
# =====================
# Extra configurations that are used throughout the build process.
copybutton_prompt_is_regexp = True
copybutton_prompt_text = (
    r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
)
intersphinx_mapping = {
    "Sphinx": ("https://www.sphinx-doc.org/en/stable/", None),
    "matplotlib": ("https://matplotlib.org/stable/", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "pandas": ("https://pandas.pydata.org/docs/", None),
    "python": ("https://docs.python.org/3", None),
    "scikit-learn": ("https://scikit-learn.org/stable/", None),
    "scipy": ("https://docs.scipy.org/doc/scipy/reference/", None),
}
todo_include_todos = True

# Add raw HTML code to the document.
rst_epilog = ""
with open(RAW_LINKS_PATH) as f:
    rst_epilog += f.read()
