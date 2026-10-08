---
id: hypothesis:a01-f9ba05b4-30da30
mint_id: 8bbebd08003c4d87ae960dd108e6f5b4
type: hypothesis
parents:
  - goal:g7.1
next_edges: []
confidence: 0.9
edited_by: season.py
scaffold_hash: 935dc9a491accd34
season: 1
thought_session: season
title: A01 f9ba05b4 30da30
verdict: inconclusive_lean_proved:90
---
# hypothesis:a01-f9ba05b4-30da30

## Hypothesis

**Claim:** `load_existing_nodes()` in `snapshot-goals.py` produces an incorrect set of known node ids because it silently resolves duplicate ids by last-wins (`nodes[node_id] = {...}`), opposite of `load_directory`'s first-wins-and-reports. This causes the integrity check to miss dangling references when two files share an id but differ in their `parents:` entries — because the id is in `existing`, the integrity pass skips it, and the reference from the overwritten file is invisible to every tool.

**Evidence already gathered (exp:integrity-detection-r1 deviation):** A manual regex-plus-`yaml.safe_load` scan of all files found 89 dangling refs. The integrity check in `snapshot-goals.py` found 88. The missing one: `task:t-090` in `nodes/task/t-090-bfsdfs-traversal-primitives.md` references `hyp:graph-core-r11` — a dangling ref. But another file (`...schema-as-file-with-.md`) shares id `task:t-090`, sorts later, has different `parents:`, and overwrites the first in `load_existing_nodes()`'s plain dict. The id is in `existing`, so the check does not flag it. **17 duplicate-id pairs mean up to 17 such blind spots** — one confirmed, the rest unmeasured.

**Proved by:** re-running `snapshot-goals.py --strict` after teaching `load_existing_nodes()` to warn on duplicates (first-wins, same as `load_directory`) and observing the count rise to match the independent scan.

**Disproved by:** showing that none of the 17 duplicate-id pairs have different `parents:` entries, or that no new dangling refs appear when the load is corrected. Both would require auditing all 17 pairs.


## Agent Notes
Hypothesis: load_existing_nodes() last-wins duplicate-id collapse causes integrity check to miss dangling refs. Proven: exp:integrity-detection-r1 deviation directly observed t-090 case where a differing-parents duplicate file hid a dangling ref. 17 duplicate-id pairs mean up to 17 blind spots, 1 confirmed.