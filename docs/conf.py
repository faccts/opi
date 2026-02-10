#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
from subprocess import check_output, CalledProcessError, TimeoutExpired
from pathlib import Path
import traceback

from docutils import nodes
from sphinx.transforms import SphinxTransform
from semantic_version import Version

# needs_sphinx = '1.0'

def git_branch(cwd) -> str:
    """Returns the git branch name."""
    try:
        b = check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=cwd, text=True, timeout=5,
        ).strip()
    except CalledProcessError:
        return "unknown"

    return b

def git_exact_tag(cwd) -> str | None:
    """Returns the git exact tag name."""
    try:
        return check_output(
            ["git", "describe", "--tags", "--exact-match"],
            cwd=cwd, text=True, timeout=5,
        ).strip()
    except CalledProcessError:
        return None

extensions = [
    "sphinx-prompt",
    "sphinx.ext.autosectionlabel",
    "notfound.extension",
    "sphinx_copybutton",
    "sphinx.ext.mathjax",
    "sphinx.ext.napoleon",
    "sphinx_design",
    "myst_nb",
    "autoapi.extension",
]

# >myst_nb settings
nb_execution_mode = "off"

source_suffix = {
    ".ipynb": "myst-nb",
}

autosectionlabel_prefix_document = True

# >Automatic API generation
autoapi_type = "python"
autoapi_dirs = [os.path.abspath("../src/opi")]
autoapi_root = "contents/api"
autoapi_template_dir = os.path.abspath("_templates/autoapi")
autoapi_keep_files = True
autoapi_add_toctree_entry = True
autoapi_options = [
    "members",
    "undoc-members",
    "private-members",
    "special-members",
    "show-inheritance",
    "show-module-summary",
    "imported-members",
]
autoapi_ignore = []
# // Autodoc config
autodoc_typehints = "description"

# > Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# > The suffix(es) of source filenames.
# > You can specify multiple suffix as a list of string:
source_suffix = [".md", ".rst"]

# > The master toctree document.
master_doc = "index"

# > General information about the project.
project = "ORCA Python Interface Documentation"
copyright = "2025, FACCTs"
author = "FACCTs"


origin = Path(__file__).resolve().parent
full_version = ""
# > The short X.Y version.
version_short = ""
# > Using "main" as fallback
release_branch = "main"
# > Disabling git advices
os.environ["GIT_ADVICE"] = "0"
try:
    branch = git_branch(origin)
    tag = git_exact_tag(origin)
except (CalledProcessError, TimeoutExpired, OSError):
    traceback.print_exc()
    sys.exit(1)
else:
    try:
        release_branch = branch if branch != "HEAD" else "main"

        if tag and tag.startswith("v"):
            version_string = tag.removeprefix("v")
            full_version = Version(version_string=version_string)
            version_short = f"{full_version.major}.{full_version.minor}"
        else:
            # Not on a release tag
            if branch == "main":
                version_short = "nightly"
            # on a release branch
            elif branch.startswith("release/"):
                # e.g. "release/1.0" -> "1.0-dev"
                version_short = f"{branch.removeprefix('release/')}-dev"
            # on a feature branch
            else:
                version_short = "dev"
    except:
        traceback.print_exc()
        sys.exit(1)


# > Language
language = "English"

# > Exclude patterns
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    ".venv",
    "_tools",
    "README.md"
]

# > If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False

myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "dollarmath",
    "attrs_inline",
    "attrs_block",
]

# > Warnings
suppress_warnings = [
    "mystnb.unknown_mime_type"
]

# > -- Options for HTML output ----------------------------------------------
# > The theme to use for HTML and HTML Help pages.  See the documentation for
# > a list of builtin themes.
html_theme = "furo"

# > Theme options are theme-specific and customize the look and feel of a theme
# > further.  For a list of options available for each theme, see the
# > documentation.
html_title = f"OPI {version_short} Docs"
html_logo = "img/assets/opi_logo_thumbnail.svg"

html_show_sphinx = False
html_show_copyright = False

html_additional_pages = {
    "search": "search.html",
}

html_theme_options = {
    "light_css_variables": {
        "color-sidebar-background": "transparent",
        "color-sidebar-item-background--hover": "transparent",
        "color-sidebar-link-text--top-level": "#64757d",
        "color-sidebar-link-text": "#64757d",
        "color-brand-primary": "#579aca",
        "color-brand-content": "#579aca",
        "color-code-background": "#f8f8f8",
    },
}

pygments_style = "friendly"

# > Add any paths that contain custom static files (such as style sheets) here,
# > relative to this directory. They are copied after the builtin static files,
# > so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

html_css_files = [
    "css/custom.css",
]

# > -- Options for HTMLHelp output ------------------------------------------

# > Output file base name for HTML help builder.
htmlhelp_basename = "ORCA Python Interface Docs"

# > -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',
    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',
    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',
    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# > Grouping the document tree into LaTeX files. List of tuples
# > (source start file, target name, title,
# >  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, "DOCS.tex", "DOCS Documentation", "FACCTS", "manual"),
]

# > -- Options for manual page output ---------------------------------------

# > One entry per manual page. List of tuples
# > (source start file, name, description, authors, manual section).
man_pages = [(master_doc, "OPI Docs", "OPI Documentation", [author], 1)]

# > -- Options for Texinfo output -------------------------------------------

# > Grouping the document tree into Texinfo files. List of tuples
# > (source start file, target name, title, author,
# >  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        "DOCS",
        "DOCS Documentation",
        author,
        "DOCS",
        "One line description of project.",
        "Miscellaneous",
    ),
]

# > -- Options for notfound ------------------------------------------------
notfound_urls_prefix = None


# > Inject Download Buttons
class InjectNotebookButtons(SphinxTransform):
    default_priority = 5

    def apply(self):
        docname = self.env.docname

        html = ""
        if docname.startswith("contents/notebooks/"):
            ipynb_file = f"_static/{docname}.ipynb"
            github_url = f"https://github.com/faccts/opi/blob/{release_branch}/docs/{docname}.ipynb"
            html = f"""
            <div class="button-row">
                <a href="{github_url}" class="orca-btn">View on GitHub <i class="fab fa-github"></i></a>
            </div>
            """

        if html:
            self.document.insert(0, nodes.raw('', html, format='html'))


def setup(app):
    app.add_transform(InjectNotebookButtons)
    app.add_css_file("fontawesome/css/all.min.css")
