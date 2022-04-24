# -*- coding: utf-8 -*-
#

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

sys.path.insert(0, os.path.abspath('../../py-package-template-master'))
from py_pkg.__version__ import __version__


# -- Project information -----------------------------------------------------

project = 'Python Cross Platform Toolkit for Windows and Linux variables, shortcuts and start menu shortcuts'
copyright = '2021, Jiri Otoupal'
author = 'Jiri Otoupal'

# The short X.Y version
version = __version__[:-2]
# The full version, including alpha/beta/rc tags
release = __version__


# -- Extension configuration -------------------------------------------------
