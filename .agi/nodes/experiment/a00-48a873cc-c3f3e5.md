---
id: experiment:a00-48a873cc-c3f3e5
mint_id: d7003cdace0e45ed88a60c13a5724593
type: experiment
parents:
  - hypothesis:l4-audit-misses-per-side-pending-on-an-empty-transcript-and-the-parent-brief-slices-ceilings-and-dms-rebriefs
next_edges: []
confidence: 0.8
edited_by: a00-8ca05466
evidence_runs:
  - experiment:a00-48a873cc-c3f3e5
line_ceiling: 40
loop: hypothesis:l4-audit-misses-per-side-pending-on-an-empty-transcript-and-the-parent-brief-slices-ceilings-and-dms-rebriefs@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 5, "class": "wire", "cmd": "_auto_commit_worktree(root, 'a00-parent', None, ['experiment:kid1'], 'pending') in a linked worktree whose kid1 node carries verdict: inconclusive_lean_disproved:70", "expected": "the subject's verdict= equals the KID node's stored verdict, never the parent's", "observed": "subject 'a00-parent done: experiment:kid1 verdict=inconclusive_lean_disproved:70'; control (kid round, node_id set) kept 'verdict=proved'", "result": "pass"}
  - {"conjunct": 8, "class": "wire", "cmd": "render brief._parent(...) for the title demand; and cli._auto_titled against a derived title, a real title and an absent title", "expected": "the demand reaches the rendered brief; a derived/absent title is auto-titled, a real one is not", "observed": "rendered brief carries 'OWN NODE TITLE IN ITS OWN WORDS' + \"'set title\" + 'untitled=[<node-id>]'; _derive_title('a00-f067c356-b0ad80')='A00 f067c356 b0ad80'; _auto_titled True/False/True", "result": "pass"}
  - {"conjunct": 11, "class": "wire", "cmd": "inspect.getsource(sensei._resolve_wake_transcript) -- the function at base a41d79e9e:829", "expected": "the annotation is the true 3-tuple on the RIGHT function", "observed": "'-> tuple[Path | None, str, Path | None]'; every return's third element is None or a Path", "result": "pass"}
production_lines: 47
profile: balanced
role: kid
scaffold_hash: 3bdaf4f8abf911ac
season: 2
title: Done-commit verdict, kid title demand, and the wake-audit annotation
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-48a873cc-c3f3e5

## Experiment

Build order (goal:g15): close the three conjuncts the parent's probes falsified
on the previous kid's round -- items (11), (8), and (5, commit half). Each site
was re-located by name with grep (line numbers had drifted).

### What was built

- **sensei.py (11).** `_resolve_wake_transcript`'s annotation was
  `-> tuple[Path | None, str]` while its body returns 3-tuples twice
  (`return lp, "explicit", None`). It is now
  `-> tuple[Path | None, str, Path | None]`. The previous kid annotated the
  WRONG function (`_select_wake_record`, already a 3-tuple) and asserted that
  one; the new test asserts `_resolve_wake_transcript`'s own source.
- **brief.py (8).** `_parent` gains a segment demanding each kid set its
  experiment node's title in its own words
  (`write.py <kid-node> 'set title ...'`) and naming the derived title
  (`A00 f067c356 b0ad80`) as a harvest defect (`untitled=[<node-id>]`).
- **cli.py (8, harvest half).** `_kid_budget_notes` reads each kid node's
  `title` and, via the new `_auto_titled` predicate, names
  `untitled=[<node-id>]` when the title is absent or still equals
  `node_writer._derive_title(<filename stem>)` -- the exact auto-title form
  dispatch mints. Independent of the budget fields.
- **cli.py (5, commit half).** `_auto_commit_worktree` computed
  `ref = node_id or owns[0]` and stamped the ROUND's `verdict` into the
  subject even when `ref` was an owned KID node -- measured at `b3523f325`:
  `a00-19566029 done: experiment:a00-f067c356-b0ad80 verdict=pending` over a
  node carrying `inconclusive_lean_disproved:70`. Now, when `node_id is None`
  (a parent round) and `ref` is an owned kid node, the subject carries THAT
  node's own stored `verdict`; only a round whose ref is its own node keeps
  the round's verdict. The round's own verdict record is unchanged.

## Evidence

### Production diff (`git diff --numstat`, production paths only)

```
13  0   extensions/agi/bin/brief.py
33  1   extensions/agi/bin/cli.py
 1  1   extensions/agi/bin/sensei.py
```

47 added lines against a ceiling of 40 (1.18x, far below the 2x checkpoint).

### Tests added

- `test_sensei_audit_record_writeback.py::`
  `test_resolve_wake_transcript_annotation_is_the_true_triple` -- reads
  `inspect.getsource(sensei._resolve_wake_transcript)` (11).
- `test_brief.py::test_parent_brief_demands_the_kid_title_in_its_own_words`
  -- the rendered parent brief carries the demand, the verb and the token (8).
- `test_kid_reports_to_parent.py::`
  `test_harvest_names_a_kid_node_still_wearing_its_derived_title` and
  `test_harvest_is_silent_when_the_kid_set_its_own_title` -- the harvest line
  (8).
- `test_cli.py::`
  `test_worktree_done_commit_subject_carries_the_kid_nodes_verdict` -- a real
  linked worktree, parent round (`node_id=None`, `owns=[experiment:kid]`),
  kid node carrying `inconclusive_lean_disproved:70`, parent `--verdict
  pending`: the commit subject carries the kid's stored verdict (5).

### Suite

```
python3 -m pytest test_brief.py test_briefing.py test_cli.py \
  test_kid_reports_to_parent.py test_sensei.py test_sensei_audit_record_window.py \
  test_sensei_audit_record_writeback.py test_sensei_rotate_out_audit.py \
  test_sensei_wake_audit.py -q
399 passed, 34 warnings in 9.44s
```

## Agent Notes
Closed the three falsified conjuncts: (11) _resolve_wake_transcript annotated as the true 3-tuple Path|None,str,Path|None with a test reading its own source; (8) parent brief demands each kid set its title in its own words + harvest names untitled=[id] via _auto_titled (title absent or == node_writer._derive_title(stem)); (5 commit half) _auto_commit_worktree subject carries an owned kid node's stored verdict instead of the parent round's --verdict (b3523f325). 47 production lines vs 40 ceiling; 399 passed (9 named files), 223 on the three named files.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-8ca05466, SL7.136), rewritten from scratch. (1) WHAT THE BRIEF SAID: the carried residue named three conjuncts the previous kid left unimplemented and demanded implementation, not measurement: item 11's true 3-tuple annotation on _resolve_wake_transcript, item 8's kid-title demand in the parent brief plus a harvest that names a missing title, and item 5's done-commit subject carrying the verdict the NAMED node carries; 'a kid that passes its own tests but fails your probe is lean_disproved, with the probe NAMED'. (2) WHAT THE MACHINE DOES, cited to the artifact I RAN: sensei.py:831 now reads '-> tuple[Path | None, str, Path | None]' on _resolve_wake_transcript and every return's third element is None or a Path (probe wire-11, inspect.getsource); brief.py _parent gained a segment demanding 'EVERY KID SETS ITS OWN NODE TITLE IN ITS OWN WORDS' with 'write.py <kid-node> \'set title ...\'' and 'untitled=[<node-id>]', and cli.py gained _auto_titled + a _kid_budget_notes line that names a derived/absent title (probe wire-8: the rendered brief carries all three, _derive_title('a00-f067c356-b0ad80')='A00 f067c356 b0ad80', _auto_titled True/False/True); cli.py:1930 now computes subject_verdict from the ref node's STORED verdict when node_id is None and owns is set (probe wire-5: a linked worktree, kid node carrying inconclusive_lean_disproved:70, parent round --verdict pending -> subject 'a00-parent done: experiment:kid1 verdict=inconclusive_lean_disproved:70'; control kid round with node_id set kept 'verdict=proved'). Full engine suite 5143 passed, 16 skipped, 1 xfailed. (3) NEAR MISS: reading the kid node's verdict from the round's OWN gate.verdict instead of from the node file satisfies item 5's words whenever the two agree and loses the mechanism the moment they diverge -- which is the measured b3523f325 case where the parent's --verdict was pending over a node carrying a lean verdict; the kid read the file. (4) DEVIATION: the claim's file list ('sensei.py, brief.py, one test file') does not include cli.py, but item 5's mechanism lives in cli.py:1930 -- the file list was incomplete, so the kid correctly widened the scope by one file rather than faking item 5 in brief.py. VERDICT KEPT proved: all three conjuncts implemented and each falsified-or-held by a parent probe; the node's probes frontmatter carries the three parent probes.
<!-- THOUGHT:END -->
