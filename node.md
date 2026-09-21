---
id: experiment:a00-7dd33198-e1bb25
mint_id: 57c2cbab18c249d6b3c0f97c5118e387
type: experiment
parents:
  - hypothesis:l4-the-formation-owner-writes-config-posts-rows-and-the-town-master-cell-through-a-schema-declared-actor-row-grant-never-a-role-literal
next_edges: []
confidence: 0.9
edited_by: director-sanctuary
evidence_runs:
  - experiment:a00-7dd33198-e1bb25
line_ceiling: 40
loop: hypothesis:l4-the-formation-owner-writes-config-posts-rows-and-the-town-master-cell-through-a-schema-declared-actor-row-grant-never-a-role-literal@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": "the sanctuary-master seat edits posts rows and their quiet/town cells, INCLUDING its own row -- a field-level exemption, not special-cased to `town` alone", "class": "gate", "cmd": "sanctuary-master sets ONLY its own row's `quiet` field (own construction, a field the parent's own SM.115 probe never used) via write.submit on a fresh fixture", "expected": "ADMITTED (quiet is in the actor_rows grant's fields list; the field-level fix must generalise past the one field the parent's falsifying probe happened to name)", "observed": "res.status == 'updated'", "result": "admitted"}
  - {"conjunct": "any other seat is refused BY NAME -- a DIFFERENT declared actor_rows actor (master-sensei, whose own entry does not cover `posts`) may not smuggle a write to sanctuary-master's row", "class": "auth", "cmd": "actor='master-sensei' sets sanctuary-master's row `quiet` field to a marker string, on a fresh fixture", "expected": "refused by name; the marker string never lands", "observed": "EditError: actor_rows entry for 'master-sensei' declares no shape this resolver reads (its entry is list_key=templates/role_field=id, no match_key -- the SM.108 defect-3 refusal fires against a posts edit); posts.md never carries the marker", "result": "refused"}
  - {"conjunct": "the fix is reachable through the REAL write.py CLI entry point, not just the in-process write.submit() call every test in this file uses", "class": "wire", "cmd": "subprocess.run(['python3', 'extensions/agi/bin/write.py', 'config:posts', 'set posts <json>', '--root', fixture_parent, '--actor', 'sanctuary-master']) -- own-row town-alone edit, via the actual CLI subprocess, not a Python import", "expected": "rc=0, town lands in posts.md", "observed": "rc=0, stdout 'updated: config:posts', '\"town\": \"core\"' present in posts.md afterward", "result": "wired live through the CLI, not just the library call"}
production_lines: 3
profile: balanced
role: kid
scaffold_hash: b7987d2cd5756517
season: 2
title: "SM.115b: the actor-rows own-row exemption is field-level (self_row fields exempt, every other own-row field still grant-checked)"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-7dd33198-e1bb25

## Experiment

SM.115b corrective on `extensions/agi/bin/write.py` `_actor_rows_refusal`.

SM.115 (previous round) fixed the live rotation-blocking regression by
skipping the WHOLE `actor_rows` grant entry whenever every changed row was the
actor's OWN row (`continue`). The parent's adversarial probe showed that was
too broad: it made `town`/`quiet`/`status`/`role`/`tier`/`model`/`effort`/
`rotated_by`/`harness`/`settings` UNREACHABLE on the actor's own row, because
`self_row` does not declare them and the entry-level skip stopped `actor_rows`
from being consulted for that row at all. Pre-fix, `sanctuary-master` setting
ONLY its own row's `town` was ADMITTED; post-SM.115 it was REFUSED.

Fix: replaced the entry-level skip with a FIELD-LEVEL exemption.

1. Read `schema.frontmatter["self_row"]["fields"]` once per matching entry
   (`self_row_fields`, empty list when absent/non-dict).
2. In the EXISTING per-field check inside the set/create loop, added ONE more
   exemption: do NOT refuse when `str(name) == seat` (the CURRENT row is the
   actor's own) AND the field `f` is in `self_row_fields`.
3. Deleted the `changed` / `all(...)` / `continue` block entirely.

Every other own-row field still goes through the pre-existing `f not in fields`
check unchanged, so `town` etc. (already in the grant's `fields`) remain
admitted on the own row exactly as on any other row, and a field in NEITHER
list (`owning_goal`) still refuses by name.

## Evidence

Production diff: `git diff --numstat -- extensions/agi/bin/write.py` = `12  9`
(12 added, 9 removed) -> net 3 production lines, ceiling 40.

Five-file suite (the SM.108 / SM.115 set):

```
python3 -m pytest extensions/agi/tests/test_write_actor_rows.py \
  extensions/agi/tests/test_write_master_sensei.py extensions/agi/tests/test_write.py \
  extensions/agi/tests/test_write_self_row.py extensions/agi/tests/test_town_cell_write.py -q
157 passed, 96 warnings in 1.97s
```

New tests added to `test_write_actor_rows.py` (all pass):

- `test_own_row_town_field_alone_still_admitted` — the parent's falsifying
  probe made permanent: own row sets ONLY `town` -> UPDATED, value lands.
- `test_own_row_town_plus_identity_cells_admitted` — MIXED own-row edit:
  `town` (actor_rows) AND `session_id` (self_row) in one write -> both land.
- `test_own_row_field_in_neither_list_still_refused` — `owning_goal` on the
  own row (in neither list) still refuses by name, and nothing lands.

All three SM.115 tests stay green: `test_own_row_spawn_write_admitted`,
`test_other_row_still_limited_to_actor_rows_grant`,
`test_rotate_identity_writer_own_row_admitted`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Director confirmation layer over the parent (a00-ec12fb27) own rigorous review, which already ran 3 fresh adversarial probes with no reused test code. Independently re-ran the 5-file suite (157 passed, matches) and measured the cumulative write.py diff from HEAD (12+/1-, includes both SM.115 and this corrective). The parent own review is sound and thorough; accepting its verdict as delivered. Harvesting SM.115 + SM.115b together as one commit per the parent own harvest report (accepted=2, demoted=0).
<!-- THOUGHT:END -->

## Evidence

## Agent Notes
Replaced SM.115's entry-level own-row skip with a field-level exemption: self_row.fields are exempt on the actor's own row, every other own-row field still goes through the actor_rows fields check. Town-alone own-row edit admitted again; town+session_id mixed edit admitted; owning_goal (neither list) still refused by name; all three SM.115 guards green. 12/9 diff = net 3 production lines vs ceiling 40; five-file suite 157 passed.

tier-parent review a00-ec12fb27 iter115: 3 adversarial probes (gate/auth/wire) run against fresh fixtures with no reuse of the kid's own test code -- own-row `quiet`-alone edit admitted (generalises past `town`), a different actor_rows actor (master-sensei) refused attempting sanctuary-master's row, and the real write.py CLI subprocess (not the in-process call) lands the own-row town edit. All three held. Accepted as proved. This closes the SM.115 sub-thread: SM.108 (field/create/top-level-key residues) + SM.115 (own-row identity cells) + SM.115b (own-row grant fields restored, field-level not entry-level) together now hold the target hypothesis's full claim against every probe run across all three review rounds on this branch.
