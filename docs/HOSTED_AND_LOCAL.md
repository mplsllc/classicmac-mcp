# Hosted and Local Execution Model

ClassicMacMCP deliberately separates the public/hosted knowledge service from private machine execution.

## Hosted service

The hosted service is designed to be safe for public multi-user operation. It may:

- serve curated knowledge;
- validate manifests and compatibility policy;
- search public provenance/evidence;
- coordinate authenticated capability requests;
- maintain audit metadata and rate limits;
- identify compatible providers registered by a user.

The hosted service must not contain reusable credentials for a user's vintage Macintosh or private LAN.

The hosted process does not expose generic:

- shell execution;
- SSH command execution;
- arbitrary AppleScript;
- arbitrary AppleEvent construction;
- GUI clicking/typing;
- raw TCP/FTP access to target machines.

## Local/private execution service

A machine owner runs a provider/bridge under their own control. The local provider owns:

- SSH/FTP/TCP credentials;
- host keys and local network addresses;
- CodeWarrior automation details;
- local source/workspace paths;
- machine-specific packaging/deployment tools;
- physical/emulator machine locks;
- final authorization for mutating operations.

The local provider can reject a hosted request even when the hosted service considers the user authorized.

## Capability model

Authorization is semantic and narrow. Examples:

- `project.read`
- `codewarrior.read`
- `codewarrior.build`
- `codewarrior.project_mutate`
- `machine.deploy`
- `machine.launch`
- `machine.capture`

A bridge enrollment does not imply all capabilities.

## Request flow

```text
MCP client
   |
   v
hosted ClassicMacMCP
   |  authenticate + authorize semantic operation
   v
owner-controlled provider
   |  local policy + machine/project identity
   v
CodeWarrior / Retro68 / target machine
   |
   v
structured evidence result
```

A provider may also run entirely locally via stdio without using the hosted service.

## Secrets

Public project/machine manifests contain identifiers and capabilities, not secrets.

Secrets are referenced from provider-local configuration or a deployment secret store. They must not be committed to `classicmac-mcp`, `classicmac-kb`, or public project manifests.

## Network assumptions

Vintage target systems should normally remain on a trusted/private network segment. The architecture should avoid requiring a Classic Mac to expose a service directly to the public Internet.

Existing projects such as Classic Control, AgentBridge, and Classic Mac Hardware MCP are useful local-LAN/provider prior art, but their local trust assumptions are not inherited by the hosted service.

## Operation lifecycle

Mutating operations follow:

1. authorize requested semantic capability;
2. acquire required project/machine lock;
3. positively identify machine, IDE, project, target, and source revision;
4. perform one bounded operation;
5. verify the postcondition;
6. collect evidence;
7. release lock;
8. return structured result.

A transport timeout does not prove the remote operation stopped. Before retrying any mutation, the provider must query observable state and decide whether the original request completed, is still active, or failed.

## Hosted deployment

Production hosted MCP uses TLS and Streamable HTTP. Authentication, resource/audience validation, rate limiting, audit logging, and abuse controls are infrastructure responsibilities and are documented separately in the private `classicmac-infra` repository.

The public repository defines the security contract; private infrastructure implements deployment-specific details.
