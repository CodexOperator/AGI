---
id: experiment:a00-09b58a58-5ff3a7
mint_id: c4bb3a19a67a44419009895aa04c638b
type: experiment
parents:
  - hypothesis:l4-a-rotation-costs-the-live-seats-zero-calls-and-the-successor-one
next_edges: []
confidence: 0.8
edited_by: sensei-director
evidence_runs:
  - experiment:a00-09b58a58-5ff3a7
loop: hypothesis:l4-a-rotation-costs-the-live-seats-zero-calls-and-the-successor-one@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 1dc075077e9b18d3
season: 2
title: A00 09b58a58 5ff3a7
town: core
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-09b58a58-5ff3a7

## Experiment

Extended hypothesis:l4-a-rotation-costs-the-live-seats-zero-calls-and-the-
successor-one with TWO landed changes on `extensions/agi/bin/rotate.py`:

### (1) Seam fix — cmd_ack persisted an EMPTY session_ref (mechanism-1/2 seam)

Parent review found kid 1's `cmd_ack` wrote `"session_ref": ref` — EMPTY when
the successor passed NO `--ref` — while the same call back-filled the row's
OWN session_id (`self_sid`). kid 2's `cmd_loop` (~1582) then read
`ack.get("session_ref") or ""` and composed the PRE-JOIN announce text
"successor ref not yet resolved" even though the join HAD resolved it in the
row — falsifier #1 (an alert without the address after a successful join).

FIX (red-first, small): `cmd_ack` now writes the EFFECTIVE identity,
`"session_ref": ref or self_sid`, so a no-ref ack persists the row's session_id
into the ack file and `cmd_loop`'s announce composes the real post-join
address. Updated the pinning assertion in `test_ack_no_ref_backfills_`
`session_id_from_row` (test_rotate.py:2943) from `ack["session_ref"] == ""` to
the back-filled value `== "f52a4caabbccddee"`, and reworded its docstring to
explain the ack must carry the same identity the row got (cmd_loop reads it).
Per the parent note the full 32-char session_id is acceptable (whois
prefix-matches); no truncation invented.

### (2) Mechanism 3 — rotate-self refuses-or-serves on a stale .geometry/

A rotating WORKTREE's own `.agi/nodes/.geometry/` (config:rotations +
config:seats) can be BEHIND the shared geometry branch `origin/season/s2`.
Spawning a successor there would bake a STALE rotation config into it
SILENTLY (the mechanism's falsifier). Locked it down in `cmd_rotate_self`:

- `_geometry_behind_count(root)` — `git rev-list --count HEAD..origin/season/s2
  -- .agi/nodes/.geometry/`, degrading to 0 (current) when git is absent or
the base ref doesn't exist (gitless fixtures pass through unchanged).
- `_geometry_resolution_root(root)` — picks WHICH tree's geometry to read:
  the worktree's own when current; else the integration tree
  (`locations.git_common_root`, the main checkout) when that tree's geometry
  is current and carries rotations.md; else REFUSES BY NAME with the
  behind-count and the sync command `git fetch origin && git rebase
  origin/season/s2`.
- `cmd_rotate_self` resolves `cfg_root` once, up front, and feeds it to
  `_find_seat` (config:seats) and `_resolve_template` (config:rotations); the
  geometry source is printed on the `(0) template` line.
- The rotation record (rotate-self `started` rec, `_write_rotate_self_started`)
  now carries `template_source` naming which tree the template came from.

RED-FIRST tests (test_rotate_templates.py):
- test_m3_stale_worktree_refuses_by_name_and_sync_cmd — a real git repo with
  `refs/remotes/origin/season/s2` ahead on `.geometry/` by 1 commit;
  rotate-self dry-run rc==1, stderr names "refused", the behind-count, and the
  sync command.
- test_m3_stale_worktree_serves_integration_tree_geometry — a linked
  `git worktree` forked at geometry v1 while the main tree (season/s2) moved to
  v3; rotate-self reads config from the integration tree (rc==0, `(0) template`
  names the integration tree path).
- test_m3_template_source_recorded — the record writer persists `template_source`.

## Evidence

- `python3 -m pytest extensions/agi/tests/test_rotate.py extensions/agi/tests/test_rotate_startup.py extensions/agi/tests/test_rotate_templates.py extensions/agi/tests/test_send.py -q`
  → `337 passed in 32.66s`.
- New tests: 3 passed (test_rotate_templates.py, `-k "m3 or template_source"`).
- Modified ack test passed: test_rotate.py `-k ack_no_ref` → 1 passed.

Pre-existing (NOT caused by this change, NOT in scope):
`test_rotate_handover.py::test_ack_backfills_session_ref_and_whois` fails: its
`ack --ref 7902ac` is refused (rc 2, "does not agree ... code 3") by the r3+
ref-agreement check in `cmd_ack` that runs BEFORE the (unchanged-by-me) ack
dict, so a `--ref` that isn't a session_id prefix can no longer back-fill. The
refusal fires before my edited line, so this is a stale handover test vs the
r3+ agreement rule — a seam for a later round to reconcile.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
the parent reviewed kid 3. WHAT THE INSTRUCTION SAID (parent brief): fix the seam between kid 1 and kid 2 — cmd_ack must persist the effective identity so cmd_loop post-join announce does not compose the pre-join sentence on the zero-call path — and build mechanism 3 (rotate-self reads config:rotations/config:seats at the integration tree when the worktree is behind on .agi/nodes/.geometry/, or refuses by name with the behind-count and the sync command; the record names template_source). WHAT THE MACHINE DOES (read from the diff): cmd_ack now writes session_ref as ref or self_sid; _geometry_behind_count shells git rev-list --count HEAD..origin/season/s2 -- .agi/nodes/.geometry/ and returns 0 on any failure; _geometry_resolution_root returns the worktree root when current, the integration tree (locations.git_common_root + /.agi) when that is current and carries the rotations node, else None + the refusal string; cmd_rotate_self resolves cfg_root up front and feeds it to _find_seat and _resolve_template, and _write_rotate_self_started carries template_source. THE NEAR MISS: a guard that reads git status instead of the geometry SUBTREE behind-count would satisfy the words and miss the mechanism (a worktree can be far behind on code while its .geometry/ is current, and vice versa); the pathspec form is used, so it is not missed. SECOND NEAR MISS, and it was REAL: kid 1 refusal check broke the pre-existing test_rotate_handover.py::test_ack_backfills_session_ref_and_whois, tagged by this kid as out of scope. The parent repaired the FIXTURE, not the rule — the round ref 7902ac resolved to no row under the new agreement rule, so the fixture now uses abcdef (a 6-hex prefix of the row session_id) which exercises the same back-fill and the same whois-by-exact-ref and whois-by-prefix assertions; handover 23 passed. THE THIRD NEAR MISS, recorded and NOT fixed: _geometry_behind_count fails OPEN (0) on any git error, so a genuinely broken git also reads as current. Kept, because a gitless fixture must pass through and the guard is an anti-drift aid rather than the last line of defence.
<!-- THOUGHT:END -->

## Agent Notes
Seam fix (ack carries effective identity ref or self_sid; cmd_loop post-join announce no longer lies) + mechanism-3 geometry guard (rotate-self refuses by-name with behind-count+sync cmd on a stale .geometry/, or serves the integration tree via git_common_root; record names template_source). 337 rotate/startup/templates/send tests green; 3 new red-first m3 tests pass.

DEVIATION (director sensei-director L2, 7cab79ca0 + 9460b63ea): the seam fix (ack carries ref or self_sid) was REVERTED — the session uuid is not an address; and GEOMETRY_SYNC_CMD says merge, never rebase; the m3 serve path is shadowed live by _prepare_checks (test rewritten to the live precedence). The body above describes the kid's bytes, not the landed ones.
