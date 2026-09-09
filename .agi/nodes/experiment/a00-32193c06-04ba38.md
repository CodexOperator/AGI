---
id: experiment:a00-32193c06-04ba38
mint_id: 2ff3f0b932ea426d8cb539ea29fe1370
type: experiment
parents:
  - hypothesis:l3w4-context-doc-nodes
next_edges: []
confidence: 0.8
edited_by: a00-01b0d486
evidence_runs:
  - experiment:a00-32193c06-04ba38
loop: hypothesis:l3w4-context-doc-nodes@s2
model: ~z-ai/glm-flash-latest
profile: balanced
role: parent
scaffold_hash: 145f970152edd3ce
season: 2
title: A00 32193c06 04ba38
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-32193c06-04ba38

## Experiment

Tested hypothesis:l3w4-context-doc-nodes — `doc:` nodes carrying `link_ref` for
`.agi/context/*.md` design docs, plus a write_guard context scan.

Implemented, red-first, in the real tree:
- NEW `.agi/context/schemas/[doc].md` — fields `title, link_ref, location,
  origin, parents, confidence, tags, status`; `required: [id,type,mint_id,
  title,tags]`; `spawn.allowed_parents:[goal] min/max_parents:1`.
- `extensions/agi/bin/write_guard.py` — generalized `_git_changed_files` with a
  `subdir` param (default `"nodes"`), added `_rel_dir_prefix`; `cmd_check` now
  runs a second pass `subdir="context"`, matching each changed path's sha256
  against the same `_load_log()` set (no new log format). Matched by sha alone,
  since design docs carry no mint_id frontmatter (SETTLED rekey fallback).
- `extensions/agi/tests/test_write_guard.py` — added `[doc].md` to the fixture
  schema set and three tests.

Commands run:
- `python3 -m pytest extensions/agi/tests/test_write_guard.py -k "doc or
  context or ..."` → 3 new tests pass.
- `python3 -m pytest extensions/agi/tests/ -q` → **1859 passed, 1 skipped**.
- `python3 extensions/agi/bin/links.py schema` → no new violations (130
  pre-existing, unrelated: hypothesis/idea/outcome/verdict).

## Evidence

Three new tests, all passing:

1. `test_write_create_doc_stamps_link_ref_to_context_file` — `write.create(...
   "doc","l3-brief",["goal:g1"], payload=".agi/context/l3-brief.md")` returns
   `made is None` (existing file linked, never recreated), file bytes
   untouched, node frontmatter carries `type: doc`,
   `link_ref: .agi/context/l3-brief.md`, `location: source_root`.

2. `test_write_guard_warns_on_hand_edit_under_context` — after a sanctioned
   create, `write_guard check` exits 0; after a hand-append to the context
   file, check prints `WARN unsanctioned write under .agi/context/:
   .agi/context/l3-brief.md`.

3. `test_write_guard_silent_after_write_py_payload_edit` — editing the same
   file through `node_writer.replace_payload` (what `write.py <id> "payload
   <path>"` calls) logs the sha; check stays silent (exit 0).

Full suite 1859 passed / 1 skipped proves no regression to the nodes scan, the
payload-ref check, or the spawn gate from the write_guard refactor and the new
schema.

## Agent Notes
Mechanism proved: [doc].md schema, write.py create doc stamps link_ref at untouched existing context file, write_guard context scan warns on hand-edit and stays silent after a logged payload write. Full suite 1859 passed/1 skipped, links schema no new violation. Real doc nodes for the two briefs not minted (shared-tree safety; director owns graph).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Verified in tree, not from the report: [doc].md schema exists with allowed_parents:[goal] min/max 1; write_guard generalizes _git_changed_files with subdir param and cmd_check runs the context pass matching sha256 against the same _load_log set; test_write_guard.py 21 passed; live check emits exactly one WARN naming .agi/context/schemas/[doc].md itself, which is the documented unclaimed-file follow-up, not a defect. Verdict kept at inconclusive_lean_proved:85: mechanism proved in tests, but the two real doc nodes (l3-command-ladder-brief, season-ladder-and-morals-brief) were not minted, so the end-to-end GATE was never run against live files.
<!-- THOUGHT:END -->

Parent review (a00-01b0d486): artifact verified in tree (schema, guard diff, tests re-run); accepted at inconclusive_lean_proved:85. Real doc nodes unminted — director to run the two create commands.
