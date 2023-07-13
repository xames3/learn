.. _writing-essentials:

.. Author: Akshay "XA" Mestry <xa@mes3.dev>
.. Created on: Tuesday, June 27 2023
.. Last updated on: Wednesday, June 28 2023

##################
Writing Essentials
##################

As we embark on this journey of knowledge exploration and sharing, it is 
crucial to establish clear guidelines that ensure consistency, professionalism,
and readability across all the content on this platform. By following these 
principles, we can maintain a high standard of content, making 
:ref:`learn-index` a valuable resource for beginners entering the world of
AI and Math. Here, we have defined some essential guidelines that shape the 
design and writing practices of content presented on this platform. We will 
cover key elements that contribute to the professionalism and consistency of 
our material, such as using the right source code format, adhering to best 
coding practices, and giving credit to the historians who have helped and 
continue to support us in this process. By embracing and following these 
guidelines, you too can contribute to create high-quality, accessible content 
that empowers learners from all backgrounds to delve into the fascinating 
world of AI and the underlying math powering it.

So, let's dive in and discover how we can make every contribution to L.E.A.R.N 
even better!

************************
Embrace ReStructuredText
************************

To maintain uniformity, all pages on L.E.A.R.N must be written in
`ReStructuredText <https://shorturl.at/vzGUW>`_ (.rst) format. L.E.A.R.N
embraces the use of ReStructuredText as the preferred format for all page
content. ReStructuredText is a lightweight and versatile markup language
specifically designed for documentation and technical writing. You can read about ReStructuredText on `Wikipedia <https://shorturl.at/gktBU>`_.

Structure and Readability
#########################

ReStructuredText provides a simple yet powerful way to structure and organize
content. With its intuitive syntax, we can create clear headings, subheadings,
paragraphs, and lists. By using consistent and logical sectioning, readers can
easily navigate through the content and comprehend the hierarchy of
information.

Cross-Referencing and Navigation
################################

ReStructuredText allows for effortless cross-referencing between different
sections or topics across the whole platform. This feature of ReStructuredText
enables us to create hyperlinks that connect related concepts, allowing our
readers to explore the interconnectedness of various concepts and the
underlying math behind it. Furthermore, by utilizing the navigational and
inherently intuitive features of ReStructuredText, such as auto table of
contents generation, we enhance the content writer's experience, making it
easier for learners to find and access the desired information.

Formatting and Code Presentation
################################

In the context of technical writing, effective presentation of code and its
related elements is crucial. ReStructuredText provides specific
`directives <https://shorturl.at/qGUZ6>`_ and
`blocks <https://shorturl.at/jmzNO>`_ for displaying code snippets, syntax
highlighting, and inline code formatting. By leveraging these features, we can
clearly differentiate code from regular text, making it more visually distinct
and easily identifiable. This obvious color-formatting enhances readability and
ensures that learners can grasp the code-related concepts more efficiently.

.. tab-set::

    .. tab-item:: Built-in Directive

        .. code-block:: restructuredtext

            .. toctree:: 
              :caption: Guidelines
              :maxdepth: 3
              :numbered:
  
              _documentation/guidelines/writing-essentials
              _documentation/guidelines/why-not-markdown

    .. tab-item:: Custom Directive

        .. code-block:: restructuredtext

            .. authors::
              :affiliations: DePaul University, Chicago, IL
              :emails: xa@mes3.dev
              :names: Akshay "XA" Mestry

    .. tab-item:: Code Block

        .. code-block:: restructuredtext

            .. code-block:: python

                print("Hello hello!")

Portability and Compatibility
#############################

ReStructuredText is designed to be portable and platform independent. It is
easy to convert L.E.A.R.N into various output formats, including
`HTML <https://shorturl.at/bcnp5>`_, `PDF <https://shorturl.at/chov5>`_,
etc. This flexibility allows us to reach a broader audience and ensures that
our content can be accessed and consumed across different devices and
platforms. If you are thinking why we are not using Markdown, please see
:ref:`why-not-use-markdown`

.. tab-set::

    .. tab-item:: HTML

        .. code-block:: bash

            $ git clone git@github.com:xames3/learn.git 
            $ cd learn/docs/
            $ make clean && sphinx-build -W -E -a -b html source/ build/

    .. tab-item:: PDF

        .. code-block:: bash

            $ git clone git@github.com:xames3/learn.git
            $ cd learn/docs/
            $ pip install --user rst2pdf
            $ rst2pdf source/ output.pdf

************************
Limit Source Code Length
************************

In the pursuit of maintaining readability and preventing horizontal scrolling,
it is crucial to adhere to a specific source code length limitation within the
source files on L.E.A.R.N. Thus, the recommended guideline is to keep each
line of source code within **79** characters.

Readability and Comprehension
#############################

By restricting the source code length, we promote readability and enhance
comprehension for learners. Long lines of code can be overwhelming and
challenging to follow, especially for beginners. By adhering to the 79-
character limit, we encourage concise and focused snippets, ensuring that 
readers can easily grasp the concepts being presented. Breaking down complex 
code into shorter lines also eases mental parsing and reduces the chances
of errors.

Consistency and Aesthetic Appeal
################################

By imposing a consistent source code length limitation, we maintain a uniform
look across the platform. This consistency fosters a sense of professionalism 
and establishes L.E.A.R.N as a reliable resource. Uniformity in code formatting
not only enhances the overall aesthetics of the website but also signals to 
readers that attention to detail and quality are paramount.

Maintainability and Adaptability
################################

Keeping code within a reasonable length has long-term benefits for 
maintainability and adaptability. Shorter lines of code are easier to modify, 
refactor, or adjust when necessary. They promote the adoption of best 
practices such as proper indentation and consistent formatting, which in turn 
contribute to code cleanliness and understandability. By practicing 
disciplined code length control, we facilitate future updates, enhancements, 
and collaborations among folks contributing to L.E.A.R.N.

Compliance with Coding Standards
################################

Almost all the examples which will be provided on L.E.A.R.N will be based in 
Python. Therefore, the main coding standards and style guides, such as
`PEP 8 <https://shorturl.at/nqFL9>`_  for Python, recommends limiting the
length of source code lines. Adhering to these standards ensures that the code 
on L.E.A.R.N aligns with industry conventions and best practices. It also 
encourages contributors and readers to adopt coding practices that are widely 
accepted and recognized, promoting code consistency across the broader AI 
community.

*********************
Follow Best Practices
*********************

To maintain professionalism and ensure the clarity and effectiveness of our
content on L.E.A.R.N, it is crucial to adhere to best practices when writing
and formatting the source files. By following these guidelines, we can create
consistent and well-structured content that is easy to comprehend and 
navigate.

Meaningful Section and Subsection Headings
##########################################

Clear and descriptive headings are fundamental to organizing and structuring 
our content effectively. Utilize informative section and subsection headings 
that provide a logical flow and hierarchy to the material. Well-defined 
headings act as signposts, guiding readers through the content and helping 
them locate specific topics or concepts quickly.

.. code-block:: restructuredtext

    ##################
    Writing Essentials
    ##################

    ************************
    Embrace ReStructuredText
    ************************

    Structure and Readability
    #########################

    Code Block References
    *********************

    Specific Section
    ================

    Random Subsection
    -----------------

Organize Information with Bullet Points, Numbered Lists, and Tables
###################################################################

When presenting content in a structured manner, consider using bullet points, 
numbered lists, or tables. These formatting elements make complex concepts 
more digestible and improve readability. Bullet points and numbered lists help 
break down information into bite-sized chunks, while tables provide a visual 
representation of data or comparisons.

Code Blocks and Syntax Highlighting
###################################

Differentiating code from regular text is crucial for readability. Utilize 
code blocks to set code snippets apart from normal text. Code blocks visually 
highlight the code and preserve its formatting. Additionally, employ syntax 
highlighting to enhance the readability of the code snippets further. Syntax 
highlighting applies assorted colors and fonts or styles to different code 
elements, making it easier for readers to identify keywords, variables, and 
syntax patterns. See this code snippet for example...

.. code-block:: python

    def build_module() -> ModuleType:
        """Build the learn extension from ``_extensions`` directory."""
        spec = importlib.util.spec_from_file_location(MODULE, EXTENSION_PATH)
        module = importlib.util.module_from_spec(spec)  # type: ignore
        sys.modules[MODULE] = module
        spec.loader.exec_module(module)  # type: ignore
        return module

Inline Code Formatting
######################

Inline code formatting should be used to highlight specific code elements or 
variables within the body of the text. By wrapping code elements in backticks 
(``), we visually distinguish them from regular text and draw attention to 
their significance. Inline code formatting helps readers recognize code 
references or specific code terms, reinforcing their understanding of the 
subject matter. This is ``different`` from this.

Cross-Referencing
#################

To establish connections between related topics and enable seamless 
navigation, utilize cross-referencing. By referring readers to relevant 
sections, chapters, or definitions across the platform, cross-referencing aids 
in reinforcing concepts and encourages further exploration. Use hyperlinks to 
create these references thus, allowing readers to jump directly to the 
referenced information. This point is already highlighted earlier under 
`Cross-Referencing and Navigation`_ section.

Hyperlinks for External References and Citations
################################################

When referring to external sources, such as research papers, articles, 
definitions, webpages, or documentation, include hyperlinks to provide readers 
with additional resources for further exploration. Hyperlinks add credibility 
to the content and demonstrate thorough research. Do ensure that the 
hyperlinks are descriptive, directing readers to reliable and relevant sources 
that deepen their understanding of the topic. See how to add hyperlink in
ReStructuredText `here <https://shorturl.at/ryZ16>`_.

******************************
Consistent Filename Convention
******************************

To maintain proper organization and clarity in file management, it is 
important to adhere to a consistent filename convention for all files on
L.E.A.R.N.

Lowercase and Hyphen-Separated
##############################

Filenames should be in lowercase to ensure consistency and avoid confusion. 
Additionally, words within the filename should be separated by hyphens (-) 
rather than underscores or any spaces. This convention enhances readability 
and makes filenames more visually appealing.

Descriptive and Meaningful
##########################

Filenames should be descriptive and reflect the content or purpose of the 
file. This helps both contributors and maintainers quickly identify the file 
they are looking for. Choose concise and meaningful names that accurately 
represent the file's context and content. For example, if the file contains a 
tutorial on implementing a neural network, a decent and acceptable filename 
could be something like ``neural-network-implementation.rst``.

Use of Abbreviations and Acronyms
#################################

When appropriate, abbreviations or acronyms can be used in filenames to keep 
them concise. However, it is important to ensure that the abbreviations are 
widely understood and do not introduce confusion.

Avoid Special Characters and Spaces
###################################

To maintain compatibility across different operating systems and avoid 
potential technical issues, filenames should not include special characters or 
spaces. Stick to alphanumeric (a-z0-9) characters and hyphens for optimal 
compatibility.
