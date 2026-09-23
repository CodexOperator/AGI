---
id: experiment:a00-571008cf-route-surfaces
mint_id: 512ea8065c784e6088e7f8b813da8b8d
type: experiment
parents:
  - hypothesis:a00-571008cf-60b678
next_edges: []
edited_by: a00-571008cf
line_ceiling: 40
loop: goal:g7.31.3.1@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: b57a0e0e5cff56f2
season: 2
testable_claim: Every cold-seat brief/custom-instruction surface either declares the five pane routes or provably does not; brief.assemble omits them
title: "Round-2 route-surface sweep: only director-belam-duties declares the five; brief.assemble omits them"
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-571008cf-route-surfaces

## Experiment
Round-2 sweep of `goal:g7.31.3.1`: every OTHER cold-seat brief / custom-
instruction surface declares the five pane routes, or provably does not, by
artifact + `file:line`. Round-1 surfaces (grok profile SoT) not redone:
`doc:director-grok-internals.md:152`, `doc:unified-director-brief.md:36`.

## Evidence

### A. `brief.assemble` output (pi/copilot cold-seat brief) — DOES NOT CARRY THE FIVE
Builders are inline text, no route list: `brief.py:_kid:1317`, `_parent:1573`,
`_director:872`, `_prime_director:978`, `_liaison:942`, `_survival_brief:761`,
entry `assemble:2029`. Assembled 5 tiers + 2 survival profiles
(`.agi/sessions/iter-DH.165/a00-571008cf/brief_all.txt`):
```
route-list lines (regex routes:): 0   across all tiers
workflow token count:            0   across all tiers
write/read/send/dispatch/rotate/spawn: scattered English/tool mentions only
```
C3: the assembled brief does NOT list the five; `workflow` is absent entirely.

### B. `extensions/agi/briefs/*.md` (grep -c, word-boundary)
```
file                                      write read send disp  wf rot spawn routes:
director-belam-duties.md                    7    8    2    8    3   6    1   YES L14
prime-director-successor.md                 5    6    6    6    2  11    3   -
commands.stream.fragment.md                 1    3    0    0    5   0    0   -
workflows.geometry.md                       1    1    0    0   14   0    0   -
master-sensei-duties.md                     1    2    0    1    0  10    0   -
sensei-director-duties.md                   2    1    0    6    0   3    0   -
rotations.geometry.md                       1    1    1    0    0   5    2   -
seats.councils.fragment.md                  0    1    0    1    0   0    0   -
crons.services.fragment.md                  1    0    0    0    0   0    0   -
harness-config.fragment.json                1    0    0    0    0   0    0   -
```
Only `director-belam-duties.md:14` declares all five as routes.

### C. `config:rotations` — template text, no route list
Node `.agi/nodes/.geometry/rotations.md`; payload `extensions/agi/briefs/rotations.geometry.md`.
`brief_file`: director `.agi/sessions/quorum/{seat}.md` (node L55, payload L13);
prime `extensions/agi/briefs/prime-director-successor.md` (node L91, payload L17).
Director target `.agi/sessions/quorum/director-belam.md` carries all five tokens
(w8 r9 s2 d10 wf4 rot6 sp2) but NO route declaration (`grep -n routes …` → none).

### D. Other surfaces
`extensions/agi/lib/agent-prompt.md`: read=0, wf=1, no routes line.
`skills/agi/SKILL.md`: all five tokens (wf=10); L60 names `workflow.py` "the
only sanctioned workflow dispatch route" but no single five-name route line.
`.agi/context/`: no route declaration (unrelated `routes` prose only).

## C2 — surfaces missing one or more of the five
`brief.assemble` output (no route list, wf=0); `commands.stream.fragment.md`,
`crons.services.fragment.md`, `harness-config.fragment.json`,
`master-sensei-duties.md`, `seats.councils.fragment.md`,
`sensei-director-duties.md`, `workflows.geometry.md`, `agent-prompt.md` each
lack ≥1 token. Declared five-name route-lists among swept surfaces: 1
(`director-belam-duties.md:14`), joining round 1's 2.

## Result
Sweep exhaustive over the 4 named surface classes + 2 found by grep. Falsifier
HOLDS: `director-belam-duties.md:14` (reached via the rotation `brief_file`
quorum scratchpad pointer, `.agi/sessions/quorum/director-belam.md:1`) declares
all five; the `brief.assemble` output provably does not. Raw dump:
`.agi/sessions/iter-DH.165/a00-571008cf/evidence.txt`.
<!-- BODY:END -->
