"""\
Authors Directive for L.E.A.R.N
===============================

Author: Akshay Mestry (XAMES3) <xa@mes3.dev>
Created on: Wednesday, May 03 2023
Last updated on: Wednesday, May 03 2023

This module provides a custom directive for L.E.A.R.N's custom theme,
that allows authors and contributors to add list of authors or
contributors to their documentation in a specific format.

L.E.A.R.N's author/contributor layout is created using the ``authors``
directive, which is included as part of this project. The directive is
implemented below, and is available to use by co-authors/contributors
when building or submitting a patch for the documentation.

.. note:: This directive is compatible with Sphinx 3.0 and higher.

.. note::

    This module is designed specifically for the Sphinx's L.E.A.R.N
    theme, hence the directive may not be available or may be
    implemented differently for different themes. Please consult the
    documentation for more information.

The authors list can be styled using CSS. The class encapsulating the
authors is ``learn-authors``, the author's name and affiliation is
``author``, whereas the email class is ``email-link``.

.. code-block:: css

    .learn-authors {
      ...
      display: flex;
      flex-direction: row;
      justify-content: center;
      ...
    }

    .author {
      ...
      align-items: center;
      display: flex;
      flex-direction: column;
      ...
    }

    .author a.email-link {
      ...
      color: #000;
      margin-bottom: 50px;
      ...
    }

This will style the authors list with required fonts and alignments.
"""

from __future__ import annotations

import typing as t

import jinja2
from docutils.nodes import Element
from docutils.nodes import Node
from docutils.parsers.rst import Directive
from docutils.parsers.rst import directives
from docutils.parsers.rst import roles
from sphinx.writers.html import HTMLTranslator

__all__ = [
    "Authors",
    "AuthorsNode",
    "depart_authors_html",
    "visit_authors_html",
]

AUTHORS_TEMPLATE: t.Final[jinja2.Template] = jinja2.Template(
    """\
    {% for name, email, affiliation in content %}
        <div class="author">
            <p><b>{{ name }}</b></p>
            <p>{{ affiliation }}</p>
            <a href="mailto:{{ email }}" class="email-link">{{ email }}</a>
        </div>
    {% endfor %}
    """
)


class AuthorsNode(Element):
    pass


class Authors(Directive):
    """A directive class for the ``authors`` directive.

    This class allows using a custom ``authors`` directive and maps the
    source reStructuredText to ``AuthorsNode`` element doctree node.

    By using the ``authors`` directive, it allows contributors or
    authors to mention author(s)' name, affiliations and email for the
    written content. This class' rendering HTML behavior is further
    extended using another Python function, ``visit_authors_div``.

    Example::

        .. authors::
            :names: John Wick%Winston Scott
            :emails: babayaga@hightable.biz%themanager.ny@hightable.biz
            :affiliations: The Boogeyman%The Manager - NY Continental

    :var has_content: A boolean flag to allow content in the directive,
                      defaults to ``True``.
    :var final_argument_whitespace: A boolean flag, may the final
                                    argument contain whitespace, set to
                                    ``True``.
    :var option_spec: A mapping of option names to validator functions.
    """

    has_content: bool = True
    final_argument_whitespace: bool = True
    option_spec = {
        "names": directives.unchanged_required,
        "emails": directives.unchanged_required,
        "affiliations": directives.unchanged,
    }

    def run(self) -> list[Node]:
        """Create node from the reStructuredText source.

        This method processes the directive's arguments, options and
        content, and return a list of Docutils/Sphinx nodes that will be
        inserted into the document tree at the point where the directive
        was encountered.

        :return: List of Docutils node for ``authors`` directive.
        """
        self.options["class"] = ["learn-authors"]
        roles.set_classes(self.options)
        node = AuthorsNode("\n".join(self.content), **self.options)
        self.add_name(node)
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]


def visit_authors_html(self: HTMLTranslator, node: AuthorsNode) -> None:
    """Node visitor function which maps ``AuthorsNode`` element to the
    HTML output.

    This function allows the rendering of the abstract of a topid on the
    webpage. It relies on ``Jinja`` templating to perform the expansion
    and rendering of the HTML source code.
    """
    raw = {"names": None, "emails": None, "affiliations": None}
    interested_attributes = ["names", "emails", "affiliations"]
    for attribute in interested_attributes:
        raw[attribute] = node.attributes.pop(attribute).split("%")
    names, emails, affiliations = (
        raw["names"],
        raw["emails"],
        raw["affiliations"],
    )
    content = map(lambda n, e, a: (n, e, a), names, emails, affiliations)  # type: ignore[call-overload]
    html_src = AUTHORS_TEMPLATE.render(content=content)
    self.body.append(f"{self.starttag(node, 'div')}{html_src}")


def depart_authors_html(self: HTMLTranslator, node: AuthorsNode) -> None:
    self.body.append("</div>")
