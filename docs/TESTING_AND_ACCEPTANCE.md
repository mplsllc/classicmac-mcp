# Testing and Acceptance

ClassicMacMCP treats tests as evidence gates, not just implementation checks. A passing host-side test does not establish target behavior.

## Test classes

### 1. Schema/unit tests

Run on modern CI hosts and verify:

- manifest/schema validation;
- applicability filtering;
- knowledge provenance integrity;
- deterministic compatibility scanner behavior;
- provider result-envelope parsing;
- security defaults.

### 2. Negative-control tests

Every compatibility gate that can fail should include a deliberate known-bad input. This protects against false-green gates caused by warning suppression, compiler mode, missing test execution, or accidental fallback.

The MacSurf C89 gate history is the reference lesson: a host check initially appeared to pass because warnings were suppressed; a deliberate invalid construct exposed that the gate itself was ineffective.

### 3. Retro68 compatibility tests

Retro68 provides fast target-aware validation but is not the authoritative CodeWarrior compiler.

Maintain a compiler-difference suite covering at least:

```text
compat/cw8/
  language/
  headers/
  preprocessor/
  abi/
  linker/
  project-model/
```

When Retro68 passes code that CodeWarrior rejects, classify the difference and add a regression rule/test where practical.

### 4. CodeWarrior tests

These run against the declared authoritative IDE/toolchain and verify:

- exact project identity;
- compile/update/build behavior;
- diagnostics retrieval;
- project membership/access-path behavior;
- artifact identity;
- known automation success/failure modes.

A no-error AppleEvent result is insufficient. The expected state change must be observed.

### 5. Hardware/runtime tests

These establish behavior that depends on the actual Classic Mac environment. Preserve:

- source/artifact identity;
- machine identity;
- OS/toolchain identity;
- test steps;
- logs/diagnostics;
- pass/fail observation.

Hardware success does not automatically generalize to other machine/OS/toolchain combinations.

## Reference fixture

Create a small `classicmac-mcp-fixture` project before broad mutating provider work. It should contain:

- several C89 source files;
- a resource file;
- one user/system access-path dependency;
- a known clean build;
- a deliberate compiler error mode;
- a deliberate linker/project-membership failure mode;
- a small visible/runtime assertion;
- deterministic build marker/version output.

The fixture is safer than using MacSurf as the first test target for every new MCP capability.

## Build acceptance contract

A successful CodeWarrior build operation requires all applicable conditions:

1. correct machine/IDE/project/target identity;
2. intended source transfer verified;
3. CodeWarrior operation completed or was reconciled after timeout;
4. build diagnostics satisfy project policy;
5. expected output artifact exists;
6. artifact identity changed when inputs required a rebuild;
7. result/evidence is attached to the attempt.

Launching or packaging a stale binary is a build failure even if CodeWarrior returned no error.

## Mutation acceptance

For project mutation such as add/remove file:

1. capture pre-state;
2. perform one mutation;
3. query post-state through an independent/read path where possible;
4. compare expected effect;
5. retain evidence;
6. rollback/stop if postcondition is ambiguous.

The historical CW8 Add Files AppleEvent demonstrates why return-code-only acceptance is unsafe.

## Timeouts

A timeout is an `unknown_state` until reconciled. Required flow:

```text
operation sent
   |
 timeout
   |
 query IDE/process/project/artifact state
   |
 +---------+-----------+
 |         |           |
completed  active      failed/unchanged
 |         |           |
accept     wait        safe recovery decision
```

Never blindly replay a state-changing operation after timeout.

## CI vs hardware gates

Public CI should remain reproducible without private repositories or machines. Private/server CI may add owner-only corpora and hardware/provider integration suites.

Public green CI means the public software/KB is internally valid. It does **not** imply a CodeWarrior or hardware verification level.

## Promotion tests

A knowledge claim being promoted to canonical status should fail review if:

- cited evidence cannot be resolved;
- applicability is broader than the evidence;
- a contradiction is hidden rather than linked;
- validation level is stronger than the recorded experiment;
- the record silently depends on modern C/POSIX behavior not established for the target.
