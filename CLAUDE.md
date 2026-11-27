# CLAUDE.md

Guidance for Claude Code when working in this repository.

## Project

**agentforge** is an open-source AI agent platform, licensed under Apache 2.0.
It is in its early days. Check `docs/adr/` for decisions already made before you propose new ones.

## Tech stack and commands

- **Language:** Python 3.12 or later, developed on 3.14, with type hints on all function signatures
  (ADR-0003).
- **Model access:** Claude through the Anthropic API, behind a provider interface that agent code
  depends on. Tests use a fake provider and make no network calls (ADR-0002).
- **Tooling:** uv, pytest, Ruff, Pyright in strict mode and GitHub Actions (ADR-0004).
- **Layout:** the package is in `src/agentforge/`, and `tests/` mirrors its structure.

Install dependencies with `uv sync`, and add them with `uv add` (`uv add --dev` for development
tools). All of these must pass before a change is merged:

```
uv run ruff format --check
uv run ruff check
uv run pyright
uv run pytest
```

## About the maintainer

The maintainer is a software architect coming back to hands-on coding after about 25 years away.
They know system design well, but modern languages, tools and idioms may be new to them.

- **Explain non-obvious code.** When you write or change code, briefly explain any modern idioms,
  language features, library conventions or tooling it relies on (for example async/await,
  decorators, generics, dependency injection, package managers or build configuration).
  Put lasting explanations in code comments, and one-off explanations in your reply.
- Skip explaining simple, self-evident code. Focus on the *why* and on anything surprising.
- Relate new ideas to architectural concepts where that helps.

## Rules

1. **Add tests with every feature.** Every new feature or bug fix comes with automated tests in
   the same change. Run the tests and report the results honestly before calling the work done.
2. **Never commit secrets.** That includes API keys, tokens, passwords, private keys and `.env` files.
   Read configuration from environment variables, and commit only placeholder examples
   (such as `.env.example`). Keep `.gitignore` up to date. If you find a secret in the working
   tree or in a diff, stop and warn the maintainer.
3. **Record decisions as ADRs in `docs/adr/`.** Write an Architecture Decision Record for each
   significant decision: a technology choice, a structural pattern, a dependency, or a
   cross-cutting convention.
   - Copy `docs/adr/0000-template.md`.
   - Number the files in order: `NNNN-short-kebab-title.md`.
   - Never rewrite an accepted ADR. To change a decision, write a new ADR and mark the old one
     as `Superseded by ADR-NNNN`.
