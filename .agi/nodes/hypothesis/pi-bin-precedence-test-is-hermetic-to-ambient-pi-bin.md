---
id: hypothesis:pi-bin-precedence-test-is-hermetic-to-ambient-pi-bin
mint_id: c6a25cd3890349a99dd0456a6f4bcc45
type: hypothesis
parents:
  - hypothesis:core-sync-0923-residues
next_edges: []
confidence: 0.9
edited_by: director-engine
scaffold_hash: 00f6af7b57cbbd8c
season: 2
testable_claim: "test_adapters.py::test_pi_bin_env_var_wins_over_config (test_adapters.py:165-169) is hermetic to the ambient environment: it clears PI_BIN (monkeypatch.delenv, raising=False) before asserting the config value, so it passes both with PI_BIN exported (as this box's profile and tmux -g do) and with it unset, while pi_adapter.resolve_bin (bin/adapters/pi_adapter.py:40, env over config) stays byte-unchanged; proved by running the test under PI_BIN=/x and under env -u PI_BIN (both pass) with test_adapters.py green."
title: "test_adapters: the PI_BIN precedence test is hermetic to an ambient PI_BIN (0923 R4; assigned: director-engine)"
town: core
---
# hypothesis:pi-bin-precedence-test-is-hermetic-to-ambient-pi-bin

# hypothesis:pi-bin-precedence-test-is-hermetic-to-ambient-pi-bin

## Hypothesis

```
residue    0923 R4 of hypothesis:core-sync-0923-residues · same family as L1 (pi bin precedence)
bytes      test_adapters.py:165-169 asserts resolve_bin({"bin": "/from/config"}) == "/from/config" BEFORE any PI_BIN handling
           bin/adapters/pi_adapter.py:40 resolve_bin = env PI_BIN over config -- correct, stays byte-unchanged
measured   director-engine 08:0xZ 09-23: PI_BIN exported (box profile + tmux -g) -> 1 failed · env -u PI_BIN -> 1 passed
proves     the test clears PI_BIN (monkeypatch.delenv, raising=False) before the config assertion -> passes BOTH ways
           (PI_BIN=/x and env -u PI_BIN) · test_adapters.py green · no adapter byte changes
disproves  a precedence change in pi_adapter.py · a skip · a test that passes only one way
```

## Agent Notes
assigned: director-engine (0923 residues, belam 07:36Z 09-23); minted by director-engine after verifying the bytes.
