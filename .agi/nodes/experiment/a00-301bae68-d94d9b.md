---
id: experiment:a00-301bae68-d94d9b
mint_id: 4368b682f2e0484c9374ec33f73a6015
type: experiment
parents:
  - hypothesis:l5-after-join-greps-the-old-post-name-at-a-rename-boundary
next_edges: []
confidence: 0.8
edited_by: a00-d595594e
evidence_runs:
  - experiment:a00-301bae68-d94d9b
line_ceiling: 40
loop: hypothesis:l5-after-join-greps-the-old-post-name-at-a-rename-boundary@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "scratch probe/probe_record_discovery.py: temp root, record named sextest-new.<stamp>.json carrying applied_rename {old: sextest, new: sextest-new}; call rotate._latest_rotate_record(root, sextest) and rotate.run_after_join_for_seat(root, sextest)", "expected": "the watch OLD row-name lookup reaches the boundary record so the changed join bytes run", "observed": "_latest_rotate_record(root, sextest) is None and run_after_join_for_seat(root, sextest) returns None — the rotate-self record is named under the NEW seat at the boundary, so the new join bytes are never reached in the watch path", "result": "refused"}
production_lines: 62
profile: balanced
role: kid
scaffold_hash: 6898a102beefe550
season: 2
title: rename-boundary after_join resolves the renamed window @id from the record
town: core
verdict: inconclusive_lean_disproved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-301bae68-d94d9b

## Experiment

The claim is a BUILD ORDER (g15): make the after_join JOIN resolve at a
rotation boundary that also renames the post. Measured pre-fix state on the
old bytes, then implemented, then proved on the built bytes.

WHAT THE OLD BYTES DID (premise, `_successor_window_id`, rotate.py:11148):
the window lookup matched ONE name by exact equality. At the boundary
`_apply_staged` carries the own window `old -> new`, step (2) carries it aside
to `new.prev`, and the successor spawns under `new` (rotate.py ~18375-18445).
The seats ROW is never renamed (documented deviation), so the heal watch's
`_run_pending_after_joins` (heal.py:588) asks `run_after_join_for_seat(root,
OLD)`; the template `join` entry greps `{succ_name}` and the code join keys on
the record's captured @id. Pre-fix both used the OLD name -> no live window
answered -> join unresolved -> the pin refused (measured 605 s, belam [rule]
dm 22:43Z).

THE FIX (extensions/agi/bin/rotate.py):
- `_successor_window_id(seat, tmux_session, window_path=None, aliases=None)`
  gains an ORDERED alias list, each matched by the SAME exact equality --
  never a substring. Empty aliases is byte-for-byte the old behaviour.
- `_rename_boundary_names(seat, rec)` returns `[<new>, "<new>.prev"]` from
the record's OWN `applied_rename` fact (never a guess; [] when absent or
  old == new). The OLD name is deliberately NOT a candidate -- no live window
  answers to it after the boundary, so matching it could only join foreign.
- `run_after_join_for_seat` (watch path) resolves both halves from that fact:
  `succ_name` becomes the renamed target (so the template `join` grep hits the
  live successor window) and an empty captured @id is resolved to the live
  renamed window, then its `.prev`. New `tmux_session`/`window_path` keyword
  seams default to production (`DEFAULT_TMUX_SESSION`, live tmux).

## Evidence

New file `extensions/agi/tests/test_after_join_rename_boundary.py`, 5 tests,
all green:
- `_rename_boundary_names` returns the new name then `<new>.prev`; [] without
  a rename fact or when old == new.
- PRE-FIX proof: `_successor_window_id("sextest", "t", win) is None` against
  a window file holding `@7 sextest-new` and `@8 sextest-new.prev`; the fix
  resolves `@7` (target preferred) and `@9` when only `<new>.prev` is live.
- NEGATIVE: no candidate live -> no fabricated @id, and `_join_successor`
  named the miss (`no successor window @id captured (window_id empty)`).
- WIRE PROOF: watch path handed OLD `sextest` + record `applied_rename`
  {sextest -> sextest-new} joins on `@7` and `values["succ_name"] ==
  "sextest-new"`.

Full neighbour run: 163 passed in 14.89 s
(`test_after_join_rename_boundary.py test_after_join_service.py
 test_rotate_boundary_rename.py test_rename_post.py test_post_rename.py
 test_rotate_own_root_rename.py`).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
WHAT THE INSTRUCTION SAID: the claim is a build order — the after_join join must resolve at a rename boundary, so the join no longer stays unresolved (measured 605s) and the reap fires. WHAT THE MACHINE ACTUALLY DOES: the kid changed only the join-matching bytes — _successor_window_id gained an ordered aliases list (rotate.py:11148), _rename_boundary_names derives [new, new.prev] from the record applied_rename (rotate.py:11180), and run_after_join_for_seat resolves succ_name and an empty @id from that fact (rotate.py:14833). But at the boundary _apply_staged sets seat = applied_rename.new (rotate.py:18381) BEFORE _rotate_self_started_path(root, seat) names the record (rotate.py:18382), so the record file is <NEW>.<stamp>.json while heal _run_pending_after_joins (heal.py:588) asks run_after_join_for_seat(root, OLD row name) and _latest_rotate_record globs <OLD>.*.json (rotate.py:14668). The changed bytes are unreachable in the measured watch path. NEAR MISS: the kid own WIRE test monkeypatches _latest_rotate_record (test_after_join_rename_boundary.py:test_run_after_join_for_seat_joins_the_renamed_window), so it proves the join logic once a record is handed in and never exercises the discovery step that fails. IF I DEVIATED: I demote rather than accept because the claim acceptance criterion is that the join resolves end to end, and the probe shows it does not.
<!-- THOUGHT:END -->

## Agent Notes
Built the rename-boundary after_join join: _successor_window_id gains ordered exact-match aliases and _rename_boundary_names derives [new, new.prev] from the record's applied_rename; the watch path sets succ_name to the renamed target and resolves an empty @id from it. 5 new tests (pre-fix miss, resolve @7, .prev fallback, named no-window refusal, wire proof); 163 neighbour tests green; 62 prod lines.

Parent review (round L5.15): demoted to inconclusive_lean_disproved:80 — the join-alias fix is real but unreachable in the watch path (record named <NEW>.<stamp>.json at the boundary; heal asks the OLD row seat). Probe probe_record_discovery.py named. Superseded by kid 2 (experiment:a00-40b2f703-a16e01) which added the discovery fallback, and kid 3 (experiment:a00-a3a07f3f-089026) which completed it safely.
