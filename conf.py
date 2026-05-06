# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Interaktívna učebnica Fyziky'
copyright = '2026, Matej Krempaský'
author = 'Matej Krempaský'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'nbsphinx',
]

language = 'sk'

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
exclude_patterns = ['_build', '**/_build/**']