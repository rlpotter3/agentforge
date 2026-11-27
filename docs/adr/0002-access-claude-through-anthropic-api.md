# ADR-0002: Access Claude through the Anthropic API, behind a provider interface

- **Status:** Accepted
- **Date:** 2026-11-27

## Context

agentforge needs to call a language model. The plan was to use Claude through Google Vertex AI,
but that is blocked:

- A test request to Claude Haiku 5.5 on the global endpoint failed with HTTP 429 (quota exceeded).
- The project's global quotas for Claude Haiku, Sonnet, Opus and Fable show zero.
- We upgraded the account and asked for a quota increase. The request was denied.
- We tested again on 2026-11-27, in case an overnight process had changed the quota. The result was
  the same: HTTP 429 on `global_online_prediction_requests_per_base_model` for
  `anthropic-claude-haiku`.

We don't know when, or whether, Vertex AI access will be granted. Development of the core agent
abstractions should not wait for it.

Two other forces apply. agentforge is open source, so contributors need a way to run it that
doesn't depend on our cloud project. And we may still want Vertex AI later, so the choice should
be cheap to reverse.

## Decision

1. **Use the Anthropic API (first-party) as the initial way to call Claude**, through the official
   Anthropic SDK for whichever language we choose.
2. **Put model access behind a small provider interface** that agentforge owns. Agent code depends
   on the interface. Only the adapter behind it knows which platform serves the request.
3. **Keep the interface to what we use**, starting with messages, streaming and tool use. We add to
   it when a feature needs it, and we don't try to cover other model vendors in advance.
4. **Read configuration from environment variables**: the API key (`ANTHROPIC_API_KEY`, the name
   the SDK looks for) and the model ID. Only placeholders go in `.env.example`.
5. **Test against a fake provider.** Automated tests make no network calls and need no credentials.

## Alternatives considered

- **Wait for or appeal the Vertex AI quota decision.** This keeps one bill and Google Cloud IAM,
  but blocks progress with no known end date. We can still pursue it alongside this decision.
- **Claude Models on Google Cloud (Anthropic managed).** Anthropic runs this service, and it is
  reached with Google credentials and billed through Google Cloud Marketplace. It needs no API key
  and is closer to the first-party API than Vertex AI is. We have not tested whether our project
  can use it, or how its quotas and prices compare. It needs a Marketplace subscription and a new
  Anthropic organisation, and contributors would need a Google Cloud project of their own. This is
  the strongest candidate for a second adapter.
- **Claude through another cloud (Amazon Bedrock or Microsoft Foundry).** This adds a second cloud
  account to set up and secure, and we have not checked what quota a new account would get.
- **Call the SDK directly, with no interface.** This is less code today. Changing platform later
  would then touch agent code, and tests would be harder to isolate.
- **Use a third-party multi-model library.** This offers many vendors at once, but adds a large
  dependency and its own abstractions before we know what we need.

## Consequences

- Development can proceed. A test request to Claude Haiku 5.5 through the Anthropic API succeeded
  on 2026-11-27.
- There is a long-lived secret to protect. It stays out of the repository, and deployed
  environments will need a secret store.
- Usage is billed by Anthropic, separately from Google Cloud. The Google Cloud budget alerts don't
  cover it, so we need a spend limit or alert on the Anthropic account.
- The first-party API has rate limits of its own, so we still need to handle HTTP 429.
- Some features of the first-party API are missing on Vertex AI, including Message Batches, the
  Files API, the Models API and server-side code execution. If agent code relies on one, moving to
  Vertex AI gets harder. Adopting such a feature should be a deliberate, recorded choice.
- A later Vertex AI adapter should be small, because the Anthropic SDK has a Vertex AI client with
  the same messages interface. Authentication, configuration and feature differences still need
  their own tests.
- This ADR does not choose the programming language or the default model. Both need to be settled
  before the interface is written.
