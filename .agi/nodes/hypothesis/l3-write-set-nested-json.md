---
id: hypothesis:l3-write-set-nested-json
mint_id: fbee8aac27be42b0afc1961fd4a7bb68
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: ubuntu
scaffold_hash: 1deeeb131febb259
season: 1
testable_claim: write.py set accepts a JSON list or object value for a frontmatter key (coerced through the schema, round-tripped byte-stable), so a nested table such as the ladder roles rows can be written through write.py and the write guard stays silent
title: L3 write.py set nested json
---
# hypothesis:l3-write-set-nested-json

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OBSERVED L3.01 (kid a00-3feeca19, ladder roles table): write.py cannot set a nested roles list, JSON-list coercion is broken, so the kid hand-edited .agi/nodes/.geometry/ladder.md and write_guard.py check now warns unsanctioned write on that file. Second finding from the same kid: dispatch.py's iteration_id parser rejects free strings such as iter-L3.01 (only L3.01 passes), one throwaway attempt errored cleanly. FILES: extensions/agi/bin/write.py (verb_set coercion), node_writer or schema coercion helpers, extensions/agi/bin/dispatch.py (iteration id parser: accept iter-<id> by stripping the prefix, say so in --help), tests. FIX: set KEY <json> parses a value that starts with [ or { as JSON and writes it as a YAML block, round-trip byte-stable; then re-set the ladder's roles through write.py so the guard log carries the file's current bytes and the WARN goes silent (do not change the rows' content). VERIFY: red-first test for a nested list set on a temp node; write_guard.py check silent on this repo afterwards; dispatch.py accepts iter-L3.09 and L3.09 alike. REPORT: one experiment node under this hypothesis, verdict, evidence_runs as a list (pass --evidence-runs), every verify command with its actual output in the body. Do not commit, push, or run grid.py commit.
