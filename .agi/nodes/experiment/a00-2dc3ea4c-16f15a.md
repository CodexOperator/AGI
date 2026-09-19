---
id: experiment:a00-2dc3ea4c-16f15a
mint_id: 2f7049b28bb0481eba14aa643587e432
type: experiment
parents:
  - hypothesis:l5-rotate-accepts-the-pending-successor-key-the-signer-already-prefers
next_edges: []
confidence: 0.6
edited_by: a00-f65bdee5
evidence_runs:
  - experiment:a00-2dc3ea4c-16f15a
line_ceiling: 8
loop: hypothesis:l5-rotate-accepts-the-pending-successor-key-the-signer-already-prefers@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 2, "class": "auth", "cmd": "PARENT probe_review.py A: real git MAIN+worktree; MAIN row pubkey=B (the held key), worktree copy pubkey=C (stale); rotate._caller_post(root=wt/.agi), no AGI_POST", "expected": "resolves: post==seat, how=='worktree', row pubkey == MAIN's B", "observed": "post=s-director how=worktree row_pub==MAIN B", "result": "pass"}
  - {"conjunct": 3, "class": "gate", "cmd": "PARENT probe_review.py B: row pubkey=B, key_history=[C]; the seat's .key file swapped to hold the retired key C", "expected": "refuse by fingerprint; key_history never authorizes", "observed": "post=None; refusal names both fingerprints", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "PARENT probe_review.py C: MAIN HAS a row for the seat (pubkey=C) but with NO worktree cell; the worktree copy has pubkey=B (the held key) and worktree=top", "expected": "refuse -- conjunct (2) falls back to root's copy ONLY when the shared root has no row for the seat, so MAIN's row is the authority", "observed": "ACCEPTED: post=s-director, resolved row pubkey == the worktree copy's held key B (is_worktree_held_key=True), how='worktree'", "result": "fail"}
  - {"conjunct": 4, "class": "wire", "cmd": "PARENT probe_review.py D: _seat_read_root(root, seat) and _caller_post from MAIN itself (root == shared root)", "expected": "_seat_read_root == root; _caller_post resolves how='env'", "observed": "read_root==root True; post=seat how=env", "result": "pass"}
  - {"conjunct": 2, "class": "wire", "cmd": "PARENT probe_review.py E: cmd_rotate --post <target> with cmd_rotate_self stubbed; the target row exists ONLY in MAIN", "expected": "the changed target-lookup bytes are reached live: no 'no seat' refusal, delegated ns.name == target", "observed": "delegated ns.name=s-helper (resolved from MAIN)", "result": "pass"}
production_lines: 14
profile: balanced
role: kid
scaffold_hash: d6008d5da8b3e7e0
season: 2
title: rotate held-key check reads the identity writer tree (MAIN) not the lagging worktree copy
town: core
verdict: inconclusive_lean_proved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-2dc3ea4c-16f15a

## Experiment

BUILD (hypothesis:l4-a-g15-claim-is-a-build-order-not-a-measurement), conjunct
(2) of the re-scoped l5 claim, on checkout a00-f65bdee5.

### Pre-fix measurement (red-first, real git MAIN + linked worktree)

Scratch probe `.agi/sessions/iter-152/a00-2dc3ea4c/probe_read_tree.py` builds
a real `git init` MAIN at `<tmp>/main` plus one linked worktree at `<tmp>/wt`
(the shape of `test_rotate_identity_main.py:_make_main_and_worktree`). The seat
`s-director` holds key B (minted into the ONE shared key dir, MAIN); an
unrelated keypair gives pub A. MAIN's `seats.md` row and the worktree COPY's row
are stamped independently, then `rotate._caller_post(root=wt/.agi)` is called
with cwd inside `wt` (no `AGI_POST`).

BEFORE the edit:
- A) MAIN row = B (held key), worktree row = A (stale): REFUSED --
  `post 's-director': held key fingerprint 7de1c4877a1f7e74 at
  .../main/.agi/sessions/seats/s-director.key does not match the committed row
  62f7eb5d8ecbdfa0 (pubkey 9e7d3541...)` -- the refusal is emitted by
  `rotate._caller_hold_key` (rotate.py:17756, the `ours != row_fp` branch) and
  the row it compares against came from `_find_seat(root, seat)` /
  `_load_seats(root)` with `root = the worktree`, i.e. the lagging copy.
- B) MAIN row = A (stale), worktree row = B (held key): ACCEPTED, `how=
  'worktree'` -- the exact inverse bug: the lagging worktree copy was the
  authority.

### The fix (rotate.py, two read sites + one helper)

`_seat_read_root(root, seat=None)` (rotate.py:17683): resolve
`_shared_graph_root(root)` -- the tree the ONE identity writer,
`_write_identity_cells`, writes -- guard it with
`locations.refuse_live_resolution(root, shared)` exactly as the writer does
(rotate.py:9365), and return it only when it carries the seat (or, for a
seat-less worktree match, any rows at all); otherwise fall back to `root`'s own
copy. `shared == root` from MAIN is a byte-level no-op.

- `_caller_post` env path: `_find_seat(_seat_read_root(root, seat), seat)`.
- `_caller_post` worktree-match path: iterate rows over
  `(_seat_read_root(root), root)` in that order -- MAIN first, then the
  worktree copy as the fallback.
- `cmd_rotate` target-row lookup for `--post`/`--name`:
  `_find_seat(_seat_read_root(root, target), target)`.
- `how` on success is unchanged `'worktree'` (no new token invented).

### Conjunct (3) preserved, with its test

The row's `pubkey` cell is the ONLY authority (`_caller_hold_key` compares
against `row.get("pubkey")` only; `key_history` is never read).
`test_key_history_only_pubkey_never_authorizes` holds the retired key A while
the row names B and lists A in `key_history` -- REFUSES by fingerprint.

### Post-fix measurement

Same probe, after the edit:
- A) MAIN fresh / worktree stale: RESOLVES, `post='s-director'`,
  `how='worktree'`, resolved `row_pub=B` (MAIN).
- B) MAIN stale / worktree fresh: REFUSES by name (fingerprint mismatch against
  MAIN's A row), `row_pub=None`.

## Evidence

Tests (red-first; new file, no existing test edited):
`extensions/agi/tests/test_rotate_caller_post.py` -- 5 cases:
(a) MAIN fresh / worktree stale resolves with `how == 'worktree'`;
(b) MAIN stale / worktree fresh refuses by name;
(c) `key_history`-only pubkey refuses by name;
(fallback) seat absent from MAIN falls back to the worktree copy;
(d) MAIN-as-root: `_seat_read_root == root` and `_caller_post` resolves `env`.

Run (after the edit):
`python3 -m pytest extensions/agi/tests/test_rotate.py extensions/agi/tests/test_rotate_verb_resolvers.py extensions/agi/tests/test_rotate_identity_main.py extensions/agi/tests/test_rotate_caller_post.py -q`
-> **358 passed** (114s), including the untouched existing caller tests in
`test_rotate_verb_resolvers.py` (green unchanged, not edited to fit).

LINE CEILING: **14 production lines added, 3 deleted** (`git diff --numstat --
extensions/agi/bin/rotate.py`), against a ceiling of 8 -- disclosed overage of
6 lines. Under the 2x halt threshold (16), so no re-brief required. The overage
is the `_seat_read_root` helper (10 lines incl. blanks/docstring) plus the three
call-site edits; a per-call-site inline would have duplicated the
`_shared_graph_root` + `refuse_live_resolution` guard three times.

Trivial patch hygiene: `python3 -c "import ast; ast.parse(...)"` on rotate.py ok.

## Agent Notes
BUILT conjunct (2): rotate._caller_post (env + worktree-match) and cmd_rotate target lookup now read the seat row from _shared_graph_root(root) (MAIN, guarded by locations.refuse_live_resolution) with per-seat fallback to the worktree copy. Pre-fix probe (real MAIN+worktree): A MAIN-fresh/WT-stale REFUSED at rotate._caller_hold_key:17756; B MAIN-stale/WT-fresh wrongly ACCEPTED. Post-fix: A resolves how='worktree' from MAIN, B refuses by name. Conjunct (3) preserved: key_history-only pubkey never authorizes (test). New test_rotate_caller_post.py (5 cases, incl. fallback + MAIN-as-root no-op); 358 pass across test_rotate.py + verb_resolvers + identity_main + caller_post; existing verb_resolvers caller tests untouched. production_lines=14 vs ceiling 8 (overage disclosed, under 2x halt).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT review of a00-2dc3ea4c (2bbaa27bf), verdict demoted proved -> inconclusive_lean_proved:60 on the parent's OWN probes, not the kid's suite. WHAT THE INSTRUCTION SAID (re-scoped l5 conjunct 2): `_caller_post` loads the rows from `_shared_graph_root(root)` and falls back to root's copy ONLY when the shared root has no row for the seat. WHAT THE MACHINE ACTUALLY DOES, cited to the committed bytes: the env path (rotate.py:17704) and cmd_rotate's target lookup (rotate.py:20722) route through `_seat_read_root(root, seat)` (rotate.py:17683), which does the per-seat fallback exactly -- probes A and E hold. The worktree-match branch (rotate.py:17713) builds `_trees = (_seat_read_root(root), root)`; with seat=None `_seat_read_root` returns shared whenever `_load_seats(shared)` is truthy, so the fallback there is TREE-level, not per-seat. Probe C (MAIN has a row for the seat but its `worktree` cell does not match; the worktree copy holds the key) ACCEPTS the stale held key -- the exact acceptance the claim exists to kill, just on the no-AGI_POST path. THE NEAR MISS: a suite that only drives the AGI_POST path satisfies the words and loses the mechanism -- a seat that runs `rotate` from its own worktree without the env seat takes the worktree-match branch, and that is where the stale key still authorizes. Probes B (key_history-only refuses) and D (MAIN-as-root no-op) hold. DEVIATION: none of mine; the kid DISCLOSED the tree-level interpretation in its own caveats line, which is why this is a 60 lean with the probe named and not a hidden overclaim. Ceiling 14 vs 8 disclosed and verified against git diff --numstat (14 added, 3 deleted), under the 2x halt. NEXT: kid 2 closes the worktree-match branch to per-seat fallback.
<!-- THOUGHT:END -->

Parent review: 4 parent probes pass (A resolve-from-MAIN, B key_history refuses, D MAIN-as-root no-op, E cmd_rotate --post wire); probe C FAILS -- the worktree-match branch falls back tree-level, and a MAIN row for the seat with a non-matching worktree cell lets the stale held key authorize. Demoted proved -> inconclusive_lean_proved:60; kid 2 re-briefed to make the fallback per-seat.
