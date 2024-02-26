# Configuration file for the Sphinx documentation builder.

# -- Path setup --------------------------------------------------------------

import os
import sys
sys.path.insert(0, os.path.abspath('../src'))  # Adjust this path to your source code

# -- Project information -----------------------------------------------------

project = 'CS 472 Project'
copyright = '2024, Kamil'
author = 'Kamil'

# The full version, including alpha/beta/rc tags
release = '0.1.0'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',  # Include documentation from docstrings
    'sphinx.ext.doctest',  # Test snippets in the documentation
    'sphinx.ext.intersphinx',  # Link to other project's documentation
    'sphinx.ext.todo',  # Support for todo items
    'sphinx.ext.viewcode',  # Add links to source code
    # Add any other Sphinx extensions here.
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------

html_theme = 'alabaster'  # There are many other themes available
html_static_path = ['_static']

# -- Extension configuration -------------------------------------------------

# If you have any Sphinx extension configurations, they can be added here.
