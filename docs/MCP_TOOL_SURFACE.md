# MCP Tool Surface

This document distinguishes the tools implemented by the hosted/read-only core from planned private execution capabilities.

## Implemented hosted/read-only tools

### `classicmac_about`

Returns server mode, version, trust-boundary information, knowledge paths, validation levels, and retrieval-layer summary.

### `classicmac_validate_project`

Validates a portable project manifest and reiterates toolchain authority. Validation does not contact hardware or compile code.

### `classicmac_scan_c89`

Runs deterministic strict-C89 policy checks over supplied source text. It is not a compiler and does not establish CodeWarrior compatibility.

### `classicmac_validation_ladder`

Explains the meanings and limits of `static_verified`, `retro68_verified`, `codewarrior_verified`, and `hardware_verified`.

### `classicmac_search_knowledge`

Searches canonical reviewed knowledge. When a project manifest is supplied, applicability filters exclude explicitly incompatible records.

This is the default trusted target-programming retrieval surface.

### `classicmac_get_knowledge`

Returns one canonical knowledge record with expanded provenance/evidence.

### `classicmac_search_history`

Searches configured full Git histories. Results are raw evidence candidates and are marked noncanonical.

### `classicmac_search_documents`

Searches explicitly opted-in current repository/workflow documents. Results are marked noncanonical.

### `classicmac_search_references`

Searches an optional separate vendor/historical reference index. Results are always:

- noncanonical;
- follow-up-only;
- labeled with corpus and source layer;
- accompanied by an applicability warning.

A public deployment may return no results if no private/reference corpus is configured.

## Retrieval intent

A normal coding workflow should usually proceed:

```text
search_knowledge
      |
      +-- sufficient -> use scoped canonical guidance
      |
      +-- insufficient/unknown
             |
             +-> search_history / search_documents
             |
             +-> search_references when vendor/historical context is useful
```

The MCP should not inject every layer automatically into every prompt.

## Planned private/local semantic tools

These names represent intended semantics, not currently exposed hosted tools.

### CodeWarrior identity/read

```text
codewarrior.get_ide_identity
codewarrior.get_capabilities
codewarrior.get_project_identity
codewarrior.get_active_target
codewarrior.list_targets
codewarrior.list_project_files
codewarrior.get_access_paths
codewarrior.get_build_state
codewarrior.get_build_messages
```

### CodeWarrior mutation/build

```text
codewarrior.compile_file
codewarrior.update_project
codewarrior.build
codewarrior.remove_object_code
codewarrior.add_project_file
codewarrior.remove_project_file
codewarrior.import_project
codewarrior.select_target
codewarrior.run
```

These require private/local provider authorization, locking, identity verification, postcondition verification, and structured evidence.

### Machine/deployment

```text
machine.status
machine.deploy
machine.launch
machine.capture
machine.retrieve_artifact
```

### Validation

```text
compatibility.check_project
retro68.preflight
```

## Tools intentionally not exposed

The normal MCP API will not expose generic:

```text
run_shell(command)
run_ssh(command)
run_applescript(source)
send_appleevent(raw_event)
click(x, y)
call_codewarrior_plugin_function(symbol, args)
```

Those capabilities may exist internally inside a provider implementation, but agents interact through bounded semantic operations.

## Tool-result requirements

State-changing operations eventually use a common result envelope containing:

- attempt ID;
- semantic operation;
- provider identity;
- project/machine/toolchain identity;
- status/failure class;
- timestamps;
- postconditions;
- evidence references.

Transport stdout, AppleScript results, screenshots, or raw IDE messages are evidence attachments rather than the semantic API itself.

## Versioning

Public tool signatures should be conservative. Provider/backend improvements must not require agents to know whether the operation is implemented by AppleEvents, native Plugin API calls, GUI automation, FTP/LaunchAPPL, or another bridge.

When semantics must change incompatibly, version the operation/schema rather than silently reinterpret an existing field.
