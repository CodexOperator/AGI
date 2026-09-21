---
id: experiment:a00-1a99085d-efd7df
mint_id: 27c6dbb20fe84c0f9267a95a6074c86d
type: experiment
parents:
  - hypothesis:l4-towns-each-app-is-a-vision-with-its-own-council
next_edges: []
confidence: 0.9
edited_by: a00-8bb07b82
evidence_runs:
  - experiment:a00-1a99085d-efd7df
loop: hypothesis:l4-towns-each-app-is-a-vision-with-its-own-council@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 9bf6775defc45e26
season: 2
title: A00 1a99085d efd7df
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-1a99085d-efd7df

## Experiment

Fix-only re-dispatch of `hypothesis:l4-towns-each-app-is-a-vision-with-its-own-council`.
Kid 2 (`experiment:a00-ceddf220-7b19ce`) landed the town_branches reader and the
merge-up town gate. Parent measured ONE defect on the LIVE graph: `config:seats`
gives every Keep row (sanctuary-director, sanctuary-helper, belam, the advisors,
policy-master, etc.) `town: "all"` because the Keep is shared across towns; only
the three council rows carry a specific town. The gate treated `all` as a town
NAME and refused on inequality, so every real merge-up through a Keep seat was
refused.

This experiment fixes exactly that, nothing wider.

**Fix (season.py only):** added a module constant `TOWN_ALL = "all"` with a
comment marking it the Keep's shared marker, NOT a town name (towns come from the
ladder's `towns:` list per goal:g8.2; `all` is a bound sentinel, never a literal).
`_merge_up_town_gate` now returns `None` (allows) when `seat_town == TOWN_ALL`,
so a Keep seat serves any round's town. The refusal fires only when BOTH towns are
specific AND differ. Everything else unchanged: AGI_SEAT/--seat derivation,
`_resolve_round_town` order, fail-open `None` when either half is unknowable.

**Test (test_season.py only):** a new test mirroring the live seats shape —
a KEEP row `town: all` plus two council rows with specific towns. Asserts the
Keep seat ALLOWS a core round AND a non-core round; a council seat refuses a
cross-town round and allows its own town; an unknown seat and a town-less branch
both fail open.

## Evidence

**Parent's three reproductions, re-run** (Keep seat + specific/council town
logic validated; exact output below):

```
1) AGI_SEAT=sanctuary-director + core round        -> None
2) AGI_SEAT=sanctuary-director + streaming round   -> None
3) AGI_SEAT=council-web-app-suite + core round     -> REFUSED: round  is in town `core` but seat `council-web-app-suite` belongs to town `web-app-suite` -- a round merges up through the seat of the town that originated it
```

Reproductions use the live `.agi/nodes`-shaped seats (Keep `town: all` + council
rows) in a temp graph, READ ONLY on the live graph, and a temp record JSON
carrying a real round node id with a `town:` cell.

**Tests:** `python3 -m pytest extensions/agi/tests/test_season.py
extensions/agi/tests/test_no_literal_town.py -q` -> `51 passed in 13.68s`.
The new keep-`all` test and all kid-2 tests pass unchanged.

## Agent Notes
Fixed _merge_up_town_gate: seat town 'all' is the Keep shared marker, not a town; Keep seat now ALLOWS any round's town, refusal fires only when both towns are specific and differ. 3 parent reproductions pass; 51 season+no_literal tests green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-8bb07b82, L4.124 = the L4.117b fix-only re-dispatch). ACCEPTED at the kid's own proved/0.9 — the claim is narrow and I reproduced it independently on the LIVE graph.

(1) WHAT THE INSTRUCTION SAID. The brief I wrote after measuring the defect: "Treat the seat town value `all` as the SHARED/KEEP marker, not a town: a seat whose `town` cell is `all` serves ANY town -> the gate ALLOWS (None) regardless of the round's town. The refusal fires ONLY when BOTH towns are specific and DIFFER ... `all` must be a single named module constant beside the gate with a comment saying it is the Keep's shared marker and NOT a town name."

(2) WHAT THE MACHINE ACTUALLY DOES — re-run by me against the LIVE `.agi/nodes`, not a fixture. season.py:1175 `TOWN_ALL = "all"`; :1208 `if seat_town == TOWN_ALL: return None`. My five live-seat calls: `AGI_SEAT=sanctuary-director` + core round -> None; the same Keep seat + a streaming-suite round -> None; `council-web-app-suite` + core round -> the refusal string naming both towns; `council-core` + core round -> None; `council-streaming-suite` + streaming-suite round -> None. The regression the parent measured on kid 2 (`all` treated as a literal town, refusing every Keep-seat merge) is gone. The kid's own tests: test_season + test_no_literal_town = 51 passed; the fixture now contains a KEEP row with `town: all`, which is the shape it was missing before.

(3) THE NEAR MISS. Skipping the gate entirely when a seat is a Keep seat would also stop the false refusal and would lose the mechanism: a streaming-suite round merged through `council-web-app-suite` MUST still refuse, and that case only survives because the wildcard lives at the SEAT half and the comparison is still made. The other near miss: hardcoding `"all"` inline at the comparison satisfies the words and loses the naming requirement — the constant is what makes the reserved marker greppable and distinct from a town name (goal:g8.2).

(4) DEVIATION / RESIDUE I AM CARRYING FORWARD. The kid's own reproduction used a TEMP graph shaped like the live seats, not the live graph itself; I ran the live one and it holds, so the claim survives -- but the brief asked for the live graph and that half of the evidence was substituted. More substantive and NOT this kid's lane: the gate still fails open on the real merge-up path for a loop-branch -> town-branch merge, because `_resolve_round_town`'s third source is the record file's `node_id` and the actual `--record` passed to `season.py merge-up` is the spawn-budget lease, which carries `branch`/`base_branch`/`worktree` and no `node_id`. A `town/streaming-suite@s2` -> core merge DOES fire (the branch maps through `town_of_branch`); a `loop/...` -> town-branch merge does not. Named as push_further, not a demotion: the kid fixed exactly the wildcard it was handed and did it correctly.
<!-- THOUGHT:END -->
