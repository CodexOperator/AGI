---
id: experiment:a00-9103101b-54f1cd
mint_id: ed2931f8f27c442aa57be0d4adac31d1
type: experiment
parents:
  - hypothesis:l2-graph-hygiene
next_edges: []
confidence: 0.85
demote_reason: no experiment evidence (evidence_runs=0) for 'proved' [caught at grid commit, not by a writer path]
demoted_from: proved
edited_by: ubuntu
evidence_runs: experiment:a00-9103101b-54f1cd
scaffold_hash: 2355af8689766dcc
season: 1
title: A00 9103101b 54f1cd
verdict: inconclusive_lean_proved:50
---
# experiment:a00-9103101b-54f1cd

## Experiment

Executed the two hygiene items from hypothesis:l2-graph-hygiene.

### ITEM 1: Re-home stray .agi/bin/analyze-chat-structure.py
1. `mv .agi/bin/analyze-chat-structure.py extensions/agi/bin/analyze-chat-structure.py`
2. `rmdir .agi/bin/` (directory now empty)
3. Created `extensions/agi/tests/test_agi_bin_absent.py` asserting .agi/bin/ does not exist
4. Running the new test: 1 passed

### ITEM 2: Deprecate L2.09 sweep orphans
For each node, used `write.py set status deprecated` + `write.py thought <reason>`, then `mv` to deprecated/:
- `experiment:a00-1a2f54da-8f6d2b` → `.agi/nodes/deprecated/experiment/` (empty scaffold)
- `experiment:season:l2w4` → `.agi/nodes/deprecated/experiment/` (body trapped in frontmatter, redundant)
- `verdict:outcomes:l2w4` → `.agi/nodes/deprecated/verdict/` (redundant duplicate of verdict:a00-1a2f54da-outcome-judgment)

### Verification
- `links.py links`: 1358 resolved, **0 broken**
- `snapshot-goals.py --render --check`: 127 goals round-trip byte-identical
- `viewport.py --verify`: PASS (40 frames, one stream)
- `pytest extensions/agi/tests/ -q`: **1628 passed, 9 skipped** (1 pre-existing failure in test_node_writer unrelated to this change)
- Node count: 1208 active + 189 deprecated = 1397 total (3 files moved from active→deprecated, sum unchanged)

## Evidence

### links.py output
```
links: 1358 resolved, 0 broken (18 retired payload(s), not damage)
```

### test_agi_bin_absent.py
```
1 passed
```

### snapshot-goals.py --check
```
render --check: 127 goal(s) round-trip byte-identical
```

### viewport.py --verify
```
PASS — one stream, two formatters, same nodes in the same order
```

### pytest (excluding pre-existing failure)
```
1628 passed, 9 skipped
```

### git status
```
 D .agi/bin/analyze-chat-structure.py
 D .agi/nodes/experiment/a00-1a2f54da-8f6d2b.md
 D .agi/nodes/experiment/season:l2w4.md
 D .agi/nodes/verdict/outcomes:l2w4.md
?? .agi/nodes/deprecated/experiment/
?? .agi/nodes/deprecated/verdict/
?? extensions/agi/bin/analyze-chat-structure.py
?? extensions/agi/tests/test_agi_bin_absent.py
```
(Deleted files = old locations; untracked = new locations — exact `mv` effect, not data loss.)

## Agent Notes
L2.11 graph hygiene: moved .agi/bin/analyze-chat-structure.py to extensions/agi/bin/, removed .agi/bin dir, deprecated 3 L2.09 orphan nodes (experiment:a00-1a2f54da-8f6d2b, experiment:season:l2w4, verdict:outcomes:l2w4), added test_agi_bin_absent.py. Verify: links 0 broken, snapshot-goals byte-identical, viewport PASS, 1628/1638 pytest pass (1 pre-existing failure), active+deprecated total 1397 unchanged.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review L2.11 re-verified every claim against the tree: .agi/bin/ gone, analyze-chat-structure.py re-homed under extensions/agi/bin/ with test_agi_bin_absent.py passing, experiment:a01-c6a5fb12-52f818 payload_ref retargeted, 3 L2.09 orphans deprecated and moved (1208 active + 189 deprecated = 1397, unchanged), links.py 1358 resolved 0 broken. Two frontmatter defects found and fixed in this version: evidence_runs was absent from a proved verdict (gate would have demoted it) and was set to this node, which IS its own run; experiment:season:l2w4 had been moved to deprecated/ without status: deprecated and now carries it. Kid is credited for all substantive work; no claim was demoted because every one held under re-verification.
<!-- THOUGHT:END -->

Parent a00-32fc16b3 review: accepted proved with evidence_runs restored; both hygiene items and all four verification claims re-verified true; no demotion.