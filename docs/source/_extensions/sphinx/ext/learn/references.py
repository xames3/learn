"""\
Reference Directive for L.E.A.R.N
=================================

Author: Akshay Mestry <xa@mes3.dev>
Created on: Friday, July 28 2023
Last updated on: Monday, July 31 2023

This module provides a custom directive for L.E.A.R.N's custom theme,
that allows authors and contributors to add a dedicated references
section to their documentation. The directive identifies and collects all
the links present within the documentation page and collates them in a
dedicated section for easy reference.

L.E.A.R.N's external references are created using the ``references``
directive, which is included as part of this project. The directive is
implemented below, and is available to use by authors and contributors
when building the documentation.

.. note:: This directive is compatible with Sphinx 3.0 and higher.

.. note:: It is encouraged to mention references for credibility.

.. note::

    This module is designed specifically for the Sphinx's L.E.A.R.N
    theme, hence the directive may not be available or may be
    implemented differently for different themes. Please consult the
    documentation for more information.

The references can be styled using CSS. The class encapsulating the
reference is ``learn-references`` and the references itself are
``references``.

.. code-block:: css

    .learn-references ol {
      ...
      text-align: left;
      font-size: 1.375rem;
      ...
    }

    .learn-references>ol>li>p {
      ...
      text-align: left;
      ...
    }

    .references-border {
      ...
      font-size: 1.375rem;
      ...
    }

This will style the list of references with required colors and format.

.. versionadded:: 1.0.2
    Added support for creating a dedicated references section through
    the ``references`` directive. The directive handles all the
    external links used in the current document and puts them together
    as a list.
"""

from __future__ import annotations

import typing as t

import jinja2
from docutils import nodes
from docutils.nodes import Element
from docutils.nodes import Node
from docutils.parsers.rst import Directive
from docutils.parsers.rst import roles
from sphinx.writers.html import HTMLTranslator

__all__ = [
    "References",
    "ReferencesNode",
    "depart_references_html",
    "visit_references_html",
]

REFERENCES_TEMPLATE: t.Final[jinja2.Template] = jinja2.Template(
    """\
    <h2>References</h2>
    <ol>
        {% for (title, link) in content %}
            <li>
                <p>{{ title }},&nbsp;<a href="{{ link }}" target="_blank"
                    class="references-border">{{ link }}</a></p>
            </li>
        {% endfor %}
    </ol>
    """
)


class ReferencesNode(Element):
    pass


class References(Directive):
    """A directive class for the ``references`` directive.

    This class allows using a custom ``references`` directive and maps
    the source reStructuredText to ``ReferencesNode`` element doctree
    node.

    By using the ``references`` directive, it allows contributors or
    authors to render a dedicated references section for the provided
    content. This class' rendering HTML behavior is further extended
    using another Python function, ``visit_references_div``.

    Example::

        .. references::

            arxiv >> Papers are published on arXiv every day.
            python >> We will be using Python all the time.

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

        :return: List of Docutils node for ``references`` directive.
        """
        self.options["class"] = ["learn-references"]
        roles.set_classes(self.options)
        node = ReferencesNode("\n".join(self.content), **self.options)
        self.add_name(node)
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]


def visit_references_html(self: HTMLTranslator, node: ReferencesNode) -> None:
    """Node visitor function which maps ``ReferencesNode`` element to the
    HTML output.

    This function allows the rendering of the references of a topic on the
    webpage. It relies on ``Jinja`` templating to perform the expansion
    and rendering of the HTML source code.
    """
    content: list[tuple[str, str]] = []
    pairs: dict[str, str] = {}
    corrections = node.children[0].astext().splitlines()
    node.remove(node.children[0])
    for correction in corrections:
        doc, new = correction.split(" >> ")
        pairs[doc] = new
    for target in node._document.findall(nodes.target):
        if target.hasattr("refuri") and target.indirect_reference_name:
            title = target["names"][0]
            content.append((pairs.get(title, title.title()), target["refuri"]))
    html_src = REFERENCES_TEMPLATE.render(content=content)
    self.body.append(f"{self.starttag(node, 'div')}{html_src}")


def depart_references_html(self: HTMLTranslator, node: ReferencesNode) -> None:
    self.body.append("</div>")
