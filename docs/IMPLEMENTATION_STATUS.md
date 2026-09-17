# Implementation Status

## Implemented

- hosted/local trust boundary;
- compatibility/evidence hierarchy;
- semantic CodeWarrior API model;
- provider abstraction and failure taxonomy;
- project/backend domain model;
- CodeWarrior project-engine architecture;
- private-reference corpus rules;
- source hierarchy and promotion policy in ClassicMacKB;
- initial tests for backend authority and provider result invariants.

## In progress

- strict project/machine manifest loading;
- read-only MCP tools for project/provider inspection;
- vendor-document semantic indexing;
- CodeWarrior XML importer design;
- exact CW8 SDK/API inventory.

## Deliberately not enabled yet

- public mutating hardware tools;
- arbitrary shell/AppleScript/FTP/GUI tools;
- native CodeWarrior plug-in control;
- automatic promotion of vendor/book material into canonical knowledge;
- replacing CodeWarrior authority with Retro68.

## Next acceptance gate

CI must remain green while the manifest/provider contracts are connected to the MCP read-only tool surface.