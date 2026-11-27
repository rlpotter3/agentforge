# ADR-0007: Support Python 3.12 and 3.13

- **Status:** Accepted
- **Date:** 2026-11-27

## Context

[ADR-0003](0003-use-python-for-the-platform.md) requires Python 3.12 or later, and
[ADR-0004](0004-python-tooling-and-project-layout.md) develops on 3.14 and tests on 3.12 and 3.14.

We plan to evaluate NeMo Guardrails. Its latest release at the time of writing (0.25.0) requires a
Python version below 3.14. Changing versions is cheapest now, while there is little code.

## Decision

1. **Support Python 3.12 and 3.13:** `requires-python` is `>=3.12,<3.14`.
2. **Develop on 3.13:** `.python-version` selects it.
3. **Test on 3.12 and 3.13** in continuous integration. Type checks still target 3.12 locally, and
   each CI job checks against its own version.
4. **Require one summary check, `ci-ok`, before merging.** It succeeds only when every version's
   job succeeds, so the branch rules don't change when the tested versions do.

This replaces the version requirement in ADR-0003 and the versions named in ADR-0004. Their other
decisions stay in force.

## Alternatives considered

- **Stay on 3.14 and run NeMo Guardrails as a separate service:** keeps the newest Python, but
  commits us to another service before we have evaluated the library.
- **Stay on 3.14 and wait for support:** no change now, but no known date.
- **Install NeMo Guardrails only on older versions:** our features would then differ by Python
  version.
- **Require each version's check by name:** no extra job, but the branch rules need editing at every
  version change.

## Consequences

- agentforge can't be installed on Python 3.14 or later.
- We have to lift the upper limit, through a new ADR, once our dependencies support newer versions.
  We should check this when we adopt or drop NeMo Guardrails.
- Python 3.12 receives only security fixes, and 3.13 is at or near the end of its regular bug-fix
  period. This makes lifting the limit more pressing over time.
