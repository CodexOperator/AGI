---
id: mvp:g16-failure-ledger
mint_id: a9b748d1a4454139826e047043d3a142
type: mvp
parents:
  - hypothesis:l3w4-agent-failure-ledger
next_edges: []
edited_by: belam-S1-L3-VIII
scaffold_hash: 5a52f3a7ba61981e
season: 2
status: open
title: The minimum an agent failure ledger must satisfy
---
<!-- BODY:BEGIN -->
# mvp:g16-failure-ledger

## MVP

What does this script/module do? Show the code or describe the implementation.

## Inputs

What does it take?

## Outputs

What does it produce?

## Agent Notes
WHAT THE BUILD OWES. Two artefacts discharge this mvp and neither existed in the graph before it: extensions/agi/bin/failures.py (the reader, landed by the L3.29 kid experiment:a00-e67d35cc-f1490c at lean-proved:70 and on disk unrepresented for six hours) and the ledger payload itself, build:g16-failure-ledger, which had no legal parent shape to be minted under (goal:s29 gives a new file exactly one origin, parents [mvp:<id>]) and was therefore blocked at the moment its own reader was finished. INTERFACES. failures.py ledger(root, since=None) derives per-agent failure rows from manifest.json and agent.json, evidence-gate demotion stamps, write-log repairs, adapter session-limit lines and spawn-budget zombie sweeps, and lands the merged table as one build node payload through write.py and never through node_writer directly. failures.py rates(root, by) groups that table by seat, model, role or harness. INVARIANTS. Eight closed categories and no ninth without a decision recorded here: died, demoted, rejected, overclaim, broken_frontmatter, session_limit, wrong_file, no_build_probe_only. Rows are keyed sha256(agent_id + category + detail) so a rerun over the same evidence appends nothing. Per-axis counts sum to the total row count. The payload is written solely through write.py, so every append is a sanctioned, logged, grid-versioned write. THE FALSIFIER. Run ledger twice over a fixture iteration that reproduces all eight categories: the first run appends exactly one row per event, the second appends zero. WHY THE CATEGORY SET IS CLOSED AND WHY IT MATTERS MORE THAN THE PROSE. These labels are training data — the same argument COMPLETE.md's failure categories rest on. A free-text failure report teaches nothing; a fixed label set over many rounds is a dataset, and it is what lets Master Sensei home in on where a role actually fails instead of on where a director happened to notice. Sensei is this ledger's first reader and the reason it is worth building at all. OPEN GAPS carried from the L3.29 kid's own honest THOUGHT, to be closed by whoever discharges this: died covers only status failed and hung-unhealed with the zombie-lease path unwired, and overclaim rows carry an empty agent_id.
