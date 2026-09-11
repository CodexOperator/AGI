---
id: experiment:a00-ca9ccc60-add747
mint_id: b1011d0e973e420498d74a748bd38fb0
type: experiment
parents:
  - hypothesis:l4-the-template-test-reads-the-live-rotations-node
next_edges: []
confidence: 0.9
edited_by: a00-876e8be8
evidence_runs:
  - experiment:a00-ca9ccc60-add747
loop: hypothesis:l4-the-template-test-reads-the-live-rotations-node@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: a26ca850df4ba1f1
season: 2
title: A00 ca9ccc60 add747
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-ca9ccc60-add747

## Experiment

g15 claim (hypothesis:l4-the-template-test-reads-the-live-rotations-node):
build, not measure — rewrote `extensions/agi/tests/test_rotate_templates.py`
(L4.179) so the startup-parse tests read `templates.*.startup.first_turn`
straight from the CHECKED-IN `.agi/nodes/.geometry/rotations.md` (BOTH roles,
director + prime_director) instead of the mirrored `FIXED_FIRST_TURN` /
`_FIXED_TEMPLATES_BODY` fixture, which could stay green while the live node
regressed (e.g. to the dead `rotate.py whois`).

Changes (tests-only; rotations.md is read, never written):
1. Dropped `FIXED_FIRST_TURN` and the dead `_FIXED_TEMPLATES_BODY`.
2. Added `_live_first_turn()` — loads the live node frontmatter templates via
   `graph_core.persistence.frontmatter`, returns every role's
   `startup.first_turn` entry list. Resolves the node at
   `<repo-root>/.agi/nodes/.geometry/rotations.md`.
3. `test_uniquely_director_first_turn_is_the_shipped_outer_shape` now guards
   the LIVE node: asserts both `director` and `prime_director` templates exist,
   `rotation-record` in director, and `seat-row` gone.
4. `test_every_first_turn_producing_verb_parses_and_no_placeholder_empty`
   iterates every role's first_turn from the live node, renders each cmd with
   fixture `STARTUP_VALUES`, asserts no used placeholder renders empty, and
   runs `<argv0> <verb> -h` for each producing python verb (exit 0). Now it
   must check >= 2 verbs (one per template), so both live templates are held.
5. Module docstring updated: the startup tests READ the live node (never write
   it); the resolution/refusal tests still use a throwaway .agi fixture root.
6. `test_falsifier_old_rotate_whois_does_not_parse` kept load-bearing.

## Evidence

As checked-in (eb03a22bc), suite passes:
`python3 -m pytest extensions/agi/tests/test_rotate_templates.py -q`
→ `8 passed in 1.38s` (re-run after edit: 1.62s).

PROOF (scratch copy of the tree, ONE template line reverted):
- Copied `extensions/` + `.agi/nodes/.geometry/rotations.md` to
  `/tmp/proof-l4191`.
- Reverted ONLY the director `rotation-record` line to
  `rotate.py whois {seat}` (prime_director left at the fixed `status`).
- Ran the scratch suite →
  `FAILED test_every_first_turn_producing_verb_parses_and_no_placeholder_empty`
  `AssertionError: director/rotation-record verb 'whois' does not parse:`
  `rotate.py: error: argument cmd: invalid choice: 'whois' (choose from
  'meter','spawn','loop','ack','status',...)`
  `assert 2 == 0`
  `1 failed, 7 passed`.

So a dead command in the LIVE node now fails the suite (it used to stay green
via the mirror). FALSIFIER (green on a non-verb) is shown NOT to hold: a live
node naming `whois` trips the parse assertion.

Verified every producing verb in both live templates parses on this tree:
`rotate.py status`→0, `send.py whois`→0, `send.py read`→0,
`spawn_budget.py status`→0, `provisioning.py status`→0, `commands.py run`→0.
The prime template's `account` cmd is `curl` (not a python producer) and
`write-verbs` is `-h` help-only — both correctly skipped by
`_producing_python_verb`.

Scratch dir removed after the proof.

## Agent Notes
Rewrote test_rotate_templates.py startup-parse tests to read templates.*.startup.first_turn from the LIVE .agi/nodes/.geometry/rotations.md (both roles); dropped the mirrored FIXED_FIRST_TURN/_FIXED_TEMPLATES_BODY. Suite 8 passed on checked-in tree; scratch copy with one director line reverted to rotate.py whois fails (assert 2==0), so a dead live command now fails the suite.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-876e8be8, L4.191). (1) THE INSTRUCTION SAID (target testable_claim): "the test loads templates.*.startup.first_turn from the checked-in .agi/nodes/.geometry/rotations.md (BOTH templates) ... the dead _FIXED_TEMPLATES_BODY / FIXED_FIRST_TURN fixture is dropped. PROOF: on a scratch COPY of the tree with one template line reverted to `rotate.py whois`, the test FAILS; on the tree as checked in it passes." (2) WHAT THE MACHINE DOES: `_live_first_turn()` (extensions/agi/tests/test_rotate_templates.py:181-203) loads the live node with graph_core.persistence.frontmatter.load_node_file at parents[3]/.agi/nodes/.geometry/rotations.md and returns every role with a non-empty startup.first_turn; both startup tests read it (lines 226-290) and the parse test asserts set(first_turn) >= {director, prime_director}. `grep FIXED_FIRST_TURN` finds the names only in two comments — the fixture is gone. RAN: `python3 -m pytest extensions/agi/tests/test_rotate_templates.py -q` on this checkout → 8 passed in 1.75s. REPRODUCED THE FALSIFIER INDEPENDENTLY: copied extensions/ + .agi/nodes/.geometry/rotations.md to /tmp/proof-l4191-parent, reverted exactly the first director rotation-record line to `rotate.py whois`, ran the same suite → 1 failed, 7 passed, the failure being the parse assertion (rotate.py: invalid choice: whois, exit 2). So the live node now genuinely drives the test: a dead command in the shipped templates fails the suite, which the mirrored fixture could not do. (3) NEAR MISS: keeping FIXED_FIRST_TURN as a "canonical outer shape" and adding a live-load assertion only in the new parse test — that satisfies the words and loses the mechanism, because a regression to `rotate.py whois` in the live node still passes the mirrored outer-shape guard and the parse test would then be the only detector while a second mirrored copy silently drifts. This version drops both fixture constants entirely, so there is one source of truth. (4) DEVIATION: none; tests-only, rotations.md read and never written, scope matches the claim.
<!-- THOUGHT:END -->

REVIEWED by parent a00-876e8be8 (L4.191): accepted proved. Independent re-run: 8 passed on checkout; scratch copy with one director first_turn line reverted to rotate.py whois fails the parse assertion (1 failed, 7 passed). FIXED_FIRST_TURN/_FIXED_TEMPLATES_BODY dropped (comments only). parents resolves; evidence_runs is a real node id.
