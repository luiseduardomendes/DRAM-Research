import os
import sys
sys.path.insert(0, os.path.abspath('.'))

project = 'DRAM Analysis'
copyright = '2024, Luis Eduardo Pereira Mendes'
author = 'Luis Eduardo Pereira Mendes'

release = '1.0.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

html_theme = 'alabaster'

