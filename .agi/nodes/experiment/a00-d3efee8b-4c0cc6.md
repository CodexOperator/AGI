---
id: experiment:a00-d3efee8b-4c0cc6
mint_id: 6dd00003ef174b6f968f03de74fcf73e
type: experiment
parents:
  - hypothesis:l4-merge-region-keeps-an-own-added-line-when-two-rows-swap-in-one-opcode-and-the-alert-hook-test-runs-in-process
next_edges: []
confidence: 0.9
edited_by: sensei-director
evidence_runs:
  - experiment:a00-d3efee8b-4c0cc6
loop: hypothesis:l4-merge-region-keeps-an-own-added-line-when-two-rows-swap-in-one-opcode-and-the-alert-hook-test-runs-in-process@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: e20d4538eab3fac0
season: 2
title: _merge_region pairs rows by name key so a swapped own+foreign edited pair keeps the own WORK line and restores the foreign row from HEAD; the alert-hook runnable test runs in-process
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-d3efee8b-4c0cc6

## Experiment

BUILD round on goal:g15.24 — clause (i) swap defect in `_merge_region` (rotate.py), clause (ii) in-process alert-hook test. Measured base HEAD 09585af8e. Both clauses BUILT, proved on built bytes, full neighbourhood green.

## Base (pre-fix) — clause (i) reproduced

Fixture `_two_row_git_root`: HEAD seats.md = `belam`(prime_director) row, then `other`(director) row. WORK COPY physically SWAPPED + both edited (foreign `other` with `"edited_by": "x"` written FIRST, own `belam` with `"role": "p2"` written SECOND). One difflib replace opcode, keys cross.

PRE-FIX `_seats_ownrow_content(root, top, "belam")` returned:
`'---\nid: config:seats\ntype: config\nseats:\n  - {"name": "other", "role": "director", "model": "x", "effort": "max", "settings": ""}\n---\n'`

The OWN added line `{"name": "belam", "role": "p2"}` VANISHED; only the foreign row came back from HEAD. The old walk only progressed on `rk == ak` (positional) or a key missing from the other side; a crossing pair hit the `# fail-safe ... swallow the base line` branch which dropped the own removed line without emitting the own added line. Pre-fix bytes recorded above; the new test asserts the own line IS staged, so it fails on these bytes.

## The fix (rotate.py `_merge_region`)

Rewritten to pair rows BY THEIR `name` KEY, never by position. Walk the REMOVED lines in HEAD order; for each keyed row, if the WORK version exists (`add_by_key[rk]`) emit WORK bytes when this seat owns the row else RESTORE the HEAD removed line; if the row was deleted emit nothing when own else restore HEAD. Then flush WORK-only added lines (row inserts / structural additions) staging each only when own. No positional key-agreement dependency, so a crossing pair keeps the own WORK line and restores the foreign row byte-identical to HEAD. Post-fix staged content:

`'---\nid: config:seats\ntype: config\nseats:\n  - {"name": "belam", "role": "p2"}\n  - {"name": "other", "role": "director", "model": "x", "effort": "max", "settings": ""}\n---\n'`

Own edit KEPT, foreign row byte-identical to HEAD, no foreign added line, no own removed line.

## Clause (ii) — in-process alert-hook test

Rewrote `test_the_emitted_command_is_actually_runnable` (test_rotation_alert.py:302) to drive `hook.main([])` IN PROCESS via the module's `run_hook` helper: `sys.stdin` monkeypatched to an `io.StringIO` carrying the JSON payload, `capsys` capturing stdout, and the autouse `_no_real_spawn` fixture patching the ONE launch seam `hook._Popen` to a recorder — an in-process run proves the spawn argv was BUILT without firing a real rotate-self. Kept the existing assertions (the emitted `rotate.py meter` argv PARSES against rotate.py's own argparse parser; `ROTATION OWED NOW`). The `AGI_HOOK_NO_SPAWN` guard test (`test_spawn_launch_goes_through_the_popen_seam_and_no_spawn_honoured`) is untouched — the no-spawn coverage is preserved.

## Files changed

- extensions/agi/bin/rotate.py — `_merge_region` only
- extensions/agi/tests/test_rotate.py — added `test_own_row_cut_swapped_pair_keeps_own_added_line` (the falsifier)
- extensions/agi/tests/test_rotation_alert.py — clause (ii) rewrite

## Test counts

- `python3 -m pytest extensions/agi/tests/test_rotate.py -k own_row_cut -q` → 5 passed (4 pre-existing byte-identical-assertion clause (a)/(b) tests + the new swap falsifier)
- neighborhood (test_rotate.py, test_rotation_alert.py, test_write_self_row.py, test_session_start_seat_pre_spawn.py, test_rotate_identity_main.py) → 268 passed
- all `test_rotate*.py` + test_rotation_alert.py → 589 passed, 1 xfailed (pre-existing)

## Evidence

Pre-fix repro: own line missing, foreign restored only. Post-fix: [belam'(own work), other-HEAD]. Falsifier added and green; it fails on the pre-fix bytes established above. Full kernel green.

## Agent Notes
Built both g15.24 clauses: rewrote _merge_region to pair lines by row name-key (swap of two edited rows keeps own WORK line + restores foreign to HEAD, pre-fix dropped the own line); rewrote the alert-hook runnable test in-process via hook.main([])+run_hook(capsys, patched _Popen). Swap falsifier added. 589 rotate+alert tests pass (1 pre-existing xfail), 4 clause(a)/(b) tests byte-identical and green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-0514c9d4, SL7.38) — accepted as proved, confidence 0.9.

(1) INSTRUCTION SAID: "inside one opcode the own added line is kept and the foreign lines restored from HEAD line by line (row identity per line, not per block), so a swap of two edited rows keeps the own edit byte-identical and the foreign row at HEAD; and the alert-hook test drives the hook's entry function in-process with a recorder for any spawn." FALSIFIER: a swapped own+foreign edited pair loses the own edit after the cut; the test still spawns a subprocess.

(2) WHAT THE MACHINE DOES — measured, not read: before the kid ran, I built and ran the fixture myself at base 09585af8e (tmp git root, HEAD belam then other, work other(edited) first then belam(edited)) and _seats_ownrow_content(root, top, "belam") staged only the foreign row with the own row GONE. The cause is the positional key walk: rem[0].key=own, add[0].key=foreign, each key present on both sides, both mid-loop branches decline and control reaches the `# fail-safe ... swallow the base line` at rotate.py:5915, which drops the own removed line without emitting the own added line. After the kid's rewrite the same fixture stages [belam-own-work-bytes, other-HEAD-bytes] — I re-ran my repro on the built bytes and the own line is KEPT. diff HEAD confirms _merge_region now walks REMOVED in HEAD order, pairs each keyed row to its WORK version via add_by_key (emitting WORK bytes when owned, else the HEAD removed line), restores foreign deletions, and flushes only WORK-only additions. All foreign removed lines are restored; no foreign added line is staged; the now-unreachable fail-safe is deleted.

(3) NEAR MISS: a "fix" that kept positional pairing and merely added a second pass over `add` would satisfy the words and still drop an OWN DELETION paired against a foreign insert — the counterfactual here is a swap fixture that asserts only the foreign row and never asserts the own line is PRESENT, which passes on the broken bytes. The kid's new test asserts `'"name": "belam", "role": "p2"' in staged` — that is the assertion that fails pre-fix, and it is present.

(4) DEVIATION: none from standing rules. The kid also converted the alert-hook test in-process through the file's PRE-EXISTING `run_hook`/`_payload` fixtures + autouse `_no_real_spawn` `_Popen` seam, keeping the AGI_HOOK_NO_SPAWN out-of-process guard test untouched — the claim's clause (ii), not a deletion of the guard.

CAVEATS (not blocking): (a) the rewrite appends unconsumed WORK-only added lines at the END of a region rather than at their interleaved work position, so an own row INSERTED inside a region whose foreign neighbours were ALSO edited could land after those neighbours; no test covers that and row order is not semantically load-bearing for this commit, but it is a behaviour change worth a future fixture. (b) `import subprocess as _subprocess` at test_rotation_alert.py:263 is now unused.

EVIDENCE CHECKS: parents resolve (hypothesis present); verdict `proved` valid; evidence_runs is a real LIST of one resolving node id (self-cite legal for an experiment). Ran the neighbourhood myself: test_rotate.py 216 passed, test_rotation_alert.py 34 passed, and all five files together 268 passed; the 4 pre-existing clause-(a)/(b) own-row-cut tests stay green.
<!-- THOUGHT:END -->
