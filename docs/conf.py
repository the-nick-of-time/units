# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
from decimal import Decimal
from pathlib import Path

from pypandoc import convert_file
from pypandoc.pandoc_download import download_pandoc

# Allow imports from main package by autodoc
sys.path.insert(0, os.path.abspath(".."))

# -- Convert readme to RST ---------------------------------------------------
if not (Path.home() / "bin" / "pandoc").exists():
    download_pandoc()

rst_text = convert_file("../README.md", format="gfm", to="rst")
without_title = rst_text.split('\n')[3:]
rst_readme = Path("README.rst")
rst_readme.write_text('\n'.join(without_title))

# -- Table of SI prefixes ----------------------------------------------------
from pyunitx._api import _SI_PREFIXES

headers = ','.join(["SI Prefix", "Short Prefix", "Order of Magnitude"])
body = [f"{p},{s},10\\ :sup:`{Decimal(m).adjusted()}`" for p, s, m in _SI_PREFIXES]
# lines = [','.join(line) for line in [headers] + body]
csv_si = Path("prefixes.csv")
csv_si.write_text('\n'.join([headers] + body))

# -- Table of resistor color codes -------------------------------------------
from pyunitx.resistance import Color

headers = ','.join(["Letter", "Color"])
body = [f"{c.value},{c.name}" for c in Color if c is not Color.BLANK]
csv_color = Path("colors.csv")
csv_color.write_text('\n'.join([headers] + body))

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
    'sphinx.ext.intersphinx',
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

# -- Intersphinx configuration -----------------------------------------------
# Allow links to python standard library documentation
intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}
