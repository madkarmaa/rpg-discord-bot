"""
Custom package
--------------

Custom package for this Discord bot, containing all its dependencies.
"""

import os

__all__ = []

for filename in os.listdir(os.path.dirname(__file__)):
    if filename.endswith(".py") and not filename.startswith("__"):
        __all__.append(filename[:-3])
