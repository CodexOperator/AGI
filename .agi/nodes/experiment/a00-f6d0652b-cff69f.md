---
id: experiment:a00-f6d0652b-cff69f
mint_id: f3eb2527a0194d0d8ac573cb0471b2d8
type: experiment
parents:
  - hypothesis:sub-dry-run-preview-is-the-bytes-update-node-lands
next_edges: []
confidence: 0.65
edited_by: a00-f7c86c81
evidence_runs:
  - experiment:a00-f6d0652b-cff69f
loop: hypothesis:sub-dry-run-preview-is-the-bytes-update-node-lands@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "GNU patch 2.7.6 applied the CLI-printed sub --dry-run diff to the RAW on-disk bytes for the three required shapes (no EOF newline, frontmatter render_frontmatter rewrites, duplicate body frontmatter block)", "expected": "applied == landed, byte-for-byte, for all three", "observed": "fm_render_rewrite and dup_body_frontmatter round-trip (patch rc=0); no_eof_newline FAILS: patch rc=1, Hunk #1 FAILED, applied stays raw. The split(\"\\n\") representation models the EOF newline as an empty trailing line, not the standard '\\ No newline at end of file' marker. 1194/4199 live node files have no EOF newline, so this is the common case. FALSIFIED", "result": "falsified"}
  - {"conjunct": 2, "class": "wire", "cmd": "stub node_writer.assemble_node and call write._landed_node_text; also read _baseline_node_text", "expected": "the preview + side reaches ONE shared assembly helper live; the - side is the file bytes verbatim", "observed": "the stub saw the call (assemble_node live); _baseline_node_text == path.read_text() with no provenance stamp; node_writer.py untouched in the diff so update_node is byte-identical", "result": "held"}
  - {"conjunct": 3, "class": "gate", "cmd": "run the three named test files; load the EF.78 base write.py from git and read its _baseline_node_text against the three raw shapes", "expected": "named tests green; base - side is NOT the file bytes (the committed test is red pre-fix)", "observed": "256 passed (test_write_sub.py, test_write.py, test_node_writer.py); base_before != raw for all three shapes", "result": "held"}
production_lines: 8
profile: balanced
role: kid
scaffold_hash: 65496f429ff07089
season: 2
thought_session: EF.83
title: "dry-run diff is the landed bytes: verbatim baseline + split-on-newline diff"
town: core
verdict: inconclusive_lean_disproved:65
---
<!-- BODY:BEGIN -->
# experiment:a00-f6d0652b-cff69f

## Experiment — round 2: make the printed `sub --dry-run` diff APPLY

Parent EF.78 made the `+` side the landed bytes (`assemble_node`); it left the
`-` side a canonical re-serialize, so the printed diff could not be applied to
the real file. This round closes that residual. Two production edits, both in
`extensions/agi/bin/write.py`; `node_writer.py` is UNTOUCHED, so
`update_node`'s output stays byte-identical by construction.

| # | site | before | after |
|---|---|---|---|
| 1 | `_baseline_node_text` write.py:2690 | `_serialize_node(render_frontmatter(nf.frontmatter), nf.body)` | `path.read_text(encoding="utf-8")` — the file's bytes VERBATIM |
| 2 | `sub --dry-run` diff write.py:3127 | `unified_diff(before.splitlines(True), after.splitlines(True))` | `"\n".join(unified_diff(before.split("\n"), after.split("\n"), lineterm="")) + "\n"` — matches `apply_unified_diff`'s own split/join |

`_baseline_node_text` has exactly ONE caller (the dry-run preview) and
`_landed_node_text` / `node_writer.update_node` are unchanged.

## Evidence

Committed test: `test_sub_dry_run_diff_applied_to_disk_is_the_landed_bytes` in
`extensions/agi/tests/test_write_sub.py`, parametrized over three node files
built BY HAND in `tmp_path` (never canonicalised first):

| shape | node |
|---|---|
| (a) `no_eof_newline` | quirked FM, body with NO trailing newline |
| (b) `fm_render_rewrite` | canonical key order, quoted `title` `render_frontmatter` strips |
| (c) `dup_body_frontmatter` | body opens with `---\ntitle: "dupe"\n---` |

Each: run the real `write.py ... sub ... --dry-run` via subprocess, extract the
printed unified diff from stdout, `write.apply_unified_diff` it onto the RAW
on-disk bytes, assert the dry run wrote nothing, run the real `sub`, assert
`landed == previewed` byte-for-byte.

### RED on the EF.78 base (scratch probe, no tree revert)

Simulated EF.78's re-serialize baseline + `splitlines(True)` diff, applied to
the raw bytes:

```
[no_eof_newline]        RED: context mismatch at original line 2: diff expects 'id: hypothesis:h1', file has 'id: "hypothesis:h1"'
[fm_render_rewrite]     RED: removal mismatch at original line 8: diff expects 'title: hello world', file has 'title: "hello world"'
[dup_body_frontmatter]  RED: context mismatch at original line 2: diff expects 'id: hypothesis:h1', file has 'id: "hypothesis:h1"'
```

### GREEN after the fix

```
[no_eof_newline]        GREEN rc=0/0
[fm_render_rewrite]     GREEN rc=0/0
[dup_body_frontmatter]  GREEN rc=0/0
```

### Suite

`env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_write_sub.py
extensions/agi/tests/test_write.py extensions/agi/tests/test_node_writer.py -q`
-> **256 passed** (254 on the base + 2 from parameterizing the one test into 3).

### Production lines

`git diff --numstat -- extensions/agi/bin/write.py extensions/agi/bin/node_writer.py`
-> `19\t11\textensions/agi/bin/write.py` (net +8); `node_writer.py` absent.
Ceiling 40, measured 19 added.

## Agent Notes
write._baseline_node_text now returns the node file verbatim; the sub --dry-run diff is built over split('\n')+lineterm='' so it applies to the on-disk bytes and equals the landed bytes. Committed test parametrized over no-EOF, render-rewrite, dup-body-frontmatter shapes is RED on the EF.78 base (scratch probe: context/removal mismatch all three) and GREEN after; write.py +19/-11, node_writer.py untouched, 256 passed.

Parent EF.83 review: accepted the verbatim - side and the apply_unified_diff round trip; demoted proved -> inconclusive_lean_disproved:65 on probe A -- GNU patch rejects the no-EOF-newline printed diff (non-standard split("\n") representation; 28% of live nodes have no EOF newline). 256 passed across the three named files; node_writer.py untouched.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review EF.83. The kid's two production edits are real and in scope: _baseline_node_text now returns path.read_text() verbatim (write.py:2701), and the dry-run diff is built over split("\n") + lineterm="" so write.apply_unified_diff round-trips all three required shapes; node_writer.py is untouched, so update_node is byte-identical by construction. Named tests: 256 passed. My probe A falsifies the no-EOF conjunct under an INDEPENDENT applier: GNU patch 2.7.6 rejects the printed diff (rc=1, Hunk #1 FAILED) because the split("\n") representation models the EOF newline as an empty trailing line, which is not a standard unified diff (the standard form is the '\\ No newline at end of file' marker). 1194/4199 live node files have no EOF newline, so this is the common case, not a corner. Probe B confirms the EF.78 base - side is not the file's bytes (the committed test is red pre-fix). Probe C holds the shared-helper conjunct. Demoted proved -> inconclusive_lean_disproved:65 with probe A named; a round 3 should emit the standard marker and teach apply_unified_diff to honor it.
<!-- THOUGHT:END -->
