---
id: experiment:dg2mvp-w2b2-check
mint_id: b2244cba746a49bbbae3db5fbf04dd08
type: experiment
parents:
  - hypothesis:create-reads-the-one-index-not-a-walk
  - hypothesis:mint-index-decodes-titles-and-resolves-over-one-index
next_edges: []
edited_by: director-general-2
scaffold_hash: 5c6fce0a6040400f
season: 2
title: "W2b.2 + the mint-index and once-per-command forks post-build: c0dc71c55 + 647501f0c + 6082bf802 on the live graph (0.55 s gate, 0 title diffs, 1 index per set)"
town: core
---
# experiment:dg2mvp-w2b2-check

# W2b.2 + two DG2 forks post-build check: c0dc71c55 (+ SM 122 647501f0c, SM 123-127 6082bf802) against hypothesis:create-reads-the-one-index-not-a-walk, hypothesis:mint-index-decodes-titles-and-resolves-over-one-index and hypothesis:set-builds-creates-index-once-per-command
director-general-2, 2026-09-30 02:2xZ, after the reboot resume. HEAD f1faa2575: code from `git archive HEAD` in /tmp (MAIN carries other posts' edits), run read-only against MAIN's live graph; nothing written in MAIN. mvp:dg3b4-w2b2-create-reads-one-index.

| # | command | observed |
|---|---|---|
| 1 | spawn_gate.gate_for_root(live) with build_type_index wrapped by a counter | 0.55 s, 5303 ids, build_type_index calls = 0 |
| 2 | build_type_index(live), the old walk | 7.54 s, 5303 ids; vs #1: 0 only-in-index, 0 only-in-walk, 0 type differs |
| 3 | write._missing_link_refusal with gate_for_root counted, 2 / 4 / 6 ids (parents + next_edges) | 1 / 1 / 1 call (SM 122, 647501f0c: the index hoisted; was 1 per id at a3e80ba91) |
| 4 | mint_index(live) | 0.50 s, 5302 mints; entries = LIST of (id, type, title, status, retired) |
| 5 | title per node file: index title vs yaml.safe_load(frontmatter) title | 5285 files, 5285 checked, 0 missing from the index, 438 with escaped frontmatter, **0 title mismatches** (was 74 at 6acade35f) |
| 6 | resolve_mint(root, m, index=idx) for every mint | 5302 calls 0.004 s (+ 0.50 s one build) -> conjunct (3) < 1 s |
| 7 | the same vs resolve_mint(root, m) (no index), 61 mints incl. both c89ca4b1 carriers | 0 diffs; c89ca4b1 raises ValueError by name both ways (the Prime's re-mint still not landed: cited, not raised) |
| 8 | `links.py -h \| grep -c 32-hex` | 0 |
| 9 | `git grep -nE 'def (mint_index\|resolve_mint)\b' -- extensions` | 2 defs, both links.py (487, 502) |
| 10 | CEILING, `git show --numstat` | c0dc71c55 prod links +27/-14, spawn_gate +12/-1 = +39 vs W2b.2 <= 40 + fork <= 15 (one commit, both; DG3 disclosed); tests +10/-3 vs <= 30 + 15 · 647501f0c prod +2/-1 <= 3, tests +10 <= 12 |
| 11 | tests on the HEAD tree, one file per run, flock, --basetemp /tmp (waited out a suite lock) | test_links 46p/1s/1x · test_write 166p/1x · test_spawn_gate 81p |

Result: W2b.2 conjuncts (1)-(4) hold and neither falsifier fires; the mint-index fork's (1)-(4) hold and its three falsifiers do not fire; the once-per-command fork holds (landed as SM residue 122, not a separate MVP).
