"""\
Abstract Directive for L.E.A.R.N
================================

Author: Akshay Mestry (XAMES3) <xa@mes3.dev>
Created on: Wednesday, May 03 2023
Last updated on: Sunday, May 07 2023

This module provides a custom directive for L.E.A.R.N's custom theme,
that allows authors and contributors to add an abstract to their
documentation. An ``abstract`` is a brief summary of the document's
contents that is displayed prominently at the top of the page, helping
readers quickly understand the scope and purpose of the document.

L.E.A.R.N's abstract is created using the ``abstract`` directive, which
is included as part of this project. The directive is implemented below,
and is available to use by authors and contributors when building the
documentation.

.. note:: This directive is compatible with Sphinx 3.0 and higher.

.. note:: The abstract should be a single paragraph of text.

.. note::

    This module is designed specifically for the Sphinx's L.E.A.R.N
    theme, hence the directive may not be available or may be
    implemented differently for different themes. Please consult the
    documentation for more information.

The abstract can be styled using CSS. The class encapsulating the
abstract is ``learn-abstract`` and the abstract itself is ``abstract``.

.. code-block:: css

    .learn-abstract {
      text-align: left;
    }

    .abstract {
      ...
      max-width: 650px;
      margin: auto auto 2.5rem auto;
      ...
    }

    .abstract::before{
      ...
      font-weight: bold;
      content: "Abstract. ";             # The "Abstract" prefix...
      ...
    }

This will style the abstract with required colors and format.
"""

from __future__ import annotations

import typing as t

import jinja2
from docutils.nodes import Element
from docutils.nodes import Node
from docutils.parsers.rst import Directive
from docutils.parsers.rst import roles
from sphinx.writers.html import HTMLTranslator

__all__ = [
    "Abstract",
    "AbstractNode",
    "depart_abstract_html",
    "visit_abstract_html",
]

ABSTRACT_TEMPLATE: t.Final[jinja2.Template] = jinja2.Template(
    """<p class="abstract">{{ content }}</p>"""
)


class AbstractNode(Element):
    pass


class Abstract(Directive):
    """A directive class for the ``abstract`` directive.

    This class allows using a custom ``abstract`` directive and maps the
    source reStructuredText to ``AbstractNode`` element doctree node.

    By using the ``abstract`` directive, it allows contributors or
    authors to render an abstract for the provided content. This class'
    rendering HTML behavior is further extended using another Python
    function, ``visit_abstract_div``.

    Example::

        .. abstract::

            Some abstract about a topic...

    :var has_content: A boolean flag to allow content in the directive,
                      defaults to ``True``.
    :var final_argument_whitespace: A boolean flag, may the final
                                    argument contain whitespace, set to
                                    ``True``.
    """

    has_content: bool = True
    final_argument_whitespace: bool = True

    def run(self) -> list[Node]:
        """Create node from the reStructuredText source.

        This method processes the directive's arguments, options and
        content, and return a list of Docutils/Sphinx nodes that will be
        inserted into the document tree at the point where the directive
        was encountered.

        :return: List of Docutils node for ``abstract`` directive.
        """
        self.options["class"] = ["learn-abstract"]
        roles.set_classes(self.options)
        node = AbstractNode("\n".join(self.content), **self.options)
        self.add_name(node)
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]


def visit_abstract_html(self: HTMLTranslator, node: AbstractNode) -> None:
    """Node visitor function which maps ``AbstractNode`` element to the
    HTML output.

    This function allows the rendering of the abstract of a topic on the
    webpage. It relies on ``Jinja`` templating to perform the expansion
    and rendering of the HTML source code.
    """
    content = node.children[0].astext().replace("\n", " ")
    node.remove(node.children[0])
    html_src = ABSTRACT_TEMPLATE.render(content=content)
    self.body.append(f"{self.starttag(node, 'div')}{html_src}")


def depart_abstract_html(self: HTMLTranslator, node: AbstractNode) -> None:
    self.body.append("</div>")
