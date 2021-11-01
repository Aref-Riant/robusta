#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Robusta documentation build configuration file, created by
# sphinx-quickstart on Wed Apr 28 13:48:20 2021.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
    "sphinx_design",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
source_suffix = [".rst", ".md"]

# The master toctree document.
master_doc = "index"

# General information about the project.
project = "Robusta"
copyright = "2021, Robusta"
author = "Natan Yellin"

# The short X.Y version.
version = "DOCS_VERSION_PLACEHOLDER"
# The full version, including alpha/beta/rc tags.
release = "DOCS_RELEASE_PLACEHOLDER"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "manni"
# pygments_dark_style = "monokai"

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False
html_theme = "furo"
# html_theme_path = [furo.get_pygments_stylesheet()]

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
html_theme_options = {
    # 'analytics_id': 'G-G03HKXT60G',
    "collapse_navigation": False,
    # "navigation_depth": 0,
    # "toc_title": "On this page",
    # "repository_url": "https://github.com/robusta-dev/robusta/",
    # "path_to_docs": "docs",
    # "home_page_in_toc": True,
    # "use_download_button": False,
    # "use_edit_page_button": True,
    # "use_repository_button": True,
    # 'titles_only': False
    "light_css_variables": {
        # "color-brand-primary": "#255a7e",
        # "color-brand-primary": "black",
        "color-brand-primary": "#e83e8c",
        "color-brand-content": "#e83e8c",
    },
    "dark_css_variables": {
        "color-brand-primary": "#7C4DFF",
        "color-brand-content": "#7C4DFF",
        "color-sidebar-link-text": "black",
    },
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

html_css_files = [
    "custom.css",
]

# html_logo = "images/small-robusta-logo.jpg"
# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = "Robustadoc"

# -- Options for LaTeX output ---------------------------------------------

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

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, "Robusta.tex", "Robusta Documentation", "Robusta", "manual"),
]

# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [(master_doc, "Robusta", "Robusta Documentation", [author], 1)]

# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        "Robusta",
        "Robusta Documentation",
        author,
        "Robusta",
        "One line description of project.",
        "Miscellaneous",
    ),
]


def setup(app):
    app.add_css_file("custom.css")
