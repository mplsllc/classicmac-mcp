# Immediate Implementation Sequence

This file captures the next concrete engineering sequence after the initial architecture/docs pass.

1. Make CI green after project/provider model additions.
2. Add strict manifest loaders for project and machine YAML.
3. Add read-only MCP tools for manifest validation and backend/provider capability explanation.
4. Add private-reference source metadata to the KB indexer.
5. Add vendor-document semantic indexing with multipart/manual hierarchy support.
6. Build a public tiny CodeWarrior fixture project and exported XML fixture.
7. Define the CodeWarrior XML importer with unknown-setting preservation.
8. Add a provider fake and orchestration tests for timeout recovery/postcondition checking.
9. Implement the first real private provider around the proven `mplsllc/workflow` contract.
10. Inventory exact CW8 plug-in SDK headers/API versions on the target environment before native plug-in implementation.

No mutating hosted tools should be enabled before items 1–8 are stable.