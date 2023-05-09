"""\
L.E.A.R.N's Sphinx Extension
============================

Author: Akshay Mestry (XAMES3) <xa@mes3.dev>
Created on: Wednesday, May 03 2023
Last updated on: Wednesday, May 03 2023

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
"""

from __future__ import annotations

import typing as t

from ._abstract import Abstract
from ._abstract import AbstractNode
from ._abstract import depart_abstract_html
from ._abstract import visit_abstract_html
from ._authors import Authors
from ._authors import AuthorsNode
from ._authors import depart_authors_html
from ._authors import visit_authors_html

if t.TYPE_CHECKING:
    from sphinx.application import Sphinx


def setup(app: Sphinx) -> dict[str, t.Any]:
    app.add_node(AbstractNode, html=(visit_abstract_html, depart_abstract_html))
    app.add_node(AuthorsNode, html=(visit_authors_html, depart_authors_html))
    app.add_directive("abstract", Abstract)
    app.add_directive("authors", Authors)
    return {"parallel_read_safe": True, "parallel_write_safe": True}
