# Dj_Fitness_Asmt/__init__.py

# ==============================
# Import all functions from logics.py
# ==============================
from . import logics
from . import constants

# Dynamically add all functions from logics to this namespace
for attr_name in dir(logics):
    if not attr_name.startswith("_"):
        attr = getattr(logics, attr_name)
        if callable(attr):
            globals()[attr_name] = attr

# Dynamically add all constants from constants.py to this namespace
for attr_name in dir(constants):
    if not attr_name.startswith("_"):
        globals()[attr_name] = getattr(constants, attr_name)

# Optional: define __all__ for safe wildcard imports
__all__ = [name for name in globals() if not name.startswith("_")]
