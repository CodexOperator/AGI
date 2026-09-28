---
id: hypothesis:box-logs-dir-resolves-from-one-config-cell
mint_id: 1896599e76554d3b84559bb9297f1e07
type: hypothesis
parents:
  - goal:g6.49
  - hypothesis:cron-layer-keeps-its-disk-footprint-bounded
next_edges: []
edited_by: director-engine
scaffold_hash: 94dac3cecacc1acf
season: 2
testable_claim: crons.logs_dir(root) reads logs.dir (default {home}/logs, value unchanged); grid.py:1768 and rotate.py:6911 call it; {logs} renders from it; no engine literal names the dir
title: "The box logs dir resolves from ONE config cell (logs.dir) so moving every log is one cell edit (assigned: director-engine)"
town: core
---
# hypothesis:box-logs-dir-resolves-from-one-config-cell

## Why this exists
Prime [decision] 2026-09-27 22:2xZ, relaying the OWNER (verbatim on town:local-maxxing): a new disk is mounted for LOGS and sequential
scratch ONLY -- never worktrees or test tmp; each writer moves by a config cell/symlink WITH its writer, never by a live mv under a running
writer. The move plan is thought-master's (box/guard); "DE: the engine log-path cells are yours". This round builds the cell, not the move.

## Measured
- `extensions/agi/bin/crons.py:453-457` `logs_dir()` -- "the ONE place `enforce_log_caps` looks" -- returns the literal `Path.home() / "logs"`.
- `extensions/agi/bin/grid.py:1768` the grid-sync log bypasses it: `Path.home() / "logs" / f"grid-sync-...log"`.
- `extensions/agi/bin/rotate.py:6911` reaper-log discovery bypasses it: `expanded = Path.home() / "logs"`.
- `.agi/nodes/.geometry/crons.md:62` the crontab already renders a `{logs}` placeholder; `.agi/config.json` `logs` holds cap_mb / rotations /
  alerts_file / also_manage but NO directory cell. Box io PSI some avg60 ~61 at 22:3xZ (the TMM.306 gate needs < 50).

## CLAIM
The box logs directory resolves from ONE config cell, `logs.dir` in `.agi/config.json` (value `{home}/logs`: today's path, unchanged by this
round), read by `crons.logs_dir(root)`; grid.py:1768 and rotate.py:6911 call that resolver instead of their literals, and the crontab's `{logs}`
renders from it -- so moving every box log is ONE cell edit plus `crons.py apply`, and no engine file names the directory.

## Dispatch line
config-max: `logs.dir` cell (value `{home}/logs`) in the existing `logs` block · template-max: none (crons.md already writes `{logs}`) ·
code: the resolver reads the cell + the two call sites stop hard-coding it. NEVER change the cell's VALUE (the move is thought-master's).

## FALSIFIERS
1. `git grep -n 'home() / "logs"' -- extensions/agi/bin` still hits outside the resolver's default.
2. With `logs.dir` set to a tmp dir in a tmp graph, `crons.logs_dir`, the grid-sync log path, reaper-log discovery or the rendered `{logs}`
   crontab line names a path outside that tmp dir.
3. With the cell ABSENT, any of them differs from today's `{home}/logs` (the default must be byte-identical behaviour).

## TESTS
New `extensions/agi/tests/test_logs_dir_resolves_from_one_cell.py` (falsifiers 2 and 3, tmp graphs only) + neighbourhood
test_crons.py test_crons_log_cap_declared_scope.py test_crons_disk_footprint_bounds.py test_bin_help_smoke.py (timeout 900, --basetemp under
/tmp, env -u TMUX -u TMUX_PANE). Never a live crontab, pane, seat or real `crons.py apply`.

## FILE SCOPE
extensions/agi/bin/crons.py · extensions/agi/bin/grid.py · extensions/agi/bin/rotate.py · .agi/config.json (the ONE new cell) ·
extensions/agi/tests/test_logs_dir_resolves_from_one_cell.py · the kid's own node

## CEILING
HARD CAP: 1 kid · <= 15 production lines net · <= 60 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut.
PARENT: paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit.
ANON: no user name, home or repo path value, mount path, host, IP or hardware name in any byte; patterns write <user>.

## CORRECTIVE DH.676 -- closes mur-director-engine-44 DH.667-k1 demote
BASE      CUT FROM season2/loops/hypothesis-box-logs-dir-resolves-a00-8f91136c tip c0ba1f156 (branch de-base-676; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
DESIGN    (director, over the brief) the brief's Measured line was WRONG: `.agi/config.json` box.logs_dir already exists and [box].md:18 REQUIRES it -- it is THE one cell. So: DROP logs.dir entirely; crons.logs_dir(root) reads box.logs_dir ONLY; set its VALUE to `{home}/logs` (expands to the same dir on this box -- byte-identical behaviour, the old literal home path is gone); `{home}` expands, a relative value resolves against box.root, a malformed value raises by name like logs.alerts_file; a resolved dir that does not exist is a LOUD refusal line from enforce_log_caps (never a silent []); the no-arg logs_dir() form is removed (every caller passes root). The disk-footprint bound (item on enforce_log_caps) must hold on THIS box's shape: a schema-valid box block in the fixture.
1. Verdict field contradicts the round's own review (node:21 verdict: proved / confidence 0.85)
2. HARD CEILING breached twice (19 net production lines vs 15; 64-line test vs 60)
3. Relative logs.dir honoured verbatim (CWD-relative 'var/logs', not resolved against box.root)
4. Malformed logs.dir falls back silently and masks a valid box.logs_dir (crons.py:469)
5. logs.dir declared nowhere (precedence exists only in a docstring)
6. Previously-inert box.logs_dir now live for four writers, with no log line
7. Legacy-marker project splits the claim (agi-tree.config.json at a repo root short-circuits the .agi retry)
8. THE ROUND TURNS THE DISK-FOOTPRINT BOUND OFF ON THIS BOX, AND ITS OWN TESTS CANNOT SEE IT. Measured against the committed bytes and the live configs (.agi/config.json in the worktree and the main repo both carry `box.logs_dir: <home>/logs`; $HOME=<home> and <home>/logs exists and holds 46 MB of live logs -- agi-crons-agi-3fbc6951.log.1 sits at exactly 16777216 bytes = the 16 MB `logs.cap_mb`, so the cap is holding TODAY): after the round `crons.logs_dir(.agi) -> <home>/logs` (is_dir False) where the old literal gave <home>/logs (is_dir True). Consequence chain, all read from the committed code: crons.py:720-721 `cap, out, d = ..., logs_dir(root)` then `if not d.is_dir(): return []` -- enforce_log_caps now returns [] and bounds NOTHING, so the 46 MB already in ~/logs grows with no cap; grid.py:1769 sends the every-5-min grid-sync redirect to a nonexistent dir; rotate.py:6912 stops finding the 10 MB and growing agi-reaper-agi-2f118e6f.log, which keeps growing in the old dir; and .geometry/crons.md:62 `AGI_REAPER_LOG: "{logs}/..."` now names the nonexistent dir, so the reaper writes a second, uncapped file. The hypothesis this round hangs under is `hypothesis:cron-layer-keeps-its-disk-footprint-bounded`, and the owner's stated pressure (box io PSI ~61, a new log disk pending) is exactly what this breaks. No committed test covers the live shape: the new fixture (test file :25) writes a box block with root/user/tmux_session only, and test_memory_alarm.py:162 asserts `crons.alerts_log(root).parent == crons.logs_dir()` -- a comparison that is vacuous precisely when the cell is present.
9. The new fixture is not a schema-valid box block, which is why falsifier 3 could be proved and the live shape stayed invisible: `.agi/context/schemas/[box].md:18` declares `required: [root, logs_dir, tmux_session, user]`, and `_graph()` (test file :25) omits logs_dir. The 'cell absent' case the test proves byte-identical is a shape the schema forbids on a real box.
10. A green test that certifies less than the claim: `test_the_box_logs_dir_cell_is_the_same_one_cell` (test file :54-64) asserts only crons.logs_dir and grid.cron_log for the box cell. The claim's other two named surfaces -- the rendered `{logs}` crontab line and `enforce_log_caps`' directory -- are unasserted for the box cell, so 'the cap follows the cell' is unevidenced on the path that actually matters.
11. Test-suite fragility the '3 passed' line hides: the new tests reach the placeholder map through boxes.py:26-27 (`parents[3]/.agi/context/schemas/[box].md`). Extracted into an engine tree with no `.agi/`, 2 of the 3 fail with `BoxSchemaError: ... declares no 'placeholders:' map` (measured), because `_graph()` builds a graph with no schema of its own. Pre-existing engine coupling, not this round's defect, but '3 passed' is tree-dependent and should not be cited as bare evidence.
12. Stale surface the round leaves behind: crons.py:449 and :479 still name the no-arg `logs_dir()` while every caller now passes a root, and the no-arg form still returns the default -- the one hole the node's own Caveats names. A future caller that forgets its root silently writes to the old dir, which is the one dir the live logs are in.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_logs_dir_resolves_from_one_cell.py test_memory_alarm.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/bin/crons.py · extensions/agi/bin/grid.py · extensions/agi/bin/rotate.py · extensions/agi/tests/test_logs_dir_resolves_from_one_cell.py · extensions/agi/tests/test_memory_alarm.py · .agi/config.json · .agi/nodes/.geometry/crons.md · .agi/nodes/experiment/a00-36a7c300-c9956a.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 25 production lines net over c0ba1f156 · <= 80 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)


## OPEN at the 2026-09-28 merge-up (director-engine; belam [decision] 00:0xZ: in-progress included)
STATUS    IN PROGRESS, not landed: DH.676 PLACED (parent a00-a6dd3d2f); open loop branch season2/loops/hypothesis-box-logs-dir-resolves-a00-a6dd3d2f d22b6f2d1 -- murq125 reviewing.
ROUNDS    this post's rounds on this node: DH.667 DH.676; the open round's bytes live on its loop branch, never on the post branch, until its mur clears.


## CORRECTIVE EG.2 -- closes mur-director-engine-47 DH.676-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-box-logs-dir-resolves-a00-a6dd3d2f tip d22b6f2d1 (branch de-base-EG.2; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. Undeclared {home} token in a schema-REQUIRED cell — .agi/context/schemas/[box].md:12 / boxes.resolve_placeholders raises BoxSchemaError on the raw cell; green only via the crons.py:866 override
2. Cap dir keyed to the RUNNING user's HOME, not box.user — .agi/config.json:192 / crons.py:488
3. paths.py audit can no longer classify a logs literal — extensions/agi/bin/paths.py:20
4. Hard-cap breach with an invented cap — .agi/nodes/experiment/a00-0331624d-832c81.md:135 (33 net production lines reported as '(ceiling 40)')
5. hypothesis testable_claim/title still name the abandoned logs.dir cell — .agi/nodes/hypothesis/box-logs-dir-resolves-from-one-config-cell.md:12
6. Second hand-rolled token map outside the schema resolver — extensions/agi/bin/rotate.py:6915
7. UNCOVERED CHANGE (the round's second surface has no test at all): rotate.py:6910-6917 is exercised by NOBODY. test_logs_dir_resolves_from_one_cell.py:52 asserts rotate._reaper_log_path(graph) == target/'agi-reaper-old.log', but the _graph() fixture (test file :25-41) writes no nodes/.geometry/crons.md, so the assertion is satisfied by the FALLBACK glob at rotate.py:6918-6924 — 'agi-reaper-old.log' matches agi-reaper-*.log — never by the changed lines. The only committed test of the node branch, test_rotate_autopsy.py:132-145, uses an ABSOLUTE path, not a {logs} token. So the falsifier-2 claim 'reaper-log discovery' in the node's row 2 (:44-49) and the 'second stale surface closed in the same pass' (:67-70) are asserted by an unrelated code path. UNVERIFIED — the probe I WOULD run (and did not, per the standing prohibition on rotate-family probes inside the Prime's pane): a fixture writing repo/.agi/nodes/.geometry/crons.md containing AGI_REAPER_LOG: "{logs}/agi-reaper-agi-2f118e6f.log" and asserting rotate._reaper_log_path(graph) == target/'agi-reaper-agi-2f118e6f.log', plus the negative that a value prefixed with a renamed placeholder no longer expands.
8. MISSING FIXTURE GUARD (latent real-resource touch): the new test file carries NO autouse HOME redirect, while its sibling declares one MANDATORY — test_crons_disk_footprint_bounds.py:63-75, 'NEVER let a test in this file see the real ~/logs … Without this, a test that declares `logs` cells rotates the REAL reaper log. A first draft of this file did exactly that, on this box, at 02:39Z.' And the new file deliberately exercises the ABSENT-cell path, which resolves to the REAL ~/logs (test file :56-63, crons.logs_dir(graph) == Path.home()/'logs'). Today nothing real is touched — I read both files and ran them: the only two enforce_log_caps calls (:72, :77) both use a declared tmp cell that either does not exist (early loud return, :741-747) or is empty, and the absent-cell test is pure path math — but the property holds by the fixtures' current content, not by a guard. One added enforce_log_caps line to the absent-cell test rotates the live reaper log.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
SEARCH    git grep or a NAMED path only -- NEVER a recursive grep / rg / find over /tmp, the repo root or .agi/worktrees (belam [red] 06:56Z: two such searches held io PSI at 84)
TESTS     test_logs_dir_resolves_from_one_cell.py test_memory_alarm.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/bin/crons.py · extensions/agi/bin/paths.py · extensions/agi/bin/rotate.py · extensions/agi/tests/test_logs_dir_resolves_from_one_cell.py · extensions/agi/tests/test_memory_alarm.py · .agi/config.json · .agi/context/schemas/[box].md · .agi/nodes/experiment/a00-0331624d-832c81.md · .agi/nodes/experiment/a00-36a7c300-c9956a.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over d22b6f2d1 · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective EG.2: mur-director-engine-47 DH.676-k1 residues batched into one corrective (orders above, generated from the verdict files).
<!-- THOUGHT:END -->
