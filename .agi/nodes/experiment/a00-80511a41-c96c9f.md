---
id: experiment:a00-80511a41-c96c9f
mint_id: 639e20c4146c4600b7e8b34fdeed9c8f
type: experiment
parents:
  - hypothesis:l4-a-town-is-a-super-node-whose-cells-derive-its-branch-names
next_edges: []
confidence: 0.9
edited_by: a00-c653f5de
evidence_runs:
  - experiment:a00-80511a41-c96c9f
loop: hypothesis:l4-a-town-is-a-super-node-whose-cells-derive-its-branch-names@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: c674b1eef43da9d1
season: 2
title: A00 80511a41 c96c9f
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-80511a41-c96c9f

## Experiment

g15 round I-3b, continuation 3 — the FINAL DELIVERABLE block: three paste-ready
`write.py create town` lines carrying BOTH the `AGI_SEASON` season control AND
the REAL vision ids, proven by running THOSE EXACT STRINGS. Round-state:

- `experiment:a00-061c8dfd-9c6c20` (kid 1) shipped the schema + `towns.py` +
  the loader tests; its `## Prime create lines` block had the RIGHT vision ids
  but NO season control (a `--dry-run` proof that never reaches the stamp).
- `experiment:a00-3628613c-2cc463` (kid 2) MEASURED the root cause:
  `node_writer._stamp_env_fields` (node_writer.py:770-777) overwrites a node's
  `season` at mint time from `AGI_SEASON` > ladder `current_season`, so kid 1's
  lines mint all three towns `season: 2` on the live `current_season: 2` ladder.
- `experiment:a00-91c6c811-ffa1f7` (kid 3) added the `AGI_SEASON` control but
  wrote its core line with FIXTURE placeholder ids `["vision:a","vision:b",
  "vision:c"]` and built its fixture with those same placeholders (its
  test_town_mint_lines.py:89,117,149). Those ids resolve to NOTHING on the live
  tree — a block that trades real ids for seasons is not a fix.

The FINAL block below is the ONE the Prime pastes. It is also the ONE the test
runs: `extensions/agi/tests/test_town_mint_final.py` reads this block out of
THIS node file (the code fence under `## Prime create lines (final)`) and
executes each parsed line through a real subprocess on a fixture whose vision
nodes are the five REAL ids — never placeholders. The only thing the test
injects is `--root <fixture>` (the one environmental argument the Prime does
not paste: the Prime runs from the repo root); everything else — command,
`--actor prime_director`, every `--set`, the vision ids, the `AGI_SEASON` env —
is byte-for-byte what the node says. So the node block and the tested strings
cannot drift.

**Vision-id mapping caveat.** `vision:streaming-suite` and
`vision:web-app-suite` each carry a `town:` cell naming their charter vision,
so those two lines' `--set visions=…` are author-explicit. Core's three are
INHERITED from kid 1's reading of the ladder's THOUGHT block
(`.geometry/ladder.md:149` says only "core = the three season-2 visions" and
does NOT enumerate them — owner ruling 2026-09-11 01:0xZ in doc:l4-owner-
decisions), and are now independently VERIFIED live as the only three season-2
vision nodes with NO `town:` cell: `vision:alive`, `vision:all-is-one`,
`vision:self-perpetuating`. The Prime should confirm that enumeration when
pasting; the test's live-tree listing only proves the ids RESOLVE, not that the
ownership set is the owner's final word.

## Prime create lines (final)

```sh
AGI_SEASON=2 python3 extensions/agi/bin/write.py create town core --parent ladder:ladder --actor prime_director --set 'visions=["vision:alive", "vision:all-is-one", "vision:self-perpetuating"]' --set council=council-core --set season=2
AGI_SEASON=1 python3 extensions/agi/bin/write.py create town streaming-suite --parent ladder:ladder --actor prime_director --set 'visions=["vision:streaming-suite"]' --set council=council-streaming-suite --set season=1
AGI_SEASON=1 python3 extensions/agi/bin/write.py create town web-app-suite --parent ladder:ladder --actor prime_director --set 'visions=["vision:web-app-suite"]' --set council=council-web-app-suite --set season=1
```

## Record correction

For a Prime reading the older nodes so the round is not misread:

- kid 1's block is SUPERSEDED: it has no `AGI_SEASON` control, so on the
  running prime's shell it mints all three towns `season: 2`, giving the two
  suite towns branch names from a season they are one behind in.
- kid 3's block is SUPERSEDED: its core line cites placeholder vision ids
  `vision:a/b/c` that resolve to nothing live; the block it calls
  "corrected" is not paste-ready.
- Everything else in both stands: `--parent ladder:ladder`, `--actor
  prime_director`, the three council names, the produced `[town].md` schema,
  the `towns.py` loader and its ruling-table contract.

The negative corner (the same line WITHOUT season control lands `season: 2`)
stays owned by kid 2's
`test_town_mint.py::test_season_set_is_overridden_at_mint_time` — cited, not
duplicated.

## Evidence

New test file `extensions/agi/tests/test_town_mint_final.py` (4 tests). It
builds the same fresh fixture project as kid 2/3 (live `[town].md` copied
byte-for-byte, `current_season: 2` ladder, three council rows + a
`prime_director` row, `nodes/ladder/ladder.md`, and vision nodes whose ids are
EXACTLY the five REAL ids above), then READS the block from THIS node file and
runs each line through a real subprocess. Asserted, all three towns, fully:

- `test_block_reconstructs_the_deliverable` — the node-block lines, parsed,
  reconstruct the module `DELIVERABLE` tuple exactly (a typo'd vision id, a
  wrong season, a dropped council all fail here).
- `test_delivered_lines_mint_the_ruling_cells` — each create exits 0 and
  `nodes/town/<slug>.md` exists; `towns.load_towns` gives EVERY town the FULL
  `visions` set equal to the delivered list (not just core), plus `council`
  and `season`; `towns.town_tuples` equals the ruling table exactly
  (core/2/2/council-core, streaming-suite/1/2/council-streaming-suite,
  web-app-suite/1/2/council-web-app-suite);
  `towns.derive_names("core", <minted season>, post=…, loop_round=…,
  agent=…)` equals the ruling literal table.
- `test_delivered_vision_ids_resolve_on_the_live_tree` — every vision id in
  the delivered lines resolves to a file under the LIVE `.agi/nodes/vision/`,
  the check the placeholder-id block was blind to.

```
$ python3 -m pytest extensions/agi/tests/test_town_mint_final.py extensions/agi/tests/test_town_mint.py extensions/agi/tests/test_town_mint_lines.py -q
..............                                                           [100%]
14 passed in 1.82s  # 4 final + 8 kid2 mint + 2 kid3 lines
```
The final file alone: `test_town_mint_final.py -q` → 4 passed. (The
`tier-gate: phantom running record … (dead) -- skipped` line on the tree is a
leftover dead-pid record reported once by conftest; it skips, not fails.)

## Agent Notes
Final DELIVERABLE block: AGI_SEASON control + REAL vision ids; test reads the node block and runs its exact strings via subprocess on a fixture of the five real ids; 4 passed, 14 with kid2/3 neighbors. Core ids independently verified as the 3 season-2 visions with no town cell; mapping still inherited from kid1, Prime should confirm.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW I-3b continuation 3 (a00-c653f5de, L4.333), rewritten from scratch on this version.

WHAT THE INSTRUCTION SAID: ship ONE paste-ready block carrying both the AGI_SEASON control and the real vision ids, and prove it by running the delivered strings, with the vision ids listed against the LIVE tree.

WHAT THE MACHINE ACTUALLY DOES: parent re-ran test_town_mint_final.py -> 4 passed, and read the mechanism rather than the report. _read_node_block_lines reads NODE_FILE (this node, line 53) and regexes the fence under '## Prime create lines (final)'; a missing file raises, a fence with other than three lines asserts. test_block_reconstructs_the_deliverable cross-checks each parsed line against the module DELIVERABLE tuple, so a drift on either side fails; test_delivered_lines_mint_the_ruling_cells runs those parsed lines through a real subprocess and asserts the FULL visions set for EVERY town, plus council, season, town_tuples and derive_names on the minted core's own season; test_delivered_vision_ids_resolve_on_the_live_tree lists the ids against .agi/nodes/vision/. Five town test files together: 26 passed. ls .agi/nodes/town/ does not exist.

THE NEAR MISS: the obvious way to satisfy 'prove the delivered lines' is to keep the lines in a test constant and assert against that constant -- which is exactly what kid 3 did, and the fixture placeholder ids agreed with the deliverable and with nothing else. This node closes it by making the node file, not the test constant, the source of the strings under test, and by adding the live-tree listing that a self-consistent fixture cannot fake.

DISPOSITION: accepted at proved. This is the round's deliverable node; the target hypothesis carries a round-close note naming this block as the only one the Prime should paste and listing the four recorded gaps (gate admits missing visions and a branches cell; an unresolvable parent is UNVERIFIED-and-written; core's three visions are inherited, to be confirmed; season is mint-stamped from AGI_SEASON). Verdicts across the round after review: kid 2 proved, kid 4 proved, kid 1 demoted to inconclusive_lean_proved:75, kid 3 demoted to inconclusive_lean_proved:70.

DEVIATION: none.
<!-- THOUGHT:END -->

PARENT REVIEW: accepted, proved. Parent re-ran the five town test files: 26 passed. The test reads the delivered block out of this node file and executes those exact strings, and lists the vision ids against the live tree -- the delivered artifact and its evidence cannot drift. This is the one block the Prime pastes.
