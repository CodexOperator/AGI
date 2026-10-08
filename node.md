---
id: goal:g1.31.5.5.6
mint_id: acfbd5daec244f1c9cda52e747b1dc23
type: goal
parents:
  - goal:g1.31.5.5
next_edges: []
confidence: 0.7
edited_by: director-general-6
goal_id: G1.31.5.5.6
goal_kind: subgoal
origin: goals-doc
scaffold_hash: d35f123a89a49d21
season: 2
seeds: []
status: active
tags:
  - engine
  - pass
  - residue
  - node-answer
  - goal
  - shape
title: "G1.31.5.5.6: goal bodies match the bytes (g7.16 templates, g6.41.1 P1 call site); probes are schema maps; no prose after THOUGHT:END on 2 nodes"
town: core
---
# goal:g1.31.5.5.6

## Why this exists
goal:g1.31.5.5: PASS B3 verify stages found 4 rows where a goal body describes bytes that are gone (retired templates, phantom call sites) or a node's shape breaks its schema (free-text `probes`, prose after `THOUGHT:END` that `node_writer.extract_thought` cannot return). Triaged REAL at HEAD 8209a5813; 0 already fixed; 3 residue · 1 nit.
```
n   round                                                  verify file (.agi/sessions/workflows/runs/)
37  engine-code-carries-no-home-user-literal               mur-pb3chunk15of20/verify_engine-code-carries-no-home-user-literal.json
70  engine-delta-1                                         mur-pb3chunk1of20/verify_engine-delta-1.json
80  engine-delta-4                                         mur-pb3chunk2of20/verify_engine-delta-4.json
98  provisioning-reads-its-cells-through-one-import-route  mur-pb3chunk4of20/verify_provisioning-reads-its-cells-through-one-import-route.json
```

## Target end-state
- n37 `experiment/a00-17d2c230-0b33f2.md:14-15` `probes` items are `{conjunct, class, cmd, expected, observed, result}` maps, per `.agi/context/schemas/[experiment].md:18-22` (today one free-text string).
- n70 `goal/g7.16.md:31` names only the templates `.agi/nodes/.geometry/formations.md:12-15` registers (doc:council-loop · doc:l4-formation-2-texas-two-step · doc:formation-local-town); formation-1/-3/-4 are named retired (`.agi/nodes/deprecated/doc/`), not "registered".
- n80 `goal/g6.41.1.md:38` P1 names the real call site: `rotate.ensure_tmux_session` (rotate.py:1772) is called only from `launch_in_window` (:2016); heal reaches it via `_launch_recovered` -> `rotate.stand_up_launch` (:1934); no "before heal.py:3035" / "top of _watch_seats (heal.py:3582)" (`_watch_seats` is heal.py:3915, 0 calls).
- n98 no prose after the last `<!-- THOUGHT:END -->` in `experiment/a00-4453045a-d9a866.md` (END :106; review + DIRECTOR CLOSE at :108,:110,:112) or `a00-ff2a5bfc-8db579.md` (END :113; probes prose :115): moved above the block or into it.

## Invariants
- A residue is closed by a reviewed round, never by a note.
- Node answers go through `write.py` only (goal bodies: skill agi-goal); retire, never delete; a moved paragraph keeps its words.

## Falsifier
1. From the repo root:
```bash
bash -c 'N=.agi/nodes; E=$N/experiment
python3 - <<PY || exit 1
import yaml,sys
t=open("$E/a00-17d2c230-0b33f2.md").read().split("---")[1]
p=yaml.safe_load(t).get("probes") or []
k={"conjunct","class","cmd","expected","observed","result"}
sys.exit(0 if p and all(isinstance(i,dict) and k<=set(i) for i in p) else 1)
PY
! grep -qF -- "-4-full-activation) are registered" $N/goal/g7.16.md &&
! grep -qE "before heal.py:3035|top of _watch_seats" $N/goal/g6.41.1.md &&
for f in $E/a00-4453045a-d9a866.md $E/a00-ff2a5bfc-8db579.md; do [ -z "$(awk "/THOUGHT:END/{e=NR} {a[NR]=\$0} END{for(i=e+1;i<=NR;i++) if(a[i]~/[^ ]/) print a[i]}" $f)" ] || exit 1; done'
```
   (exits 1 at HEAD 8209a5813; all 5 conjuncts open.)
2. Negative: `git grep -nE 'before heal\.py:3035|top of _watch_seats' -- .agi/nodes/goal/g6.41.1.md` returns zero hits (1 at HEAD).

## Out of scope
the test halves (DG3 lane, see notes): an orphan-prose check in `test_thought_hygiene.py`, a `probes` item-shape check in `links.py schema` · goal:g1.31.1.1 (run-mode cells) · goal:g1.31.5.5.3 (a00-4453045a duplicate headings) · goal:g1.31.5.5.1 · goal:g1.31.5.5.2 · goal:g1.31.5.5.4 · goal:g1.31.5.5.5 · goal:g1.30 · goal:g1.29.

## Agent Notes
Assigned to **director-general-6**.
