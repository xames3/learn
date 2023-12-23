"""\
Reading Time Directive for L.E.A.R.N
====================================

Author: Akshay Mestry <xa@mes3.dev>
Created on: Friday, December 22 2023
Last updated on: Saturday, December 23 2023

This module provides a custom directive for L.E.A.R.N's custom theme,
that allows authors and contributors to add a reading time prompt to
their documentation.

L.E.A.R.N's reading time prompt is created using the ``reading``
directive, which is included as part of this project. The directive is
implemented below, and is available to use by authors and contributors
when building the documentation.

.. note:: This directive is compatible with Sphinx 3.0 and higher.

.. note:: The reading should be a single paragraph of text.

.. note::

    This module is designed specifically for the Sphinx's L.E.A.R.N
    theme, hence the directive may not be available or may be
    implemented differently for different themes. Please consult the
    documentation for more information.

The reading time prompt can be styled using CSS. The class encapsulating
the prompt is ``learn-reading``.

.. code-block:: css

    .learn-reading {
      text-align: center;
    }

This will style the prompt with required colors and format.
"""

from __future__ import annotations

import typing as t

from docutils.nodes import Element
from docutils.nodes import Node
from docutils.parsers.rst import Directive
from docutils.parsers.rst import roles
from sphinx.writers.html import HTMLTranslator

__all__ = [
    "Reading",
    "ReadingNode",
    "depart_reading_html",
    "visit_reading_html",
]

READING_PROMPT_TEMPLATE: t.Final[
    str
] = """<p id="readingTime">0 mins read</p>"""


class ReadingNode(Element):
    pass


class Reading(Directive):
    """A directive class for the ``reading`` directive.

    This class allows using a custom ``reading`` directive and maps
    the source reStructuredText to ``ReadingNode`` element doctree
    node.

    By using the ``reading`` directive, it allows contributors or
    authors to render a reading time prompt for the written content.
    This class' rendering HTML behavior is further extended using
    another Python function, ``visit_reading_div``.

    Example::

        .. reading::

    :var has_content: A boolean flag to allow content in the directive,
                      defaults to ``False``.
    :var final_argument_whitespace: A boolean flag, may the final
                                    argument contain whitespace, set to
                                    ``False``.
    """

    has_content: bool = False
    final_argument_whitespace: bool = False

    def run(self) -> list[Node]:
        """Create node from the reStructuredText source.

        This method processes the directive's arguments, options and
        content, and return a list of Docutils/Sphinx nodes that will be
        inserted into the document tree at the point where the directive
        was encountered.

        :return: List of Docutils node for ``reading`` directive.
        """
        self.options["class"] = ["learn-reading"]
        roles.set_classes(self.options)
        node = ReadingNode("\n".join(self.content), **self.options)
        self.add_name(node)
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]


def visit_reading_html(self: HTMLTranslator, node: ReadingNode) -> None:
    """Node visitor function which maps ``ReadingNode`` element to
    the HTML output.

    This function allows the rendering of the reading time prompt of a
    topic on the webpage. It relies on ``Jinja`` templating to perform
    the expansion and rendering of the HTML source code.
    """
    self.body.append(f"{self.starttag(node, 'div')}{READING_PROMPT_TEMPLATE}")


def depart_reading_html(self: HTMLTranslator, node: ReadingNode) -> None:
    self.body.append("</div>")
