# Security Model

ClassicMacMCP is designed for a future in which a public hosted MCP service may be used by unrelated people while private bridges can control real vintage computers. Security therefore starts with a hard separation between public knowledge and private execution.

## Assets

Protect at minimum:

- user identities and authorization grants;
- private machine addresses and credentials;
- SSH keys, FTP passwords, bridge enrollment secrets, and OAuth credentials;
- source code and private project metadata;
- compiler/build artifacts and logs that may contain private paths/data;
- vintage machines and filesystems;
- hosted service integrity and the public knowledge corpus;
- provenance/evidence records.

## Threats

The service must assume:

- model/tool inputs can be prompt-injected or malicious;
- authenticated users can attempt cross-tenant access;
- callers may submit hostile paths, project manifests, archives, source text, or oversized inputs;
- credentials may be targeted through logs/errors/tool output;
- an LLM may repeat a destructive action after a timeout;
- vintage transports may provide weak or no cryptographic protection;
- a bridge may be compromised independently of the hosted service;
- a malicious or mistaken knowledge contribution could poison future code generation.

## Core controls

### Trust-domain separation

The hosted core MUST NOT require direct credentials to users' Classic Macs.

A private bridge is separately enrolled and enforces its own local authorization. Hosted authorization can narrow authority but cannot expand beyond local bridge policy.

### Least privilege

Tools are separated by capability. Example scope families:

- `knowledge:read`
- `project:validate`
- `evidence:read`
- `bridge:discover`
- `build:run`
- `artifact:transfer`
- `target:run`
- `target:delete`
- `project:mutate`

Read access must not implicitly grant mutation or execution.

### No arbitrary shell as the primary API

Public tools expose semantic operations. Adapters own command construction. Any future escape-hatch shell/debug tool must be explicitly privileged, disabled by default, audited, and never necessary for the normal workflow.

### Filesystem containment

Local paths supplied by a client must resolve beneath explicitly configured project/artifact roots. Reject traversal, symlink escapes where applicable, device paths, and arbitrary host filesystem access.

Remote Mac paths are validated by the selected transport/provider. Root deletion and equivalent destructive operations are denied by default.

### Secret handling

- secrets never appear in project manifests committed to public repositories;
- prefer secret references, OS keychains, SSH agents, or a production secret manager;
- never pass secrets as process arguments;
- redact credentials/tokens from logs and exception text;
- never echo secret values back through MCP results;
- production secret rotation must be documented and testable.

### Authentication and authorization

The remote MCP deployment must follow the current MCP authorization specification and OAuth security requirements.

At the resource server:

- validate token issuer where applicable;
- validate token audience/resource for this service;
- validate expiry and required scopes;
- do not accept tokens minted for another resource;
- do not pass client bearer tokens through to downstream systems;
- bind authorization decisions to the authenticated subject and tenant;
- record authorization failures without exposing token contents.

### Transport

Public production MCP is HTTPS only. Administrative endpoints are not exposed unauthenticated.

Vintage transports such as plain FTP are permitted only inside an explicitly configured private network/trust zone and never treated as confidential or authenticated merely because they are old-machine compatible.

### Rate limits and quotas

Rate limit at several levels:

- unauthenticated/IP edge;
- authenticated identity/tenant;
- MCP method/tool name;
- bridge;
- machine/project;
- destructive/mutating operation quotas.

Vintage-machine adapters also implement pacing independent of public API rate limits.

### Concurrency and locks

Operations that mutate a CodeWarrior project or use a single-machine execution facility acquire explicit locks. A timed-out operation retains an uncertain state until the adapter re-establishes identity/status.

### Audit

Audit state-changing requests and authorization decisions with:

- request/attempt ID;
- authenticated actor/tenant;
- tool/capability;
- project/machine opaque IDs;
- outcome and policy decision;
- evidence reference;
- timestamps/trace IDs.

Do not log secrets, full source bodies by default, or credential-bearing configuration.

### Input/resource bounds

Set maximum sizes/timeouts for source scans, manifests, diagnostic output, uploads, logs, and tool results. Output must be bounded before returning it to the model.

## Knowledge-base security

Knowledge poisoning is a security and correctness concern.

Canonical public knowledge changes through reviewable Git commits/PRs. Every technical claim states provenance, applicability, and epistemic state. Automated ingestion may propose records but must not silently promote a proposal to `verified`.

Unverified external code examples are not target-programming knowledge.

## Provider-specific notes

### SSH / AppleScript / CodeWarrior

- use a dedicated low-privilege account where possible;
- pin/verify SSH host keys;
- serialize IDE operations;
- positively identify the open project/target before mutation;
- verify postconditions instead of trusting a successful AppleEvent return code.

### FTP / LaunchAPPL

The `classic-mac-hardware-mcp` prior art intentionally uses plain FTP for RumpusFTP compatibility. A ClassicMacMCP provider using the same approach must treat it as a local/private transport, pace operations, serialize LaunchAPPL per machine, and never expose raw credentials to hosted callers.

## Production checklist

Before public deployment:

- [ ] TLS and HSTS at the public edge.
- [ ] OAuth/resource-server validation tests.
- [ ] tenant-isolation tests.
- [ ] path traversal/symlink escape tests.
- [ ] secret-redaction tests.
- [ ] per-tool authorization tests.
- [ ] destructive-tool default-deny tests.
- [ ] rate-limit/abuse tests.
- [ ] audit-log review.
- [ ] dependency/SBOM/security scanning.
- [ ] backup and restore drill.
- [ ] bridge compromise/revocation procedure.
- [ ] vulnerability disclosure policy.
