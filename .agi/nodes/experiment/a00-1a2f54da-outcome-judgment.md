---
id: experiment:a00-1a2f54da-outcome-judgment
mint_id: f98b1c521be144428c4864fced4eaec9
type: experiment
parents:
  - hypothesis:l2w4-outcomes-judged
next_edges: []
scaffold_hash: 3ad9bcd164173e31
season: 1
status: complete
tags:
  - season
  - judgment
title: "Experiment: Season 1 outcome judgments"
---

# experiment:a00-1a2f54da-outcome-judgment

## Experiment

Collected pre-state with `python3 extensions/agi/bin/season.py status` (23 tier-0 outcomes lacked judged_against). Inspected every node under `nodes/outcome/`, traced each chain back to its goal parent (MVP→verdict→hypothesis→idea→goal). Ran `python3 extensions/agi/bin/season.py judge <outcome> --against <goal>` for all 23 outcomes:

```
outcome:cli-invocation-r1 -> goal:g7.1 (lens goal:g7)
outcome:schema-registry-r1 -> goal:g3.2 (lens none, goal parentless)
outcome:schema-registry-r2-bracket-convention -> goal:g3.2 (lens none)
outcome:environment-indexers-r1 -> goal:g6.1 (lens goal:g6)
outcome:session-management-r1 -> goal:g8.4 (lens none)
outcome:session-management-r1-r1 -> goal:g8.4 (lens none)
outcome:graph-core-chain-persistence-r13 -> goal:g1.5 (lens goal:g1)
outcome:exporters-r1 -> goal:g9.3 (lens goal:g9)
outcome:graph-core-r1 -> goal:g1.4 (lens goal:g1)
outcome:renderers-r1 -> goal:g9.4 (lens goal:g9)
outcome:autoresearch-tree-skill-r1 -> goal:g3.5 (lens none)
outcome:chain-engine-r1 -> goal:g9.2 (lens goal:g9)
outcome:a00-1467544f-aaaa25 -> goal:g3.1 (lens goal:g3)
outcome:a00-5510b3ee-67fb62 -> goal:g13.1 (lens goal:g13)
outcome:embeddings-r2 -> goal:g11.2 (lens none)
outcome:embeddings-r3 -> goal:g11.2 (lens none)
outcome:a00-c8365a0c-85a6d1 -> goal:g4.3 (lens goal:g4)
outcome:a00-ddbe3410-outcome001-chain-bootstrap -> goal:g2.1 (lens goal:g2)
outcome:a00-ddbe3410-outcome002-structural-repair -> goal:g2.1 (lens goal:g2)
outcome:a00-ddbe3410-outcome003-iterative-traversal -> goal:g2.1 (lens goal:g2)
outcome:a00-fd594bfd-ad6af8 -> goal:g13.1 (lens goal:g13)
outcome:writers-routed-post-wire-and-cli -> goal:g4.2 (lens goal:g4)
outcome:environment-indexers-r1 -> goal:g6.1 (lens goal:g6)
```

Re-ran `season.py status` to confirm 0 outcomes lacking judged_against. Verified `python3 extensions/agi/bin/links.py links` (1331 resolved / 0 broken) and `python3 -m pytest extensions/agi/tests/ -q` (1622 passed, 9 skipped).

Recorded pre/post outputs under Evidence.

## Evidence

- `season.py status` before: 23 report(s) with no judged_against field (Tier 0)
- `season.py status` after: same counts, but orphan report line absent (0 missing judgments)
- `links.py links`: 1331 resolved, 0 broken
- `pytest extensions/agi/tests/ -q`: `1622 passed, 9 skipped`
- `season.py judge` per-outcome outputs (see Experiment block list)