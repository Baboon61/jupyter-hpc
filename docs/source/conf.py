# Configuration file for the Sphinx documentation builder.

# -- Project information

project = 'ai-bunker'
copyright = '2026, Bastien Hervé'
author = 'Bastien Hervé'

release = '0.1'
version = '0.1.0'

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx_design',
    'sphinx_tabs.tabs',
]

templates_path = ['_templates']

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'

# -- Options for EPUB output
epub_show_urls = 'footnote'
