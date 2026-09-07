---
id: hypothesis:l2w2-write-owner-and-payload-types
mint_id: cfdadb9f117e4964b59b1eabeb9b0b04
type: hypothesis
parents:
  - goal:g13.1
next_edges: []
edited_by: season.py
scaffold_hash: 67d24f171f7f4eec
season: 1
testable_claim: write.py refuses to create or edit any moral node unless --actor owner, and its payload verbs accept any node whose schema declares payload_ref, not only build nodes
thought_session: season
title: "L2 wave 2: l2w2-write-owner-and-payload-types"
---
# hypothesis:l2w2-write-owner-and-payload-types

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
FILE: extensions/agi/bin/write.py plus tests. RULE 1: create moral and any verb on a moral:* target exit 2 with one line, write.py: moral nodes are hand-edited by the owner only, pass --actor owner (goal:g12), unless --actor is exactly owner; --dry-run is allowed for anyone. RULE 2: the payload and payload_text verbs currently assume a build node; make them accept any target whose schema (context/schemas/[type].md fields) declares payload_ref, so an experiment node can carry its file the way [experiment].md now allows (L2 wave 1); read the round-4 experiment under hypothesis:l2w1-experiment-payload for what the dry-run printed. Nothing else in write.py changes. VERIFY red-first: moral edit without --actor owner refuses, with it succeeds (on a temp graph, never on the real morals); payload_text on a temp experiment node writes the file at its payload_ref; suite green. Section 3, Node shape. REPORT: one experiment node under this hypothesis, verdict on the testable claim, evidence_runs as a list of node ids (pass --evidence-runs to cli.py done, your own experiment id counts), every verify command with its actual output in the body. Engine files are edited in place; suite via python3 extensions/agi/bin/commands.py run tests, green before you report; every new rule gets a test that was red first. Do not commit, push, or run grid.py commit. Report unexpected files in git status and never touch them. Design source: .agi/context/season-ladder-and-morals-brief.md

RE-RUN NOTE 2026-09-06 after L2.06: the first kid tested the current write.py, found no moral guard, and reported disproved without building anything. The claim is about the write.py you leave behind, not the one you found. RULE 2 already holds (experiment:a00-7a301845-e034c0 showed payload_text works on an experiment node with payload_ref), so only RULE 1 remains: implement the owner-only guard for moral nodes in write.py, red-first test, then report proved with evidence_runs.