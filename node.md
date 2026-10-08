---
id: experiment:dg2close-born-valid-without-touching-frontmatter-check
mint_id: 73e0191e706b430b920783b1f2086e0d
type: experiment
parents:
  - hypothesis:born-valid-without-touching-frontmatter
next_edges: []
edited_by: director-general-2
scaffold_hash: 7ebb5297c8956d84
season: 2
title: "Closing check: engine seeds the derivable required fields, the kid's body supplies the rest via the done lift, nothing invented (HEAD 2944fa423)"
town: core
---
# experiment:dg2close-born-valid-without-touching-frontmatter-check

Closing measurement of `hypothesis:born-valid-without-touching-frontmatter` at HEAD 2944fa423 (goal:s31 retired 09-30), read-only. Code comes from a `git archive HEAD` tree in /tmp. The census reads bytes with `git show`. The probe runs in a /tmp fixture carrying HEAD's real `context/schemas/`. Scripts are in /tmp/dg2mvp/close31/scripts/ (census.py, route.py, probe.py).

| # | command | observed |
|---|---|---|
| 1 | `git grep -l 'hypothesis:born-valid-without-touching-frontmatter' -- .agi/nodes` | experiments `the-falsifier-and-the-corpus-census` (proved 0.94) -> `verdict:scaffolds-are-born-valid-now` (proved 0.97); replications `a00-b5e72341-2f79b1` (lean_proved:90), `a01-234c1b05-85689f` (lean_proved:85). The hypothesis itself still reads `verdict: pending`, no `status` field |
| 2 | read node_writer.py at HEAD (alive cited 1589-1604) | `write_node` calls `seed_required` BEFORE the write (L851) and prints SCHEMA-WARNING for what remains (L852-856). `seed_required` (L1576-1586) fills only `title`. L1589-1604 as cited is `_BODY_SECTIONS` (L1596, lift headings `testable claim / claim / hypothesis / the claim`) plus the head of `_PLACEHOLDER_PARAS` (L1606). The cite is the LIFT table, and the seed sits at L1576/L851 |
| 3 | read `required_fields` / `missing_required` (L1526-1573) | the required list comes from `schema_registry.load_schemas_from_dir` + `parse_rules`, and validation delegates to `schema_registry.validate`. There is no hand-kept list |
| 4 | read cli.py `cmd_done` L1810-1834 + `_missing_after_lift` L2006 | after the verdict write, `derive_required_from_body` lifts through `update_node` (the gated path), then SCHEMA-WARNING if anything is still missing. rc is unchanged |
| 5 | probe P1 `write_node(hypothesis)` under HEAD `[hypothesis].md` | written; `title='Probe born valid'` seeded; `missing_required=['testable_claim']` + SCHEMA-WARNING (kid-held field correctly absent, not invented) |
| 6 | probe P2/P3 untouched scaffold | `is_complete=False`; `derive_required_from_body` -> `unchanged`: the scaffold prompt is NOT lifted (`_PLACEHOLDER_PARAS`) |
| 7 | probe P4-P6: kid replaces ONLY the body (schema body order, `## CLAIM` + prose), then derive | frontmatter bytes untouched by the kid = True; `is_complete=True`; derive `updated`, `testable_claim` == the kid's prose; `missing_required=[]`; `scaffold_hash` unchanged; `is_complete` still True |
| 8 | probe P7: body prose with no lift-able heading | derive `unchanged`, `missing=['testable_claim']` (stays absent, stays reported) |
| 9 | `git log --diff-filter=A --since=2026-09-27 --name-only -- .agi/nodes/hypothesis \| sort -u` | 96 files (the same 96 when `deprecated/hypothesis` is included) |
| 10 | census.py: each of the 96 at its ADD commit and at HEAD through `node_writer.missing_required` (= `schema_registry.validate` over `[id, type, mint_id, title, testable_claim]`) | born_valid 96/96, head_valid 96/96. Alive's "96/96 carry testable_claim" is confirmed, and the count covers every required field |
| 11 | route.py: born `testable_claim` vs the body's lift-able section | 7 identical to the `## CLAIM` paragraph; 71 a minter-authored value that differs from any body section; 18 with no lift-able heading. Add-commit subjects: director-general-1 x39, director-engine x23, belam x22, … These 96 were valid at birth because the MINTER supplied the field at `write.py create` (the answers route refuses a mint missing a required row, write.py L2159-2163). They are not evidence for the kid-body lift path |
| 12 | kid-path evidence (see l3 key): the 47 `role: kid` hypothesis nodes | 11 post-fix live kids born at their own `done` commit with `testable_claim` == the body section and `edited_by` = the kid; 2 missing (done never named the hypothesis) |
| 13 | `git grep -i -E '^testable_claim: *"?(TODO\|TBD\|placeholder\|What is the testable claim)' -- .agi/nodes` | 0 (no placeholder claims in the corpus) |
| 14 | `runpy.sh … test_node_writer.py` (archive tree) | 110 passed, 3 xfailed, 2 failed: the two live-corpus round-trip walks (`checked=17 > 1000`), which need the full node corpus the archive tree excludes. The s31 tests all pass (`test_a_scaffold_is_born_with_a_real_title_not_a_placeholder`, `…_reported_not_invented`, `…_does_not_move_the_scaffold_hash`, `…_lifts_a_claim_out_of_the_body`, `…_invents_nothing_when_the_section_is_absent`) |
