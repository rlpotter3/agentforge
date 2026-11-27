# agentforge

**Status: Day 1 of 30**

agentforge is an open-source platform for building, running and managing AI agents.
It aims to provide the foundations that agent-based applications need,
including orchestration, tool integration and observability, as clean, well-tested,
well-documented building blocks.

## Project principles

- **Tested:** every feature ships with automated tests.
- **Secure by default:** no secrets in the repository. Configuration comes from the environment.
- **Decisions are documented:** architectural decisions are recorded as ADRs in [`docs/adr/`](docs/adr/).

## Roadmap

The project is being built in public over 30 days. The first milestones will
set the tech stack, project structure and core agent abstractions. Each decision
will be captured as an ADR.

## Getting started

1. [Install uv](https://docs.astral.sh/uv/getting-started/installation/). On Windows:
   `winget install --id=astral-sh.uv -e`, then open a new terminal.
2. Install Python and the dependencies into a local virtual environment (`.venv/`):

   ```
   uv sync
   ```

3. Run the checks. All four must pass before a change is merged:

   ```
   uv run ruff format --check
   uv run ruff check
   uv run pyright
   uv run pytest
   ```

`uv run ruff format` (without `--check`) fixes formatting.

## Contributing

Contributions are welcome. Before you open a pull request:

1. Include tests for any new behaviour.
2. Make sure you have committed no credentials or `.env` files.
3. Add an ADR for any significant architectural change.

## License

[Apache License 2.0](LICENSE)
