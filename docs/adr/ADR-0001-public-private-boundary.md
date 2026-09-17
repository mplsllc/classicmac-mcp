# ADR-0001: Separate public knowledge from private hardware authority

- Status: Accepted
- Date: 2026-09-16

## Context

ClassicMacMCP is intended for public/community use, while vintage development machines are privately owned, weakly isolated by modern standards, and often reachable only through trusted LAN/SSH/FTP/OSA workflows.

A hosted multi-user MCP must not become a transitive control path into a maintainer's G3 or another user's machine.

## Decision

The hosted/public service and local/private execution provider are separate trust domains.

The hosted service may provide knowledge, validation, discovery, authorization, coordination, and audit functions. Reusable machine credentials and private network details remain local/private.

A local provider independently authorizes and executes semantic operations against explicitly configured machines/projects.

## Consequences

Positive:

- public KB access does not imply hardware access;
- machine credentials can remain off the hosted service;
- users can run local-only stdio workflows;
- local policy can deny a hosted request;
- different providers can support different networks/machines.

Costs:

- provider enrollment/authentication requires explicit design;
- evidence must cross a trust boundary cleanly;
- some operations require coordination between hosted and local components.

## Rejected alternatives

- Hosting Patrick's G3 connection directly in the public MCP.
- Exposing arbitrary SSH/AppleScript/TCP tools from the hosted service.
- Treating an authenticated MCP user as automatically authorized for every enrolled machine.
