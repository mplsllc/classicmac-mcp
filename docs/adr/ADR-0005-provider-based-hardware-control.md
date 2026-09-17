# ADR-0005: Hardware control is provider-based

- Status: Accepted
- Date: 2026-09-16

## Context

Existing prior art already implements useful pieces of Classic Mac control: FTP/LaunchAPPL deployment, native TCP/OSA helpers, AppleEvent-driven IDE automation, screenshots, and application control. Reimplementing every transport would duplicate work and tightly couple the platform to one machine topology.

## Decision

ClassicMacMCP defines semantic provider contracts. Transport/hardware projects may implement those contracts without becoming the public MCP abstraction.

The platform will support multiple providers such as:

- SSH + AppleScript/AppleEvents;
- Classic Control-style native helper;
- AgentBridge-style native control;
- Classic Mac Hardware MCP-style FTP/LaunchAPPL deployment;
- emulator providers;
- future native CodeWarrior plug-in providers.

Providers expose capabilities, identity, locking requirements, and structured evidence.

## Consequences

Positive:

- useful prior art can be reused/adapted;
- projects are not coupled to Patrick's current G3 topology;
- different users can supply their own bridge/machine implementation;
- security policy can differ between hosted coordination and local execution.

Costs:

- provider capability negotiation is required;
- behavior differences must be normalized into common result/failure semantics;
- conformance tests are needed.

## Rejected alternatives

- A monolithic MCP with embedded SSH/FTP/GUI assumptions.
- A generic remote-shell provider as the main public interface.
- Requiring every target machine to run the same custom native daemon.
