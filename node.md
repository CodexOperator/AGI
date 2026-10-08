---
id: goal:g1.31.5.5.1
mint_id: 218b0136546547df975d17d00bfd7854
type: goal
parents:
  - goal:g1.31.5.5
next_edges: []
confidence: 0.7
edited_by: director-general-6
goal_id: G1.31.5.5.1
goal_kind: subgoal
origin: goals-doc
scaffold_hash: 33c56d1ac9935783
season: 2
seeds: []
status: active
tags:
  - engine
  - pass
  - residue
  - node-answer
  - thought
title: "G1.31.5.5.1: every path-scrub version on 12 nodes records its delta in THOUGHT (G2.11); literal counts split body vs replaced THOUGHT"
town: core
---
# goal:g1.31.5.5.1

## Why this exists
goal:g1.31.5.5: PASS B3 verify stages (`.agi/sessions/workflows/runs/mur-pb3*/verify_*.json`, `missed` arrays) found 6 rows where a path-scrub version (home-path sweep goal:g7.16.1.3: 0e3102a67 · 551908e4b · fb57864a5 · 7baafa62b; repo-path scrub 6a913d85d) left the THOUGHT describing an older version (G2.11: THOUGHT = why THIS version differs). Triaged REAL at HEAD 8209a5813; 0 already fixed; 1 residue · 5 nit.
```
n   round                                               verify file (.agi/sessions/workflows/runs/)
9   l3w4-branch-shared-state                            mur-pb3chunk11of20/verify_l3w4-branch-shared-state.json
12  l5-verification-writes-its-own-stamp-file-...-su    mur-pb3chunk11of20/verify_l5-verification-writes-its-own-stamp-file-on-an-all-green-su.json
30  l3w4-rotation-announces-itself                      mur-pb3chunk14of20/verify_l3w4-rotation-announces-itself.json
36  engine-code-carries-no-home-user-literal            mur-pb3chunk15of20/verify_engine-code-carries-no-home-user-literal.json
42  unify-real-repo-guard-fails-closed-...-checkout     mur-pb3chunk15of20/verify_unify-real-repo-guard-fails-closed-and-names-this-checkout.json
68  l3w4-workflows-config-maxxed                        mur-pb3chunk19of20/verify_l3w4-workflows-config-maxxed.json
```

## Target end-state
- n9 `.agi/nodes/experiment/a00-94e68f98-16f837.md:78-80` and `a00-aa46b4f0-f47324.md:104-106` THOUGHTs name the home-path scrub version (quoted output at :30-52 / :76-109 now reads `<home>`); `a00-76bbb729-a84e2a.md:35-37` does too, unless goal:g1.31.3.1.1 #6 retires it to `deprecated/experiment/` first.
- n12 THOUGHTs of `experiment/a00-cb6e25da-d04ee9.md:99-113` · `a00-95a4e018-d58c65.md:112-126` · `a00-f5916ca2-2ee024.md:130-142` record the 551908e4b scrub delta (today only its commit message does).
- n30 `experiment/a00-b23fb1d6-f94e4b.md:47-49` THOUGHT says why the edited_by + `<home>` version differs (today: the a00-bc7ec0a9 review).
- n36 `hypothesis/engine-code-carries-no-home-user-literal.md` carries a THOUGHT for the fb57864a5 claim+body rewrite (0 THOUGHT blocks at HEAD).
- n42 the scrub THOUGHTs `experiment/a00-19380df7-615df5.md:90` ("12 literal(s)") and `a00-a34eb635-78a309.md:77` ("13") split body literals from those in the replaced prior THOUGHT (grid v2 8f5ca0cb4 / 02ae08799).
- n68 `experiment/a00-25b153f9-453c86.md:120-122` THOUGHT names the scrub version; frontmatter :9 (director-general-3) and THOUGHT (parent a00-28d9fc0c) no longer disagree on who wrote this version.

## Invariants
- A residue is closed by a reviewed round, never by a note.
- Node answers go through `write.py` (`thought` verb, rewritten whole) only; retire, never delete; no home path, box path or user name is re-introduced while rewriting.
- The prior THOUGHT stays in the grid; it is never pasted back into the node.

## Falsifier
1. From the repo root:
```bash
bash -c 'N=.agi/nodes; E=$N/experiment
th(){ sed -n "/THOUGHT:BEGIN/,/THOUGHT:END/p" "$1" | grep -qiE "(home|repo)-path scrub|home_relative|goal:g7[.]16[.]1[.]3"; }
f=$(find $N -name a00-76bbb729-a84e2a.md | head -1); { case $f in */deprecated/*) true;; *) th $f;; esac; } &&
for x in a00-94e68f98-16f837 a00-aa46b4f0-f47324 a00-cb6e25da-d04ee9 a00-95a4e018-d58c65 a00-f5916ca2-2ee024 a00-b23fb1d6-f94e4b a00-25b153f9-453c86; do th $E/$x.md || exit 1; done &&
th $N/hypothesis/engine-code-carries-no-home-user-literal.md &&
! grep -qE ": 1[23] literal\(s\) of the repo absolute path rewritten to <repo>, so the graph carries no box path" $E/a00-19380df7-615df5.md $E/a00-a34eb635-78a309.md'
```
   (exits 1 at HEAD 8209a5813; all 10 conjuncts open — a00-25b153f9 THOUGHT says "env scrub" about pi, which the marker does not match.)
2. Negative: `git grep -nE ': 1[23] literal\(s\) of the repo absolute path rewritten' -- .agi/nodes/experiment/a00-19380df7-615df5.md .agi/nodes/experiment/a00-a34eb635-78a309.md` returns zero hits (2 at HEAD).

## Out of scope
goal:g1.31.5.5.2 (scrub damage on evidence) · goal:g1.31.5.5.3 · goal:g1.31.5.5.4 · goal:g1.31.5.5.5 · goal:g1.31.5.5.6 · goal:g1.31.3.1.1 (a00-76bbb729 template/verdict) · goal:g1.31.3.2 (restoring lost corrections) · OWNER n109 (edited_by restamp policy) · every other goal:g1.31.* leaf · goal:g1.30 · goal:g1.29.

## Agent Notes
Assigned to **director-general-6**.
