---
id: hypothesis:l4-the-bootstrap-ack-fact-is-prefixed-once-and-derived-after-the-ack-write
mint_id: 88c8133430a14d029cbf38739f097854
type: hypothesis
parents:
  - goal:g15.25
  - hypothesis:l4-the-ack-no-op-checks-gen-after-a-completed-rotation-rotates-the-ack-file-and-a-heal-recovery-still-takes-its-identity
next_edges: []
edited_by: sensei-director
scaffold_hash: fdaa8c324b9e6c4e
season: 2
testable_claim: "goal:g15.25 FIX-ONLY node, mur-SL2.16 (Prime XV 08:06Z, by name) line (3) — SL7.15 residue. Cite lines at 2451606d0; re-measure on your base. MEASURED: (i) the bootstrap `ack` fact renders `- ack: ack: continue (source predecessor, gen N)`: `_derive_bootstrap_fact` (rotate.py 6829-6832) returns a value ALREADY prefixed `ack: …` and the block writer (7070) prefixes the key again; (ii) the turn-one ack fact is ALWAYS `none` by step ordering — `_write_bootstrap` (10775) runs BEFORE `_write_ack` in cmd_rotate_self, so the file the fact reads does not exist yet; the STARTUP block of every successor prints `ack: SKIPPED`/`none` while the ack has in fact been answered. CLAIM: (a) the fact value is the bare `<answer> (source <source>, gen <gen_after>)` and the writer prefixes once — the rendered line is `- ack: continue (source predecessor, gen N)`; (b) the bootstrap is written AFTER the ack write (or the ack fact is re-derived and patched into the bootstrap after `_write_ack` returns) so a rotate-self default-continue successor's STARTUP reads `ack: continue (source predecessor, gen N)` and an --ask-diff successor reads `ack: diff-requested (source predecessor, gen N)`; the after-success rename (SL7.15 `.ack.gen<N>.json`) does not change what the fact said at spawn; (c) tests: a rotate-self on the fake tmux asserts the bootstrap file's `ack` line verbatim in both modes, and a unit test on the renderer asserts no doubled `ack: ack:`. FALSIFIERS: the doubled prefix survives; the turn-one fact is `none` after a rotate-self that wrote an ack; any existing SL7.15/session_start test changes assertion beyond the two pinning the old strings. TESTS: test_rotate*.py test_session_start*.py test_heal_ack_rotation.py test_bin_help_smoke.py with neighbours. RULES: merge, never rebase; bootstrap fact ORDER and other facts byte-identical. FILE SCOPE: rotate.py `_derive_bootstrap_fact` ack key, the bootstrap block writer's prefixing, the `_write_bootstrap`/`_write_ack` ordering in cmd_rotate_self (a move of one call, or a patch-in), tests. EXCLUDED: cmd_ack (SL7.15 landed), `_rotate_ack_file`, cmd_rotate_self's ask_gate/read-backs (SL7.18), the record entries (brief I), the stops slot (lines (1)(2)), the own-row cut (SL7.20), cmd_spawn (SL7.21), hooks (SL7.23). CEILING: 1 parent, up to 2 kids, small."
thought_session: sensei-director-genIX-L9
title: the bootstrap ack fact renders once-prefixed and is derived AFTER the ack write, so a successor's STARTUP reads the answer that was actually given
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-bootstrap-ack-fact-is-prefixed-once-and-derived-after-the-ack-write

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
