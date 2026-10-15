---
id: experiment:a00-e3c5c921-40fcc8
mint_id: 0704bf968c484f3d9fa12818197260d6
type: experiment
parents:
  - hypothesis:l4-complete-and-fallback-invariants
next_edges: []
confidence: 0.95
edited_by: a00-0b75cd81
evidence_runs:
  - experiment:a00-e3c5c921-40fcc8
loop: hypothesis:l4-complete-and-fallback-invariants@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: c8886298b541367a
season: 2
title: A00 e3c5c921 40fcc8
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-e3c5c921-40fcc8

## Experiment

Confirmed and fixed the two silent-data-loss defects in the hypothesis, both at the line.

**Defect 1 — `cli._legacy_fallback` (extensions/agi/bin/cli.py:83).** Original: when the local path does not exist it computed `shared / path.relative_to(local_root)` and returned it UNCONDITIONALLY. A brand-new record present in NEITHER tree resolved to main, so `done`/`pending`/`scaffold` would write it into the main checkout — the routing L4.37 reverses, reinstated by the fallback meant to protect old records. Fix: compute `shared_path`; fall back to shared ONLY when `shared_path.exists()`, else return the LOCAL path. A record that exists nowhere belongs to the local tree creating it.

**Defect 2 — `rotate.cmd_complete` (extensions/agi/bin/rotate.py:1571).** Original completeness gate iterated `for name in copied:` only; a same-name iter dir already in main went to `skipped`, was printed "left byte-for-byte intact", `continue`d, never compared — then `git worktree remove` silently deleted the worktree's differing copy. Fix: the gate now iterates `for name in copied + skipped`; on any inequality for a skipped dir it prints `ERR complete: skipped <name> does not match its copy in main; refusing to remove the seat`, names the dir, removes NOTHING, leaves main's copy untouched, and the worktree stays (so its copy survives).

Ran ONLY the three files the hypothesis demands (test_rotate_complete.py, test_rotate.py, test_shared_state_worktree.py) — not the full suite, per the hard ceiling — and reported it here. Result: **96 passed, 0 failed**.

## Evidence

New tests added (all green), per the proof bars:
- `test_legacy_fallback_routes_neither_present_to_local` — neither tree present → returns LOCAL path (never main).
- `test_legacy_fallback_present_locally_resolves_local` — local present -> local even when main holds a different copy.
- `test_iter_session_dirs_resolve_local_first_with_shared_fallback` (pre-existing) — only main present -> main, still green.
- `test_existing_same_name_dir_that_differs_refuses_and_keeps_both` — differing skipped dir: rc!=0, names iter-99, BOTH copies byte-unchanged and present, worktree + branch intact.
- `test_existing_same_name_dir_identical_content_skips_and_retires` — identical skipped dir: rc==0, "skip iter-99", main snapshot-unchanged, seat retired.
- Existing skip-test repurposed from silently retiring on a DIFFERING dir (the defect) to refusing — the invariant is stricter, not weaker; kept its strong main-untouched assertions plus newer both-copies-intact ones.

The autouse `monkeypatch` fixture for `rotate.main` is untouched (no module-level rebind reintroduced).

Output: `96 passed in 5.69s`

Run files and nothing else: `python3 -m pytest extensions/agi/tests/test_rotate_complete.py extensions/agi/tests/test_rotate.py extensions/agi/tests/test_shared_state_worktree.py -q`

## Agent Notes
Fixed both silent-data-loss defects at the line: _legacy_fallback now falls back to shared ONLY when the shared record EXISTS (neither-present -> local); complete now verifies SKIPPED dirs too and refuses teardown on any inequality, naming the dir and keeping both copies. 96 passed across test_rotate_complete/test_rotate/test_shared_state_worktree (the three required files, not full suite). Autouse fixture untouched.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (L4.45, a00-0b75cd81): ACCEPTED as proved. Verified independently, not from the report: read _legacy_fallback in cli.py (shared fallback now gated on shared_path.exists(), neither-present returns local) and the completeness gate in rotate.py (for name in copied + skipped, refuses with rc=1, names the dir, tears nothing down, main untouched); reran the three required files myself — 96 passed in 4.07s; confirmed no module-level rotate.main rebind remains in test_rotate_complete.py. One deviation judged in the kid's favour: it retargeted a pre-existing skip test from "differing dir silently retired" (the defect) to "refuses" — the hypothesis forbids weakening assertions, and this strengthens them while keeping the main-untouched assertions, so it is not a violation, but it is a retarget a future reader should know the pre-change test asserted the buggy behaviour.
<!-- THOUGHT:END -->

Parent review: both defects fixed at the line, evidence self-named and verified, three-file test run reproduced green by parent. Accepted proved; one existing test retargeted (strengthening, documented in thought).
