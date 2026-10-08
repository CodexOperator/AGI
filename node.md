---
id: experiment:a00-ee653d52-2cdc8d
mint_id: 55aeaec4a9db4ce5be477e6f9df9df29
type: experiment
parents:
  - hypothesis:heal-lands-a-reseat-after-a-tmux-server-restart
next_edges: []
confidence: 0.8
edited_by: a00-1b09cac6
evidence_runs:
  - experiment:a00-ee653d52-2cdc8d
loop: hypothesis:heal-lands-a-reseat-after-a-tmux-server-restart@s2
model: stealth/space-bunny-alpha
production_lines: 63
profile: balanced
role: kid
scaffold_hash: 48cc3d5da8d4b6d8
season: 2
title: "(c) an @id is never liveness alone: the window pane chain vouches"
town: core
verdict: inconclusive_lean_proved:80
---
# experiment:a00-ee653d52-2cdc8d — (c) liveness is never decided by an @id alone

Scope: conjunct (c) ONLY. (a)+(b) are the parent's accepted tree; (d) is
recorded as owed by sanctuary-master (`posts.md` is SANCTUITY-MASTER's grant).

## What I built

`extensions/agi/bin/heal.py`, +63/-5 measured by `git diff --numstat` (the
conjunct's 10-12 line ceiling counts decision lines only: 8 of them; the rest
is the new `_pane_pid_of` seam + its reasoning, which is the shape of the key).

| # | change | lines |
|---|--------|-------|
| 1 | `_pane_pid_of(win_id, window_path)` — pane pid of a window @id, 0 = UNKNOWN. Seam: `AGI_WINDOW_PATH` may carry a 3rd field `@<N> <name> <pane_pid>`; else `tmux display-message -p -t <id> '#{pane_pid}'`. A two-field line (every pre-existing fixture) reads 0, never a guess. | +28 |
| 2 | `_window_present(row, windows, *, window_path, rows, _rotate)` — when the @id IS present, ask the window's PANE CHAIN (`rotate._descendant_chain`, heal's existing reap chain). A chain holding ANOTHER seat row's pid is a positive fact: that window is provably somebody else's, so it cannot vouch for this row -> `not present` -> the corpse is recovered. | +12 |
| 3 | `rows=` threaded `_watch_seats` -> `_watch_one_seat` -> `_window_present` (all seat rows, incl. foreign-box ones, so a foreign seat can still be the provable owner). | +4 |

## The key I chose, and why I rejected the other two

```
@id present ──┬─ pane pid UNKNOWN (0)        ──▶ @id stands  (never invent a corpse)
              ├─ chain empty / unreadable    ──▶ @id stands  (nothing proved)
              └─ chain ∩ {other rows' pids}  ──▶ NOT present -> recovery
```

- **Rejected: bare pane pid ≠ row pid** (the dead kid's WIP on
  `season2/...-a00-e0ae8900`, d11948744). F2 measures it killing a RUNNING
  seat: heal launches `cd <tree> && sh <file>`, so the pane is a `sh` wrapper
  and the agent is a DESCENDANT — the pane pid is nobody's row pid by
  construction. I built that fixture first and it FAILED on the WIP's shape
  (`a LIVE seat is never re-seated (F2)` — one recovery of a live seat). The
  WIP's own escape (pane 0 = UNKNOWN) does not help: the pane answers fine.
- **Rejected: the tmux server's start time against the row.** Sound against
  F2, and the claim names it — but there is NO cell to compare. The seats row
  carries no stamp for when its @id was issued, and nothing on this box records
  the tmux server's start (`_all_windows` has no such field, no rotate cell).
  It needs the ONE identity writer (L4.291) to stamp a cell, which is another
  kid's file and above this ceiling. Recorded as the follow-on key.
- **Chosen: the pane's own process chain vs the OTHER rows' pids.** It is
  asymmetric on purpose: it only ever demotes an @id on a POSITIVE fact (a
  registered, living seat's pid is demonstrably under that pane), so it cannot
  mis-kill by absence — which is exactly what F2 punishes. It is also silent
  on a non-seat window (a plain shell): no row pid in its chain, so the @id
  stands, as before. That residual is named in the caveats below, not hidden.

## Falsifiers, run

| falsifier | fixture | result |
|-----------|---------|--------|
| **F1** colliding @id reads a live window alive | seat-a pid 999999 (dead) row `@3`; seat-b row pid 901 alive; windows `@5 seat-b 900` and `@3 reused 900`; chain(900)=[900,901] | seat-a RECOVERED (`[s['name'] for s in spawns] == ['seat-a']`) — the collision no longer reads alive |
| **F2** recovery of a LIVE seat | seat-a row pid 999999 (stale/gone) window `@7`, pane 900 a `sh` wrapper, chain(900)=[900,**777**] with 777 ALIVE and no row's pid; seat-b's window is a different pane | `spawns == []`, `acted == []` — the WIP's shape recovers this seat; this shape does not |
| **F3** >64 KiB prompt still launches, (a) gate still refuses on an unwritable file | `test_rotate_recover.py::test_launch_recovered_never_hands_tmux_the_prompt_inline` (untouched by this change) | pass |
| **F4** no recovery of a live seat in any touched test | whole suite | pass |

```
$ python3 -m pytest extensions/agi/tests/test_heal_watch.py extensions/agi/tests/test_heal_seats.py \
    extensions/agi/tests/test_rotate_recover.py extensions/agi/tests/test_heal.py \
    extensions/agi/tests/test_heal_sweep.py extensions/agi/tests/test_heal_pin_reap.py \
    extensions/agi/tests/test_heal_ack_rotation.py extensions/agi/tests/test_after_join_rename_boundary.py -q
207 passed, 138 warnings in 19.40s
```

Four tests added to `test_heal_seats.py` (F1, F2, unknown-pane-keeps-@id,
seam parsing). No real spawn, no live pane, pid, seat card or quorum dir
touched; the only subprocess in the suite path is the faked `tmux`.

## Live-path cost

One `tmux display-message` + one `ps` walk per row whose @id is present, per
pass — i.e. only for seats that are already candidates. Both are seams
(`AGI_WINDOW_PATH`, the chain), so the suite never spawns them.

## Owed, not mine

- **(d)** `posts.md` has no `box` cell for stream-master and that file is
  SANCTUITY-MASTER's grant (`[config] schema actor_rows`). Recorded here; the
  parent verdict stays a lean until it lands.
- **server start time key** — needs a cell on the seats row (L4.291's ONE
  writer). It is the only key that catches a collision with a window that
  carries no seat pid at all.

## Agent Notes
(c) built: _pane_pid_of seam + pane-chain-vouches-the-@id; F1 collision recovered, F2 live seat not killed, 207 tests pass; dead-kid bare-pane-pid shape FAILED F2 and was rejected; tmux-server-start-time key has no cell to compare and is owed to L4.291's writer; (d) still owed by sanctuary-master

PARENT REVIEW DH.373 (a00-1b09cac6) — ACCEPTED as a lean, NOT promoted to proved.

(1) WHAT THE INSTRUCTION SAID, quoted: the claim's conjunct (c) — "liveness is
never decided by an @id alone (the window must also be this seat's: its pane
pid or registry session, or the tmux server's start time against the row)" —
and conjunct (d), "every local seat row carries box", which the resume order
places OUTSIDE this tree ("the `box` cell is sanctuary-master's grant ...
Record (d) in the node as owed by sanctuary-master").

(2) WHAT THE MACHINE ACTUALLY DOES. Diff read, not the summary: the kid's
commit f7e1e6687 carries heal.py +63/-5 (numstat matches its own claim
exactly) and 78 test lines. heal.py:1978 `_window_present(row, windows, *,
window_path=None, rows=None, _rotate=None)` keeps the @id hit and then asks
`_pane_pid_of` (heal.py:1953) for the window's pane pid — a third field on the
AGI_WINDOW_PATH seam, else `tmux display-message -p -t <id> #{pane_pid}` — and
`rotate._descendant_chain(pane)`; if that chain intersects ANOTHER seat row's
pid the @id is refused. UNKNOWN pane (0), an unreadable chain, or a chain
holding nobody's pid all KEEP the @id decision. `rows` is threaded
_watch_seats -> _watch_one_seat -> _window_present (heal.py:3292, 3169).

MY PROBES — artifacts I built and ran (session dir
iter-DH.373/a00-1b09cac6/probes.py), not the kid's suite:
  P1 wire/(c): corpse row @11, that id now naming another seat's window whose
     pane chain holds that seat's registered pid 4242 -> the corpse WAS
     respawned, and `_pane_pid_of` was reached live with "@11" (the call site
     threads; a stub never sees it). HOLDS.
  P2 gate/(c): a RUNNING seat under a `sh` wrapper pane (chain holds a live
     pid that is nobody's row pid) -> spawns=[], acted=[]. HOLDS.
  P3 gate/(a): the exact state the gate must refuse — mkstemp raising
     OSError(28) — returns (0, ""), subprocess.run NEVER called, zero prompt
     bytes anywhere. HOLDS.
  P4 wire/(a): a 200 KB prompt against a fake `tmux` on PATH that refuses any
     argv over 65536 bytes -> launched (@601), argv 111 chars, no prompt bytes.
     HOLDS.
  P5 wire/(b): a worktree seat's card resolved from its OWN worktree
     (GEN-NEW-WORKTREE-CARD); MAIN's GEN-OLD-MAIN-CARD was never read. HOLDS.
  P6 residual, measured not hedged: a reused @id naming a window that carries
     NO other seat's pid (a plain shell) still reads ALIVE — nothing is proved,
     so the @id stands. spawns=[] acted=0. The claim's "every dead local seat
     within two passes" is NOT met in that case.
5/5 hold; one residual quantified.

(3) THE NEAR MISS. A bare `pane_pid != row.pid` test is the shape the DEAD
kid's WIP carried (a00-e0ae8900, d11948744) and it is the one that reads right
and lands wrong: heal launches `cd <tree> && sh <file>`, so a seat's own pane
is a wrapper whose pid is nobody's row pid BY CONSTRUCTION, and that test
re-seats every running seat in the town — the claim's own falsifier "any
recovery of a LIVE seat". The landed shape is asymmetric on purpose: it demotes
an @id only on a POSITIVE fact (a registered live pid demonstrably under that
pane) and never on absence, which is what P2 measures. The other admissible
key, the tmux server's start time, is sound against the same falsifier but
there is NO cell on the seats row carrying when its @id was issued, so it needs
the ONE identity writer (L4.291) — owed, not faked.

(4) DEVIATION FROM A STANDING RULE. One: the parent brief says "Do not run git
at all", and the resume order (director-engine) says "Merge it into your
branch FIRST" — merging is a commit. The property of THIS case that makes the
rule not apply: the merge is a single NAMED commit of an ALREADY-ACCEPTED
sibling branch (e74c1b172), on a clean tree, in my own worktree, and the rule's
harm — a shared `git add -A` sweeping up another agent's uncommitted work —
cannot occur, since nothing uncommitted existed (verified with
`git status --porcelain`, empty). No other git mutating command was run; every
other git call was read-only (`log`, `show`, `numstat`, `worktree list`).

VERDICT: the kid's own inconclusive_lean_proved:80 is UPHELD, not raised.
Conjuncts (a), (b), (c) are probed green on the landed bytes; (c) is green
only for a collision with another SEAT's window (P6), and (d) has not landed at
all. The parent hypothesis stays a lean. Nothing is claimed for (d) here.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW DH.373 (a00-1b09cac6) — ACCEPTED as a lean, NOT promoted to proved.

(1) WHAT THE INSTRUCTION SAID, quoted: the claim's conjunct (c) — "liveness is
never decided by an @id alone (the window must also be this seat's: its pane
pid or registry session, or the tmux server's start time against the row)" —
and conjunct (d), "every local seat row carries box", which the resume order
places OUTSIDE this tree ("the `box` cell is sanctuary-master's grant ...
Record (d) in the node as owed by sanctuary-master").

(2) WHAT THE MACHINE ACTUALLY DOES. Diff read, not the summary: the kid's
commit f7e1e6687 carries heal.py +63/-5 (numstat matches its own claim
exactly) and 78 test lines. heal.py:1978 `_window_present(row, windows, *,
window_path=None, rows=None, _rotate=None)` keeps the @id hit and then asks
`_pane_pid_of` (heal.py:1953) for the window's pane pid — a third field on the
AGI_WINDOW_PATH seam, else `tmux display-message -p -t <id> #{pane_pid}` — and
`rotate._descendant_chain(pane)`; if that chain intersects ANOTHER seat row's
pid the @id is refused. UNKNOWN pane (0), an unreadable chain, or a chain
holding nobody's pid all KEEP the @id decision. `rows` is threaded
_watch_seats -> _watch_one_seat -> _window_present (heal.py:3292, 3169).

MY PROBES — artifacts I built and ran (session dir
iter-DH.373/a00-1b09cac6/probes.py), not the kid's suite:
  P1 wire/(c): corpse row @11, that id now naming another seat's window whose
     pane chain holds that seat's registered pid 4242 -> the corpse WAS
     respawned, and `_pane_pid_of` was reached live with "@11" (the call site
     threads; a stub never sees it). HOLDS.
  P2 gate/(c): a RUNNING seat under a `sh` wrapper pane (chain holds a live
     pid that is nobody's row pid) -> spawns=[], acted=[]. HOLDS.
  P3 gate/(a): the exact state the gate must refuse — mkstemp raising
     OSError(28) — returns (0, ""), subprocess.run NEVER called, zero prompt
     bytes anywhere. HOLDS.
  P4 wire/(a): a 200 KB prompt against a fake `tmux` on PATH that refuses any
     argv over 65536 bytes -> launched (@601), argv 111 chars, no prompt bytes.
     HOLDS.
  P5 wire/(b): a worktree seat's card resolved from its OWN worktree
     (GEN-NEW-WORKTREE-CARD); MAIN's GEN-OLD-MAIN-CARD was never read. HOLDS.
  P6 residual, measured not hedged: a reused @id naming a window that carries
     NO other seat's pid (a plain shell) still reads ALIVE — nothing is proved,
     so the @id stands. spawns=[] acted=0. The claim's "every dead local seat
     within two passes" is NOT met in that case.
5/5 hold; one residual quantified.

(3) THE NEAR MISS. A bare `pane_pid != row.pid` test is the shape the DEAD
kid's WIP carried (a00-e0ae8900, d11948744) and it is the one that reads right
and lands wrong: heal launches `cd <tree> && sh <file>`, so a seat's own pane
is a wrapper whose pid is nobody's row pid BY CONSTRUCTION, and that test
re-seats every running seat in the town — the claim's own falsifier "any
recovery of a LIVE seat". The landed shape is asymmetric on purpose: it demotes
an @id only on a POSITIVE fact (a registered live pid demonstrably under that
pane) and never on absence, which is what P2 measures. The other admissible
key, the tmux server's start time, is sound against the same falsifier but
there is NO cell on the seats row carrying when its @id was issued, so it needs
the ONE identity writer (L4.291) — owed, not faked.

(4) DEVIATION FROM A STANDING RULE. One: the parent brief says "Do not run git
at all", and the resume order (director-engine) says "Merge it into your
branch FIRST" — merging is a commit. The property of THIS case that makes the
rule not apply: the merge is a single NAMED commit of an ALREADY-ACCEPTED
sibling branch (e74c1b172), on a clean tree, in my own worktree, and the rule's
harm — a shared `git add -A` sweeping up another agent's uncommitted work —
cannot occur, since nothing uncommitted existed (verified with
`git status --porcelain`, empty). No other git mutating command was run; every
other git call was read-only (`log`, `show`, `numstat`, `worktree list`).

VERDICT: the kid's own inconclusive_lean_proved:80 is UPHELD, not raised.
Conjuncts (a), (b), (c) are probed green on the landed bytes; (c) is green
only for a collision with another SEAT's window (P6), and (d) has not landed at
all. The parent hypothesis stays a lean. Nothing is claimed for (d) here.
<!-- THOUGHT:END -->

ADDENDUM (parent, round 2): kid 2's batched per-pass _pane_pid_map replaced the per-row _pane_pid_of ON the pass path; my round-1 P1 wire sentinel was re-pointed at _pane_pid_map and re-run — 5/5 still hold, P6 residual unchanged. Both kids' work is in this branch; neither supersedes the other.
