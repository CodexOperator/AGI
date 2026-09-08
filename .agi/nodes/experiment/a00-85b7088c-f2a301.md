---
id: experiment:a00-85b7088c-f2a301
mint_id: 57baa3c868c44838bdf03473b4be5520
type: experiment
parents:
  - hypothesis:l3w4-seat-graph-view
next_edges: []
confidence: 0.8
edited_by: a00-1252ec68
evidence_runs:
  - experiment:a00-85b7088c-f2a301
loop: hypothesis:l3w4-seat-graph-view@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: fc181a8dcf03eb49
season: 2
title: "\"Round 2 — the layered agent-hierarchy / graph map with toggle\""
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-85b7088c-f2a301

## Experiment

ROUND 2 of hypothesis:l3w4-seat-graph-view — the LAYERED MAP (owner's fuller
design, HANDOFF item 42): the agent hierarchy view AND the graph view, as two
layers over one structure, one keypress swapping which is on top, the layer
beneath "just peeking around". Round 1 landed the base layer (seats inline on
their node via OccupantIndex); this round is the second layer and the switch.

Built in `bin/viewport.py` (221 insertions + 8 deletions, additive):

- **THE TIE IS THE POINT — now rendered.** `build_anchor_index(registry_rows,
  fm_by_id)` reads each seat's `personality_ref` (quorum advisor → its ONE
  vision) and `owning_goal` (director-kid → its ONE perpetual goal) off
  `config:seats`. An anchor only resolves if the node actually exists — an
  unresolvable or absent tie is `unanchored`, never invented. Against the real
  corpus this resolves all seven: adv-* → vision:self-perpetuating /
  all-is-one / alive, and dir-g1/g15/g16 + liaison → goal:g1/g15/g16/g17.
  belam is correctly unanchored (top of the tree, no tie).
- **One `AnchorIndex`, one `layer` — both formatters** (goal:g9.7 one level
  down). `render_human` and `render_llm` take the same optional `anchors` and
  `layer` and state the same facts. Hierarchy lines sort deterministically
  (tier desc, then role order prime_director<parent<director, then name), with
  per-role glyphs: `◆` apex, `◈` advisor, `◎` director.
- **Layer on top renders full; the under-layer peeks faint.** Human: the
  under-layer is `~ `-prefixed so it reads as background in a plain terminal.
  Llm: both blocks are emitted, the top one pointed at by
  `_map_layer_on_top: <layer>` — and the graph frame lines are left untouched
  so `_FRAME_LINE` still parses the ids `--verify` leans on.
- **One keypress toggles:** interactive `m` (or `--layer graph|hierarchy`)
  swaps which layer sits on top. Status line shows `layer_top=<layer>`.
- **Livestream-safe:** no pane ever renders a secret; the round-2 block
  references no key/token/authorization/.env/password surface (a dedicated
  test scans for it). Read-only throughout — the seats registry is read, never
  written; `rotate.py` untouched.

ACTUAL OUTPUT, `--live` (real corpus, measured):

human (`--layer hierarchy`, top of frame):

```
agent hierarchy  (tier · role · → graph anchor)
◆ belam  prime_director  tier3  (unanchored)
◈ adv-alive  parent  tier3  → vision:alive
◈ adv-all-is-one  parent  tier3  → vision:all-is-one
◈ adv-self-perpetuating  parent  tier3  → vision:self-perpetuating
◎ dir-g1  director  tier1  → goal:g1
...
```

llm, the same hierarchy block:

```
## agent hierarchy
- seat belam (prime_director, tier 3) (unanchored)
- seat adv-alive (parent, tier 3) → vision:alive
- seat adv-all-is-one (parent, tier 3) → vision:all-is-one
- seat adv-self-perpetuating (parent, tier 3) → vision:self-perpetuating
- seat dir-g1 (director, tier 1) → goal:g1
- seat dir-g15 (director, tier 1) → goal:g15
- seat dir-g16 (director, tier 1) → goal:g16
- seat liaison (director, tier 1) → goal:g17
_map_layer_on_top: graph_
```

`--verify`: `PASS — one stream, two formatters, same nodes in the same order`.

## Evidence

Six red-first tests in `extensions/agi/tests/test_viewport.py` (40 → 47
passed), all written before the code existed:

- `test_the_tie_resolves_advisor_to_vision_and_director_to_goal` — the falsifier
  that the `personality_ref`/`owning_goal` → node binding resolves.
- `test_a_seat_with_no_tie_is_unanchored_never_invented` — belam (no tie) and a
  dangling `vision:GONE` both land unanchored, never fabricated onto a node.
- `test_hierarchy_renders_each_seat_at_its_anchor_both_readers` — the same
  anchors appear in the human pane and the llm pane (g9.7).
- `test_layer_on_top_swaps_which_layer_renders_faint` — graph-on-top makes the
  hierarchy the faint `~ ` under-layer and vice versa; header states the top.
- `test_the_layered_llm_keeps_frame_ids_parseable` — the hierarchy block must
  never break `--verify`'s frame-id scan.
- `test_the_live_map_prints_no_secret` — livestream guard, no creds in round 2.
- `test_the_map_toggle_is_bound_in_the_interactive_tui` — the `m` key exists,
  not just the render path.

RUNS (all green):

- `pytest extensions/agi/tests/test_viewport.py -q` → **47 passed** (was 40).
- `pytest extensions/agi/tests/ -q` → **2045 passed, 1 skipped** (full suite,
  no regressions — round 1's 2015 + 30 across the tree).
- `viewport.py --verify` → **PASS** (g9.7 intact: same frames, same order,
  briefing facts in both; hierarchy is additive, frame lines undisturbed).
- `viewport.py --live --emit human|llm` rendered the hierarchy block with all
  seven anchors resolved against the real corpus.

CAVEAT, recorded honestly: the "peeking" metaphor is approximated as a
`~ `-faint line block beneath the top layer rather than a true overlay — a
plain terminal has no alpha, so "shows through faintly" becomes "rendered
dimmed below, labeled". The llm pane represents the under-layer by annotation
(`_map_layer_on_top`) rather than visual dimming, because its frame lines must
stay `_FRAME_LINE`-parseable. The `m` toggle and `--layer` flag on and off
cleanly with only the two intended files changed.

## Agent Notes
Round 2 layered map landed: agent-hierarchy layer drawn at its graph anchors
(the tie — advisor→vision, director→goal), graph layer, one-keypress swap,
faint under-layer, g9.7 parity, livestream-safe (no secret surface). 7
red-first tests green, 2045 full suite, --verify PASS.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW EDIT (a00-1252ec68, L3.37): I accept this node as the kid wrote it — verdict, evidence and caveats all survive an independent re-run. Why I am adding a version at all: the review must live where the work is. What I checked beyond the report: (1) the seven new tests actually pass and the full viewport suite is green (47 passed); (2) --verify still passes, so the g9.7 one-stream-two-readers invariant the brief forbade breaking is intact; (3) --live --layer hierarchy on the real corpus shows the tie — belam unanchored, three advisors each on a vision node, four directors on their goals — which is the whole point of this round; (4) the diff is additive over two files only, the seats registry is read and never written, rotate.py untouched. Why lean-proved and not proved: nobody has watched the m toggle on a real tty, and the owner has not seen the layered map; that is a human-eye gap, not a test gap, so 85 is the honest ceiling. Nothing demoted.
<!-- THOUGHT:END -->

PARENT REVIEW a00-1252ec68 (L3.37): ACCEPTED at inconclusive_lean_proved:85. Verified independently, not from the report: pytest test_viewport.py 47 passed; viewport --verify PASS; --live --layer hierarchy renders the hierarchy layer with the tie visible (belam unanchored, advisors -> visions, directors -> goals) against the real corpus. Diff additive, two files, no seats-registry write, no rotate.py change, no secret surface. Verdict stays lean-proved rather than proved: the interactive m toggle has never been exercised by a human on a real tty, and the peeking metaphor is a faint-block approximation rather than a true overlay — both honestly recorded in the caveats. evidence_runs is a self-run list; parents resolve; no orphan.