"""\
Authors Directive for L.E.A.R.N
===============================

Author: Akshay Mestry <xa@mes3.dev>
Created on: Wednesday, May 03 2023
Last updated on: Friday, August 11 2023

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

.. versionadded:: 1.0.1
    Added support for embedding links to author's profile. This allows
    us to link author's profile/url/resume to it's name in the author
    section itself.

.. versionchanged:: 1.0.2
    Directive extensions are now called with their names, no underscore
    prefixes are used.

.. versionchanged:: 1.0.3
    Author details are now formatted as table instead of list.
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
    <table id="authors">
        <tr>               
        {% for name in contents %}
            {% if name[3] != "#" %}
                <td class="name-link">
                    <a href="{{ name[3] }}" target="_blank">{{ name[0] }}</a>
                </td>
            {% else %}
                <td class="name-link">{{ name[0] }}</td>
            {% endif %}
        {% endfor %}
        </tr>
        <tr>               
        {% for affiliation in contents %}
            <td class="affiliation">
            {% for affiliation_break in affiliation[2] %}
                <p class="affiliation-link">{{ affiliation_break }}</p>
            {% endfor %}
            </td>
        {% endfor %}
        </tr>
        <tr>               
        {% for email in contents %}
            <td class="email-link">
                <a href="mailto:{{ email[1] }}">{{ email[1] }}</a>
            </td>
        {% endfor %}
        </tr>
    </table>
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
            :names: John Wick[%]Winston Scott
            :emails: babayaga@hightable.biz[%]themanager.ny@hightable.biz
            :affiliations: The Boogeyman[%]The Manager - NY Continental
            :links: https://linkedin.com/in/JW[%]https://ht.com/winston

    :var has_content: A boolean flag to allow content in the directive,
                      defaults to ``True``.
    :var final_argument_whitespace: A boolean flag, may the final
                                    argument contain whitespace, set to
                                    ``True``.
    :var option_spec: A mapping of option names to validator functions.

    .. versionadded:: 1.0.1
        Added support for links options to embed links in the name.
    """

    has_content: bool = True
    final_argument_whitespace: bool = True
    option_spec = {
        "names": directives.unchanged_required,
        "emails": directives.unchanged_required,
        "affiliations": directives.unchanged,
        "links": directives.unchanged,
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

    .. versionchanged:: 1.0.3
        The ``contents`` variable is type casted to list instead of
        being an iterator to loop over the Jinja template multiple
        times.
    """
    raw: dict[str, str | list[str]] = {}
    interested_attributes = ["names", "emails", "affiliations", "links"]
    for attribute in interested_attributes:
        raw[attribute] = node.attributes.pop(attribute).split("[%]")
    names, emails, affiliations, links = (
        raw["names"],
        raw["emails"],
        [affiliation.split("\\n") for affiliation in raw["affiliations"]],
        raw["links"],
    )
    contents = list(
        map(
            lambda n, e, a, l: (n, e, a, l), names, emails, affiliations, links
        )
    )  # type: ignore[call-overload]
    html_src = AUTHORS_TEMPLATE.render(contents=contents)
    self.body.append(f"{self.starttag(node, 'div')}{html_src}")


def depart_authors_html(self: HTMLTranslator, node: AuthorsNode) -> None:
    self.body.append("</div>")
