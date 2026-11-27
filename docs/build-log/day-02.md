# Build log: Day 2 of 30

**Date:** 2026-11-27

## Summary

I unblocked access to Claude, recorded the main technical decisions, set up the Python project with
continuous integration, and protected the repository. There is no application code yet beyond the
package skeleton and one test. I did the work with Claude Code.

## What I did

### Model access

- Retested Claude on Vertex AI. It failed again with HTTP 429, because the quota is still zero.
- Switched to the Anthropic API. A test request to Claude Haiku 5.5 succeeded.

### Decisions

| ADR | Decision |
|---|---|
| [0002](../adr/0002-access-claude-through-anthropic-api.md) | Access Claude through the Anthropic API, behind a provider interface |
| [0003](../adr/0003-use-python-for-the-platform.md) | Use Python |
| [0004](../adr/0004-python-tooling-and-project-layout.md) | Use uv, pytest, Ruff, Pyright and GitHub Actions, with a "src" layout |
| [0005](../adr/0005-route-model-calls-through-litellm-proxy.md) | Route model calls through an optional LiteLLM proxy, from December 8 at the earliest |
| [0006](../adr/0006-model-provider-interface.md) | Define an asynchronous streaming provider interface |
| [0007](../adr/0007-support-python-3-12-and-3-13.md) | Support Python 3.12 and 3.13 |

### Project setup

- Installed uv and built the project skeleton: the `agentforge` package, a first test and the lint,
  format and type checks.
- Added a CI workflow that runs the checks on every pull request.
- Moved development to Python 3.13.

### Repository

- Added `CONTRIBUTING.md` and `SECURITY.md`.
- Turned on private vulnerability reporting.
- Protected `main`: changes need a pull request and a passing `ci-ok` check, and force pushes and
  deletion are blocked.
- Confirmed that secret scanning and push protection are on.
- Merged pull requests #1 to #5.

### Planning

- Reviewed my 30-day plan against the repository and found changes to make.

## Challenges

- **Vertex AI is still unavailable.** The plan's Vertex AI steps need to use the Anthropic API
  instead.
- **Python 3.14 was too new for one planned tool.** The latest NeMo Guardrails release requires an
  older version, so I limited the project to 3.12 and 3.13.
- **Required checks are tied to their names.** Changing Python versions meant updating the branch
  rules. They now require a single summary check, so the next version change won't.
- **LiteLLM needs care.** It had compromised releases in March and October 2026, so I plan to pin a
  checked version and wait before upgrading.

## Open items

- Decide whether to use Google's Agent Development Kit (ADK) before building the provider interface.
  It may replace much of ADR-0006.
- Check whether I meet the requirements for the Google Business Profile, LinkedIn and Meta APIs.
- Write the product brief.
- Add issue templates and a pre-commit configuration.
- Test secret push protection safely.
- Add Terraform and keystore ignore rules, and turn on Dependabot security updates.

## Next

Issue templates and the pre-commit configuration, then the product brief and the ADK decision.
