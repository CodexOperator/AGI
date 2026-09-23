---
id: experiment:a00-9b37d43d-5e1153
mint_id: bd2c70b3510142e3a04add576deb55df
type: experiment
parents:
  - hypothesis:sub-dry-run-preview-is-the-bytes-update-node-lands
next_edges: []
confidence: 0.9
edited_by: a00-632e0d0d
evidence_runs:
  - experiment:a00-9b37d43d-5e1153
loop: hypothesis:sub-dry-run-preview-is-the-bytes-update-node-lands@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "scratch probe_parent.py: build tmp graph, run the real `write.py sub world => WORLD --dry-run`, extract the printed diff, apply it with write.apply_unified_diff and GNU patch 2.7.6 to the raw on-disk bytes for shape no_eof_newline", "expected": "marker present, write applier == landed, patch rc=0 and == landed, no phantom '+' line", "observed": "marker=True write_applier=True patch_rc=0 patch_ok=True no_phantom=True", "result": "held"}
  - {"conjunct": 2, "class": "wire", "cmd": "same probe for fm_render_rewrite, dup_body_frontmatter, a canonical node, blank_tail, and fm_only_noeof (not in the kid's list)", "expected": "no phantom empty context/added line; marker iff the raw bytes lack a trailing newline; both appliers == landed", "observed": "fm_render_rewrite/dup/blank_tail marker=False; fm_only_noeof marker=True; all write_applier=True patch_rc=0 patch_ok=True no_phantom=True", "result": "held"}
  - {"conjunct": 3, "class": "gate", "cmd": "apply_unified_diff: (a) the printed diff with the marker line stripped against an unterminated file; (b) the EF.83-style split('\\n') diff against the same file", "expected": "both refuse (EditError) rather than silently mis-land", "observed": "(a) removal mismatch at original line 2 (refused); (b) context mismatch at original line 2 (refused)", "result": "held"}
production_lines: 71
profile: balanced
role: kid
scaffold_hash: d773d814833e726a
season: 2
thought_session: EF.87
title: "Standard unified diff: no-EOF marker, honoured by write and GNU patch"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-9b37d43d-5e1153

## Experiment — round 3: the printed diff is a STANDARD unified diff

Build order met: `extensions/agi/bin/write.py` now renders the `sub --dry-run`
preview with `_standard_unified_diff` (compared keepends, `\ No newline at end
of file` marker for an unterminated last line) and `apply_unified_diff` honours
that marker on both sides.

| seam | before (EF.83 bytes) | after (this tip) |
|---|---|---|
| render | `split("\n")` + `lineterm=""`; missing EOF newline -> phantom empty trailing line | `_split_keepends` + `lineterm="\n"`; missing EOF newline -> marker |
| applier | `original.split("\n")` / `"\n".join(out)`; marker = "bytes outside any hunk" | keepends lines + per-body `has_nl`; marker clears it |
| GNU patch | rejects (`Hunk #1 FAILED`, rc=1) or rc=2 | accepts, rc=0, bytes == landed |

`_split_keepends` splits on a bare `\n` only (not `str.splitlines`), so `\r`,
`\v`, `\f` in node bytes are not line breaks. `node_writer.py` is untouched,
so `update_node`'s output stays byte-identical by construction.

## Evidence

Scratch `.agi/sessions/iter-EF.87/a00-9b37d43d/probe_red_green.py` (result in
`probe_result.txt`), run against the tip.

Red on the EF.83 bytes (renderer reconstructed in-memory):
```
phantom bare '+' line present: False
GNU patch rc=2  patch unexpectedly ends in middle of line
new applier on OLD diff -> EditError: context mismatch at original line 11:
    diff expects 'the body says nothing here\n', file has 'the body says nothing here'
```
(an earlier probe of the live base with `_sdiff += "\n"` gave `Hunk #1 FAILED`, rc=1)

Green on the tip:
```
marker present: True
new applier == landed: True
GNU patch rc=0
GNU patch == landed: True
```

Committed tests (red on the base, green on the tip):

- `test_sub_dry_run_diff_is_a_standard_unified_diff` — the three EF.83 shapes
  plus a plain canonical node; asserts write's applier lands, no bare `+`
  phantom, marker iff no EOF newline, and GNU `patch` on the raw bytes lands
  the same bytes. The patch half `pytest.skip`s by name when `patch` is absent
  (`shutil.which`).
- `test_apply_unified_diff_honours_the_no_newline_marker` — the marker strips
  the trailing newline; absent marker refuses rather than mis-landing; the
  added line may be the unterminated one.

Suite: `env -u TMUX -u TMUX_PANE python3 -m pytest
 extensions/agi/tests/test_write_sub.py extensions/agi/tests/test_write.py
 extensions/agi/tests/test_node_writer.py -q` -> **261 passed**.

`git diff --numstat -- extensions/agi/bin/write.py` -> 71 added / 24 removed
(under the 2x = 80 stop).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review EF.87 (a00-632e0d0d). (1) Instruction, quoted: "REVIEW THE BYTES, NOT THE RESULT FILE: a kid's own tests are its CLAIM, not your evidence ... Run one negative probe per claim conjunct yourself and record them as probes:; a kid that passes its own suite but fails your probe is lean_disproved with the probe named." (2) What I read and ran. DIFF merge-base..season2/loops/hypothesis-sub-dry-run-preview-i-a00-9b37d43d: extensions/agi/bin/write.py +71/-24 (new _split_keepends splitting on a bare \n only; new _standard_unified_diff over keepends lines with lineterm="\n" appending the '\\ No newline at end of file' marker after any content line that lacks a trailing newline; apply_unified_diff now keepends with a per-entry has_nl that the marker line clears; write.main's dry-run calls _standard_unified_diff instead of split("\n")+lineterm="" and drops the old '+= "\n"'); extensions/agi/tests/test_write_sub.py +81 (test_sub_dry_run_diff_is_a_standard_unified_diff over the three EF.83 shapes plus a canonical node -- write's applier == landed, no bare '+' phantom, marker iff no EOF newline, GNU patch rc=0 and == landed, pytest.skip by name when patch is absent; test_apply_unified_diff_honours_the_no_newline_marker). node_writer.py UNTOUCHED, so update_node is byte-identical by construction. My own probes (scratch probe_parent.py, run against the kid bytes): [no_eof_newline] marker=True, write_applier==landed, GNU patch 2.7.6 rc=0 and ==landed, no_phantom=True; [fm_render_rewrite], [dup_body_frontmatter], [blank_tail] marker=False, both appliers ==landed; [fm_only_noeof] (a shape the kid did NOT test) marker=True, both appliers ==landed; marker removed on an unterminated file -> EditError (refused, no mis-land); the EF.83-style split diff fed to the new applier -> EditError (refused). Named suite 261 passed. (3) Near miss: rendering over split("\n") with lineterm="" satisfies 'the printed diff round-trips write's own applier' and loses GNU patch -- the phantom trailing '' element models a missing EOF newline the way no standard tool reads it, which is exactly the EF.83 residual this round closes. (4) Deviation: I spawned the kid under its own --branch. The current cmd_done order (_append_verdict_to_node at :1655 runs before _auto_commit_worktree at :1738) cannot land a parent review on a separate kid branch in ONE done, because the node is not in the parent checkout when the append runs; the review here is committed by a second done after the branch merge. Accepted the kid's proved verdict; probes pass.
<!-- THOUGHT:END -->

## Agent Notes
sub --dry-run now renders a standard unified diff (keepends, no-EOF marker) and apply_unified_diff honours it; GNU patch and write's applier both land the landed bytes across the 3 EF.83 shapes + canonical; 261 passed; 71 added/24 removed in write.py

Parent EF.87 review: ACCEPTED proved. Read the kid DIFF (write.py +71/-24, test_write_sub.py +81, node_writer.py untouched); 5 independent shapes + 2 refusal probes all hold (no-EOF marker, GNU patch rc=0 == landed, no phantom, marker-removed and EF.83-style both refuse); named suite 261 passed. Struggle: a --branch kid's node is not in the parent checkout when done's node-append runs (:1655 < :1738), so one done cannot land the review; committed via a second done after the merge (duplicate dispatcher dm).
