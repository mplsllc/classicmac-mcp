# Provider Contract

## Purpose

ClassicMacMCP separates semantic development operations from transport and machine-control mechanisms. A provider implements a bounded set of capabilities against a machine, toolchain, emulator, or bridge.

The public MCP interface must not degenerate into `run_shell`, `run_applescript`, `send_ftp`, or arbitrary GUI control.

## Provider classes

Providers may implement one or more capability families:

- machine identity and health;
- file transfer/deployment;
- CodeWarrior automation;
- native CodeWarrior plug-in communication;
- Retro68/local build execution;
- emulator control;
- application launch/termination;
- diagnostics/log/capture retrieval.

Examples of possible implementations include SSH + AppleEvents, Classic Control-style OSA execution, AgentBridge-style native control, Classic Mac Hardware MCP-style FTP/LaunchAPPL, and emulator-specific bridges.

## Capability discovery

Every provider returns a structured capability document. Capabilities are explicit and versioned.

Example:

```yaml
provider: workflow-ssh-cw
provider_version: 1
machine: g3-imac
capabilities:
  machine.identity:
    mode: read
  codewarrior.build:
    mode: mutate
    implementation: appleevent
    verification: project_and_artifact_postconditions
  codewarrior.add_project_file:
    mode: mutate
    implementation: gui
    verification: project_membership_postcondition
  app.run:
    mode: mutate
```

Unsupported operations are absent rather than simulated with arbitrary command execution.

## Required invariants

A provider must:

1. positively identify the target machine before mutation;
2. positively identify the target project/toolchain when relevant;
3. enforce project/machine allowlists locally;
4. serialize operations at the narrowest safe boundary;
5. use explicit timeouts;
6. treat timeout as ambiguous state, not automatic failure/rollback;
7. verify postconditions for state-changing operations;
8. return structured diagnostics and evidence metadata;
9. never log secrets;
10. refuse capabilities it cannot verify safely.

## Operation lifecycle

A mutating operation follows:

```text
request
  -> authorization
  -> machine identity
  -> project/toolchain identity
  -> lock
  -> precondition capture
  -> execute bounded provider operation
  -> postcondition verification
  -> evidence record
  -> unlock
```

If execution times out, the provider enters recovery/inspection before any retry.

## Evidence return

Provider results should contain enough information for the orchestration layer to create an evidence record:

```yaml
operation_id: ...
provider: workflow-ssh-cw
machine_id: g3-imac
started_at: ...
ended_at: ...
status: success
preconditions: {...}
postconditions: {...}
diagnostics: [...]
artifacts: [...]
raw_evidence_refs: [...]
```

The provider may return references to private logs/captures without exposing them publicly.

## Read versus mutate

Read-only capabilities may be exposed more broadly. Mutating capabilities require explicit local authorization even when the hosted MCP has already authorized the user.

Hosted authorization is necessary but not sufficient for local execution.

## CodeWarrior provider rule

A CodeWarrior provider implements semantic operations such as:

- IDE/project/target identity;
- update/build/compile;
- diagnostics;
- project membership;
- access paths/preferences when verified;
- launch/debugger operations only when verified.

The provider chooses the evidenced control surface: AppleEvent, native plug-in API, GUI automation, or another bounded mechanism. Clients do not choose raw scripts.

## Compatibility with third-party bridges

Third-party Classic Mac MCP/bridge projects should normally be integrated behind this provider contract rather than forked or reimplemented.

Their local-trust assumptions remain local. ClassicMacMCP must not automatically expose a third-party bridge's broad raw-command capability through the hosted public service.

## Failure classes

Provider failures should be classified at least as:

- `identity_mismatch`
- `authorization_denied`
- `capability_unavailable`
- `transport_failure`
- `timeout_state_unknown`
- `operation_rejected`
- `postcondition_failed`
- `toolchain_failure`
- `target_runtime_failure`

This allows the agent to reason about what failed without inferring from unstructured text.