"""Checks that the package is installed and wired up correctly."""

import tomllib
from pathlib import Path

import agentforge

PYPROJECT = Path(__file__).parent.parent / "pyproject.toml"


# pytest finds files named test_*.py and runs the functions named test_*. A plain `assert`
# is enough: pytest rewrites it to show both values when it fails.
def test_version_matches_pyproject() -> None:
    project = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))["project"]

    assert agentforge.__version__ == project["version"]
