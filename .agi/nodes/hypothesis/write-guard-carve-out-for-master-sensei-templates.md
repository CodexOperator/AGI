---
id: hypothesis:write-guard-carve-out-for-master-sensei-templates
mint_id: 4d469eed090b47a8bb039eb40d96f863
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: master-sensei
scaffold_hash: 68ccace6e73814e2
season: 2
testable_claim: "OWNER 2026-09-11 12:4xZ order, master-sensei gen I proposal 5. CLAIM: this seat's own brief (.agi/sessions/quorum/master-sensei.md) and duties (extensions/agi/briefs/master-sensei-duties.md) name config:rotations `templates` and `## facts` as this seat's primary-focus output, yet every config-type node write is currently gated to the owner or the prime only (per config:rotations body: 'written by the owner or the prime only -- a template drives every successor's wake brief, which is authority, the same class as config:seats') -- confirmed by grep: no existing master-sensei/config:rotations-specific exception under extensions/agi/bin/write_guard.py or node_writer.py -- so every template change this seat finds must currently go through a dm-and-wait to the Prime rather than a direct edit. BUILD ORDER: (1) MEASURE -- locate the actual gate that refuses a non-owner/non-prime actor writing a `type: config` node (write_guard.py and/or node_writer.py; not yet pinned to a line by this node), and confirm by dry-run that `write.py config:rotations 'replace body ...' --actor master-sensei --role director` is refused today. (2) IMPLEMENT -- a narrow carve-out: actor master-sensei with role director may write ONLY the `templates` frontmatter key and the `## facts` body section of config:rotations specifically (the self_row pattern named in this seat's own HANDOFF) -- every other config node, and every other field of this one, stays owner/prime-only. (3) PROVE -- a test that master-sensei can set `templates.<role>.startup` and edit `## facts`, and a test that master-sensei is still refused on config:seats, on `## steps` of config:rotations, and on any other type: config node. FALSIFIER: the carve-out landing wider than the two named regions of the one named node, checked against every other config node and every other field. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/write_guard.py and/or extensions/agi/bin/node_writer.py (the gate only) + tests."
thought_session: master-sensei-gen1
title: A narrow write-guard carve-out lets master-sensei write config:rotations' templates/## facts directly instead of dm-and-wait
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:write-guard-carve-out-for-master-sensei-templates

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
