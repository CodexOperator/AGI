---
id: mvp:dg3-p-park-tag
mint_id: 1ae88237dd7c4233b2cb996e92ae6b85
type: mvp
parents:
  - verdict:dg2-p-park-tag
next_edges: []
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
               in the same call (one stderr line per carrier: `unparked <id> (parked:<goal>)`)
verification   _grep_live: ONE `git grep --no-index -lzF` under nodes/ (no rglob), deprecated/ skipped
               parked_carriers(goal) -> the tag carriers (shared by the hook and the check)
               check_formation: FAIL while any THOUGHT carries the retired `parked: formation` mark; wake = the tag carriers
migration      12 THOUGHT parks -> tag parked:g7.16.2 (count gate 12 -> 12; 0 marks left); each THOUGHT keeps its one-line
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
Neighbourhood (formation_readback, write, write_answers_file, write_schema_checked, bin_help_smoke): 280 passed, 7 skipped, 1 xfailed (row T).

## CEILING, disclosed
Production: +63 / -9 over the ceiling's 30 (engine 55 added incl. docstrings; schemas 8). The overage is the shared git-grep reader
(_grep_live + parked_carriers), which the check and the hook both call, so the tag has ONE reader. Tests +40 / -12 (<= 60).

## Falsifier
1. `git grep -l 'parked:g7\.16\.2' -- .agi/nodes/goal .agi/nodes/hypothesis | wc -l` prints 12 (the gated count); check_formation PASS.
   (4 non-carriers that named the literal tag were reworded to `parked:<goal>`, so the grep counts carriers only.)
2. Negative: live nodes whose node_writer.thought_text carries `parked: formation` = 0.
