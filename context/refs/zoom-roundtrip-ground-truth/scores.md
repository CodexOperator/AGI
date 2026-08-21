# Recall scoring — zoom round-trip claim loss

Scored by the opus orchestrator against the pre-registered ground-truth lists.
6 complete round trips (2 subjects x 3 trials). Fresh haiku agent for every
zoom operation; 12 haiku agents total, no shared context.

## Subject A — task:t-005 (n = 14 claims/trial)

| claim | cat | T1 | T2 | T3 |
|-------|-----|----|----|----|
| A-D1 seeded generator | DESC-prose | Y | Y | Y |
| A-D2 rooms | DESC-prose | Y | Y | Y |
| A-D3 connecting corridors | DESC-prose | Y | Y | Y |
| A-D4 floor/wall meshes | DESC-prose | Y | Y | Y |
| A-D5 deterministic per seed | DESC-prose | Y | Y | Y |
| A-D6 id T-005 | DESC-meta | N | N | N |
| A-D7 effort L | DESC-meta | N | N | N |
| A-D8 tier 0 | DESC-meta | N | N | N |
| A-D9 status pending | DESC-meta | N | N | N |
| A-D10 origin build-site | DESC-meta | N | N | N |
| A-P1 no blockers declared | DEP | N | N | N |
| A-F1 src/dungeon/ | PATH | N | N | N |
| A-A1 same seed twice -> identical | ACC | Y | Y | Y |
| A-A2 eyeball in browser | ACC | Y | N | N |

Trial totals: T1 7/14 = 0.500, T2 6/14 = 0.429, T3 6/14 = 0.429.
Subject A overall: 19/42 = **0.452**

Per category (pooled 3 trials): DESC 15/30 = 0.500 (prose 15/15 = 1.000,
metadata 0/15 = 0.000), INV n=0 N/A, DEP 0/3 = 0.000, PATH 0/3 = 0.000,
ACC 4/6 = 0.667.

`src/dungeon/` was already absent from all 3 children files — the path died at
zoom-IN, not at zoom-out.

## Subject B — idea:goal-playable-dungeon-crawler (n = 23 claims/trial)

| claim | cat | T1 | T2 | T3 |
|-------|-----|----|----|----|
| B-D1 root goal for GOALS.md §G1 | DESC | N | N | N |
| B-D2 upgrade dungeon-crawler scene | DESC-prose | Y | Y | Y |
| B-D3 Three.js | DESC-prose | N | N | N |
| B-D4 one node at a time | DESC-prose | N | N | Y |
| B-D5 title "Goal G1: ..." | DESC-meta | N | N | N |
| B-D6 confidence 1.0 / status open | DESC-meta | N | N | N |
| B-P1 town-scene | DEP | N | Y | N |
| B-P2 dungeon-generation | DEP | Y | Y | Y |
| B-P3 damage-logic | DEP | Y | Y | Y |
| B-P4 enemy-ai | DEP | Y | Y | Y |
| B-P5 inventory | DEP | Y | Y | Y |
| B-P6 quests | DEP | Y | Y | Y |
| B-P7 save-load | DEP | Y | Y | Y |
| B-P8 multiplayer-net | DEP | Y | Y | N |
| B-I1 must respect SPEC.md §V | INV | N | N | Y |
| B-I2 §V4 cited by id | INV | N | N | Y |
| B-I3 no lights | INV | N | N | Y |
| B-I4 MeshBasicMaterial only | INV | N | N | Y |
| B-I5 mark §T rows | INV | N | N | N |
| B-F1 GOALS.md | PATH | N | N | N |
| B-F2 SPEC.md | PATH | N | N | Y |
| B-A1 verify in real browser | ACC | N | N | N |
| B-A2 HTTP 200 proves nothing | ACC | N | N | N |

Trial totals: T1 8/23 = 0.348, T2 9/23 = 0.391, T3 13/23 = 0.565.
Subject B overall: 30/69 = **0.435**

Per category (pooled 3 trials): DESC 4/18 = 0.222 (prose 4/9 = 0.444, meta+D1
0/9 = 0.000), INV 4/15 = 0.267, DEP 21/24 = 0.875, PATH 1/6 = 0.167,
ACC 0/6 = 0.000.

## Pooled — both subjects, 111 claim-instances

**Overall recall = 49/111 = 0.441**

| category | recall | n (instances) |
|----------|--------|---------------|
| DESC prose | 0.792 | 19/24 |
| DEP | 0.778 | 21/27 |
| ACC | 0.333 | 4/12 |
| INV citation | 0.267 | 4/15 |
| PATH | 0.111 | 1/9 |
| DESC structured metadata | 0.000 | 0/24 |

## Two-stage diagnosis (where the claim died)

Grep of the intermediate children files shows the invariant citation was carried
into exactly ONE child in all 3 subject-B trials, never into all six:

- T1 child 1: "respecting SPEC.md V4 (no dynamic lights—MeshBasicMaterial only)"
  — note the § sigil already stripped. Summarizer then dropped it entirely.
- T2 child 1: "respecting the Three.js scene constraints (MeshBasicMaterial, no
  lights)" — rule content kept, citation id destroyed at zoom-IN. This is the
  pre-registered "content-without-citation" degradation mode.
- T3 child 1: "Must respect SPEC.md §V4 (MeshBasicMaterial, no lights)" and
  child 4: "Must reference SPEC.md §T rows". Only trial where a citation
  survived zoom-out — and §T still died.

So a parent-level universal ("**Every** chain landing code must respect §V")
becomes a local property of one child at zoom-in, then reads as minority detail
at zoom-out and is discarded. Loss is two-stage and compounding.
