---
id: hypothesis:l2w1-experiment-payload
mint_id: f18251da0e4948bd900d864282191a56
type: hypothesis
parents:
  - goal:g12.3
next_edges: []
edited_by: director
scaffold_hash: c2f9ccdd6efc4bfc
testable_claim: "[experiment].md declares payload_ref and location so an experiment node can carry a file the way a build node does"
thought_session: agi-master-2026-09-06
title: "L2 wave 1: l2w1-experiment-payload"
---
# hypothesis:l2w1-experiment-payload

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
FILE: .agi/context/schemas/[experiment].md, only this file; do not edit write.py, wave 2 owns it. CHANGE: fields gain payload_ref (str, path relative to location, same meaning as in [build].md) and location (str; source_root by default, or graph_root, repo_root, or any key under locations in the project config). Neither required. Body: experiments are build nodes in practice (section 1, parent seam): the tier-0 unit is an experiment whose payload is written through the node's own write operation. Copy the payload_ref and location wording from [build].md rather than inventing new. VERIFY: links.py schema unchanged for experiment; commands.py run tests green; dry-run python3 extensions/agi/bin/write.py create experiment probe --parent hypothesis:l2w1-experiment-payload --payload /tmp/probe.txt --dry-run and record what it prints; if write.py refuses a payload on a non-build type today, record that as the wave 2 item and keep the claim about the schema file only. Section 1. REPORT: write one experiment node whose parents is this hypothesis, with a verdict on the testable claim; evidence_runs must be a list of node ids, your own experiment node counts once it exists; list every verify command and its actual output in the body. Edit only the file or files named here. Do not commit, do not push, do not run grid.py. If git status shows files you did not create, report them and never touch them. Design source, read the named section before editing: .agi/context/season-ladder-and-morals-brief.md
