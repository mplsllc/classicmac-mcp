# Provider Contract

Providers implement bounded Classic Mac development capabilities behind stable semantic operations. They hide transport and machine-specific details from MCP clients.

## Provider principles

A provider:

- declares capabilities explicitly;
- owns its credentials and connection details;
- positively identifies the target before mutation;
- serializes operations where the vintage environment requires it;
- returns structured results and evidence;
- verifies postconditions;
- never assumes a timeout means an operation stopped;
- may independently deny a request.

A provider is not a generic shell.

## Provider categories

### CodeWarrior automation provider

Typical implementation: SSH to a Tiger/OS X host, then `osascript` driving CodeWarrior AppleEvents with bounded GUI fallback.

Reference implementation: `mplsllc/workflow`.

### Native Classic Mac control provider

A target-side helper exposes bounded filesystem/application/OSA operations. Prior art includes Classic Control and AgentBridge.

These providers are useful transport/control mechanisms; ClassicMacMCP still owns CodeWarrior semantics, compatibility, and evidence policy.

### Deployment/run provider

Prior art: `classic-mac-hardware-mcp` style FTP + LaunchAPPL execution.

Useful for transfer/run/hardware inventory, but not itself an authoritative CodeWarrior build interface.

### Emulator provider

Future providers may target SheepShaver, QEMU, Basilisk II, or other emulators. Emulator evidence must remain labeled separately from physical-hardware evidence.

### Native CodeWarrior plug-in provider

A future provider may run inside the IDE using the documented Metrowerks Plugin API. This provider must be version-gated against the exact installed IDE/SDK.

## Capability discovery

Providers return a capability document rather than forcing callers to infer support from provider type.

Example:

```yaml
provider_id: g3-imac-workflow
provider_kind: codewarrior-automation
machine_id: g3-imac
capabilities:
  codewarrior.get_project_identity:
    mode: read
    status: verified
  codewarrior.build:
    mode: mutate
    status: verified
  codewarrior.add_project_file:
    mode: mutate
    status: verified
    implementation: gui
  codewarrior.add_project_file.appleevent:
    status: broken
```

Capability entries may include:

- implementation (`appleevent`, `plugin_api`, `gui`, `ftp`, `launchappl`, etc.);
- evidence level;
- IDE/machine fingerprint;
- required lock scope;
- required authorization scope;
- known failure modes.

## Semantic result envelope

Every provider operation returns a common envelope:

```yaml
attempt_id: "..."
operation: codewarrior.build
provider_id: g3-imac-workflow
status: success
started_at: "..."
finished_at: "..."
identity:
  machine: g3-imac
  project: macsurf
  source_revision: "..."
  toolchain: codewarrior-8.3
postconditions:
  project_identified: true
  diagnostics_clean: true
  artifact_changed: true
evidence:
  - kind: build_messages
    ref: "..."
  - kind: artifact_identity
    ref: "..."
```

Transport-specific stdout/stderr may be attached as evidence, but callers should not need to parse it to decide whether the semantic operation succeeded.

## Locking

Locks are explicit and scoped at the narrowest safe boundary. Examples:

- `machine:g3-imac` for target-global native helpers;
- `codewarrior:g3-imac:MacSurf.mcp` for IDE/project mutation;
- `deployment:g3-imac:MacSurf` for target application replacement.

Providers that are inherently single-threaded should declare that fact and serialize accordingly.

## Identity requirements

Before mutation, the provider must establish enough identity to prevent wrong-target work. Depending on the operation this includes:

- remote host and OS;
- CodeWarrior IDE fingerprint/version;
- exact open project path;
- active target;
- source revision/dirty state;
- output artifact path and prior identity;
- destination path on target.

Do not trust positional handles such as `project document 1` until they have been resolved to the intended project.

## Failure semantics

Provider failures are classified, not flattened to `false`:

- `authorization_denied`
- `identity_mismatch`
- `capability_unavailable`
- `transport_failure`
- `operation_timeout_unknown_state`
- `compiler_failure`
- `linker_failure`
- `diagnostic_policy_failure`
- `postcondition_failed`
- `target_runtime_failure`

`operation_timeout_unknown_state` explicitly prevents blind retries.

## Adapter selection

ClassicMacMCP chooses an implementation using:

1. exact applicability to IDE/machine/project;
2. verified capability status;
3. semantic fidelity;
4. reliability/postcondition observability;
5. least privilege;
6. fallback cost.

GUI automation may be preferred over an AppleEvent when controlled evidence shows the AppleEvent is broken. A native plug-in may later supersede both if exact-version testing demonstrates safer and more deterministic behavior.
