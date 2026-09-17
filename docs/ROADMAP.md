# Roadmap

ClassicMacMCP is being built in stages so that knowledge quality, compatibility, and security mature before broad hardware mutation is exposed.

## Phase 0 — Foundation

Status: in progress.

Deliverables:

- public/private trust boundary;
- semantic CodeWarrior API model;
- compatibility and evidence levels;
- provider abstraction;
- curated Classic Mac knowledge repository;
- generated searchable history/document indexes;
- MCP v2 hosted read-only service;
- CI for both MCP and KB repositories.

Exit criteria:

- architecture and ADR set are internally consistent;
- schemas reject incompatible/ambiguous data;
- hosted MCP exposes no arbitrary shell, SSH, AppleScript, GUI, or hardware-control surface;
- knowledge retrieval distinguishes canonical facts from raw evidence and historical references.

## Phase 1 — Knowledge and compatibility

Build the reusable compatibility corpus before broad automation.

Deliverables:

- systematic mining of `mplsllc/workflow` and MacSurf history;
- private historical-reference ingestion for Metrowerks/Apple documentation;
- source applicability metadata;
- C89/CW8 compatibility scanner;
- Retro68 `cw8-compat` validation profile;
- compiler-difference regression suite;
- knowledge promotion workflow.

Exit criteria:

- known CW8/C89 traps have deterministic tests where practical;
- Retro68 results are never represented as CodeWarrior verification;
- vendor documentation is searchable but does not silently become canonical knowledge;
- project manifests constrain retrieval by target/toolchain/language.

## Phase 2 — CodeWarrior discovery and read-only control

Deliverables:

- exact IDE fingerprinting;
- AppleEvent dictionary inventory;
- native Plugin API capability inventory;
- project/target/member/access-path read APIs;
- build-state and diagnostic read APIs;
- provider capability registry.

The native Plugin API must be version-gated. The IDE 5.1 SDK API Reference is discovery evidence only until operations are demonstrated against the installed CW Pro 8.x environment.

Exit criteria:

- project identity can be proved before mutation;
- capability discovery reports implementation and evidence level;
- no operation claims support solely because a historical manual documents it.

## Phase 3 — Controlled build workflow

Deliverables:

- source transfer with post-transfer verification;
- CodeWarrior update/build/compile operations;
- text-first diagnostics retrieval;
- artifact identity checks;
- lock/attempt/evidence records;
- stale-build protection;
- deterministic recovery after timeout.

Reference implementation: the proven SSH + AppleScript/AppleEvent workflow in `mplsllc/workflow`.

Exit criteria:

- a deliberately changed fixture produces a new identified artifact;
- deliberate compiler failure blocks launch/package;
- timeout recovery does not blindly retry state-changing IDE operations;
- build success requires observed postconditions, not merely a no-error return.

## Phase 4 — Hardware providers

Deliverables:

- local/private provider runtime;
- first-party SSH/AppleEvent provider;
- adapters for useful prior art where appropriate (Classic Control, AgentBridge, Classic Mac Hardware MCP);
- deploy/run/status/capture semantics;
- per-machine serialization and policy enforcement.

Exit criteria:

- hosted service holds no reusable vintage-machine credentials;
- a local provider can independently deny an operation;
- execution evidence records machine, artifact, project, revision, and result.

## Phase 5 — Native CodeWarrior provider research

Investigate a narrowly scoped CodeWarrior plug-in/provider using the documented IDE Plugin API.

Candidate read-only capabilities:

- `CWGetIDEInfo` / API version discovery;
- project-file count/enumeration;
- access-path enumeration;
- target identity/output directory;
- structured message reporting and project metadata.

Candidate mutations such as `CWAddProjectEntry` are not enabled until exact-version compatibility and safe lifecycle behavior are verified.

Exit criteria:

- exact SDK/header compatibility is established for the installed IDE;
- native provider offers a measurable reliability advantage over existing automation;
- no generic remote-command channel is introduced into CodeWarrior.

## Phase 6 — Public hosted service

Deliverables:

- Streamable HTTP deployment;
- authentication/authorization;
- resource/audience validation;
- rate limiting and audit logs;
- public curated KB;
- private-user/project overlays;
- provider enrollment without exposing private networks.

## Phase 7 — Community platform

Deliverables:

- contribution/review process for compatibility facts;
- additional CodeWarrior releases and toolchains;
- MPW/Retro68/emulator providers;
- additional physical-machine profiles;
- reproducible fixtures and conformance suites;
- versioned knowledge snapshots.

## Non-goals for early releases

- replacing CodeWarrior with a modern compiler;
- exposing a public arbitrary shell/SSH/AppleScript tool;
- treating generic modern C/C++ knowledge as target truth;
- redistributing copyrighted vendor manuals or SDK material;
- claiming hardware behavior from emulator or host-only tests.
