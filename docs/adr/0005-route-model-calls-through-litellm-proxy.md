# ADR-0005: Route model calls through a LiteLLM proxy

- **Status:** Accepted
- **Date:** 2026-11-27

## Context

We plan to use LiteLLM for model routing, so that the model behind a request can be changed through
configuration. LiteLLM can run in two ways: as a proxy (a separate gateway service) or as a Python
library inside the application. We plan to run the proxy, and to install it on 2026-12-08 or later.

[ADR-0002](0002-access-claude-through-anthropic-api.md) chose the Anthropic API through the official
SDK, behind a provider interface. It rejected a third-party multi-model library because that added a
large dependency and its own abstractions before we knew what we needed.

LiteLLM documents an Anthropic-format
[`/v1/messages` endpoint](https://docs.litellm.ai/docs/anthropic_unified) that the official SDK can
call by changing its base URL.

Other forces:

- The proxy holds provider API keys, which makes it a valuable target.
- Compromised, credential-stealing LiteLLM releases were published in
  [March 2026](https://docs.litellm.ai/blog/security-update-march-2026) (1.82.7 and 1.82.8) and in
  [October 2026](https://securitylabs.datadoghq.com/articles/litellm-compromised-pypi-docker/)
  (1.107.0, including Docker tags such as `latest`).
- Contributors should be able to run agentforge without operating a gateway.

## Decision

1. **Run LiteLLM as a proxy for model routing**, from 2026-12-08 at the earliest. Don't add the
   LiteLLM library as a dependency of agentforge.
2. **Keep the official Anthropic SDK and our provider interface.** agentforge reaches the proxy
   through the same adapter it uses for the Anthropic API.
3. **Make the proxy optional.** Calling the Anthropic API directly stays the default, and is how we
   work until the proxy is installed. Setting `ANTHROPIC_BASE_URL` selects the proxy.
4. **Use route names.** Through the proxy, the configured model name is an alias that the proxy maps
   to a model. Routing rules live in the proxy's configuration, not in agent code.
5. **Keep each conversation on one model and deployment.** Routing chooses between conversations,
   not partway through one.
6. **Control what we run.** Pin an exact LiteLLM version or image digest, never a floating tag.
   Adopt a release only after it has been public for at least two weeks and we have checked for
   security advisories.
7. **Protect the proxy.** Don't expose it to the public internet. Keys come from environment
   variables or a secret store, never from committed files. Give agentforge a limited key, not the
   proxy's administrator key.

This adds to ADR-0002, which stays in force. It doesn't change the choice of SDK.

## Alternatives considered

- **LiteLLM as a library:** no extra service to run, but a large dependency inside our process, a
  different adapter, and routing tied to our releases.
- **Write our own routing:** full control and no third-party gateway, but we would build and
  maintain retries, fallbacks and load balancing ourselves.
- **No routing:** the least to run and secure, but changing models stays a per-application setting.

## Consequences

- Changing which model serves a route needs no change to agentforge.
- There is another service to deploy, monitor, upgrade and secure. Where it runs is not yet decided.
- We depend on the proxy preserving requests and responses faithfully. Before relying on it, test
  through it a conversation with streaming, thinking and several tool calls. A
  [reported bug](https://github.com/BerriAI/litellm/issues/41361) describes thinking blocks being
  dropped on this endpoint; check whether the version we pin is affected.
- Check which model name a response reports through the proxy, so that we can tell which model
  served it.
- Routes to models other than Claude may behave differently. Each needs the same testing first.
- The proxy may offer another way to reach Vertex AI if access is granted, without a second adapter.
- Waiting before upgrades delays fixes. An urgent security fix may justify a shorter wait after
  review.
