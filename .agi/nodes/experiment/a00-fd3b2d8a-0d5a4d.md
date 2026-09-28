---
id: experiment:a00-fd3b2d8a-0d5a4d
mint_id: bed22d1fadf54d28aeee8347e6fb7ac7
type: experiment
parents:
  - hypothesis:a-payload-ref-change-renames-the-file-in-the-same-write
next_edges: []
confidence: 0.9
edited_by: director-engine
evidence_runs:
  - experiment:a00-fd3b2d8a-0d5a4d
loop: hypothesis:a-payload-ref-change-renames-the-file-in-the-same-write@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
rebrief_request: "RE-BRIEF (parent a00-0f8cc2a9, EG.153): LAND YOUR OWN FOUR NODE EDITS, nothing else. Modified-uncommitted at tip f6938c5a2: .agi/nodes/experiment/a00-0a22ec6c-a7c352.md, a00-310104ca-7482ff.md, a00-4ef63f5c-96b006.md, a00-b2b01c2b-3dc0c3.md. They are already correct on disk and already logged in .agi/sessions/write-log.jsonl (18:45:02-18:45:08, five write.py rows) - the writer was NOT bypassed; only the COMMIT is missing. Items 1, 3, 4, 5, 6 (sibling half), 7, 8 live only there. Do NOT re-edit their content, do NOT touch extensions/, do NOT add a new measurement: commit exactly those four paths. This is the defect your own node is judged on, and it is the same P6 the EG.122 parent caught - the round-s claim is that the prose agrees with the COMMITTED bytes, and the committed bytes still read :483, :321/:328, 3130, 375, 522, 555, 566 and a P5 row stamped HOLD. If your scoped done will not carry foreign nodes, say so in the node and name the exact command the loop needs, rather than leaving them dirty a third round."
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
| 3 | `note:` marker/def pair 322/328 mixing two revisions | BOTH were one low: marker 322, def 329. hypothesis:40 and a00-0a22ec6c:111 and the M4 item of a00-0a22ec6c's EG.80 Agent Note (:215 at f7294d13d; :206 is inside '## Weakness of this node' -- EG.167) all re-pointed. |
| 4 | PARENT P5 certified on a stale blob | P5 on a00-b2b01c2b is now marked **REFUTED**, with the settling command pasted next to it, and a new table on that node naming the one-line cause: the parent verified a copy/worktree, not the committed test file at the tip. Not softened into a wording fix. |
| 5 | cited test lines drifted (cause withdrawn EG.167: defs moved +6, marker/def +1 -- no one insertion does both) | All nine hypothesis citations fixed: 159->160 (x2, :29 and :37), 76->77, 175->176, 208->209, 122->123, 301->302, 190->191, 273->274. Four further drifted citations found in the same pass and fixed, none in the brief: a00-0a22ec6c:61 :483->:489, a00-0a22ec6c:105 :439->:468, a00-310104ca:47 and a00-0a22ec6c:119 the `_graph` row text 36-38 -> 39-42, a00-4ef63f5c:41 the `_graph` helper 26-45 -> 28-43. |
| 6 | two write.py citations inside lines this round rewrote | BOTH confirmed wrong, both fixed. `def _enforce_outside_ref_gate` is write.py:**1456** (1455 is BLANK; its two callers are :1506 and :2144). The `create --payload` mint is `extra[links.LINK_FIELD] = str(payload)` at write.py:**3131**; 3130 is the `ensure_payload` call. hypothesis:42 and :44 and a00-0a22ec6c:160. |
| 7 | `edited_by` on a00-0a22ec6c named neither author nor lander | The field CANNOT carry both, and write.py overwrites it with the last writer, so it reads the LAST write.py writer (a later round moved it again: see that node frontmatter) and the three-part truth is on that node: author a00-b2b01c2b, lander director-engine by hand at dff3b6076, last writer a00-fd3b2d8a. A one-slot provenance field on a node three actors touched is a structural defect; named for the director. |
| 8 | a00-b2b01c2b's item-5 `Where` said "hypothesis:41,44,48" | :48 is the `## FILE SCOPE` heading. Corrected to `hypothesis:41,44` with the error named in place, plus the note that the numbers it moved were themselves one low at the tip. |

## Outside scope, named not touched
- `extensions/agi/bin/node_writer.py:650-653` -- `replace_payload` still never creates, so the KNOWN RESIDUAL stays open. Unchanged this round, deliberately.
- the hypothesis node write.py band citations were not re-measured by this round except the two in item 6 (director close EG.176: the band list and its :39/:41 placement were wrong, so they are dropped, not restated -- locate each band by its function name); a writer that shifts by 71 lines between rounds is named in the hypothesis's own RECORDED RESIDUE, not here.

## Evidence

```
$ git diff --numstat dff3b6076 -- extensions/agi/bin/write.py extensions/agi/bin/node_writer.py extensions/agi/tests/test_payload_rename.py
(empty: no code change)      # 0 production lines, 0 test lines over the CUT tip

$ python3 -m pytest extensions/agi/tests/test_payload_rename.py extensions/agi/tests/test_bin_help_smoke.py -q --basetemp /tmp/bf153 -p no:cacheprovider
100 passed, 6 skipped, 1 xfailed, 35 warnings in 14.06s   [the PRIOR round run, quoted; THIS tip, director-run for EG.176 at a1a1e686b: `pytest extensions/agi/tests/test_payload_rename.py -q -p no:cacheprovider` = 28 passed, 1 xfailed, 35 warnings]
```

No code was changed this round: 0 production lines, 0 test lines, node prose only. `test_payload_rename.py` is in this round's FILE SCOPE precisely so a citation could be CHECKED against it, not so a byte could be moved.

## Agent Notes
Corrective: 20 citations re-pointed at the CUT tip dff3b6076, the unset falsifier closed (dispatch line was the lie), PARENT P5 marked REFUTED with its stale-blob cause, 0 production lines.

PARENT REVIEW a00-0f8cc2a9 (EG.153) — probes run by the PARENT, not the kid. CEILING RE-MEASURED against the CUT tip: `git diff --numstat dff3b6076 f6938c5a2` = 0 production lines, 0 test lines (only .md). Title set in the kid-s own words, not derived from the filename. | probe | class | result | | P1 wire: `git show dff3b6076:extensions/agi/tests/test_payload_rename.py | sed -n "381p;528p;561p;572p;329p;322p;160p;77p;176p;209p;123p;302p;191p;274p;416p;468p;489p"` — all 17 lines land on exactly the defs/marker the node names, including `xfail` at :322 above the def at :329. The re-pointing is real, on the COMMITTED blob. | HOLD | | P2 gate: the unset falsifier the node calls CLOSED, read out of the committed writer: `git show dff3b6076:extensions/agi/bin/write.py | sed -n "2320,2330p"` shows the guard `if "payload_ref" in edit.unset_fm or links.LINK_FIELD in edit.unset_fm:` and the `EditError` at 2324-2327 naming `_payload_ref_field(_fm or {})`. The dispatch line WAS the lie; the Agent Notes were right. | HOLD | | P3 gate: the round-s own claim, grepped for every stale value (375/522/555/566/328/159/175/208/122/301/190/273/483/439/1455/3130) across all five in-scope node files IN THE WORKING TREE — zero hits. | HOLD | | P4 gate: THE SAME GREP AGAINST THE COMMITTED TIP f6938c5a2 — a00-0a22ec6c still reads :483, :439, :321/:328, `create --payload 3059 -> **3130**`, `location-only 352 -> **375**`, `failed-move 485 -> **522**`, `argv 518 -> **555**`, `dry-run 529 -> **566**`; a00-310104ca:216 still reads `(321 marker / 328 def, 483 the one-read test)`; a00-b2b01c2b:40 still reads `hypothesis:41,44,48` and its P5 row still reads `| HOLD |`, the refutation absent. Items 1, 3, 4, 5, 6 (sibling half), 7 and 8 are correct on DISK and ABSENT FROM THE RECORD. | **FAIL** | VERDICT: the BYTES are ACCEPTED — every substantive claim in the item table verified independently by the parent against the committed blob, 0 production / 0 test lines, and the one measurement item (the `unset` falsifier) settled correctly with the dispatch line corrected rather than the Agent Notes. The RECORD is INCOMPLETE: four of the six in-scope node files are logged in `.agi/sessions/write-log.jsonl` (18:45:02-18:45:08, five write.py rows, so the writer was NOT bypassed this time) but sit modified-uncommitted at f6938c5a2. NOT landed by hand: the authored region is the kid-s. RE-BRIEFED to the kid to land exactly those four paths. This is the SAME defect the EG.122 parent caught as P6 and the second-pass review named again ("the cause is a bypassed writer, not carelessness") — third round running, so the mechanism, not the kid, is now the finding for the director.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
EG.153 parent review (a00-0f8cc2a9). (1) WHAT THE ORDER SAID, quoted: "CHECK EVERY DELIVERABLE THE KID NAMES AGAINST THAT DIFF, NEVER AGAINST ITS THOUGHT OR ITS SUMMARY. A file, test, or node edit the kid CLAIMS and the diff does not carry demotes that kid to inconclusive_lean_disproved with the probe named - it is never silently patched by you and never by the director (SL7.136 kid 1 claimed a node edit its branch never carried; SM 20:33Z director gen 29)." (2) WHAT THE MACHINE ACTUALLY DOES: the kid-s own diff, `git diff --numstat dff3b6076 f6938c5a2`, carries TWO files (its own experiment node, 99 added; the hypothesis node, 11/11) and no more, while `git status --porcelain` in the shared worktree carries FOUR MORE modified node files (a00-0a22ec6c, a00-310104ca, a00-4ef63f5c, a00-b2b01c2b) holding items 1, 3, 4, 5, 6-sibling-half, 7 and 8. My probe P4 read those four files OUT OF THE COMMIT at f6938c5a2 and found every stale number the round claims to have fixed still sitting there - :483, :321/:328, 3059->3130, 352->375, 485->522, 518->555, 529->566, and a P5 row still stamped `| HOLD |`. The bytes are right and the record is empty: the round-s central claim is "the prose agrees with the COMMITTED bytes", and on the committed bytes the prose does not agree yet. (3) THE NEAR MISS: a parent that greps the WORKING TREE (my own P3, which returned zero hits) certifies the round and the next reader, arriving through git, meets the same stale numbers this round was raised to remove. The near miss is worse than a no-op - it actively discharges the item table by reading a state the loop will never publish. The second near miss, and the one worth naming for the director: since the loop-s `done` scopes its commit to the kid-s OWN node, a round that edits four FOREIGN nodes will leave three quarters of its work unpublished EVERY time, which is why the director landed EG.122-s leftovers by hand at dff3b6076 and why this defect has now survived two rounds and one re-brief. (4) NO STANDING RULE DEVIATED: I did not commit and did not land the four paths by hand, because the authored region is the kid-s (SL7.136); I re-briefed the kid instead, on its own node. I also did not re-run the kid-s suite as evidence - the four probes are the parent-s own, run against the committed blob at the CUT tip dff3b6076, and P1 is the one that shows the re-pointing is real rather than merely plausible. What the kid got RIGHT, and it is not a small thing: it ran the settling command first, pasted it verbatim, and used it to call the LAST round-s P5 REFUTED rather than to soften it - the one-line cause it names (the parent verified a copy/worktree, not the committed file) is exactly the cause of MY OWN P3/P4 pair, which is how I know it read the mechanism rather than the symptom.
<!-- THOUGHT:END -->
