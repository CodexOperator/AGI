---
id: experiment:a00-852433f1-2975a8
mint_id: 5607a1a2d58c4504b972b7d9f2f32c22
type: experiment
parents:
  - hypothesis:l4-five-unstaffed-seats-specified-none-created
next_edges: []
confidence: 0.85
edited_by: a00-852433f1
evidence_runs:
  - experiment:a00-852433f1-2975a8
loop: hypothesis:l4-five-unstaffed-seats-specified-none-created@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 9ce9f9629eb0240a
season: 2
title: A00 852433f1 2975a8
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-852433f1-2975a8

## Experiment

Ran the L4.27 assignment under `hypothesis:l4-five-unstaffed-seats-specified-none-created`: WROTE the spec doc `doc:l4-five-unstaffed-seats` (`parents: [goal:g17.1]`, the `[doc]` schema allows exactly one parent, a goal) carrying the five role cards — Goal Keeper (Sage), Draft Master, Glitch Master, Research Master, Shael — in the owner's own card grammar (`l4-owner-decisions.md:345-361`), and created NOT ONE seat, launched nothing, gave no row. Did not touch `config:seats` (`.agi/nodes/.geometry/seats.md`), minted no `config` node, touched no file under `extensions/`, `src/` or `skills/`.

Commands run:
- `write.py create doc l4-five-unstaffed-seats --parent goal:g17.1 --actor a00-852433f1 --session L4.57 --set "title=..." --set "tags=[l4, seats, spec, g17.1]"` -> SPAWN-GATE APPROVED (parents=['goal:g17.1'], schema [doc]); created the node with correct id/frontmatter.
- `write.py doc:l4-five-unstaffed-seats 'replace body 1:1 -'` (body content on stdin) -> `updated: doc:l4-five-unstaffed-seats`.
- `python3 extensions/agi/bin/links.py links` -> `links: 1910 resolved, 0 broken`.
- `bash extensions/agi/driver.sh --smoke --max-iters 1` (dry, no dispatch) -> rendered GOALS.md from 159 goals + preamble; `METRIC node_count=1930`, `active_node_count=1736`, `deprecated_node_count=194`; no deletion.

Result: the doc node exists with exactly five cards in the owner's grammar, each field cited or UNSPECIFIED; the three owner-record holes survive intact; no seat/config node exists anywhere (`.agi/nodes/config/` does not exist in this tree).

## Evidence

Verified in `.agi/nodes/doc/l4-five-unstaffed-seats.md`:
- Five card headings and five card grammar lines present: GOAL KEEPER (Sage) `:352,:355,:257`; DRAFT MASTER `:356,:341,:329,:387,:389`; GLITCH MASTER `:356,:329,:341`; RESEARCH MASTER `:356,:370` Q=UNSPECIFIED; SHAEL `:356,:372,:380`. Five `NOT:` lines, each cited (`:357` for the four masters; the Goal Keeper's NOT is `UNSPECIFIED` with its settling question).
- Hole 1 (Research Master, no question): `Q=UNSPECIFIED — the owner introduced the Research Master at :370 and gave it NO question anywhere in the text; the one question that settles it: ...`.
- Hole 2 (Shael, two questions): both recorded — `:356` `Q="What would the owner say?"` and `:372` "Shael's main question is 'Who cares the most about knowing this?'"; states `:372` is LATER (22:48Z vs 22:31Z) and the owner called it "main"; which governs is the owner's to confirm, not picked.
- Hole 3 (policy-master row fate unsettled): config:seats `.agi/nodes/.geometry/seats.md:15` row is "Policy Master", the superseded name of the Draft Master (`:387,:389`); fate banked as Q27 (`l4-owner-decisions.md:435`); changing it NOT this round; row untouched.
- Also recorded: chamber assign/receive (Masters answer to the Keep for assignment and the Council for acceptance, channel B `:356`; the Goal Keeper, being IN the Keep, answers to the Council `:352`); tooling route (`:370`); Council-to-Keep propagation (`:370`); and the closing paragraph that these cards become `seat` node bodies when L4.13 lands the `[seat]` type and are a `doc` today because that type does not yet exist.

`links.py links`: `1910 resolved, 0 broken`. Oath-baseline caveats: `proved` baselines (b) `git diff --stat` and (d) before-smoke active count are NOT confirmable in this worktree — I never ran git (forbidden; it is a shared tree), and I captured the after-smoke count (1736 active) but no pre-snapshot. The true cross-check is done by the point at merge on season/s2.

## Agent Notes
Wrote doc:l4-five-unstaffed-seats (parents goal:g17.1): five role cards in the owner's grammar, all three holes intact, no seat/config created, seats.md untouched, links 0 broken, smoke active=1736. Baselines (b) git diff and (d) pre-count await point merge verification; hence lean not proved.
