# ADR-0006: Model provider interface

- **Status:** Accepted
- **Date:** 2026-11-27

## Context

[ADR-0002](0002-access-claude-through-anthropic-api.md) decided that agent code depends on a small
interface that agentforge owns, covering messages, streaming and tool use, with tests running
against a fake provider. [ADR-0003](0003-use-python-for-the-platform.md) left open whether core
interfaces are asynchronous, and [ADR-0004](0004-python-tooling-and-project-layout.md) left
asynchronous test support until that was settled.
[ADR-0005](0005-route-model-calls-through-litellm-proxy.md) adds an optional LiteLLM proxy that
routes model calls.

The forces are:

- Agents spend much of their time waiting for model and tool calls, and may run many at once.
- Changing a synchronous interface to an asynchronous one later affects every caller.
- Long responses need streaming to avoid request timeouts.
- Claude responses can contain blocks, such as thinking blocks, that must be sent back unchanged
  in later requests. Editing earlier turns can invalidate them.
- Model output, including tool input, is untrusted data.

## Decision

### Shape

The interface is asynchronous and has one method, which streams. It is a `typing.Protocol`, so an
adapter satisfies it by having a matching method, without inheriting from it.

```python
class ModelProvider(Protocol):
    def stream(
        self, request: ModelRequest
    ) -> AbstractAsyncContextManager[AsyncIterator[ModelEvent]]: ...
```

```python
async with provider.stream(request) as events:
    async for event in events:
        ...
```

- `async with` closes the connection even if the caller stops early or an error occurs.
- A `ModelEvent` is either a `TextDelta` (a piece of text) or `Completed` (the whole response).
  A successful stream ends with exactly one `Completed`.
- A caller that wants only the final response uses a shared `complete()` helper built on `stream()`,
  so adapters implement one method.

### Data types

agentforge defines its own types as immutable dataclasses. SDK types don't appear in the interface.

| Type | Contents |
|---|---|
| `ModelRequest` | messages, system prompt, tool definitions, maximum output tokens |
| `Message` | role (user or assistant) and a sequence of content blocks |
| Content blocks | `TextBlock`, `ToolUseBlock`, `ToolResultBlock`, `OpaqueBlock` |
| `ModelResponse` | assistant message, stop reason, token usage, reported model name |
| Stop reason | end of turn, tool use, token limit, refusal, other |

- An `OpaqueBlock` holds provider data that agent code doesn't interpret. It records which format
  it came from. Agent code returns it unchanged and in its original position.
- Conversation history is append-only. Agent code doesn't edit or remove earlier messages, or
  change the system prompt or tools partway through a conversation.
- Tools run only when the stop reason is tool use, and only after their input has been validated.

### Errors

Adapters translate SDK exceptions into `ProviderError`, which says whether a retry makes sense.
Its subclass `ProviderRateLimitError` also carries the suggested wait, when there is one. Adapters
rely on the SDK's built-in retries, and the interface adds none. If a stream fails partway, the
caller discards the partial output.

### Adapters and configuration

- `AnthropicProvider` uses the SDK's asynchronous client. It calls the Anthropic API, or the
  LiteLLM proxy when `ANTHROPIC_BASE_URL` is set.
- `FakeProvider` returns scripted responses and records the requests it receives. It ships in the
  package, so that anyone building on agentforge can test with it.
- The model name is set when a provider is created, not on each request. It is a model ID when
  calling Anthropic directly, and a route name when calling through the proxy. Code that needs two
  routes creates two providers.
- The name comes from the `AGENTFORGE_MODEL` environment variable, which is required.
  `.env.example` suggests `claude-haiku-5-5` for development. Load a local `.env` file with
  `uv run --env-file .env`.
- The code lives in `src/agentforge/providers/`.

### Dependencies and tests

- Add `anthropic` as a runtime dependency, limited to its current major version.
- Add `pytest-asyncio` as a development dependency.
- The same contract tests run against both providers. Tests of the Anthropic adapter replace its
  HTTP transport, so they make no network calls and need no key. They check that a response's
  content, sent back in the next request, is unchanged.

## Alternatives considered

- **Synchronous interface:** easier to read and debug, but running calls concurrently would need
  threads, and changing later is costly.
- **Both synchronous and asynchronous interfaces:** two paths to implement and test.
- **Separate `complete` and `stream` methods:** convenient, but every adapter, including the fake,
  would implement the same behaviour twice.
- **Use the SDK's types in the interface:** less conversion code, and nothing lost in translation,
  but agent code and the fake would depend on one vendor's SDK.
- **Abstract base class:** makes the relationship explicit, but forces inheritance and adds nothing
  we need while the type checker verifies the protocol.

## Consequences

- Code that calls a model must be asynchronous, and so must its callers.
- We write and maintain conversion code in each adapter. A new kind of response block must be
  preserved as opaque data or given a type, never silently dropped.
- Append-only history limits how we can shorten long conversations. Compaction or context editing
  will need its own decision.
- Switching models partway through a conversation may lose opaque data such as thinking.
- A refusal is reported to the caller. Automatic fallback to another model is not included, and
  should be decided before we default to a model that supports it.
- Not in the interface yet: effort and thinking settings, prompt caching, images, structured
  outputs and server-side tools. Each is added when something needs it.
- Vertex AI, if access is granted, can be reached through the proxy or a later adapter.
