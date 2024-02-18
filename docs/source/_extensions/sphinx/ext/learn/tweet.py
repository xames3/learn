"""\
Tweets Directive for L.E.A.R.N
================================

Author: Akshay Mestry <xa@mes3.dev>
Created on: Sunday, August 20 2023
Last updated on: Sunday, February 18 2024

This module provides a custom directive for L.E.A.R.N's custom theme,
that allows authors and contributors to add a link to Twitter or X's
tweet as an embed to the documentation. A ``tweet`` is any message
posted to Twitter or X which may contain photos, videos, links, and
text.

L.E.A.R.N's tweet embeds are created using the ``tweet`` directive,
which is included as part of this project. The directive is implemented
below, and is available to use by authors and contributors when building
the documentation.

.. note:: This directive is compatible with Sphinx 3.0 and higher.

.. note::

    This module is designed specifically for the Sphinx's L.E.A.R.N
    theme, hence the directive may not be available or may be
    implemented differently for different themes. Please consult the
    documentation for more information.

.. note::

    The tweet structure can't be completely styled using CSS as the
    tweet is generated through an ``iframe`` which is embedded using X's
    or Twitter's JavaScript file. The class encapsulating the tweet is
    ``learn-tweet``.

.. code-block:: css

    .learn-tweet {
        max-width: 550px;
        margin: 2rem auto;
    }

.. seealso::
    Based on tutorial by Chris Holdgraf at
    https://chrisholdgraf.com/blog/2023/social-directive/

.. versionadded:: 1.0.4
    Added support for embedding tweets to the document. This allows
    us to link references to tweets related to a particular topic which
    is relevant to the context.
"""

from __future__ import annotations

import typing as t

import jinja2
from docutils import nodes
from docutils.parsers.rst import Directive

if t.TYPE_CHECKING:
    from sphinx.addnodes import document
    from sphinx.application import Sphinx

__all__ = ["Tweet", "embed_twitter_js"]

TWITTER_JS_WIDGET_FILE_URL = "https://platform.twitter.com/widgets.js"
TWEET_TEMPLATE: t.Final[jinja2.Template] = jinja2.Template(
    """\
    <div class="learn-tweet">
        <blockquote class="tweet twitter-tweet"><p lang="en" dir="ltr">
            <a href="{{ tweet }}">Tweet from @{{ author }}</a>
        </blockquote>
    </div>
    """
)


class Tweet(Directive):
    """A directive class for the ``tweet`` directive.

    This class allows using a custom ``tweet`` directive and maps the
    source reStructuredText to ``Tweet`` element doctree node.

    By using the ``tweet`` directive, it allows contributors or
    authors to embed a tweet for the provided content. This class'
    rendering JavaScript behavior is further extended using another
    Python function, ``embed_twitter_js``.

    Example::

        .. tweet:: https://twitter.com/xa_mes3/status/some-tweet-id

    :var has_content: A boolean flag to allow content in the directive,
                      defaults to ``True``.
    :var final_argument_whitespace: A boolean flag, may the final
                                    argument contain whitespace, set to
                                    ``False``.
    """

    has_content: bool = True
    final_argument_whitespace: bool = False

    def run(self) -> list[nodes.raw]:
        """Create node from the reStructuredText source.

        This method processes the directive's arguments, options and
        content, and return a list of Docutils/Sphinx nodes that will be
        inserted into the document tree at the point where the directive
        was encountered.

        :return: List of Docutils node for ``tweet`` directive.
        """
        content = self.content[0]
        author = content.split("twitter.com/")[1].split("/")[0]
        html_src = TWEET_TEMPLATE.render(tweet=content, author=author)
        node = nodes.raw("", html_src, format="html", **{"class": "tweet"})
        return [node]


def embed_twitter_js(
    app: Sphinx,
    pagename: str,
    templatename: str,
    context: dict[str, t.Any],
    doctree: document,
) -> None:
    """Register the necessary JavaScript to embed tweets on L.E.A.R.N.

    :param app: Sphinx application class.
    :param pagename: The sphinx docname related to the page.
    :param templatename: The name of the template as string.
    :param context: A dictionary of values that are given to the
                    template engine, to render the page and can be
                    modified to include custom values.
    :param doctree: A doctree when the page is created from a reST
                    documents; it will be None when the page is created
                    from an HTML template alone.
    """
    kwargs = {"charset": "utf-8"}
    if not doctree:
        return
    for raw_node in doctree.traverse(nodes.raw):
        if "tweet" in raw_node.attributes.get("class", []):
            app.add_js_file(TWITTER_JS_WIDGET_FILE_URL, 500, "async", **kwargs)
            break
