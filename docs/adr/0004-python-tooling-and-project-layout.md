# ADR-0004: Python tooling and project layout

- **Status:** Accepted
- **Date:** 2026-11-27

## Context

[ADR-0003](0003-use-python-for-the-platform.md) chose Python 3.12 or later, with type hints that
are checked in the same run as the tests. Before writing code we need to agree how the project is
laid out, how dependencies are installed, and how code is checked.

The forces are:

- A new contributor should be able to set up and check the project with a few commands.
- Everyone, including automation, should get the same dependency versions.
- Contributors work on different operating systems. The maintainer uses Windows and VS Code.
- With few contributors, we want few tools and little configuration.

## Decision

### Tools

| Job | Tool |
|---|---|
| Python versions, virtual environments, dependencies, running commands | uv |
| Build backend | `uv_build` |
| Tests | pytest |
| Linting and formatting | Ruff |
| Static type checking | Pyright, in strict mode |
| Continuous integration | GitHub Actions |

### Conventions

- `pyproject.toml` holds the project metadata and all tool configuration. Development tools are
  declared in its `[dependency-groups]` table.
- `uv.lock` is committed, so every install uses the same versions.
- `requires-python` is `>=3.12`. `.python-version` selects 3.14 for development.
- Pyright is installed from PyPI as `pyright[nodejs]`, so uv also provides the Node.js runtime it
  needs.
- These commands must all pass before a change is merged:

  ```
  uv run ruff format --check
  uv run ruff check
  uv run pyright
  uv run pytest
  ```

- GitHub Actions runs them on every pull request and every push to `main`, on Python 3.12 and 3.14.

### Layout

One installable package, using the "src layout":

```
pyproject.toml
uv.lock
.python-version
src/agentforge/     # the platform package
tests/              # mirrors the structure of src/agentforge/
docs/
```

## Alternatives considered

- **`venv` and `pip`:** come with Python, but locking versions and managing Python installations
  need extra tools.
- **Poetry:** mature and does locking well, but doesn't cover as much of the job as uv does.
- **mypy:** the long-established type checker, written in Python and needing no Node.js. We prefer
  Pyright because VS Code's Pylance extension is built on it, so the editor and the checks should
  largely agree.
- **ty:** Astral's newer type checker. It still uses 0.0.x versions without a stable API.
- **Flake8, isort and Black:** well proven, but three tools to configure where Ruff is one.
- **unittest:** comes with Python, but needs more boilerplate than pytest.
- **Flat layout** (package folder at the repository root): slightly simpler, but tests can then
  import the source folder by accident and hide packaging mistakes. The src layout avoids this.
- **Several packages in one workspace:** nothing needs to be released separately yet.

## Consequences

- Setup is: install uv, then run `uv sync`.
- uv and Ruff come from one vendor, Astral, which OpenAI announced in March 2026 that it would
  acquire. Both are MIT-licensed. Our metadata uses standard `pyproject.toml` tables, which limits
  the cost of changing tools, though `uv.lock` and the build backend setting would need replacing.
- Strict type checking catches mistakes early, but takes more effort where third-party libraries
  have incomplete types. Any suppression should be narrow and carry a comment explaining it.
- Locked versions don't update themselves. We need a routine for dependency and security updates.
- Tests don't run on Windows or macOS in continuous integration, so differences there could be
  missed. We can add them if that happens.
- Follow-up work: add the project skeleton with a first test, add Python entries to `.gitignore`,
  add the workflow file, and document the setup commands in the README.
- Asynchronous testing support depends on whether the core interfaces are asynchronous, which a
  later decision will settle.
