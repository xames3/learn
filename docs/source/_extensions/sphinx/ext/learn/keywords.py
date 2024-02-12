"""\
Keywords Directive for L.E.A.R.N
================================

Author: Akshay Mestry <xa@mes3.dev>
Created on: Wednesday, August 23 2023
Last updated on: Monday, February 12 2024

This module provides a custom directive for L.E.A.R.N's custom theme,
that allows authors and contributors to auto generate keywords for their
documentation.

L.E.A.R.N's keywords are created using the ``keywords`` directive, which
is included as part of this project. The directive is implemented below,
and is available to use by authors and contributors when building the
documentation.

.. note:: This directive is compatible with Sphinx 3.0 and higher.

.. note::

    This module is designed specifically for the Sphinx's L.E.A.R.N
    theme, hence the directive may not be available or may be
    implemented differently for different themes. Please consult the
    documentation for more information.

The keywords can be styled using CSS. The class encapsulating the
keywords is ``learn-keywords`` and the keywords itself is ``keywords``.

.. code-block:: css

    .learn-keywords {
      max-width: 80%;
      margin: 0 auto 2.5rem auto;
    }

    .keywords {
      margin: auto auto 2rem auto;
      font-weight: 400 !important;
    }

    .keywords::before{
      ...
      font-weight: bold;
      content: "Keywords: ";             # The "Keywords" prefix...
      ...
    }

This will style the keywords with required colors and format.

.. versionadded:: 1.0.5
    Added support for ``keywords`` directive to add auto generated
    keywords for the L.E.A.R.N document.
"""

from __future__ import annotations

import random
import re
import typing as t

import jinja2
import yake
from docutils.nodes import Element
from docutils.nodes import Node
from docutils.parsers.rst import Directive
from docutils.parsers.rst import roles
from sphinx.writers.html import HTMLTranslator

__all__ = [
    "Keywords",
    "KeywordsNode",
    "depart_keywords_html",
    "visit_keywords_html",
]

CONTENT_RE: re.Pattern = re.compile(r"<.*?>")
KEYWORDS_TEMPLATE: t.Final[jinja2.Template] = jinja2.Template(
    """<p class="keywords">{{ keywords|join(' · ') }}</p>"""
)


class KeywordsNode(Element):
    pass


class Keywords(Directive):
    """A directive class for the ``keywords`` directive.

    This class allows using a custom ``keywords`` directive and maps the
    source reStructuredText to ``KeywordsNode`` element doctree node.

    By using the ``keywords`` directive, it allows contributors or
    authors to render bunch of keywords for the provided content. This
    class' rendering HTML behavior is further extended using another
    Python function, ``visit_keywords_div``.

    Example::

        .. keywords:: machine learning, artificial intelligence

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

        :return: List of Docutils node for ``keywords`` directive.
        """
        self.options["class"] = ["learn-keywords"]
        roles.set_classes(self.options)
        node = KeywordsNode("\n".join(self.content), **self.options)
        self.add_name(node)
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]


def visit_keywords_html(self: HTMLTranslator, node: KeywordsNode) -> None:
    """Node visitor function which maps ``KeywordsNode`` element to the
    HTML output.

    This function allows the rendering of the keywords of a topic on the
    webpage. It relies on ``Jinja`` templating to perform the expansion
    and rendering of the HTML source code.
    """
    if node.children:
        keywords = node.children[0].astext().split(", ")
        node.remove(node.children[0])
    else:
        max_ngram_size = random.randint(1, 2)
        number_of_keywords = random.randint(4, 5)
        keyword_extractor = yake.KeywordExtractor(
            lan="en", n=max_ngram_size, dedupLim=0.9, top=number_of_keywords
        )
        keywords = map(
            lambda _: _[0],
            keyword_extractor.extract_keywords(
                CONTENT_RE.sub("", node.parent.astext())  # type: ignore
            ),
        )
    html_src = KEYWORDS_TEMPLATE.render(keywords=sorted(keywords))
    self.body.append(f"{self.starttag(node, 'div')}{html_src}")


def depart_keywords_html(self: HTMLTranslator, node: KeywordsNode) -> None:
    self.body.append("</div>")
