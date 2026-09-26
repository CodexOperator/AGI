---
id: experiment:a00-70e38375-15d522
mint_id: 1f0bdd21227346999c054d0bf7988a8b
type: experiment
parents:
  - hypothesis:a-captive-capture-rotates-even-when-its-driven-handoff-refuses
next_edges: []
confidence: 0.8
edited_by: a00-70e38375
evidence_runs:
  - experiment:a00-70e38375-15d522
loop: hypothesis:a-captive-capture-rotates-even-when-its-driven-handoff-refuses@s2
model: stealth/space-bunny-alpha
production_lines: 30
profile: balanced
role: kid
scaffold_hash: c985adbb6e43fb22
season: 2
title: "the driven rotate-self refuses with nothing done: the registry gate is the first gate"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-70e38375-15d522

## What was built

The hypothesis is proved for the CHAIN (a00-183e23e5). This round closes the
hazard the parent measured on the sibling branch a00-a8caad2f: the capture
chain's `rotate-self` step now FETCHES+MERGES at the geometry guard — and that
guard ran ABOVE the registry gate, so `rotate-self --name <unregistered>`
merged a commit and *then* refused `no seat` (measured by the parent: behind
1 -> 0, `# v2` in rotations.md, rc 1).

| conjunct | before | after |
|---|---|---|
| a driven rotation that refuses leaves NOTHING done | geometry guard -> registry gate -> (later) `_prepare_checks(perform=True)` | **registry gate is the FIRST gate** in `cmd_rotate_self`; the geometry guard runs after it |
| the invariant is enforced, not just true today | nothing read the order | `test_registry_gate_is_the_first_gate_in_rotate_self` (source order + no side-effecting call between the branch guard and the gate) |

The change is a MOVE, not new logic: `seat = args.name` + the `_find_seat` /
`row = {}` block now precede `_geometry_resolution_root`. Neither the gate nor
the geometry guard needs `cfg_root` (the gate reads `_seat_read_root(root, …)`
from the worktree root, exactly as before), so the swap changes ONE case: the
double fault (unregistered AND behind) now says `no seat`, and a REGISTERED
behind seat still gets the behind-count + `git merge --no-edit origin/season/s2`
refusal. `--prepare` already ran its own registry gate above its merge
(goal:g15.14 P1-c); this makes the non-prepare path say the same thing.

The value is structural: the sibling's merge-at-the-guard now lands BELOW the
gate, so an unauthenticated name can never reach it — and the guard test fails
loudly if a future change reintroduces the reverse order or teaches any gate
above the registry gate to fetch/push/merge.

## Evidence

```
$ env -u TMUX -u TMUX_PANE python3 .agi/sessions/iter-DH.408/a00-70e38375/probe_gate_order.py
the guard applied to three sources:
  (a) AS SHIPPED on this branch
    gate_before_geometry=True side_effects_before_gate=[] -> guard PASSES
  (b) PRE-FIX order (no merge)
    gate_before_geometry=False side_effects_before_gate=[] -> guard FAILS
  (c) PRE-FIX order + geometry-guard merge
    gate_before_geometry=False side_effects_before_gate=['_prepare_checks('] -> guard FAILS
```

(b)/(c) rebuild the pre-fix ORDER from this branch's own source (geometry block
put back above the registry block) and inject the merge a00-a8caad2f measured —
so the source-order test is NOT vacuous. The probe reads one file; it writes
nothing and runs no git.

Live bytes, tmp repo (mechanism-3 fixture shape: geometry v1, `origin/season/s2`
at v2, branch `loop/stale`):
- `--name ghost-seat` (unregistered): rc 1, stderr `ERR: no seat 'ghost-seat' …`;
  HEAD sha unchanged, `rev-list --count HEAD..origin/season/s2 -- .agi/nodes/.geometry/`
  still `1`, `# v2` absent from the working rotations.md — NO side effect.
- `--name sanctuary-director` (registered): rc 1, stderr keeps the geometry
  refusal (`behind`, `1 commit`, `git merge --no-edit origin/season/s2`), HEAD
  unchanged — the move stole nothing.

## Tests

`extensions/agi/tests/test_rotate_templates.py` (in the mechanism-3 section, so
the `_mgit_repo` / `_geometry_commit` / `SEATS_BODY` fixtures are reused, not
copied):
- `test_registry_gate_is_the_first_gate_in_rotate_self` — the order + the
  no-side-effect-above-the-gate scan (comments stripped: a call named in a
  comment is prose, not a call).
- `test_unregistered_name_behind_refuses_with_no_side_effect` — the capture
  chain's case, driven through `rotate.main`.
- `test_registered_name_behind_still_gets_the_geometry_refusal` — no regression
  in the guard that used to fire first.

```
env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_rotate_templates.py -q
  -> 35 passed
env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests \
    -k "rotate_self or rotate-self or rotate or seats or capture" -q
  -> 1223 passed, 1 skipped, 1 xfailed, 5548 deselected
```

## Guards held

No test or probe runs `rotate.py handoff`/`rotate-self` against a live seat —
every call is `rotate.main([...])` on a `tmp_path` repo; no worktree, no
network, no git beyond the one `git diff --numstat` measurement; no `grid.py`.
Production lines: `30 21 extensions/agi/bin/rotate.py` (ceiling 40).

## Weakness carried

The two runtime tests pass on the PRE-fix bytes too (today no side effect
happens above the gate), so on their own they are regression guards, not
proof; the PROOF is the source-order test, whose teeth the probe demonstrates.
The sibling's merge-at-the-guard is not in THIS worktree, so (c) is an
injected reproduction of the shape the parent measured, not its bytes.

## Agent Notes
hoisted cmd_rotate_self's registry gate above the geometry guard so a driven (capture-chain) rotation that refuses 'no seat' can never fetch+merge first; source-order guard test with a demonstrated-teeth differential, 1223 passed
