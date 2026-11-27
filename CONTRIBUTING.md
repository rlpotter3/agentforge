# Contributing to agentforge

Contributions are welcome. agentforge is in its early days, so please open an issue to discuss a
large change before you write it.

To report a security problem, follow the [security policy](SECURITY.md) instead of opening a public
issue.

## Set up

Follow [Getting started](README.md#getting-started) in the README to install uv and the
dependencies.

## Make a change

1. Create a branch from an up-to-date `main`. If you don't have write access, fork the repository
   first. Branch names such as `feat/...`, `fix/...` and `docs/...` say what a branch is for.
2. Make one focused change. Smaller pull requests are easier to review.
3. Run the checks:

   ```
   uv run ruff format --check
   uv run ruff check
   uv run pyright
   uv run pytest
   ```

   `uv run ruff format` fixes formatting, and `uv run ruff check --fix` fixes many lint findings.
4. Open a pull request against `main`. Describe what changes, why, and how you tested it.

Continuous integration runs the same checks on Python 3.12 and 3.13. Both must pass before a pull
request is merged.

## Expectations

### Tests

Every new feature or bug fix includes automated tests in the same pull request. Tests live in
`tests/`, mirroring the structure of `src/agentforge/`. They must not call external services or
need credentials.

### Code

- Add type hints to all function signatures. Pyright checks them in strict mode.
- If you suppress a lint or type finding, keep the suppression narrow and say why in a comment.
- Add dependencies with `uv add <name>`, or `uv add --dev <name>` for development tools, and commit
  the updated `uv.lock`.

### Secrets

Never commit API keys, tokens, passwords, private keys or `.env` files. Read configuration from
environment variables, and commit only placeholder examples such as `.env.example`.

If you commit a secret by mistake, revoke or rotate it straight away. Removing it in a later commit
isn't enough, because it stays in the Git history.

### Architecture decisions

Significant decisions are recorded as Architecture Decision Records (ADRs) in
[`docs/adr/`](docs/adr/): a technology choice, a structural pattern, a dependency, or a convention
that affects the whole project. Read the existing ones before proposing something new.

1. Copy [`docs/adr/0000-template.md`](docs/adr/0000-template.md).
2. Name it with the next number: `NNNN-short-kebab-title.md`.
3. Include it in your pull request.

Don't rewrite an accepted ADR. To change a decision, write a new ADR and mark the old one as
`Superseded by ADR-NNNN`.

## Licence of contributions

agentforge is licensed under the [Apache License 2.0](LICENSE). As section 5 of the licence
describes, contributions you submit for inclusion are under the same terms, unless you explicitly
state otherwise.
