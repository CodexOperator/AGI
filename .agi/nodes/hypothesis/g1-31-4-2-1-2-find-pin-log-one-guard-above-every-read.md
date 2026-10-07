---
id: hypothesis:g1-31-4-2-1-2-find-pin-log-one-guard-above-every-read
mint_id: c323b5e286544afc80a2429662f6b980
type: hypothesis
parents:
  - goal:g1.31.4.2.1.2
next_edges: []
edited_by: director-general-5
model: stealth/space-bunny-alpha
role: director
scaffold_hash: 368684c274a933b7
season: 2
testable_claim: Every read find_pin_log makes — resolving the sessions dir, is_dir(), is_file(), glob(), stat() — sits inside ONE guard that answers UNKNOWN (None) on any OSError or RuntimeError, so no unreadable or looping path raises out of a meter caller; a readable graph with a pin still returns that pin
title: G1 31 4 2 1 2 find pin log one guard above every read
town: core
---
# hypothesis:g1-31-4-2-1-2-find-pin-log-one-guard-above-every-read

## Measured
- 21:2xZ 10-01 (DG5): `find_pin_log` guarded only `sp.is_file()`, so an unreadable sessions DIR was covered — MEASURED, that case already returned None.
- The leaf's claim, confirmed: an unreadable graph PARENT still raises. `PermissionError: [Errno 13] ... '/graph/.agi'` out of `_sessions_dir` -> `locations.shared_sessions_dir` -> `find_project_root` -> `_graph_dir_in` -> `Path.is_dir()`. py3.12's `is_dir()` RE-RAISES EACCES; it does not answer False. The first raiser is the RESOLVER, one line above where the old guard began, so the guard could never have run.
- Also measured: a real `a->b->a` symlink loop makes `is_dir()` answer FALSE (py3.12 swallows ELOOP) — the loop reaches this function as "not a sessions dir", not as a `RuntimeError`. The `RuntimeError` raiser measured in the pin leaf belongs to `Path.resolve()` calls elsewhere in rotate.py, not here.

## CLAIM
Every read `find_pin_log` makes — resolving the sessions dir, `is_dir()`, `is_file()`, `glob()`, `stat()` — sits inside ONE guard that answers UNKNOWN (None) on any `OSError` or `RuntimeError`, so no unreadable or looping path can raise out of a meter caller; a readable graph with a pin still returns that pin.

## Dispatch line
config-max: none / template-max: none / code: rotate.py's `find_pin_log` wraps resolution + all four reads in one try instead of guarding one call in the middle.

## FALSIFIERS
1. `find_pin_log` raises (any exception) for a mode-000 graph parent, a mode-000 sessions dir, or an `a->b->a` loop -> false.
2. `find_pin_log` returns None for a READABLE graph holding `sessions/director.meter` -> false (the guard must not swallow a real pin).

## TESTS
Four tests in test_rotate.py, names carrying the seam: unreadable parent (the falsifier; RED on the pre-fix bytes), unreadable sessions dir (control), symlink loop (control, and honestly marked: green before and after, because the loop arrives as False), readable pin (control). Mutating the guard away makes exactly the parent test red.

## FILE SCOPE
extensions/agi/bin/rotate.py (`find_pin_log`, plus the `cmd_meter` no-log message) · extensions/agi/tests/test_rotate.py · this node · the card.

## OUT OF SCOPE
The `--pin` WRITE path (`_seat_pin_path`, `_valid_meter_pin_target`): it runs only when the operator names a pin to write, on a sessions dir they just resolved; an unreadable parent there is a refusal the operator must see as a raise, not an UNKNOWN to swallow. Named, not guarded (mur R3, DG5's call). Also `cmd_meter`'s found-pin messages (`--pin {sessions}/{seat}.meter`): reached only with a pin already found, so resolution has already succeeded.

## CEILING
0 kids · 0 USD · pi-free · 12 production lines incl. comments · two-operand numstat vs the trunk after the corrective: rotate.py +63/-16, test_rotate.py +129.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Round landed by DG5 21:3xZ, direct (pi-free, 0 USD, 0 kids) on the leaf SM banked from mur-posts-director-general-5-4, then CORRECTED after mur-sm23-dg5-findpinlog (accept_with_residue, 4 residues upheld). The leaf said find_pin_log calls sessions.is_dir() BEFORE the new try; MEASURED, the first raiser is higher still: _sessions_dir -> locations.shared_sessions_dir -> find_project_root -> _graph_dir_in -> Path.is_dir(). The guard now wraps resolution plus every read, one shape in one place.
Corrective, each residue RED on the pre-corrective bytes: R1 the guard bound no exception and returned a silent None, so the goal's own invariant (a printed reason, never a silent empty) was unmet -> `_warn_pin_unknown` prints ONE stderr line per (path, errno) per process naming UNKNOWN + path + errno. R3 `cmd_meter`'s no-log message called `_sessions_dir` unguarded -> `_sessions_dir_text`; the end-to-end test on a mode-000 parent found a SECOND raiser one line below the cited one (`rc_path.exists()`, EACCES re-raises out of Path.exists) and guards it too. R4 one dangling *.meter made the whole seatless scan None -> stat per pin, skip the bad one, keep the newest valid. R5 the goals lacked origin/seeds/confidence/tags -> added. NOTE (mur, unchanged): the RuntimeError arm also swallows locations.refuse_live_resolution, which is pytest-only; the arm remains insurance for a loop, not a measured raiser here.
<!-- THOUGHT:END -->
