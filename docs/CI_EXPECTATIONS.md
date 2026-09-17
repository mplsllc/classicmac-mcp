# CI Expectations

Public CI should verify the repository without relying on private repositories, private manuals, private networks, or vintage hardware.

Required checks:

- import/package integrity;
- unit tests;
- compatibility scanner fixtures;
- project/provider model invariants;
- public KB/retrieval contract tests;
- schema/example validation;
- no secret-bearing sample configuration.

Private integration environments may add CodeWarrior, Retro68, hardware, and private-reference tests separately.
