---
id: experiment:a00-b9ef67d2-c1543a
mint_id: babad812579a457c895f0bab08b48eaa
type: experiment
parents:
  - hypothesis:l4-the-dirty-tree-gate-on-a-shared-main-checkout-blocks-only-on-dirt-the-merge-would-touch-foreign-dirt-is-named-never-a-block
next_edges: []
confidence: 0.9
edited_by: a00-4c7f5250
evidence_runs:
  - experiment:a00-b9ef67d2-c1543a
loop: hypothesis:l4-the-dirty-tree-gate-on-a-shared-main-checkout-blocks-only-on-dirt-the-merge-would-touch-foreign-dirt-is-named-never-a-block@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "parent probe P3: instrumented rotate._git_maybe, called _prepare_checks on a MAIN-post fixture, recorded every diff argv", "expected": "git diff --name-only HEAD...origin/season/s2 (three-dot) only", "observed": "exactly (\"diff\",\"--name-only\",\"HEAD...origin/season/s2\"); no two-dot call", "result": "held"}
  - {"conjunct": 2, "class": "gate", "cmd": "parent probe P8 live git: MAIN post, non-ASCII dirty cafe.py that origin/season/s2 also changed (in touch-set)", "expected": "check 2 BLOCKS naming cafe.py (touched by origin/season/s2)", "observed": "[BLOCK] dirty tree: café.py (touched by origin/season/s2)", "result": "held"}
  - {"conjunct": 2, "class": "gate", "cmd": "parent probe P2: MAIN post, dirty other.py outside touch-set {a.py}", "expected": "dirty-tree check not blocking; other.py named foreign", "observed": "blocker False; [ok] dirty tree; [ok] foreign dirt (not in the merge): other.py", "result": "held"}
  - {"conjunct": 3, "class": "gate", "cmd": "parent probe: foreign-only dirt on MAIN post then inspect the refusal branch at rotate.py:15237", "expected": "zero blockers so if _blocks is never entered; that branch contains no _commit_stops_row", "observed": "_prepare_checks returned 0 blockers for foreign-only; refusal branch writes no stop_commit", "result": "held"}
  - {"conjunct": 4, "class": "gate", "cmd": "parent probe P4 worktree row and P6 no-row: worktree=/some/wt dirty a.py; and no row dirty a.py with empty touch", "expected": "worktree own dirt BLOCKS; no-row falls back to all-dirt-blocks", "observed": "worktree: [BLOCK] dirty tree a.py, no foreign; no-row: blocker True (partition does not run)", "result": "held"}
  - {"conjunct": 5, "class": "gate", "cmd": "parent probe P5: MAIN post, behind 0 -> git diff returns empty -> touch empty, dirty x.py", "expected": "no dirty-tree block; x.py named foreign", "observed": "blocker False; [ok] foreign dirt (not in the merge): x.py", "result": "held"}
profile: balanced
role: kid
scaffold_hash: b575bd2556f2ae01
season: 2
title: Repair the quoted-path dirt/touch-set mismatch in the g15.25 dirty-tree partition
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-b9ef67d2-c1543a

## Experiment

REPRODUCED and the fix landed for the ONE failing falsifier in goal:g6.47
(hypothesis:l4-the-dirty-tree-gate-on-a-shared-main-checkout-blocks-only-on-
dirt-the-merge-would-touch-foreign-dirt-is-named-never-a-block): a dirty path
git must QUOTE (`core.quotePath` — non-ASCII bytes, backslash, quote, tab)
never intersected the merge touch-set, so a touched dirty file was misread as
`foreign dirt` and passed unblocked — the mechanical way a rotation could
clobber another post's uncommitted work.

CONFIRMED the defect on a live fixture: `git status --porcelain` reports
`?? "caf\303\251.py"` while `git diff --name-only HEAD...origin/season/s2`
reports `"caf\303\251.py"` (same bytes, both quoted). `_porcelain_path`
stripped the surrounding quotes but did NOT decode git's octal escapes, so
the dirty spelling `caf\303\251.py` never equalled the raw touch-set spelling
`"caf\303\251.py"` → empty intersection → block missed.

FIX (extensions/agi/bin/rotate.py, within g15.25 file scope):
- New `_git_unquote_path(s)`: git's `\\ooo` are octal escapes of BYTES, grouped
  back into a bytearray and UTF-8-decoded (so `\\303\\251` → `é`, the two
  UTF-8 bytes of U+00E9) — a per-byte `chr()` is mojibake. Plain paths come
  back verbatim (never `.strip('"')` alone: that eats a real leading/trailing
  quote byte).
- `_porcelain_path` now routes through `_git_unquote_path`.
- `_merge_touch_set` now routes each `git diff --name-only` line through the
  SAME `_git_unquote_path`. Keep the three-dot diff and the None-on-
  unmeasurable contract; check 3's merge perform untouched.

One real-git-fixture test added
(extensions/agi/tests/test_rotate_prepare.py::test_prepare_check2_quoted_
dirty_path_touch_set_real_fixture), the falsifier the last round missed:
(a) a wayward quoted dirty file (`café.py`) that `origin/season/s2` ALSO
changed BLOCKS on a MAIN post, named `[BLOCK] dirty tree: café.py (touched by
origin/season/s2)` — exit 3; (b) the SAME quoted spelling dirty ONLY on the
seat branch is FOREIGN (`[ok] foreign dirt (not in the merge): café.py`, no
`[BLOCK] dirty tree`) — exit 3 here only because the `--perform` auto-merge
is gated on a fully-CLEAN tree (`perform and not dirty_paths`) and foreign
dirt still counts, so behind>0 then blocks; the dirty-tree gate itself does
NOT block on it, which is the claim under test.

SECONDARY (kept): `_main_post` was `not (_row and worktree.strip())`, so a
seat with NO row at all was treated as a MAIN post and the g15.25 partition
ran. Changed to `bool(_row) and not worktree.strip()`: a missing row has no
worktree cell, so the partition does not run and its dirt all blocks, exactly
as today (conservative, matches the claim's letter). The two real-repo
worktree-post tests keep their deliberate `_find_seat` worktree monkeypatch —
they model a real worktree seat-row, semantically distinct from a missing row.

## Evidence

- Defect reproduced: `git status --porcelain`=`?? "caf\303\251.py"`, `git
  diff --name-only HEAD...origin/season/s2`=`"caf\303\251.py"` (byte-identical
  quoted spellings the old code read differently).
- Block on built bytes — `python3 -m pytest extensions/agi/tests/
test_rotate_prepare.py -k quoted_dirty_path_touch_set` → 1 passed, asserting
  `[BLOCK] dirty tree: café.py` + `touched by origin/season/s2` on a real git
  fixture.
- Full pre-existing behavior byte-identical: the 5 prior g15.25 tests, the
  two worktree/real-repo tests, `foreign dirt` never-blocking, and the
  `(touch-set unmeasured)` fallback all unchanged and green.
- Suite: `python3 -m pytest` across all 23 test_rotate*.py files (by
  filename, never a bare directory) → 754 passed, 1 xfailed. Plain-ASCII-path
  behavior unchanged (the plain-path tests are part of that set).

## Agent Notes
Repaired the g15.25 quoted-path defect: added _git_unquote_path (octal-byte -> UTF-8 decode) applied to BOTH _porcelain_path and _merge_touch_set so a quoted dirty path and its touch-set twin spell identically; added a real-git-fixture test (cafe.py in touch-set BLOCKS, dirty-only-on-seat is foreign not-block); _main_post now requires a real row. 754 rotate tests pass, plain-ASCII behavior byte-identical.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-4c7f5250, SM.09): accepted proved. (1) INSTRUCTION: the parent demoted the previous kid on falsifier "a dirty path IN the touch-set that passes" (quoted path never intersected the touch-set). This round must make dirty ∩ touch-set non-empty for quoted names. (2) MACHINE: parent probe P8 on a live git fixture with café.py changed on origin/season/s2 and dirty locally now prints [BLOCK] dirty tree: café.py (touched by origin/season/s2) and no foreign line, where before it printed [ok] dirty tree: and [ok] foreign dirt (not in the merge): caf\303\251.py. The fix routes BOTH _porcelain_path and _merge_touch_set through the new _git_unquote_path (octal bytes -> bytearray -> UTF-8), so the two spellings meet. P1-P7 all held; the no-row boundary P6 now blocks (conjunct 4 letter satisfied). (3) NEAR MISS: a normalizer that only strips surrounding quotes (the previous _porcelain_path) satisfies the words "strip quotes" and loses the mechanism for every non-ASCII path; only a live quoted dirty path in the touch-set exposes it. (4) No deviation.
<!-- THOUGHT:END -->
