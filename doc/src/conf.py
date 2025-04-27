# pylint: disable = missing-module-docstring, invalid-name, redefined-builtin

# Configuration file for the Sphinx documentation builder.
# For more details, go to https://www.sphinx-doc.org/en/master/usage/configuration.html
import os
import sys

# Append path to the blocky source files.
sys.path.append(os.path.abspath('../../src'))


# -- Project information -----------------------------------------------------
project = 'Blocky'
copyright = '2025 Lubomir Milko'
author = 'Lubomir Milko'
release = '2.0.0'

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

add_module_names = False

html_theme = 'sphinx_rtd_theme'
