# CodeWarrior Native Plugin API

## Status

Research/design document. No native Plugin API capability is considered verified for the project's CodeWarrior Pro 8.x environment solely because it appears in the IDE 5.1 SDK documentation.

## Primary reference currently available

Private reference corpus:

- `mplsllc/macsurf-private/books/text/SDKAPIRM.txt`
- `mplsllc/macsurf-private/books/text/SDKAPIRM2.txt`

These two files are consecutive parts of one manual:

**CodeWarrior Development Tools — IDE 5.1 SDK API Reference**, revised 25-Aug-2003, Metrowerks/Freescale.

The complete copyrighted manual remains private. The public project records only metadata, API names, derived architecture notes, and independently verified compatibility facts.

## Why the API matters

The SDK shows that CodeWarrior exposes structured callbacks for IDE/project information that overlap directly with operations ClassicMacMCP currently performs through AppleEvents, GUI automation, or external filesystem inspection.

This suggests a future native provider may offer deterministic read access to project state and selected mutations without screen scraping.

## Documented capability families

The SDK's functional API index groups routines into:

- request handling;
- memory management;
- plug-in data;
- preference data;
- file management;
- directory/access-path information;
- project-file information;
- target information;
- overlay/segment information;
- IDE information;
- user interaction;
- error handling;
- COM interfaces on applicable hosts.

### IDE and API identity

Documented calls include:

- `CWGetIDEInfo`
- `CWGetAPIVersion`

`CWGetIDEInfo` is documented as returning detailed IDE version information and the latest plug-in API version available in the IDE. The SDK also describes plug-ins declaring the newest API version they need through `CWPlugin_GetDropInFlags`.

This is strategically important: a native provider should discover API/IDE compatibility at runtime rather than assume a manual's revision matches the installed IDE.

### Project-file information

Documented calls include:

- `CWGetProjectFileCount`
- `CWGetProjectFile`
- `CWAddProjectEntry`
- `CWRemoveProjectEntry`

`CWGetProjectFileCount` is documented as returning the number of files in the active project target.

`CWAddProjectEntry` is documented as adding a file to a project. The manual notes that if it is called during an active make, the IDE restarts the build operation. That lifecycle behavior is a reason to keep project mutation serialized and explicitly separated from build orchestration.

The API also exposes `CWNewProjectEntryInfo`, including per-entry ordering/settings information.

### Access paths

Documented calls include:

- `CWGetAccessPathListInfo`
- `CWGetAccessPathInfo`
- `CWGetAccessPathSubdirectory`
- `CWResolveRelativePath`

The SDK documents enumeration of user/system access paths, recursive-search state, path `CWFileSpec`, and discovered subdirectories.

This could eventually let ClassicMacMCP inspect the actual target's access-path model directly rather than infer it from project XML or UI state.

### Target information

Documented calls visible in the SDK index include:

- `CWGetTargetName`
- `CWGetTargetDataDirectory`
- `CWGetOutputFileDirectory`
- named-preference access;
- segment/overlay information.

These are candidates for structured target identity and artifact-location queries.

### Diagnostics / interaction

The common API includes routines such as:

- `CWReportMessage`
- `CWAlert`
- error/result conversion and callback-error retrieval.

The SDK also defines plug-in request/result contracts and explicit error codes. A future provider should translate these to ClassicMacMCP's structured failure taxonomy rather than expose raw SDK result values as the public API.

### VCS plug-in API

The second half of the available manual documents a Version Control System plug-in API. It is useful evidence that CodeWarrior supports structured callbacks for IDE information, file state, messages, and project interaction across more than compiler/linker plug-ins.

It is not currently a target implementation strategy for ClassicMacMCP; it is architectural prior art.

## Compatibility rule

For every API symbol, maintain separate states:

```yaml
symbol: CWGetProjectFileCount
source:
  manual: codewarrior-ide-5.1-sdk-api-reference
  status: documented
cw8:
  header_present: unknown
  linkable: unknown
  callable: unknown
  behavior_verified: false
```

Possible status progression:

```text
DOCUMENTED_5_1
    -> HEADER_VERIFIED_CW8
    -> COMPILE_LINK_VERIFIED_CW8
    -> RUNTIME_VERIFIED_CW8
    -> PROVIDER_APPROVED
```

Skipping levels is not allowed.

## Research procedure for CW8

On the actual CodeWarrior Pro 8 installation/media:

1. inventory Plugin API headers, libraries, stationery, samples, and release notes;
2. hash/version the artifacts;
3. identify API version macros and IDE compatibility notes;
4. build the smallest read-only plug-in fixture possible;
5. query `CWGetIDEInfo` and `CWGetAPIVersion`;
6. compare available headers/symbols against the 5.1 reference;
7. test read-only project/target/access-path calls;
8. record every mismatch as compatibility knowledge;
9. consider mutation only after read-only lifecycle is understood.

## Preferred first native capabilities

If compatible, implement read-only operations first:

- IDE/API identity;
- target name;
- project-file count/list;
- access-path list;
- output directory;
- selected project/target information.

These operations can be cross-checked against the proven AppleEvent/workflow path and therefore make excellent differential tests.

## Mutation policy

Calls such as `CWAddProjectEntry` or `CWRemoveProjectEntry` remain disabled until:

- exact CW8 API compatibility is established;
- project lifecycle/reentrancy behavior is understood;
- before/after state can be queried independently;
- rollback/recovery behavior is defined;
- hardware tests demonstrate reliability.

The public MCP will expose `codewarrior.add_project_file`, not `CWAddProjectEntry`. The native callback is an internal implementation detail selected by the capability resolver.

## Native bridge concept

A future CodeWarrior plug-in should expose a *small semantic protocol*, not the raw Plugin API. For example:

```text
get_ide_identity
get_project_identity
list_project_files
get_access_paths
get_target_info
get_build_state
```

The plug-in should not become a generic memory/function-call/RPC bridge into the IDE process.

## Relationship to AppleEvents

The Plugin API does not replace the Automation API by default.

AppleEvents remain valuable because they are officially exposed for IDE automation and are already proven in the current workflow. The native API is most attractive where it offers structured read access or a demonstrably more reliable implementation than AppleEvents/GUI automation.

The capability registry, not ideology about one control mechanism, decides which backend wins for each semantic operation.
