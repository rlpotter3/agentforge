# ADR-0003: Use Python for the platform

- **Status:** Accepted. Version requirement superseded by [ADR-0007](0007-support-python-3-12-and-3-13.md)
- **Date:** 2026-11-27

## Context

agentforge needs a programming language before we can write the model provider interface from
[ADR-0002](0002-access-claude-through-anthropic-api.md) or any agent abstractions.

The forces are:

- We call Claude through the official Anthropic SDK, so the language should have one.
- ADR-0002 keeps Vertex AI as a later option, so the SDK should support it too.
- Much of the platform's work is waiting on the network: model calls and tool calls.
- The project is open source, so the language should be familiar to likely contributors.
- The maintainer is returning to hands-on coding, so readability and quick feedback matter.
- The mobile app is a separate repository built with Flutter, which uses Dart.

## Decision

1. **Write the agentforge platform in Python.**
2. **Require Python 3.12 or later.**
3. **Add type hints to all function signatures**, and check them automatically with a static type
   checker in the same run as the tests.

This covers the platform repository only. It doesn't change the app's language.

## Alternatives considered

- **TypeScript:** has an official Anthropic SDK, a strong type system and good support for
  network-bound work, and it would share a language with a web front end. We have no web front end
  planned in this repository, and the app uses Dart, so that advantage doesn't apply today.
- **Go:** has an official Anthropic SDK, strong concurrency and simple single-file deployment.
  It has a smaller ecosystem of AI libraries than Python.
- **Java or C#:** both have official Anthropic SDKs and mature tooling for large systems. They
  need more ceremony for a small, fast-moving project.
- **Dart:** would share a language with the app, but Anthropic has no official Dart SDK.

## Consequences

- We can use the official `anthropic` package, including its Vertex AI client, and Python's large
  ecosystem of AI libraries.
- Python checks types only if we run a checker. Type hints are not enforced while the program
  runs, so data from outside the program (requests, model output, tool input) needs explicit
  validation.
- Handling many model and tool calls at once will need asynchronous code (`asyncio`). Whether the
  core interfaces are asynchronous must be decided before we write them, because changing it later
  affects every caller.
- Python is slower than the alternatives for CPU-heavy work. We expect network waits to dominate,
  and have not measured it.
- The app and the platform can't share code. They need a documented API contract between them.
- Python 3.12 now receives only security fixes, and python.org no longer publishes Windows
  installers for its new releases. Development and deployment should use a newer version, with
  tests also run on 3.12 for as long as we support it.
- Follow-up decisions: dependency and environment management, test framework, linter, formatter,
  type checker and repository layout. Python build and cache files also need `.gitignore` entries.
