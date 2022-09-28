# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
from pathlib import Path

from pypandoc import convert_file
from pypandoc.pandoc_download import download_pandoc

sys.path.insert(0, os.path.abspath(".."))
download_pandoc()

rst_text = convert_file("../README.md", format="gfm", to="rst")
without_title = rst_text.split('\n')[3:]
rst_readme = Path("README.rst")
rst_readme.write_text('\n'.join(without_title))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'pyunitx'
copyright = '2022, Nick Thurmes'
author = 'Nick Thurmes'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.imgmath',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'nature'

# -- Autodoc configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html

# Group module members by type: class, then function, then constant
# Also gets it to respect the order of __all__
autodoc_member_order = 'groupwise'
# Don't automatically include class members
autoclass_content = 'class'
