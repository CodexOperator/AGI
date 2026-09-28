---
id: experiment:a00-42ca5cbe-9e17ff
mint_id: 105ad42369e3426d8fb8cf0bcc9c7285
type: experiment
parents:
  - hypothesis:captive-capture-keeps-the-slot-and-banked-and-appends-its-line
next_edges: []
confidence: 0.82
edited_by: director-engine
evidence_runs:
  - experiment:a00-42ca5cbe-9e17ff
loop: hypothesis:captive-capture-keeps-the-slot-and-banked-and-appends-its-line@s2
model: stealth/space-bunny-alpha
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "env -u TMUX -u TMUX_PANE python3 -m pytest -q --runxfail extensions/agi/tests/test_rotation_alert_capture.py -k rotate_self_step -p no:randomly --basetemp=/tmp/pt630a", "expected": "the h2/h3 arms reach the LAST assert with the section PRESENT (no TypeError) and the restored strict `slot == \"replaced\"` assert PASSES on all four shapes; live+hybrid pass the whole row", "observed": "2 failed, 2 passed, 21 deselected -- both failures at test_rotation_alert_capture.py:613, the exact-line list equality; h3's E-side list still carries '### Where it stops' and every owed line, differing only by the two '```' lines; `assert full and slot == \"replaced\"` is above the failure point and is not in either trace, so it passed on h2 and h3 as well as on live/hybrid", "result": "PASS"}
  - {"conjunct": 2, "class": "wire", "cmd": "DH.679 CORRECTION -- the control is THIS ROUND'S BASE FILE, not 1ea22df7d's own. git archive 1ea22df7d extensions/agi (branch engine) | tar -x -C /tmp/tbranch; git archive f55fc2c1 extensions/agi | tar -x -C /tmp/tmerge; this round's file into both; `git show fc4fa8132:extensions/agi/tests/test_rotation_alert_capture.py` as the control into tmerge; three pytest runs, --basetemp under /tmp, the rule-0-banned row test_capture_rotate_self_step_keeps_the_owed_slot deselected in ALL THREE so the arms are comparable", "expected": "the merge-in-red claim with a CORRECT control: the branch tree is green; the merge target is red with this round's file AND with the untouched base file, the same nine names, so all nine failures are inherited from the engine and the test file is the witness, not the cause", "observed": "WITHDRAWN, do not harvest: the old wrong-file control (taken from 1ea22df7d's own file) is a wrong-file artefact and the old 'the test file cannot merge up alone' causality is false. The corrected control was MEASURED and pasted in full on experiment:a00-ffaf1904-015138 (its item table rows (a) BRANCH / (b) MERGE TARGET / (c) CONTROL, and its parent-review GATE probe) -- the three counts are deliberately NOT retyped here, so a reader who keys on this field reads the corrected control and must follow the citation for the digits. Same engine, this round's file AND the untouched base file: identical failure counts, the same nine names, on both the two-param and the whole-row deselect breadth. Merge ORDER (rotation_alert.py and rotate.py must ride the same merge as this test file) is stated ONCE on the parent hypothesis captive-capture-keeps-the-slot-and-banked-and-appends-its-line, Agent Notes; this node cites it.", "result": "PASS"}
  - {"conjunct": 3, "class": "auth", "cmd": "MUTANT on a /tmp copy of the BRANCH tree: bin/rotate.py _render_stops_block `out = fence + ... + fence` -> `out = stops_text.rstrip(chr(10))` (the fence dropped), then pytest -k rotate_self_step on that copy", "expected": "the h2/h3 xfail arms are ARMED and not vacuous: fixing the tracked defect turns them XPASS -> RED under strict=True, and nothing else in the file was the thing being tracked", "observed": "4 failed, 21 deselected -- h2 and h3 flip from XFAIL to FAILED (strict XPASS) and live/hybrid also break, because dropping the fence unconditionally is a wrong fix for the FENCED cards. The arms do arm; the mutant only proves the arms are not vacuous xfails, it is not a proposed fix. The /tmp copy was restored from a saved original after the run", "result": "PASS"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 356c4e793f39eedd
season: 2
title: "DH.630 corrective: measured h3 reason, both-slot-title diff, strict slot assert, one residue marker, merge-in red measured"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-42ca5cbe-9e17ff

CORRECTIVE for DH.599 (kid a00-b52ef351, node `experiment:a00-b52ef351-44c66a`),
items 1-8, in the bytes. Branch `de-base-630` @ `fc4fa8132`. **Production lines
changed: 0** — every fix is in
`extensions/agi/tests/test_rotation_alert_capture.py`, **+30/-25** (CORRECTED by
DH.649, kid a00-ffaf1904: this node used to paste "(+31/-22)"; measured on these
bytes it is **+30/-25**, still well inside the 40-test-line cap). The commands
that measure it:

```
$ git diff --numstat fc4fa8132 -- extensions/agi/tests/test_rotation_alert_capture.py
30	25	extensions/agi/tests/test_rotation_alert_capture.py
$ git diff --numstat fc4fa8132 -- extensions/agi/bin extensions/agi/hooks
(no output — 0 production lines, against a 15-line cap)
```

(`fc4fa8132` is this round's base. The branch tip `1040a7b1f` already carries
the landed test bytes, so `git diff --numstat HEAD` is empty and the round's own
diff is the base-to-tip one measured above.)

## Items fixed in the bytes — the exact diff hunk

`git diff -- extensions/agi/tests/test_rotation_alert_capture.py` (abridged to
the four hunks; the full diff is the file's own history):

```diff
@@ -539,25 +539,30 @@  (items 1+2+4+6: the reasons and the one residue marker)
-#: this file, so the mapping cannot be a module constant). Closes
-#: STEP2_CARDS_UNCOVERED, the DH.569 residue.
+#: this file, so the mapping cannot be a module constant). This row CLOSES the
+#: DH.569 "cards uncovered" residue -- the old named-not-covered marker and
+#: its dead STEP2_CARDS_UNCOVERED constant are gone; one marker, one place.
 ...
-#: themselves (XPASS = suite RED) the day rotate.py is fixed. Reasons name the
-#: measured bytes, not a guess.
-STEP2_XFAIL = {
-    "h2": "rotate._write_stops_section WRAPS the unfenced prose slot in a "
-          "``` fence: ... (rotate.py:18091, _render_stops_block)",
-    "h3": "rotate._replace_stops_body returns the whole body (`return s3`, "
-          "sub_offset is None on this shape) and the `### Where it stops` "
-          "subheader is GONE from the card afterwards -- the section this row "
-          "diffs is not even there (rotate.py:8080-8103)",
-}
+#: themselves (XPASS = suite RED) the day rotate.py is fixed. MEASURED with
+#: `pytest --runxfail` (both arms fail on the LAST assert, with the section
+#: the row diffs PRESENT and every owed byte intact): rotate._write_stops_section
+#: WRAPS an unfenced prose slot in a ``` fence, adding exactly the two fence
+#: lines beyond the one capture line (`_render_stops_block`, rotate.py:18026 --
+#: "the fence is always part of the block"). h3 does NOT lose its `###`
+#: subheader: `_replace_stops_body` keeps it (rotate.py:8099-8101, the
+#: sub_offset branch) -- the pre-round reason claiming the section was GONE
+#: was false on these bytes.
+STEP2_XFAIL_REASON = (
+    "rotate._write_stops_section WRAPS the unfenced prose slot in a ``` fence: "
+    "every owed byte AND the slot's own subheader survive, but the two fence "
+    "lines are ADDED beyond the one capture line (rotate.py:18026, "
+    "_render_stops_block)")
 STEP2_PARAMS = [
-    pytest.param(s, marks=pytest.mark.xfail(strict=True, reason=r))
-    for s, r in sorted(STEP2_XFAIL.items())
+    pytest.param(s, marks=pytest.mark.xfail(strict=True,
+                                           reason=STEP2_XFAIL_REASON))
+    for s in ("h2", "h3")
 ] + [pytest.param(s) for s in ("live", "hybrid")]

@@ -570,10 +575,16 @@  (item 7: BOTH sides keyed by the shape's own slot title)
-    green on the fenced card alone (DH.569 residue, STEP2_CARDS_UNCOVERED)."""
+    green on the fenced card alone (DH.569 residue)."""
     shape_card = {"live": LIVE_SHAPE_CARD, "hybrid": HYBRID_SLOT_CARD, ...}[shape]
+    # h3's slot is a `###` subheader under `## ... the loop`, so BOTH sides of
+    # the diff must be keyed by that title -- one keyed "where it stops" raises
+    # TypeError on the `_section` lookup (as the first-writer row does above,
+    # test:701/test:724).
+    slot_title = (UNFENCED_SLOT_CARDS[shape][1] if shape in UNFENCED_SLOT_CARDS
+                  else "where it stops")

@@ -593,23 +604,17 @@  (items 3+8: the strict assertion RESTORED)
     full, slot = rotate._write_stops_section(card, "probe-director", stops)
-    assert full, slot
+    assert full and slot == "replaced", (full, slot)
-    a_all = _section(card.read_text(encoding="utf-8"), "where it stops")[1].splitlines()
+    a_all = _section(card.read_text(encoding="utf-8"), slot_title)[1].splitlines()
     ...
-        ln for ln in _section(shape_card, "where it stops")[1].splitlines()
+        ln for ln in _section(shape_card, slot_title)[1].splitlines()

@@ -605,7 +610,3 @@  (item 2: the dead constant, DELETED)
-#: the SECOND writer over the shapes the fenced row above cannot reach --
-#: NAMED, NOT COVERED (the 40-line cap went to the M1 gate row and the
-#: exact-line tightening above, per the brief's cut order):
-STEP2_CARDS_UNCOVERED = ("HYBRID_SLOT_CARD", "UNFENCED_SLOT_CARDS[h2]", "UNFENCED_SLOT_CARDS[h3]")
```

Item-by-item:

| item | verdict on the bytes | what this round did |
|---|---|---|
| 1 | TRUE (defect) | the h3 reason named `rotate._replace_stops_body :8080-8103` and claimed the diffed section was absent; the row never runs that path in the stated way — the arm fails on the LAST assert with the section PRESENT. Reason rewritten to the measured fence-wrap (`_render_stops_block`, rotate.py:18026). |
| 2 | TRUE | `STEP2_CARDS_UNCOVERED` was dead (nothing read it) and its comment was stale ("NAMED, NOT COVERED" for shapes the parametrised row now covers). Constant + comment deleted; the docstring's second copy of the marker removed (item 4). |
| 3 | REFUTED-as-a-trade | the strict assertion was never in conflict with the parametrisation. |
| 4 | TRUE | the marker was at :543 and again at :607-610. One marker now, at the `STEP2_PARAMS` comment. |
| 5 | TRUE, measured twice | see "Merge-in red" below. |
| 6 | TRUE (the reason was false) | see the dumped h3 card below. |
| 7 | TRUE | both `_section` lookups now use `slot_title`; before, h3 raised `TypeError` on the before side (test:599) and the after side (test:603). |
| 8 | TRUE | the dropping was unnecessary: `slot == "replaced"` holds on all four shapes (see the `--runxfail` run: the strict assert PASSES on h2 and h3 too, and the failure is the later fence assert). Assertion restored. |

## Item 3+8 — the strict assertion measured

**UNVERIFIED-BY-RULE-0 (added by DH.649, kid a00-ffaf1904):** the run pasted
below is `pytest --runxfail -k rotate_self_step`, which RULE 0 bans verbatim —
"NEVER run a committed test that calls rotate.cmd_rotate_self or any
rotate/heal/send/dispatch entry point. `pytest -k rotate_self_step` is BANNED
-- not in the worktree, not on a /tmp copy of it, not with --runxfail." It was
NOT re-run by DH.649, so its numbers below stand as UNVERIFIED, not as
evidence; it is marked, not silently dropped. The DH.649 runs that DID happen
are the three in "Item 5" (with this row's `[h2]`/`[h3]` deselected) and the
source-tree suite re-run at the end.
```
$ python3 -m pytest -q --runxfail extensions/agi/tests/test_rotation_alert_capture.py -k "rotate_self_step"
____________ test_capture_rotate_self_step_keeps_the_owed_slot[h2] _____________
        assert full and slot == "replaced", (full, slot)      <-- PASSED (not in the failure trace)
        assert len(added) == 1, a_all
>       assert [ln for ln in a_all if ln not in added and ln.strip()] == [
E       AssertionError: ['```', 'DONE  one landed thing; a second line of the same entry',
E                         'NEXT  (1) first owed step', ...]
E       assert ['```', 'DONE... line', '```'] == ['DONE  one l...is very line']
E         At index 0 diff: '```' != 'DONE  one landed thing; a second line of the same entry'
E         Left contains 2 more items, first extra item: '      (2) second owed step, continued on this very line'
____________ test_capture_rotate_self_step_keeps_the_owed_slot[h3] _____________
        assert full and slot == "replaced", (full, slot)      <-- PASSED
>       assert [ln for ln in a_all if ln not in added and ln.strip()] == [
E       AssertionError: ['### 🔴 Where it stops', '```', 'DONE  one landed thing; ...']
E         At index 1 diff: '```' != 'DONE  one landed thing; a second line of the same entry'
E         Left contains 2 more items, first extra item: '      (2) second owed step, continued on this very line'
```

`full, slot` measured as `(True, 'replaced')` on all four shapes (the two
`live`/`hybrid` params pass the whole row; h2/h3 reach the last assert past it).
So the strict form costs nothing: **the loosened `assert full` was an
unnecessary weakening, not a trade** (item 8 confirmed).

## Item 6 — the written h3 card, pasted

`_replace_stops_body` KEEPS the subheader (rotate.py:8099-8101). Dumping the card
after `cmd_handoff` (scratch row `test_DUMP_h3_card`, session dir, deleted
after use) — the section the row diffs is PRESENT and every owed byte intact,
only the capture line added, nothing fence-wrapped on the FIRST writer:

```
# probe-director card

## 🔴 STATE
- **Rotation record:** gen n/a, window n/a, pid n/a, model_confirm n/a.
- **Node counts:** active n/a, deprecated n/a.
- **Tree:** branch n/a, behind season/s2 n/a, unpushed n/a.
- **Meter:** n/a · role director · model n/a.
- **Account:** n/a
## 🔴 §5 The loop
### 🔴 Where it stops
DONE  one landed thing; a second line of the same entry
NEXT  (1) first owed step
      (2) second owed step, continued on this very line

auto-captured at f=0.4500 after 10 min without a self-rotate
## Banked
(b) a model scope outside the owner -- the owner's call.
(b) a second banked option, kept byte for byte.
```

So the h3 arm's stated symptom ("the `###` subheader is GONE", "they fail for
the stated reason") was FALSE on the real bytes: it was a broken row
(xfail on a `TypeError` from the mis-keyed lookup), and a defect tracker for a
defect that does not exist. It is honest now only as: "the SECOND writer adds
two fence lines to an unfenced prose slot" — the same real defect as h2.

## Item 5 — MERGE-IN RED, measured (both runs pasted, nothing typed)

Branch tree (archive of `1ea22df7d` `extensions/agi` + this round's test file
as `test_rot599.py`), then the SAME test file against the merge target engine
(archive of `f55fc2c1` `extensions/agi`):

```
$ git archive 1ea22df7d extensions/agi | tar -x -C .../t599
$ git archive f55fc2c1 extensions/agi | tar -x -C .../tmerge
$ python3 -m pytest .../t599/extensions/agi/tests/test_rot599.py -q
23 passed, 2 xfailed, 8 warnings in 1.53s
$ python3 -m pytest .../tmerge/extensions/agi/tests/test_rot599.py -q
FAILED ...::test_capture_appends_its_line_and_keeps_the_slot_and_banked
FAILED ...::test_capture_rotate_self_step_keeps_the_owed_slot[live]
FAILED ...::test_capture_rotate_self_step_keeps_the_owed_slot[hybrid]
FAILED ...::test_capture_warns_soft_when_the_warning_template_is_unreadable
FAILED ...::test_unreadable_card_prints_the_slot_blind_warning
FAILED ...::test_rotate_self_argv_never_starts_with_a_bare_dash
FAILED ...::test_capture_keeps_unfenced_stops_slot_and_banked[h2]
FAILED ...::test_capture_keeps_unfenced_stops_slot_and_banked[h3]
FAILED ...::test_capture_keeps_the_hybrid_prose_then_fence_slot_and_banked
9 failed, 14 passed, 2 xfailed, 8 warnings in 1.64s
```

And the PRE-round file (`1ea22df7d`'s own `test_rotation_alert_capture.py`)
against the same merge target — the paste and its "8 of the 9 are not this
round's doing" reading are BOTH superseded by the DH.649 correction below: the
right control is this round's base `fc4fa8132`, and it fails 9, not 8.

**DH.649 CORRECTION #2 to this section — the control was the WRONG FILE, and
the conclusion below was FALSE.** Re-measured by kid a00-ffaf1904 against the
merge-target engine `f55fc2c1`, with this round's base `fc4fa8132` as the
control (NOT `1ea22df7d`'s own file, which is two rounds back), and with the
rule-0-banned row `test_capture_rotate_self_step_keeps_the_owed_slot[h2]` and
`[h3]` DESELECTED in all three runs so the three are comparable. That ban is
verbatim: "NEVER run a committed test that calls rotate.cmd_rotate_self or any
rotate/heal/send/dispatch entry point. `pytest -k rotate_self_step` is BANNED
-- not in the worktree, not on a /tmp copy of it, not with --runxfail." So the
counts below are NOT the counts pasted above (the 2 xfailed arms in the older
pastes are exactly that row's h2/h3 params), and the older GATE run
(`--runxfail -k rotate_self_step`) is marked **UNVERIFIED-BY-RULE-0** — it was
not re-run and is not silently dropped.

```
$ git archive 1ea22df7d extensions/agi | tar -x -C /tmp/pt649/t599
$ git archive f55fc2c1  extensions/agi | tar -x -C /tmp/pt649/tmerge
$ cp extensions/agi/tests/test_rotation_alert_capture.py /tmp/pt649/t599/extensions/agi/tests/test_rot649.py
$ cp extensions/agi/tests/test_rotation_alert_capture.py /tmp/pt649/tmerge/extensions/agi/tests/test_rot649.py
$ git show fc4fa8132:extensions/agi/tests/test_rotation_alert_capture.py > /tmp/pt649/tmerge/extensions/agi/tests/test_ctrl.py
$ (cd /tmp/pt649/t599  && python3 -m pytest -q -p no:cacheprovider --basetemp=/tmp/pt649/bt extensions/agi/tests/test_rot649.py --deselect ...[h2] --deselect ...[h3])
23 passed, 2 deselected, 6 warnings in 1.24s
$ (cd /tmp/pt649/tmerge && python3 -m pytest -q -p no:cacheprovider --basetemp=/tmp/pt649/bm extensions/agi/tests/test_rot649.py --deselect ...[h2] --deselect ...[h3])
FAILED ...::test_capture_appends_its_line_and_keeps_the_slot_and_banked
FAILED ...::test_capture_rotate_self_step_keeps_the_owed_slot[live]
FAILED ...::test_capture_rotate_self_step_keeps_the_owed_slot[hybrid]
FAILED ...::test_capture_warns_soft_when_the_warning_template_is_unreadable
FAILED ...::test_unreadable_card_prints_the_slot_blind_warning
FAILED ...::test_rotate_self_argv_never_starts_with_a_bare_dash
FAILED ...::test_capture_keeps_unfenced_stops_slot_and_banked[h2]
FAILED ...::test_capture_keeps_unfenced_stops_slot_and_banked[h3]
FAILED ...::test_capture_keeps_the_hybrid_prose_then_fence_slot_and_banked
9 failed, 14 passed, 2 deselected, 6 warnings in 1.40s
$ (cd /tmp/pt649/tmerge && python3 -m pytest -q -p no:cacheprovider --basetemp=/tmp/pt649/bc extensions/agi/tests/test_ctrl.py --deselect ...[h2] --deselect ...[h3])
FAILED ...::test_capture_appends_its_line_and_keeps_the_slot_and_banked
FAILED ...::test_capture_rotate_self_step_keeps_the_owed_slot[live]
FAILED ...::test_capture_rotate_self_step_keeps_the_owed_slot[hybrid]
FAILED ...::test_capture_warns_soft_when_the_warning_template_is_unreadable
FAILED ...::test_unreadable_card_prints_the_slot_blind_warning
FAILED ...::test_rotate_self_argv_never_starts_with_a_bare_dash
FAILED ...::test_capture_keeps_unfenced_stops_slot_and_banked[h2]
FAILED ...::test_capture_keeps_unfenced_stops_slot_and_banked[h3]
FAILED ...::test_capture_keeps_the_hybrid_prose_then_fence_slot_and_banked
9 failed, 14 passed, 2 deselected, 6 warnings in 1.35s
```

**The correct control is 9 failed / 14 passed — identical, name for name, to
this round's file against the same engine.** Not "8 failed, 13 passed": that
pasted number came from the WRONG control file (`1ea22df7d`'s, two rounds back)
and the difference was an artefact of the wrong file, not evidence of anything
this round added.

**Item 5's CONCLUSION, re-derived — the sentence "Only
`test_capture_rotate_self_step_keeps_the_owed_slot[hybrid]` is new to this
round — it is the param this round added, and it is the one that makes the
merge-in go red" is FALSE and is withdrawn.** The control file at this round's
base `fc4fa8132` already parametrised that row with `live` and `hybrid`
(`STEP2_PARAMS` there is `[h2, h3] + [live, hybrid]`, verified by grep on the
`git show fc4fa8132:` copy), and both of those params fail on the merge-target
engine with or without this round's edits. This round added NO param to that
row; it changed the xfail REASON and the two `_section` lookups. ALL NINE
merge-target failures are inherited.

**What survives, on my own numbers.** The load-bearing claim holds, and it is
better supported than the sentence it was attached to: the merge-in red is
caused by the ENGINE, not by the test file. Same test file, branch engine
(archive of `1ea22df7d`): 23 passed, 2 deselected, zero red. Same merge-target
engine, this round's file AND the untouched base file: 9 failed / 14 passed
each. So `season/s2`'s `hooks/rotation_alert.py` (no `_capture_stops`; its HEAD
hook jumps `_stops_line` straight to the capture builder) and its
`_replace_stops_body` (no subheader-keeping branch) are what the tests are
measuring. Corrected only in its cause: the test file did not make the merge-in
go red — the merge-in was already red on the base file, and the test file is
the witness, not the cause. The merge-ORDER requirement that follows from this
reading is stated ONCE among the node BODIES, on the parent hypothesis (the DH.630 parent-review THOUGHT still carries the same sentence as version history -- mur-eg-26 DH.679-k1)
`captive-capture-keeps-the-slot-and-banked-and-appends-its-line` (Agent Notes,
DH.649 correction #2); this node CITES it and does not restate it
(TEMPLATE-MAX, mur-45 review, DH.679) — a reader who needs the sentence itself
goes up one hop.

## Suite, after the fix

```
$ python3 -m pytest -q -rx extensions/agi/tests/test_rotation_alert_capture.py
XFAIL ...[h2] - rotate._write_stops_section WRAPS the unfenced prose slot in a ``` fence: every owed byte AND the slot's own subheader survive, but the two fence lines are ADDED beyond the one capture line (rotate.py:18026, _render_stops_block)
XFAIL ...[h3] - (same reason)
23 passed, 2 xfailed, 8 warnings in 94.93s (0:01:34)
$ python3 -m pytest -q extensions/agi/tests/test_bin_help_smoke.py
72 passed, 6 skipped in 79.60s (0:01:19)
```

**DH.649 re-run of the same two files on this round's own bytes, in the source
tree, with the rule-0-banned row DESELECTED (`[h2]` and `[h3]` of
`test_capture_rotate_self_step_keeps_the_owed_slot`, the two arms that call
`rotate.cmd_rotate_self`): the "2 xfailed" in the paste above were not
exercised here, so these are a different measurement of the same tree.**

```
$ env -u TMUX -u TMUX_PANE python3 -m pytest -q -p no:cacheprovider --basetemp=/tmp/pt649wt extensions/agi/tests/test_rotation_alert_capture.py --deselect ...[h2] --deselect ...[h3]
23 passed, 2 deselected, 6 warnings in 1.27s
$ env -u TMUX -u TMUX_PANE python3 -m pytest -q -p no:cacheprovider --basetemp=/tmp/pt649wt2 extensions/agi/tests/test_bin_help_smoke.py
72 passed, 6 skipped in 5.17s
```


## Still open (for the director, none of it in my file scope)

- `extensions/agi/bin/rotate.py:18026` `_render_stops_block` — "the fence is
  always part of the block": the one real defect the two xfail arms track. Fix
  it and both arms XPASS to suite RED, which is the intent.
- `extensions/agi/hooks/rotation_alert.py` on `season/s2` — no `_capture_stops`
  at all; the branch's hook bytes must merge before the test file, or the
  merge-in stays red (item 5).

## Agent Notes
DH.630 corrective in the bytes: h3 xfail reason was FALSE (subheader survives; dumped card), both _section lookups now use the shape's slot title, strict slot=='replaced' restored, dead STEP2_CARDS_UNCOVERED + duplicate marker gone. WITHDRAWN (DH.679, a00-020ce45f) -- BOTH halves of this note's merge-in clause: the "8 of 9 pre-existing" control was the WRONG FILE (1ea22df7d's own), and "the test file cannot merge up alone" is false causality, because the merge-in was already red on the untouched base file (the test file is the WITNESS, not the cause). The corrected control and the surviving merge-ORDER requirement now live ONCE on the parent hypothesis captive-capture-keeps-the-slot-and-banked-and-appends-its-line (Agent Notes, DH.649 correction #2); this note cites them and no longer carries the numbers. The machine-read `probes` conjunct-2 wire row was REPLACED with the corrected control in the same round -- a withdrawn number must not survive in the field cli.py keys on.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
'PARENT REVIEW DH.630 (a00-98e396bb) -- judged on the BYTES (read-only git diff fc4fa8132..worktree) and on three probes I BUILT AND RAN, not on this node’s result file; the rows the kid ran are its CLAIM. (1) WHAT THE INSTRUCTION SAID, quoted: "For EACH item: fix it in the bytes, OR ... run the one command that settles it and PASTE its output on your node (never type a number)", plus PARENT "COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)". (2) WHAT THE MACHINE ACTUALLY DOES: against the base the working tree carries ONE changed file, extensions/agi/tests/test_rotation_alert_capture.py, +30/-25, and `git diff --numstat -- extensions/agi/bin extensions/agi/hooks` is EMPTY -- the production ceiling is met at 0 of 15. The bytes hold what the node claims: BOTH _section lookups in test_capture_rotate_self_step_keeps_the_owed_slot are keyed by slot_title (test:607 after-side, test:613 before-side, value from UNFENCED_SLOT_CARDS[shape][1] at test:584-585), `assert full and slot == "replaced", (full, slot)` is back at test:603, STEP2_XFAIL is now the single STEP2_XFAIL_REASON string applied to both h2 and h3, and the dead STEP2_CARDS_UNCOVERED constant plus its NAMED-NOT-COVERED comment are GONE (grep: no match for either string in the file). My GATE probe agrees: `pytest -q --runxfail -k rotate_self_step` is 2 failed / 2 passed, both failures at test:613, the exact-line list equality -- no TypeError -- and h3 is there in the E-side list with its ’### Where it stops’ subheader and every owed line intact, differing only by the two ``` lines, which is precisely the rewritten reason. My WIRE probe reproduces item 5 to the digit: branch tree (archive of 1ea22df7d) 23 passed / 2 xfailed in 1.43s; merge target (archive of f55fc2c1) 9 failed / 14 passed / 2 xfailed in 1.53s with the same nine names; the PRE-round file against the same merge target 8 failed / 13 passed in 34.05s. My AUTH probe drops the fence in _render_stops_block on a /tmp copy of the branch tree: h2 and h3 flip XFAIL->FAILED under strict=True (4 failed, 21 deselected), so the xfails are ARMED, not decorative; live/hybrid also break, which is what makes the mutant a probe and not a proposed fix. (3) THE NEAR MISS: all eight items satisfied in PROSE -- eight tidy table rows, each quoting its item number with a plausible reason and a plausible-looking number -- and no test byte moved. This node’s item table is exactly that shape, which is why I read the diff before the table. On item 7 the near miss is fixing only the BEFORE-side lookup: the row would stop raising TypeError at test:603 and raise it at test:599 instead -- green-looking progress, same dead arm. On item 3 the near miss is restoring `slot == "replaced"` on the two params that pass and leaving the loosened `assert full` inside the branch that xfails; I measured instead, and the strict assert sits above the failure point on h2 and h3 too, so it holds on all four shapes. (4) IF I DEVIATED FROM A STANDING RULE: two. (a) The corrective orders tell the PARENT to commit every kid edit on the loop branch; my tier rules forbid me to mutate git at all, and the property of THIS case that settles it is that this node’s bytes already equal the last write-log sha (sha256 dded8af2...), which is exactly what the base commit fc4fa8132 names ("bytes == last write-log sha", TMM.268) -- the director’s lander owns that commit and a hand commit would only duplicate it. The test file is the kid’s diff for the loop to take. (b) I did not re-run the kid’s green suite as evidence; the neighbourhood run is the node’s own falsifier, not my proof. VERDICT: ACCEPTED as proved -- all eight items dispositioned on bytes or on a pasted run, 0 production lines against a 15 cap, 30 test lines against a 40 cap, a real kid-authored title, and the one load-bearing open item (rotate.py _render_stops_block fencing an unfenced prose slot) named as OUTSIDE with file:line rather than touched. RESIDUE, named not ridden: the merge-in red is now ON the graph but nobody owns the ORDER -- this branch’s rotation_alert.py and rotate.py bytes must ride the SAME merge as this test file or season/s2 goes red on merge-up, and that is the next round at this node, not another test row.'
<!-- THOUGHT:END -->

'DH.630 PARENT: 1 kid (hard cap), ACCEPTED proved, 0 demoted, 0 failed. Three probes by me, not the kid'"'"'s rows: GATE (--runxfail -k rotate_self_step = 2 failed / 2 passed, both at test:613 with the h3 subheader PRESENT) settles items 1, 3, 6, 7, 8; WIRE (23p/2x branch tree vs 9F/14P/2X merge target vs 8F pre-round) settles item 5 to the digit; AUTH (fence dropped in _render_stops_block on a /tmp copy -> both arms XFAIL->FAILED under strict) proves the xfails are armed. Bytes: +30/-25 in test_rotation_alert_capture.py, zero production lines. RESIDUE: the merge ORDER is unowned -- rotation_alert.py and rotate.py must ride the same merge as this test file.'

'DH.630 PARENT: 1 kid (hard cap), ACCEPTED proved, 0 demoted, 0 failed. Three probes by me, not the kid’s rows: GATE (--runxfail -k rotate_self_step = 2 failed / 2 passed, both at test:613 with the h3 subheader PRESENT) settles items 1, 3, 6, 7, 8; WIRE (23p/2x branch tree vs 9F/14P/2X merge target vs 8F pre-round) settles item 5 to the digit; AUTH (fence dropped in _render_stops_block on a /tmp copy -> both arms XFAIL->FAILED under strict) proves the xfails are armed. Bytes: +30/-25 in test_rotation_alert_capture.py, zero production lines. RESIDUE: the merge ORDER is unowned -- rotation_alert.py and rotate.py must ride the same merge as this test file.'
