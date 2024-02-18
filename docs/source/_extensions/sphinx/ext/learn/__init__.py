"""\
L.E.A.R.N's Sphinx Extension
============================

Author: Akshay Mestry <xa@mes3.dev>
Created on: Wednesday, May 03 2023
Last updated on: Saturday, December 23 2023

This module contains Sphinx's custom extension for L.E.A.R.N. Since
L.E.A.R.N uses a special ``research paper-esque`` aesthetics for it's UI
design it needs "special features" for it's documentation. Sphinx allows
adding ``extensions`` to the build process, each of which can modify
almost any aspect of document processing.

One can find several extensions contributed by various users in the
GitHub maintained, ``sphinx-contrib`` organization but for the sake of
L.E.A.R.N's design, the author chose to extend the functionality of
Sphinx by adding custom directives to it.

Written in Python, this extension is easy to install and configure, and
can be customized to suit the contributor's specific needs.

Usage::

    To use this extension, add it to the extension's list of the Sphinx
    project's ``conf.py`` file:

        extension = [
            ...
            "sphinx.ext.learn",
            ...
        ]

Contributors can configure the extension's features by adding the
relevant settings to the ``conf.py`` file.

.. note::

    Configuring this extension's behavior is still not available.

For more information on how to use this extension, please refer to the
documentation. The extension is fully documented with examples and usage
instructions to help future/fellow authors and contributors get started
quickly.

.. versionadded:: 1.0.1
    Added support for embedding links to author's profile. This allows
    us to link author's profile/url/resume to it's name in the author
    section itself.

.. versionadded:: 1.0.2
    Added support for creating a dedicated references section through
    the ``references`` directive. The directive handles all the
    external links used in the current document and puts them together
    as a list.

.. versionchanged:: 1.0.2
    Directive extensions are now called with their names, no underscore
    prefixes are used.

.. versionchanged:: 1.0.2
    Major refactoring of the ``__init__`` module. The module now
    supports dynamic object (class and functions) generation rather
    than importing each object explicitly from the module.

.. versionchanged:: 1.0.3
    Author details are now formatted as table instead of list.

.. versionadded:: 1.0.4
    Added support for ``tweet`` directive to embed Twitter's or X's
    posts into the L.E.A.R.N document.

.. versionadded:: 1.0.5
    Added support for ``keywords`` directive to add auto generated
    keywords for the L.E.A.R.N document.

.. versionadded:: 1.0.6
    Added support for ``reading`` directive to add reading time prompt
    for the L.E.A.R.N document.

.. versionadded:: 1.0.7
    Added support for custom Python code ``lexing`` using Pygments color
    theme for the L.E.A.R.N document.
"""

from __future__ import annotations

import importlib
import sys
import typing as t
from os import path as p

from .tweet import Tweet
from .tweet import embed_twitter_js

if t.TYPE_CHECKING:
    from sphinx.application import Sphinx

__version__: str = "1.0.7"

this = p.dirname(__file__)
directives: list[str] = [
    "Abstract",
    "Authors",
    "Keywords",
    "Reading",
    "References",
]


def setup(app: Sphinx) -> dict[str, t.Any]:
    """Bootstrapping L.E.A.R.N directives.

    :param app: Sphinx application class.
    :returns: Dictionary of Sphinx's read-write settings.

    .. versionchanged:: 1.0.2
        The ``setup`` function supports dynamic object (class and
        functions) generation rather than importing each object
        explicitly from the module.

    .. versionadded:: 1.0.4
        Added support for ``tweet`` directive.

    .. versionadded:: 1.0.5
        Added support for ``keywords`` directive.

    .. versionadded:: 1.0.6
        Added support for ``reading`` directive.
    """
    # TODO (xames3): Check implementation of lazy module import to
    # minimize the overhead of importing larger directive modules in
    # future.
    for directive in directives:
        title = directive
        directive = directive.lower()
        spec = importlib.util.spec_from_file_location(
            directive, p.join(this, f"{directive}.py")
        )
        module = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
        sys.modules[directive] = module
        spec.loader.exec_module(module)  # type: ignore[union-attr]
        directive_class = getattr(module, f"{title}")
        directive_node = getattr(module, f"{title}Node")
        directive_visit_node = getattr(module, f"visit_{directive}_html")
        directive_depart_node = getattr(module, f"depart_{directive}_html")
        app.add_node(
            directive_node, html=(directive_visit_node, directive_depart_node)
        )
        app.add_directive(directive, directive_class)
    app.add_directive("tweet", Tweet)
    app.connect("html-page-context", embed_twitter_js)
    return {"parallel_read_safe": True, "parallel_write_safe": True}
