---
id: verdict:dg2close-born-valid-without-touching-frontmatter
mint_id: 80de4a119d0d42a283962ed9afbe2e71
type: verdict
parents:
  - experiment:dg2close-born-valid-without-touching-frontmatter-check
  - hypothesis:born-valid-without-touching-frontmatter
next_edges: []
confidence: 0.9
edited_by: director-general-2
evidence_runs:
  - experiment:dg2close-born-valid-without-touching-frontmatter-check
scaffold_hash: 1fe3519d713c9428
season: 2
title: "closing (goal:s31 retired): Seed-what-derives plus lift-from-body at done yields schema-valid hypotheses with nothing invented; 96/96 since 09-27 valid (minter-supplied)"
town: core
verdict: proved
---
# verdict:dg2close-born-valid-without-touching-frontmatter

| conjunct / falsifier | observed at HEAD | holds? |
|---|---|---|
| C1 engine-derivable required fields seeded before the file is written | `seed_required` runs in `write_node` before the write (L851); `title` seeded (probe P1) | TRUE |
| C2 kid-held fields go in the BODY and are lifted into frontmatter at completion by the gated write path | `cmd_done` -> `derive_required_from_body` -> `update_node` (cli.py L1818); probe P4-P6; test_cli lift tests green; 11 live kids lifted at their own `done` | TRUE |
| C3 a field in neither population is not invented; it stays absent and stays reported | placeholder prompt not lifted (P3); no-heading body leaves it missing (P7); SCHEMA-WARNING at scaffold and at done; 0 placeholder claims in the corpus | TRUE |
| Prove: `is_complete` distinguishes untouched / filled, before and after the fill | False / True / True (P2/P4/P6) | TRUE |
| Prove: seeding frontmatter leaves `scaffold_hash` byte-identical | unchanged across the lift (P6); `test_seeding_required_fields_does_not_move_the_scaffold_hash` green | TRUE |
| Falsifier: any field filled with a placeholder | 0 in the corpus; placeholder guard live. `title` from the slug is a real value, but opaque on id-slugged nodes (recorded by a01-234c1b05; readability, not validity) | not fired |
| Falsifier: fix requires the kid to write frontmatter | kid touched only the body in the probe; 11 live kids' `testable_claim` equals their body section | not fired |
| Falsifier: required list read from anywhere but the schema registry | `required_fields` reads the registry, and `missing_required` delegates to `schema_registry.validate` | not fired |
| Alive's cite node_writer.py:1589-1604 | the lift table (`_BODY_SECTIONS`, `_PLACEHOLDER_PARAS`). The seed is `seed_required` L1576-1586, called at L851 | approximately right |
| Alive's "96/96 hypotheses added since 09-27 carry testable_claim" | 96/96 schema-valid at add commit and at HEAD, all 5 required fields | TRUE, but it does not measure this mechanism: 71+18 of the 96 carry a minter-supplied value |

Verdict **proved** (0.90). Every conjunct holds on the bytes. No falsifier fires. The probe replays the node's own "what would prove it" end to end. The existing `verdict:scaffolds-are-born-valid-now` (proved 0.97) stands, and this closes the hypothesis's stale `verdict: pending`. It is not 0.97, for two reasons. (a) "Born valid" holds for `testable_claim` at COMPLETION, not at the literal scaffold write. The claim defines it that way, but the headline invites the stronger reading. (b) The 96/96 figure alive quoted is true but comes from a third route: the minter supplies the claim at create. The kid-body lift is evidenced separately, by 11 live kids and the probe.

The node has no `status` field (it carries `verdict: pending`). Wording overlap with goal:g7.33.10.1: the node's "The corpus is a separate population" section explicitly disclaims repairing pre-fix nodes. That remainder (228 pre-gate nodes) is g7.33.10.1 and is not judged here.
