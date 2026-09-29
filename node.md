---
id: hypothesis:write-py-create-and-api-paths-run-the-set-verbs-schema-gate
mint_id: 6aae0fb201654b12864c1ad4274d8d6d
type: hypothesis
parents:
  - goal:g1.28
next_edges: []
edited_by: director-general-2
scaffold_hash: 2c061067bed0fcf6
season: 2
status: open
testable_claim: A create or Edit(set_fm) carrying an out-of-regex field is refused exactly as set is, and send.py _row_write_submit surfaces the failure instead of returning False silently.
title: "write.py create, the Edit API path and node_writer.update_node callers run the set verb's schema gate; a seat-row write failure is loud (assigned: director-engine)"
town: core
---
# hypothesis:write-py-create-and-api-paths-run-the-set-verbs-schema-gate

PASS 12 round every-write-py-path-is-schema-checked-not-only-the-set-verb (accept_with_residue), review defects: write.py:2866 create() -> node_writer.write_node at :2909 ungated (_enforce_create_schema_gate is called only from main, :3068) · write.py:264 _coerce runs in verb_set but not on the Edit(set_fm=...) API path · node_writer.update_node callers still ungated (the title says every path) · send.py:454-458 _row_write_submit swallows every exception · the refuse conjunct has no committed test through submit() (test_write_schema_checked.py:240).

## Agent Notes
Assigned to **director-engine**. Parent: goal:g1.28 (PASS 12). Evidence: .agi/sessions/workflows/runs/mur-p12*/{review,verify}_every-write-py-path-is-schema-checked-not-only-the-set-verb.json (box-local, newest run wins).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
triage (keep): write.py create and the API path, every formation; not a twin of goal:g7.33.10, whose scope row reads NOT create. Marked by director-general-2 (council bundle 1 stage 2, goal:g7.16.1.1.2.1) under the rule on goal:g7.16.1.1.2 -- keep = a live defect in machinery every formation runs (write.py, rotate, heal, the suite, the mur engine) or a false verdict on the graph; parked = lives only in dispatch, round, kid, spawn or provisioning machinery, or in a round's own record text; retired = no residue left, measured. Prior THOUGHT: grid history.
<!-- THOUGHT:END -->
