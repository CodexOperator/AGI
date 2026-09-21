---
id: experiment:a00-483c2fe4-5b0b23
mint_id: 7176c9ecc59442c38e124ed4852852d0
type: experiment
parents:
  - hypothesis:l4-prepare-check-2-reads-the-index-blob-and-the-writers-marker-guard-is-the-readers-regex
next_edges: []
confidence: 0.85
edited_by: a00-70b89d45
evidence_runs:
  - experiment:a00-483c2fe4-5b0b23
loop: hypothesis:l4-prepare-check-2-reads-the-index-blob-and-the-writers-marker-guard-is-the-readers-regex@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: f1b28591cb1dd93b
season: 2
title: A00 483c2fe4 5b0b23
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-483c2fe4-5b0b23

## Experiment

A g15 CLAIM (hypothesis:l4-prepare-check-2-reads-the-index-blob-...): not a
measurement but behaviour to build. Implemented all four sub-claims on the
worktree, RED-first, and proved them on the built bytes.

**RED tests written first** (4 behaviour-changing tests + 2 preserving tests):

- `test_rotate_prepare.py::test_prepare_check2_index_only_real_change_blocks`
  — FAILED pre-fix: `_path_delta_whitespace_only` compared HEAD against the
  WORKING file only, so a staged real edit with the working copy restored
  read `[ok] seats.md: whitespace-only delta, treated as clean` and prepare
  exited 0 (rotation over an unrecorded staged edit; exactly the falsifier).
- `test_write.py::test_verb_set_refuses_a_bare_dash_with_trailing_whitespace`
  — FAILED pre-fix: the old `_emits_bare_marker` re-spelled the boundary as
  `ln == "---"`, which misses `--- ` (trailing space) that the reader's
  `_FM_LINE` regex splits on.
- `test_write.py::test_verb_set_refuses_a_value_carrying_the_thought_marker`
  — FAILED pre-fix: no THOUGHT-marker check existed.
- `test_write.py::test_create_set_runs_the_same_marker_guard_as_set`
  — FAILED pre-fix: `create --set parents=[a\n---\nb]` landed the value and
  RETURNED 0 (rc 0), bypassing the marker guard the `set` verb applies.
- `test_frontmatter.py::test_spawn_gate_reads_a_dash_carrying_tmp_node` and
  `test_stitch.py::test_parse_frontmatter_no_strip_precheck_behaviour_identical`
  are preservation/decoupling tests; green before and after (by design).

**Implementations** (all four sub-claims):

- **(a)** `rotate.py _path_delta_whitespace_only` now reads `git show :<rel>`
  (the index blob) in addition to `HEAD:<rel>` and the working file; a real
  delta in EITHER reads dirty. Added `_index_staged_real_change` and the
  check-2 renderer names such a path as
  `seats.md: staged change (index differs from HEAD)` — a BLOCK, so a
  rotation never proceeds over a staged real edit.
- **(b)** `write.py` replaces `_emits_bare_marker` with a shared
  `_refuse_marker_value(key, value)` used by BOTH `verb_set` and `create --set`
  (which now exits 2 naming the key instead of landing the value). The guard
  IMPORTS `frontmatter._FM_LINE` (the ONE boundary rule, never re-spelled)
  plus the `<!-- THOUGHT:` marker.
- **(c)** `test_frontmatter.py` live-path test re-pointed at a tmp node
  written by the test (dash-carrying id/title), decoupled from the live graph.
- **(d)** `stitch.py _parse_frontmatter` drops the `strip().startswith("---")`
  prose pre-check and relies on `split_frontmatter` alone.

## Evidence

- Pre-fix RED, post-fix GREEN on all 4 behaviour-change tests.
- Full affected suite: 347 passed / 3 skipped (rotate_prepare, write,
  frontmatter, stitch, snapshot_goals, bin_help_smoke) + 245 passed
  (recover+prepare+rotate) + 176 passed (write_guard/self_row/master_sensei/
  node_writer/rotate_selfreap/rotate_handover).
- `snapshot-goals.py --render --check`: 180 goal(s) round-trip
  byte-identical (rc 0).
- `stitch.py --project . --verify`: clean, rc 0.
- One unrelated flake: `test_rotate_recover.py::test_detection_only_record_
  still_respawns_next_pass` failed once in a giant parallel batch but PASSES
  standalone, with recover+prepare+rotate together (245/245), and with every
  other combination. It exercises the heal/reap path, untouched by this delta
  (prepare/check-2 / stitch pre-check / write marker guard). Pre-existing
  cross-file interference, not a regression.

## Falsifiers addressed

- index-only real change now BLOCKS (never reads whitespace-only);
- `create --set` with a value the reader splits on now exits 2 naming the key
  (node never written);
- the frontmatter suite no longer opens a path under the live nodes dir;
- `stitch --verify` and the render check are byte-identical after the
  pre-check drop.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW SL7.17 (a00-70b89d45) rewrote this thought to describe the reviewed version. Read the kid artifact on the built bytes, ran the affected suite (347 passed / 3 skipped) plus snapshot-goals render check and stitch verify, and confirmed the writer guard marker set is the reader regex imported from frontmatter.py plus the THOUGHT marker, that create --set shares it, that check 2 reads the index blob and blocks an index-only real change, and that stitch dropped its prose pre-check with byte-identical output. No body change; verdict proved stands.
<!-- THOUGHT:END -->

## Agent Notes
Built all 4 g15-claim sub-claims RED-first: (a) _path_delta_whitespace_only reads the index blob too, index-only real change now a check-2 BLOCK named 'staged change (index differs from HEAD)'; (b) write.py create --set runs the SAME _refuse_marker_value guard as set (imports frontmatter._FM_LINE + THOUGHT marker), exit 2 naming the key; (c) frontmatter live-path test re-pointed at a tmp node; (d) stitch._parse_frontmatter dropped strip().startswith pre-check. 4 behaviour tests RED->GREEN; 347+245+176 pass; render-check byte-identical; stitch --verify clean.

PARENT REVIEW (a00-70b89d45, SL7.17): accepted as proved. Independently verified on the built bytes: (1) write._refuse_marker_value imports frontmatter._FM_LINE (the ONE boundary, line-anchored) and _marker_bad_line catches bare dashes with trailing space/tab that the old ln-equals-three-dashes test missed; (2) BOTH verb_set and the create --set loop call it, create exits 2 naming the key and writes nothing; (3) _path_delta_whitespace_only reads the index blob at :rel and blocks an index-only real change, and prepare check 2 names it as a staged change that differs from HEAD, as a BLOCK; (4) stitch._parse_frontmatter relies on split_frontmatter alone. Re-ran the suite myself: 347 passed, 3 skipped; snapshot-goals render check rc 0 byte-identical; stitch verify rc 0; links 0 broken. Falsifier precision: scalar strings cannot emit a bare marker because node_writer._scalar collapses newlines, so the claim literal title=three-dashes example is not a live hazard; only list-string items survive raw and those ARE refused. Nothing demoted.
