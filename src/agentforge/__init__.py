"""agentforge: an open-source platform for building, running and managing AI agents."""

# A folder with an __init__.py file is a Python "package". This file runs on first import.
from importlib.metadata import version

# Read the version from the installed package's metadata, so that pyproject.toml is the only
# place it is written down. Names wrapped in double underscores are Python conventions.
__version__ = version("agentforge")
