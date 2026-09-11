---
id: experiment:a00-ceddf220-7b19ce
mint_id: 0e28a2c9657545a599b6453ae873fe85
type: experiment
parents:
  - hypothesis:l4-towns-each-app-is-a-vision-with-its-own-council
next_edges: []
confidence: 0.5
edited_by: ubuntu
evidence_runs:
  - experiment:a00-ceddf220-7b19ce
loop: hypothesis:l4-towns-each-app-is-a-vision-with-its-own-council@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: b564ab4309f52f58
season: 2
title: A00 ceddf220 7b19ce
town: core
verdict: inconclusive_lean_proved:50
---
<!-- BODY:BEGIN -->
# experiment:a00-ceddf220-7b19ce

## Experiment

Residues 4 and 5 of the L4.117b re-dispatch of
`hypothesis:l4-towns-each-app-is-a-vision-with-its-own-council`: an OPAQUE
town_branches reader consulted by the stale-base guard, and a merge-up town
gate that fires without --round/--seat.

### Residue 4 — town_branches reader + guard

`spawn_gate.read_town_branches(nodes_dir)` reads the ladder's `town_branches`
map (`{}` when unset/unreadable, fail open). `town_integration_branch` is the
one town->branch resolver; `town_of_branch` the ONLY branch->town path, by
EXACT string equality on the opaque value (owner ruling 01:4xZ — the value
may be renamed at one config edit, zero code). The dispatch stale-base guard
goes through a new `_current_town_branch(git_root, nodes_dir)`: `git rev-parse
--abbrev-ref HEAD` captured + fail-open, reverse-looked up in town_branches;
when it maps to a town the round is measured against `origin/<opaque>` (fetch,
rev-parse, rev-list, diff all target that ref) and the record's `integration`
and sync cmd name it; a non-mapped branch (seat/loop/detached) keeps
today's `origin/season/s{season}` byte-for-byte. Unreachable origin remains
`unchecked`, never a false stale claim.

`season.py cmd_merge_up` base resolution now prefers the round's town
integration branch (`_town_base`) before the recorded base_branch, so a round
in town T merges up to T's town branch.

### Residue 5 — town gate fires without flags

`_merge_up_town_gate` no longer early-returns when --round/--seat are empty.
`_resolve_round_town` (one shared resolver used by the gate AND the base
resolution) derives the round's town from: --round node's `town:` cell, then
`town_of_branch(args.branch)`, then the record file's `node_id` town cell.
The seat derives from --seat, else `AGI_SEAT` env (the seat the spawn
carries). The refusal fires when both halves resolve and differ; either half
unknowable -> None (fail open; a town-less graph is untouched). --round/--seat
behaviour when passed is unchanged.

### Verification

- `git grep -c town_branches extensions/` — was 0, now non-zero in the reader
  file and its callers + tests.
- Real-tree probe (this checkout): read_town_branches -> {'core': 'season/s2',
  'streaming-suite': 'town/streaming-suite@s2', 'web-app-suite':
  'town/web-app-suite@s2'}; town_of_branch('town/streaming-suite@s2') ->
  'streaming-suite'; town_of_branch('season/s2') -> 'core';
  town_integration_branch('streaming-suite') -> 'town/streaming-suite@s2'.
- Fixture tests: a town branch ahead of season/s2 on origin but even with its
  own integration branch reads `current` while the same HEAD against the
  fallback season/s2 reads `behind` (1); the record's `integration`/sync cmd
  name the town branch on the town path and `season/s2` on the fallback;
  `_merge_up_town_gate` REFUSES a cross-town merge and ALLOWS a same-town one
  with NO --round/--seat (derived from AGI_SEAT + branch), and fails open
  (None) when neither half is derivable; the reader fails open on missing
  ladder/map; `town_of_branch` is exact-equality-only (a look-alike renamed
  branch does NOT resolve).

## Evidence

- `python3 -m pytest extensions/agi/tests/test_season.py
extensions/agi/tests/test_dispatch.py extensions/agi/tests/test_spawn_gate.py
-q` -> 219 passed.
- `AGI_TIER= python3 -m pytest extensions/agi/tests/ -q` -> 2717 passed,
  1 skipped.

## Agent Notes
Residues 4-5: opaque town_branches reader (read_town_branches/town_integration_branch/town_of_branch, exact-equality-only) wired into the dispatch stale-base guard (measures a town round against its OWN integration branch, fallback keeps season/sN byte-for-byte) and season merge-up base; merge-up town gate now fires without --round/--seat (AGI_SEAT + town_of_branch + record node_id). 219 targeted + 2717 full suite pass.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW, DEMOTED (a00-8bb07b82, L4.124 = the L4.117b fix-only re-dispatch). The kid reported proved at 0.9; the parent demotes to inconclusive_lean_proved:70, confidence 0.7. Residue 4 is proved; residue 5 carries a false-refusal defect that would block every real merge-up.

(1) WHAT THE INSTRUCTION SAID. Residue 4: "an OPAQUE town_branches reader (ladder frontmatter) that the stale-base guard and the merge-up gate consult ... git grep town_branches extensions/ must be > 0 after this round, with a test". Residue 5: "the merge-up town gate fires only with --round/--seat, which no caller passes" -> "wire the town gate".

(2) WHAT THE MACHINE ACTUALLY DOES, re-run by me on this checkout. Residue 4 is real and reproduces exactly: `git grep -c town_branches -- extensions/` is 1/2/8/2/3/9 across dispatch.py, season.py, spawn_gate.py and their tests (was 0); `read_town_branches` -> {'core':'season/s2','streaming-suite':'town/streaming-suite@s2','web-app-suite':'town/web-app-suite@s2'}; `town_of_branch('town/streaming-suite@s2')` -> 'streaming-suite'; `town_of_branch('season/s2')` -> 'core'; the value is opaque, never parsed. `_stale_base_spawn`/`_stale_base_record` take an optional `town_branch` and fall back to `origin/season/s{N}` byte-for-byte when the branch maps to no town; fail-open to `unchecked` is preserved. Targeted run: test_season + test_dispatch + test_spawn_gate + test_node_writer = 288 passed.

Residue 5 does NOT hold on the real graph. The prime landed `config:seats` with `town: all` on all thirteen Keep rows (e.g. sanctuary-director, seats.md:21) because the Keep is shared across towns; only the three council rows carry a specific town. `_merge_up_town_gate` compares `round_town == seat_town` literally, so `all` is treated as a town NAME. I called the shipped function with the live seats and a core round: `AGI_SEAT=sanctuary-director` + round town `core` -> `REFUSED: ... seat 'sanctuary-director' belongs to town 'all'`; the same seat with a streaming-suite round -> also REFUSED. Every merge-up performed by a Keep seat (which is every real merge-up -- the directors are the ones who run it) is refused. That is a false refusal on the live graph, the same class the gate exists to prevent.

(3) THE NEAR MISS. Comparing two strings and refusing on inequality satisfies "fires without --round/--seat" and loses the mechanism: `town: all` is the Keep's SHARED marker, not a town, so the comparison must treat it as a wildcard (a Keep seat serves any town; two SPECIFIC towns that differ is the only refusable case). The fixture the kid wrote used two council seats with specific towns and never exercised a Keep row, so the wildcard case was invisible to it -- a fixture that mirrors the code's assumption instead of the live graph's data.

(4) DEVIATION. None by the kid; the brief named the seat half as "the target seat's town cell from config:seats" without stating the `all` wildcard, so the kid implemented the instruction and the instruction was incomplete. The residue is mine to fix with a follow-up kid, not evidence against the reader, which is sound and is why this node is demoted rather than disproved: the town_branches half is independently verified. Residue 5 re-opened as a named follow-up: `all` wildcard + a fixture built from a Keep row.
<!-- THOUGHT:END -->

PRIME L4-VIII, merge-up 27 review by name: DEMOTED :70 -> :50. The opaque town_branches reader is MET; NOT MET: (5b) season.py:1242 _town_base precedes the recorded base_branch, so any core round with a --round or an agent.json record merges straight into season/s2, skipping the rung that cut it (fixture probe: tier1/director untouched) — reverses the l3w4 one-rung rule on merged bytes. -> g15 node.
