---
id: experiment:a00-3630fb0b-7fc642
mint_id: d63c33c647c3428b8d18d172b523378d
type: experiment
parents:
  - hypothesis:l5-rotate-accepts-the-pending-successor-key-the-signer-already-prefers
next_edges: []
confidence: 0.8
edited_by: a00-f65bdee5
evidence_runs:
  - experiment:a00-3630fb0b-7fc642
line_ceiling: 8
loop: hypothesis:l5-rotate-accepts-the-pending-successor-key-the-signer-already-prefers@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 2, "class": "auth", "cmd": "PARENT probe_review.py A (re-run on kid-2 HEAD 9ebaa6aa8): real git MAIN+worktree; MAIN row pubkey=B (the held key), worktree copy pubkey=C (stale); rotate._caller_post(root=wt/.agi), no AGI_POST", "expected": "resolves: post==seat, how=='worktree', row pubkey == MAIN's B", "observed": "post=s-director how=worktree row_pub==MAIN B", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "PARENT probe_review.py C (the gap kid 2 was re-briefed for): MAIN HAS a row for the seat (pubkey=C) with NO worktree cell; the worktree copy has pubkey=B (the held key) and worktree=top", "expected": "refuse by fingerprint -- the shared root DOES have a row for the seat, so no fallback to the copy", "observed": "post=None, refusal names both fingerprints; is_worktree_held_key=False", "result": "pass"}
  - {"conjunct": 2, "class": "wire", "cmd": "PARENT probe_review.py E (re-run): cmd_rotate --post <target> with cmd_rotate_self stubbed; the target row exists ONLY in MAIN", "expected": "the changed target-lookup bytes are reached live: no 'no seat' refusal, delegated ns.name == target", "observed": "delegated ns.name=s-helper (resolved from MAIN)", "result": "pass"}
  - {"conjunct": 3, "class": "gate", "cmd": "PARENT probe_review.py B (re-run): row pubkey=B, key_history=[C]; the seat's .key file swapped to hold the retired key C", "expected": "refuse by fingerprint; key_history never authorizes", "observed": "post=None; refusal names both fingerprints", "result": "pass"}
  - {"conjunct": 4, "class": "wire", "cmd": "PARENT probe_review.py D (re-run): _seat_read_root(root, seat) and _caller_post from MAIN itself", "expected": "_seat_read_root == root; resolves how='env' (root == shared root must be a no-op)", "observed": "read_root==root True; post=seat how=env", "result": "pass"}
production_lines: 1
profile: balanced
role: kid
scaffold_hash: 92fae85c4e4c0794
season: 2
title: rotate worktree-match branch re-resolves the seat from MAIN before accepting the held key
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-3630fb0b-7fc642

BUILD (hypothesis:l4-a-g15-claim-is-a-build-order-not-a-measurement), closing
the gap the parent found in experiment:a00-2dc3ea4c-16f15a: `_caller_post`'s
WORKTREE-MATCH branch fell back TREE-level, not per-seat, so a MAIN row for the
seat whose `worktree` cell did not match the caller's toplevel let the lagging
worktree copy's stale held key authorize the rotation (parent probe C).

### Pre-fix measurement (red-first)

Two new cases in `extensions/agi/tests/test_rotate_caller_post.py`, built on the
same real git MAIN + linked worktree fixture as the existing five:

- MAIN HAS a row for the seat but its `worktree` cell is ABSENT; the worktree
  copy holds the key (B) and `worktree=top`.
- MAIN HAS a row for the seat but its `worktree` cell points ELSEWHERE; the
  copy is the only match.

BEFORE the edit both ACCEPTED: `post='s-director'`, resolved row pubkey = the
copy's held key B -- the exact acceptance conjunct (2) exists to kill.

### The fix (1 net production line, reusing `_seat_read_root`)

rotate.py `_caller_post` worktree-match branch: once the match yields the seat
NAME, re-resolve that seat from the shared tree before accepting the row:

```python
                seat = r.get("name")
                row = _find_seat(_seat_read_root(root, seat), seat) or r
```

`_seat_read_root(root, seat)` is already per-seat (shared iff shared has that
seat row, else root), so this is the claim's exact fallback: MAIN's row when
MAIN has one, the worktree copy only when MAIN has none. Iteration order stays
shared-first; `how` stays `'worktree'`.

### Post-fix measurement

Both new cases REFUSE by fingerprint against MAIN's stale pubkey. The five
existing cases are untouched and green, including the fallback case (seat
absent from MAIN still reads the copy) and the MAIN-as-root no-op.

## Evidence

Run:
`python3 -m pytest extensions/agi/tests/test_rotate_caller_post.py extensions/agi/tests/test_rotate_verb_resolvers.py extensions/agi/tests/test_rotate_identity_main.py extensions/agi/tests/test_rotate.py -q`
-> **360 passed** (73s). `test_rotate_caller_post.py` alone: 7 passed (2 new,
5 untouched); the 2 new cases failed before the edit.

LINE CEILING: **2 added, 1 deleted** (`git diff --numstat --
extensions/agi/bin/rotate.py`), net +1 production line against a ceiling of 8 --
no overage, no re-brief.

`python3 -c "import ast; ast.parse(open('extensions/agi/bin/rotate.py').read())"` ok.

## Agent Notes
Closed parent probe C: _caller_post's worktree-match branch now re-resolves the matched seat via _seat_read_root(root, seat) before accepting the row, so a MAIN row for the seat always outranks the lagging worktree copy. Red-first: 2 new cases (MAIN row w/o worktree cell; MAIN row with mismatched cell) both ACCEPTED the stale held key before the edit, both REFUSE by fingerprint after. 360 passed across test_rotate_caller_post + verb_resolvers + identity_main + test_rotate; existing 5 caller cases untouched. 2 added/1 deleted production lines vs ceiling 8.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT review of a00-3630fb0b (9ebaa6aa8): verdict proved STANDS on the parent's OWN probes, not the kid's suite. WHAT THE INSTRUCTION SAID (re-scoped l5 conjunct 2, my probe C): the worktree-match branch must fall back to root's copy ONLY when the shared root has no row for the seat. WHAT THE MACHINE ACTUALLY DOES, cited to the committed bytes: rotate.py:17715 -17716 now reads `seat = r.get("name")` then `row = _find_seat(_seat_read_root(root, seat), seat) or r`; `_seat_read_root(root, seat)` (rotate.py:17683) is per-seat, so shared's row for the matched seat always outranks the lagging copy and the copy is read only when shared has no row for that seat. My probe C, which FAILED on the previous revision, now refuses by fingerprint; probes A/B/D/E still hold on the new bytes (5/5). THE NEAR MISS: a fix that refused on ANY shared row by name-first would also pass C but would break the intended fallback when MAIN lacks the seat; the committed fix keeps shared-first worktree matching and re-resolves per-seat, so the seat-absent fallback case still reads the copy (kid's untouched test). DELIVERABLES vs the diff: rotate.py 2 added/1 deleted (numstat verified), test_rotate_caller_post.py +30 (2 new cases, both red before the edit and green after), node present. Ceiling 8 -- no overage. DEVIATION: none.
<!-- THOUGHT:END -->

Parent review: 5/5 parent probes pass on the kid-2 bytes, incl. probe C (the gap that demoted kid 1) -- the worktree-match branch now re-resolves the matched seat per-seat from MAIN and refuses the stale held key. 2 added/1 deleted production lines vs ceiling 8; both new tests red-first. proved stands.
