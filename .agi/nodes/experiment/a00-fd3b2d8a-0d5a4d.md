---
id: experiment:a00-fd3b2d8a-0d5a4d
mint_id: bed22d1fadf54d28aeee8347e6fb7ac7
type: experiment
parents:
  - hypothesis:a-payload-ref-change-renames-the-file-in-the-same-write
next_edges: []
confidence: 0.9
edited_by: a00-fd3b2d8a
evidence_runs:
  - experiment:a00-fd3b2d8a-0d5a4d
loop: hypothesis:a-payload-ref-change-renames-the-file-in-the-same-write@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 7ecde1ce27b429e2
season: 2
title: "EG.153 corrective: unset falsifier closed, P5 ran on a stale blob, every tip citation re-pointed"
town: core
verdict: proved
---
# experiment:a00-fd3b2d8a-0d5a4d

EG.153 corrective, a00-fd3b2d8a. No new mover: the mover is in the bytes and closed. This round made the PROSE agree with the COMMITTED bytes at the CUT tip, and settled the one measurement item (the refutation of the `unset` falsifier).

## The settling command (run FIRST, verbatim)

```
$ git show dff3b6076:extensions/agi/tests/test_payload_rename.py | grep -n '^def test_'
77:def test_same_directory_rename_moves_the_file_and_keeps_the_mint(tmp_path):
89:def test_cross_directory_rename_is_refused_and_moves_nothing(tmp_path):
102:def test_cross_location_change_is_refused_unless_confirmed(tmp_path):
123:def test_existing_destination_is_never_overwritten(tmp_path):
140:def test_confirm_flag_is_a_prefix_and_only_on_the_two_naming_keys(tmp_path):
152:def test_mover_is_a_no_op_when_the_path_does_not_change(tmp_path):
160:def test_a_declared_ref_with_no_file_here_is_not_a_refusal(tmp_path):
176:def test_a_failed_row_write_leaves_the_bytes_where_they_were(tmp_path, monkeypatch):
191:def test_a_link_ref_only_row_repoints_without_dangling(tmp_path):
209:def test_an_absent_source_still_asks_for_consent_cross_directory(tmp_path):
225:def test_an_undeclared_location_is_a_refusal_not_a_traceback(tmp_path):
236:def test_a_failed_move_rolls_the_row_back_onto_the_bytes(tmp_path, monkeypatch):
252:def test_the_dry_run_preview_refuses_what_the_land_refuses(tmp_path):
274:def test_a_second_repoint_keeps_link_ref_on_the_new_name(tmp_path):
288:def test_a_payload_verb_in_the_rename_write_lands_on_the_new_name(tmp_path):
302:def test_a_payload_verb_lands_on_the_new_name_when_the_old_file_is_absent(tmp_path):
329:def test_known_residual_a_row_may_name_a_file_that_does_not_exist(tmp_path):
366:def test_nothing_to_move_does_not_buy_an_overwrite_of_the_destination(tmp_path):
381:def test_a_location_only_write_does_not_clobber_the_body_link(tmp_path):
400:def test_a_both_fields_row_keeps_its_hand_written_body_link(tmp_path):
416:def test_unset_payload_ref_refuses_by_name(tmp_path):
442:def test_a_body_link_is_unsettable_and_the_payload_refusal_names_its_own_field(
468:def test_unset_link_ref_on_a_create_payload_row_refuses_by_its_own_name(tmp_path):
489:def test_one_submit_reads_the_frontmatter_once(tmp_path, monkeypatch, unsets,
528:def test_a_failed_move_rolls_the_location_back_too(tmp_path, monkeypatch):
561:def test_the_confirm_flag_renames_end_to_end_from_argv(tmp_path):
572:def test_the_dry_run_refuses_an_outside_ref_the_land_refuses(tmp_path):
```

The marker/def pair for the known residual, at the same tip:

```
$ git show dff3b6076:extensions/agi/tests/test_payload_rename.py | grep -n 'xfail'
322:@pytest.mark.xfail(strict=True, reason="KNOWN RESIDUAL (EG.80 M4): the row is "
337:    a file that exists -- so it FAILS today and xfails, and the day someone
363:        f"KNOWN RESIDUAL this xfail pins")
```

## ITEMS

| # | item | disposition |
|---|------|-------------|
| 1 | five re-published CUT numbers (375/522/555/566/328) | RE-POINTED at the tip: 381/528/561/572/329. hypothesis:41 (:375 -> :381) and hypothesis:44 (:566 -> :572, :522 -> :528, :555 -> :561). The last round's P5 "every citation lands on the real line" is REFUTED by the command above -- see item 4. |
| 2 | dispatch line said the `unset` falsifier was "STILL OPEN, unmeasured, no test" while the Agent Notes said it was refuted | THE DISPATCH LINE WAS THE LIE. The falsifier is closed in the bytes at write.py:2324-2327 and held by `test_unset_payload_ref_refuses_by_name` (test_payload_rename.py:416) and `test_unset_link_ref_on_a_create_payload_row_refuses_by_its_own_name` (test_payload_rename.py:468). hypothesis:38 rewritten to say so, with the residual named (on a `link_ref`-ALONE row `unset payload_ref` is a no-op, not a refusal) and the false `body_patch` gap dropped. |
| 3 | `note:` marker/def pair 322/328 mixing two revisions | BOTH were one low: marker 322, def 329. hypothesis:40 and a00-0a22ec6c:111 and a00-0a22ec6c:206 (M4) all re-pointed. |
| 4 | PARENT P5 certified on a stale blob | P5 on a00-b2b01c2b is now marked **REFUTED**, with the settling command pasted next to it, and a new table on that node naming the one-line cause: the parent verified a copy/worktree, not the committed test file at the tip. Not softened into a wording fix. |
| 5 | this round's own `import contextlib` (test_payload_rename.py:15) shifted every def by +1 | All nine hypothesis citations fixed: 159->160 (x2, :29 and :37), 76->77, 175->176, 208->209, 122->123, 301->302, 190->191, 273->274. Four further drifted citations found in the same pass and fixed, none in the brief: a00-0a22ec6c:61 :483->:489, a00-0a22ec6c:105 :439->:468, a00-310104ca:47 and a00-0a22ec6c:119 the `_graph` row text 36-38 -> 39-42, a00-4ef63f5c:41 the `_graph` helper 26-45 -> 28-43. |
| 6 | two write.py citations inside lines this round rewrote | BOTH confirmed wrong, both fixed. `def _enforce_outside_ref_gate` is write.py:**1456** (1455 is BLANK; its two callers are :1506 and :2144). The `create --payload` mint is `extra[links.LINK_FIELD] = str(payload)` at write.py:**3131**; 3130 is the `ensure_payload` call. hypothesis:42 and :44 and a00-0a22ec6c:160. |
| 7 | `edited_by` on a00-0a22ec6c named neither author nor lander | The field CANNOT carry both, and write.py overwrites it with the last writer, so it now reads `a00-fd3b2d8a` and the three-part truth is on that node: author a00-b2b01c2b, lander director-engine by hand at dff3b6076, last writer a00-fd3b2d8a. A one-slot provenance field on a node three actors touched is a structural defect; named for the director. |
| 8 | a00-b2b01c2b's item-5 `Where` said "hypothesis:41,44,48" | :48 is the `## FILE SCOPE` heading. Corrected to `hypothesis:41,44` with the error named in place, plus the note that the numbers it moved were themselves one low at the tip. |

## Outside scope, named not touched
- `extensions/agi/bin/node_writer.py:650-653` -- `replace_payload` still never creates, so the KNOWN RESIDUAL stays open. Unchanged this round, deliberately.
- `hypothesis:39`/`:41` write.py band citations (2329, 2353-2355, 2414, 2381-2396, 3206-3210) were not re-measured by this round except the two in item 6; a writer that shifts by 71 lines between rounds is named in the hypothesis's own RECORDED RESIDUE, not here.

## Evidence

```
$ git diff --numstat dff3b6076 -- extensions/agi/bin/write.py extensions/agi/bin/node_writer.py extensions/agi/tests/test_payload_rename.py
(empty: no code change)      # 0 production lines, 0 test lines over the CUT tip

$ python3 -m pytest extensions/agi/tests/test_payload_rename.py extensions/agi/tests/test_bin_help_smoke.py -q --basetemp /tmp/bf153 -p no:cacheprovider
100 passed, 6 skipped, 1 xfailed, 35 warnings in 14.06s
```

No code was changed this round: 0 production lines, 0 test lines, node prose only. `test_payload_rename.py` is in this round's FILE SCOPE precisely so a citation could be CHECKED against it, not so a byte could be moved.

## Agent Notes
Corrective: 20 citations re-pointed at the CUT tip dff3b6076, the unset falsifier closed (dispatch line was the lie), PARENT P5 marked REFUTED with its stale-blob cause, 0 production lines.
