# CodeWarrior SDK Versioning Policy

## Problem

The available private corpus includes CodeWarrior documentation from multiple IDE/SDK revisions. The IDE 5.1 SDK API Reference is especially valuable for discovering native plug-in capabilities, but the first authoritative environment is CodeWarrior Pro 8/8.3.

## Rule

Documentation proves only documented behavior for its own identified version unless stronger evidence establishes compatibility elsewhere.

For any CodeWarrior native API, track separately:

- documented SDK version;
- exact header/library version observed locally;
- runtime API version reported by the IDE where discoverable;
- controlled behavior on the target IDE;
- final compatibility status.

## API discovery

The native SDK exposes API/IDE version discovery concepts such as `CWGetAPIVersion` and `CWGetIDEInfo`. Where these exist in the installed target, they should be used to fingerprint capability rather than assuming version compatibility from function names.

## Compatibility states

Suggested states:

- `documented_other_version`
- `present_in_target_headers`
- `runtime_discovered`
- `codewarrior_verified`
- `incompatible`
- `unknown`

## Design consequence

The semantic CodeWarrior API may advertise an operation even when a particular native plug-in implementation is unavailable. The capability resolver can choose AppleEvents or GUI automation until the native target API is independently verified.

This allows the project to learn from later SDK documentation without silently teaching an agent that later interfaces exist in CW8.