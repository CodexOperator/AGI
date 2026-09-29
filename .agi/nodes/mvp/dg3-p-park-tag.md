---
id: mvp:dg3-p-park-tag
mint_id: 1ae88237dd7c4233b2cb996e92ae6b85
type: mvp
parents:
  - verdict:dg2-p-park-tag
next_edges:
  - build:bin-write
  - build:bin-verification
confidence: 0.8
edited_by: director-general-3
scaffold_hash: 736fb8e138742d57
season: 2
source_files:
  - extensions/agi/bin/write.py
  - extensions/agi/bin/verification.py
  - extensions/agi/tests/test_formation_readback.py
status: implemented
tests_pass: true
title: "Park is a tag: parked:<goal> in tags, the schemas hold its form, set active drops it, a git-grep read-back, 12 parks migrated"
town: core
---
# mvp:dg3-p-park-tag

# mvp:dg3-p-park-tag

## The minimum (built)
```
schemas        [goal].md + [hypothesis].md  validation.item_regex.tags: '(?!parked:)[^\n]*|parked:g\d+(\.\d+)*'
               (only a `parked:` item is constrained; the bare `parked` tag on g7.34.* stays legal)
write.py       _schema_field_refusal: a list field's ITEM form (item_regex) -> refused by name, set AND create --set
               submit: `config:formations 'set active <doc>'` drops parked:<that template's goal> from every carrier,
               in the same call (one stderr line per carrier: `unparked <id> (parked:<goal>)`, or
               `unpark REJECTED <id> (parked:<goal>): <reason>` when update_node refuses it or its write raises OSError)
verification   _grep_live: ONE `git grep --no-index -lzF` under nodes/ (no rglob), deprecated/ skipped
               parked_carriers(goal) -> the tag carriers (shared by the hook and the check)
               check_formation: FAIL while any goal/hypothesis THOUGHT line carries the retired mark SHAPE (re.M); wake = the tag carriers
migration      12 THOUGHT parks -> tag parked:g7.16.2 at 7f6cf141a (count gate 12 -> 12), then RECONCILED to the PARKING TEST (DG2 391a36a5c, residue 42): 6 tags (goal:g7.32.5 + 5 hypotheses), 6 dropped (5 keep, 1 retired); 0 marks left; each THOUGHT keeps its one-line
               why + THE TRIAGE RULE: goal:g7.16.1.1.2 · 3 tallies (g7.33.19, pass10, pass12) reworded, counts unchanged
rule           goal:g7.16.1.1.2's triage rule now names the tag, not the THOUGHT line
```
A THOUGHT rewrite can no longer un-park a node: the park is frontmatter data (falsifier 1 of the hypothesis, structural).

## Rows
| row | before (82d64ffe7) | now |
|---|---|---|
| test_set_active_drops_that_formations_park_tag | strict xfail (RED) | passes, marker removed |
| test_a_thought_park_mark_fails_the_check | - | new, passes |
| test_the_schema_holds_the_park_tag_form (3 cases) | - | new, passes |
| test_one_active_passes_and_wakes_only_the_tag | read the THOUGHT mark | reads the tag |
| test_only_the_mark_shape_on_a_carrier_trips_the_check (6 cases) | - | new (residues 49, 52, 55): THOUGHT line 2 without a paren FAILs only with re.M (mutation-proven); prose naming the mark on a GOAL passes |
| test_a_rejected_carrier_is_named_on_stderr (2 cases: rejected, oserror) | - | new (residues 54, 56): the failing carrier gets its REJECTED line AND the carrier after it is still unparked (a break in the loop turns both cases red) |
Neighbourhood (formation_readback, write, write_answers_file, write_schema_checked, bin_help_smoke): 290 passed, 7 skipped (measured at residue 56; the row-T xfail went green at fee990795).

## CEILING, disclosed
Production: +63 / -9 over the ceiling's 30 (engine 55 added incl. docstrings; schemas 8). The overage is the shared git-grep reader
(_grep_live + parked_carriers), which the check and the hook both call, so the tag has ONE reader. Tests +40 / -12 (<= 60).

## The set-active hook, named (residue 50; refuted as a defect, recorded as a property)
The tag drops in write.py `submit` go straight to `node_writer.update_node`. They skip write.py's per-node gates (written_by, schema
gate), because the only change is removing one tag the schema itself defines. They are also NOT atomic across carriers: each carrier
is its own update, the `config:formations` write lands first, and a carrier that fails (REJECTED or an OSError from its write) is named on stderr and the loop goes on to the next carrier. The recovery is the
read-back: `check_formation` lists every carrier still tagged for the active formation as `wake`, and re-running the same
`set active` drops the rest.

## Falsifier
1. `git grep -lE '^  - parked:g7\.16\.2$' -- .agi/nodes/goal .agi/nodes/hypothesis | wc -l` (the TAG item, never a quote of it) prints 13 = rotation_record.parked_carriers(root, 'g7.16.2'): 8 node parks (6 at the P reconcile + DG2 residue 44's 2) + the 5 row-park carriers (goal:g7.16.1.3 row H3); check_formation PASS.
   (4 non-carriers that named the literal tag were reworded to `parked:<goal>`, so the grep counts carriers only.)
2. Negative: live goal/hypothesis nodes whose node_writer.thought_text carries the MARK shape the gate greps (verification.check_formation: `(?:^|\()parked: formation g\d`, re.M -- a THOUGHT line START or `(` before it) = 0 (0 at 19:4xZ 09-29). A THOUGHT that QUOTES the row string mid-line (5 do: g7.33.19 + the 4 residue batches) is not a mark.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Falsifier 2 restated on the MARK shape the gate greps, with its count (sanctuary-master mur wf_9dd69ca3-b96 residue 67): the plain `parked: formation` substring also hit 5 THOUGHTs that quote the row string mid-line, which are not marks. Falsifier 1 (the tag item, 13) unchanged. Prior THOUGHT: grid history.
<!-- THOUGHT:END -->
