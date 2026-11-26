# ADR-0001: Record architecture decisions

- **Status:** Accepted
- **Date:** 2026-11-26

## Context

agentforge is a new open-source project. Contributors, including AI coding assistants,
need to understand why the project is built the way it is, not only how.

## Decision

We will record significant architectural decisions as Architecture Decision Records (ADRs),
using the lightweight format popularised by Michael Nygard. The ADRs live in `docs/adr/`, are
numbered in order, and follow `0000-template.md`.

## Alternatives considered

- **Wiki or external docs:** these drift away from the code and are not reviewed in pull requests.
- **No formal record:** the reasons behind decisions get lost, and settled questions get reopened.

## Consequences

- Each significant decision needs a short write-up, which adds a little overhead.
- Decisions are versioned with the code and reviewed in the same pull requests.
- To change a decision, we write a new ADR that supersedes the old one. Accepted ADRs are never edited.
