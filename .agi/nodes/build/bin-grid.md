---
id: build:bin-grid
mint_id: 0c772dbafc4845e7ad419180519d4243
type: build
parents:
  - idea:engine-grid
build_kind: code
confidence: 1.0
edited_by: season.py
origin: build-scan
payload_ref: extensions/agi/bin/grid.py
season: 1
tags:
  - build
  - code
  - g2.1
thought_session: season
title: "Build: extensions/agi/bin/grid.py"
---
`extensions/agi/bin/grid.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-grid`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/bin/grid.py
parse_ok: true
inputs:
- name: argparse
  how: '`import argparse` at line 50'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: os
  how: '`import os` at line 51'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: re
  how: '`import re` at line 52'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stat
  how: '`import stat` at line 53'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: subprocess
  how: '`import subprocess` at line 54'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 55'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 56'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: locations
  how: '`import locations` at line 61'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.read_text(encoding="utf-8")` at line 367'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.read_text(encoding="utf-8")` at line 300'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.read_text(encoding="utf-8")` at line 308'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: path
  how: '`path.read_text(encoding="utf-8")` at line 316'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: src
  how: '`src.read_bytes()` at line 987'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: dst
  how: '`dst.read_bytes()` at line 946'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cli-args
  how: builds an `argparse.ArgumentParser` (module-wide, no single call site)
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: find_project_root
  how: 'defines public function `find_project_root` at line 95, signature: (start:
    Path | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: repo_root
  how: 'defines public function `repo_root` at line 158, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: git
  how: 'defines public function `git` at line 170, signature: (root: Path, *args:
    str, input_text: str | None=None, check: bool=True)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _encode_component
  how: 'defines private function `_encode_component` at line 186, signature: (s: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sanitize
  how: 'defines public function `sanitize` at line 240, signature: (node_id: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _sanitize_legacy
  how: 'defines private function `_sanitize_legacy` at line 269, signature: (node_id:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: node_ref
  how: 'defines public function `node_ref` at line 287, signature: (node_id: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _node_ref_legacy
  how: 'defines private function `_node_ref_legacy` at line 291, signature: (node_id:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: session_ref
  how: 'defines public function `session_ref` at line 295, signature: (iter_n: str,
    agent: str, node_id: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: parse_node_id
  how: 'defines public function `parse_node_id` at line 299, signature: (path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: parse_mint_id
  how: 'defines public function `parse_mint_id` at line 304, signature: (path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: parse_payload_ref
  how: 'defines public function `parse_payload_ref` at line 312, signature: (path:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: default_engine_root
  how: defines public function `default_engine_root` at line 323
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: resolve_payload
  how: 'defines public function `resolve_payload` at line 331, signature: (root: Path,
    payload_ref: str, engine_root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: parse_parents
  how: 'defines public function `parse_parents` at line 358, signature: (path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: mint_node_ref
  how: 'defines public function `mint_node_ref` at line 398, signature: (mint_id:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: MissingMintIdError
  how: defines public class `MissingMintIdError` at line 410
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: write_ref_for
  how: 'defines public function `write_ref_for` at line 420, signature: (path: Path,
    node_id: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: build_id_index
  how: 'defines public function `build_id_index` at line 439, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: build_parent_mint_trailer
  how: 'defines public function `build_parent_mint_trailer` at line 451, signature:
    (path: Path, id_index: dict[str, Path])'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ref_tip
  how: 'defines public function `ref_tip` at line 476, signature: (root: Path, ref:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: git_mode
  how: 'defines public function `git_mode` at line 496, signature: (path: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: hash_path
  how: 'defines public function `hash_path` at line 511, signature: (root: Path, path:
    Path, *, write: bool=True)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: read_tree_entry
  how: 'defines public function `read_tree_entry` at line 526, signature: (root: Path,
    rev: str, name: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: materialize_entry
  how: 'defines public function `materialize_entry` at line 549, signature: (dst:
    Path, mode: str, data: bytes)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tree_entries
  how: 'defines public function `tree_entries` at line 567, signature: (root: Path,
    path: Path, payload: Path | None, *, write: bool)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: build_tree
  how: 'defines public function `build_tree` at line 586, signature: (root: Path,
    path: Path, payload: Path | None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: read_tree
  how: 'defines public function `read_tree` at line 593, signature: (root: Path, rev:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ensure_repo
  how: 'defines public function `ensure_repo` at line 606, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_init
  how: 'defines public function `cmd_init` at line 621, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: commit_file
  how: 'defines public function `commit_file` at line 640, signature: (root: Path,
    path: Path, ref: str, msg_prefix: str, *, trailer: str | None=None, payload: Path
    | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: iter_node_files
  how: 'defines public function `iter_node_files` at line 680, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_commit
  how: 'defines public function `cmd_commit` at line 684, signature: (root: Path,
    files: list[str], do_all: bool, session: tuple[str, str] | None, prefix: str='''',
    engine_root: Path | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _resolve_read_ref
  how: 'defines private function `_resolve_read_ref` at line 767, signature: (root:
    Path, path: Path, node_id: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: resolve_ref
  how: 'defines public function `resolve_ref` at line 785, signature: (root: Path,
    node_id: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_log
  how: 'defines public function `cmd_log` at line 804, signature: (root: Path, node_id:
    str, n: int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_diff
  how: 'defines public function `cmd_diff` at line 809, signature: (root: Path, node_id:
    str, back: int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_versions
  how: 'defines public function `cmd_versions` at line 827, signature: (root: Path,
    node_id: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: version_rev
  how: 'defines public function `version_rev` at line 844, signature: (root: Path,
    ref: str, node_id: str, version: int | None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_payload
  how: 'defines public function `cmd_payload` at line 861, signature: (root: Path,
    node_id: str, version: int | None, out: str | None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: engine_tracked_files
  how: 'defines public function `engine_tracked_files` at line 886, signature: (engine_root:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_checkout
  how: 'defines public function `cmd_checkout` at line 899, signature: (root: Path,
    node_ids: list[str], do_all: bool, dest: str | None, engine_root: Path | None=None,
    unmanaged: bool=True, force: bool=False)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_status
  how: 'defines public function `cmd_status` at line 1005, signature: (root: Path,
    engine_root: Path | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _rename_ref
  how: 'defines private function `_rename_ref` at line 1039, signature: (root: Path,
    old_ref: str, new_ref: str, write: bool)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_migrate_refs
  how: 'defines public function `cmd_migrate_refs` at line 1089, signature: (root:
    Path, write: bool)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_migrate_mint_refs
  how: 'defines public function `cmd_migrate_mint_refs` at line 1150, signature: (root:
    Path, write: bool)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_sync
  how: 'defines public function `cmd_sync` at line 1245, signature: (root: Path, remote:
    str | None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cron_log
  how: 'defines public function `cron_log` at line 1259, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cron_lines
  how: 'defines public function `cron_lines` at line 1275, signature: (root: Path,
    branch: str, mins: int, log: Path, publish_engine: bool=False)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: read_crontab
  how: defines public function `read_crontab` at line 1331
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: write_crontab
  how: 'defines public function `write_crontab` at line 1336, signature: (lines: list[str])'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cmd_cron
  how: 'defines public function `cmd_cron` at line 1344, signature: (root: Path, action:
    str, mins: int, publish_engine: bool=False)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: main
  how: defines public function `main` at line 1371
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: dst
  how: '`dst.write_bytes(data)` at line 563'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stdout
  how: 37 `print()` call(s) at line(s) [629, 631, 633, 637, 663, 727, 731, 742, 751,
    762, 763, 806, 824, 838, 883, 957, 963, 969, 995, 1000, 1026, 1035, 1036, 1131,
    1136, 1140, 1145, 1215, 1227, 1231, 1235, 1240, 1256, 1353, 1357, 1367, 1368]
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
*The reasoning below was authored as `build:bin-grid@v2` and migrated here when the `@v2` convention was retired (G2.10): a version is a grid commit, not a second node file.*

`sanitize()` becomes injective, plus a `migrate-refs` subcommand to move the 810+ refs already minted under the old, non-injective scheme.

**The defect, confirmed before touching anything.** `sanitize()` escaped exactly `%` (`->%25`) and `:` (`->%3A`), then collapsed *every other* character outside `[A-Za-z0-9._%-]` to `-`. Checked `git -C agi-tree for-each-ref refs/grid/node/level3` first, as instructed: `refs/grid/node/level3/bin-stitch-v2`, `.../lib-find-root.sh-v2`, `.../skills-agi-SKILL.md-v2` were already live in the collapsed form — minted from `build:bin-stitch@v2` etc. (`@` collapsed to `-`), so a hypothetical sibling id spelled with a literal hyphen instead of `@` would silently have shared that same ref and its version history. The function's own docstring argued against exactly this failure mode for `:` and then committed it for every other character.

**The fix.** `_encode_component()` (new): `%` is escaped first (`%25`), so the escape alphabet can never be forged by input. Every character outside `[A-Za-z0-9_-]` is then percent-encoded from its UTF-8 bytes, uppercase hex (`:`->`%3A`, ` `->`%20`, `~`->`%7E`, `@`->`%40`, non-ASCII multi-byte as multiple `%XX`). `.` is the one exception kept literal for readability (`autoresearch.config.json` stays readable, doesn't become a wall of `%2E`), but only where git's own rules allow it: a `.` is escaped instead of kept literal when it is the first or last character of the component, or the second-or-later `.` in a run (kills `..`), and a component ending in the literal 4-character suffix `.lock` gets its separating dot escaped too. Because escape sequences are always `%` + two uppercase-hex characters (the ord's hex digits are always `0-9A-F`, never a lowercase letter), a trailing `.lock` in the output can only have come from a literal trailing `.lock` in the input — so that final substitution can't collide with anything the general escaping already produced. `sanitize()` itself is otherwise unchanged: still splits on the **first** colon only (that part was already correct and load-bearing — its docstring records the `exp:x-r1:extend8` outage from splitting on every colon), just calls `_encode_component` instead of the old `clean()`.

`_sanitize_legacy()` / `_node_ref_legacy()` are frozen, byte-for-byte copies of the pre-fix logic, kept only so `migrate-refs` can compute what a ref used to be. Comment on them says explicitly: never "fix" these, fixing them blinds the migration to the bug it exists to repair.

**Verified, not assumed, that the new scheme is git-safe.** Rather than trust the reasoning that `%XX` is safe on all the cited git-refname rules (no control chars/space/`~^:?*[\`, no `..`, no leading/trailing `.`, no `.lock` suffix, no `@{`, no empty component, no lone `@`), every output in the test corpus is run through `git check-ref-format --allow-onelevel` per component and through plain `git check-ref-format` on the full ref, both in the test suite and by hand against ~24 hand-picked adversarial refs (leading/trailing dots, `..` runs, `.lock`, `@`, `@{HEAD}`, unicode, embedded `%3A`) before writing any test — all passed, 0 failures.

**Property tests added (`tests/test_grid.py`), the actual point of this change:**
- `test_sanitize_is_injective_over_adversarial_corpus` — ~35 ids including `x@v2`/`x-v2` pairs, `a:b:c`/`a:b-c`, `.lock`/`.locked`, leading/trailing/`...` dots, `@`/`@{HEAD}`, unicode (`café`), a literal `%3A` vs a real `:`. Asserts no two distinct ids share a `sanitize()` output.
- `test_sanitize_output_is_a_valid_git_refname` — every id in that same corpus, `git check-ref-format --allow-onelevel` on each path component and the full ref.
- `test_sanitize_real_agi_tree_corpus_round_trips_distinctly` — reads every real id out of the actual `agi-tree/nodes/` tree (sibling of the engine repo, located the same way `find_project_root` would; `pytest.skip`s if that checkout isn't present, so the engine repo's own test suite stays portable) and asserts the same two properties over the live 800+-node corpus, not just hand-picked cases.
- 5 tests for `migrate-refs`: dry-run touches nothing; `--write` moves the ref and preserves the commit (checked via `ref_tip` equality, not just "some ref exists"); a second `--write` run is a no-op (idempotency); a pre-existing, content-different destination ref is refused, not clobbered; two distinct ids sharing one old-scheme ref are reported as a collision and *neither* is touched.
- Updated `test_sanitize_refuses_ref_hostile_chars`, which hard-coded the old collapsed output (`"hyp/weird-id---"`); it now asserts the new percent-encoded value and documents why (collapsing was lossy, which is exactly the bug this version fixes).

`cd extensions/agi && python3 -m pytest tests/ -q`: 505 passed before, **513 passed after** (8 new tests, no regressions).

**Migration — run for real against `/home/ubuntu/work/agi-tree`.** Backed up first: `git -C agi-tree for-each-ref refs/grid --format='%(refname) %(objectname)' > /tmp/grid-refs-backup.txt` (828 refs captured). Restore any single ref from it with `git update-ref <refname> <objectname>` read from that file — nothing in this run needs it (see below) but it's there for any future write.

`migrate-refs` is dry-run unless `--write`; drives entirely off node ids found on disk (not off existing ref names), computing `_node_ref_legacy(id)` vs `node_ref(id)` for each. Ids whose old ref is shared by >1 distinct id are reported as `COLLISION` and never touched (no way to tell whose history the shared ref holds). Otherwise: unchanged if old==new or the old ref has no history yet; refused as `CONFLICT` if the destination already holds different content; renamed (create new + `update-ref -d` old, using the old ref's own SHA as the compare-and-delete guard) otherwise.

**Real result: 0 renamed, 810 unchanged, 4 conflicts, 0 old-scheme collisions.** Identical on the dry run and the `--write` run (nothing to write). This was not the expected shape and is worth stating plainly.

**Finding: the fix went live mid-task and a cron beat the migration to it.** `agi-tree/agi` is a symlink to this engine repo, so the moment `sanitize()` was edited on disk, every invocation of `grid.py` anywhere under `agi-tree` — including the project's own 5-minute auto-snapshot cron (`grid.py commit --all`, see `CLAUDE.md`) — started computing the *new* ref path. Between the edit and the migration run, the cron fired (`22:40:04`) and re-snapshotted every node, including the 4 whose old/new refs actually differ: `build:.gitignore`, `build:bin-stitch@v2`, `build:lib-find-root.sh@v2`, `build:skills-agi-SKILL.md@v2`. For each, that cron commit created a fresh **v1** under the new-scheme ref, because that ref had no prior tip — while the real 2-3-version history for that same node still sits, un-superseded, on the old-scheme ref. `migrate-refs` correctly refused to overwrite those 4 (destination exists, different history) rather than guess. I checked by hand (`git rev-parse <ref>:node.md`) that all 4 pairs have **byte-identical** blob content — the cron's v1 is a content duplicate of the old ref's current tip, so no information is currently at risk — but deliberately did not splice the histories or delete either ref myself: ref deletion is called out explicitly as irreversible in this task's brief, and a manual out-of-band splice is a different, unreviewed code path from the tested `migrate-refs` logic. Concretely broken *right now*: `grid.py versions "build:bin-stitch@v2"` reports `1`, while the real history (`git rev-list --count refs/grid/node/level3/bin-stitch-v2`) is `2`. Nothing is lost, but it's under-served via the CLI until reconciled. **Recommended remedy for a human or a future iteration:** for each of the 4, confirm the two blobs still match, delete the redundant single-version new-scheme ref, then re-run `grid.py migrate-refs --write` — at that point old==new-tip-absent for all four and they migrate cleanly, carrying their full history across.

Ref counts: `refs/grid/node` was 813 when first inspected, 818 immediately before `migrate-refs` ran (concurrent cron/other-kid activity in the live repo, unrelated to this change) and **818 immediately after** — unchanged, as expected from 0 renames. `refs/grid` total 828 throughout; the 10 `refs/grid/session/*` refs were checked and are already fully alphanumeric (`refs/grid/session/9011/kid-j/mvp/zoom-runtime-contract` etc.) — old and new schemes agree on all of them today, so no session-ref migration was needed, though `migrate-refs` as written only covers `refs/grid/node/*` (session refs encode `iter`/`agent` values that aren't recoverable from node ids on disk, so a general session-ref migration isn't the same kind of operation and wasn't attempted).

**Parent review, same version: the 4 conflicts are reconciled.** The recommended remedy was executed after independently re-confirming the precondition it rests on — for all four pairs, the old-scheme ref held the real history (2, 2, 3 and 2 versions) while the new-scheme ref held a single cron-minted v1, and `git rev-parse <ref>:node.md` returned an identical blob sha on both sides of every pair. A fresh full-ref backup was taken first (`/tmp/grid-refs-backup-prereconcile.txt`, 829 refs with shas; restore any one with `git update-ref <refname> <objectname>`). The four redundant new-scheme refs were then deleted with the compare-and-swap form `git update-ref -d <ref> <sha>`, so a concurrent cron write between read and delete would abort the delete rather than silently discard it — and the delete plus `migrate-refs --write` ran as a single invocation to keep the 5-minute cron window shut. Result: 4 renamed, 811 unchanged, 0 conflicts, 0 collisions. `grid.py versions` now returns 2 / 2 / 3 / 2 for the four ids instead of 1; a second `migrate-refs --write` reports 0 renamed (idempotent); no `-v2`-suffixed or dot-stripped old-scheme ref remains under `level3/`. Ref count 819 → 815, the drop being exactly the four deleted duplicates.

This is recorded as a same-version note rather than a v3 because it completes the migration this version exists to perform — the payload edit was never finished while four of its own target refs were left forked.

**Live-deployment hazard this exposed, and it is not really about grid.py.** The cron beat the migration because `agi-tree/agi` is a symlink and the cron line invokes the engine's working tree directly (`python3 /home/ubuntu/work/agi/extensions/agi/bin/grid.py`). There is no deploy step between saving an engine file and that file running in production every 5 minutes. Before the symlink relayout the clone changed only on `git pull`, which was an implicit — if accidental — staging gate. That gate is now gone, and this is the first thing it cost. The remedy is not to undo the symlink; it is that engine edits touching ref naming, node pruning or anything else the cron exercises need the cron paused for the duration, or need to be made in a way that is safe to half-apply. Worth a goal of its own; noted here because this node is the evidence for it.

**Not migrated: the fantasia checkout.** `/home/ubuntu/work/fantasia/agi/` is an independent clone still running the pre-fix `sanitize()`, and its own 5-minute cron writes `refs/grid/*` in that repo under the old scheme. Nothing is wrong there yet — old-scheme refs are self-consistent — but the moment that clone pulls this change, its refs need `migrate-refs --write` too, and it will hit the same cron race unless the cron is paused first. Untouched here on purpose: it is a different project's data.

**Scope, stated plainly.** This fixes the *escaping* layer only: `sanitize()` is now injective, so a collision can no longer happen by accident of which characters get collapsed. It does **not** implement `goal:g2.5`'s actual target — hierarchical, zoom-encoded, alphanumeric-only ids where `sanitize()` becomes the identity function and the whole injectivity question disappears rather than being escaped around. That is a separate, much larger change (new id minting, a migration of every id string in the corpus, not just its ref encoding) and is untouched here.

**What I verified vs. assumed.** Verified: the live collapse via `for-each-ref` before editing anything; injectivity and git-refname-validity via `git check-ref-format` (not trusted from reasoning alone); the real 800+-id corpus round-trips distinctly (test skips gracefully if `agi-tree` isn't a sibling checkout, so the engine suite stays portable); the 4 conflict pairs have byte-identical content (`git rev-parse <ref>:node.md`); ref counts didn't drop; pytest 505->513. Assumed: that no other process besides this project's own documented cron could be writing grid refs concurrently (couldn't rule out a second concurrent kid running `grid.py commit`, though the timestamp and `cron: ` message prefix on all 4 conflicting commits matches the documented auto-snapshot exactly, not a kid).

**Cron subcommand superseded, not deleted — recorded 2026-08-29.** `grid.py`'s
`cmd_cron` (`read_crontab` / `write_crontab` / `cron_lines`, the code behind
`grid.py cron install`) has been superseded on this project by
`bin/crons.py`, which reads cadence and enablement from a graph node
(`nodes/.geometry/crons.md`, G10.2) rather than from install-time CLI flags.
Three concrete improvements drove the switch: (a) `crons.py` re-resolves the
branch via `git symbolic-ref` on every apply instead of capturing it once at
install time — this is exactly the S2 failure mode, where work sat on a stale
`iter24-extend-300hop` branch while a cron pushed `master` and published
nothing; `cmd_cron`'s installed line has no equivalent re-check. (b) the
`*/5` job re-runs `crons.py apply`, so editing the declaration node converges
the real crontab within 5 minutes, with no separate install step. (c)
`crons_live: false` on that node is a single-edit kill switch for every
managed line at once, where `cmd_cron` has no equivalent single flip.
Honestly: `cmd_cron` itself is untouched by this — the subcommand is still
present in this file and still fully functional if invoked. It is retired in
*practice* on this project, not removed from the code, and nothing here
stops someone from running `grid.py cron install` and getting a second,
unmanaged set of lines scheduling every job alongside `crons.py`'s managed
block. That double-scheduling risk is a real residual, not something this
change closes.
<!-- THOUGHT:END -->