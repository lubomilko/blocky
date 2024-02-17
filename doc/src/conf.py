# Configuration file for the Sphinx documentation builder.
# For more details, go to https://www.sphinx-doc.org/en/master/usage/configuration.html
import sys

# Append path to the blocky source files.
sys.path.append("../../src")


# -- Project information -----------------------------------------------------
project = 'Blocky template engine'
copyright = '2024 Lubomir Milko'
author = 'Lubomir Milko'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon'
]

autodoc_default_options = {
    'member-order': 'bysource',
    'special-members': '__init__'
}

html_theme = 'sphinx_rtd_theme'
