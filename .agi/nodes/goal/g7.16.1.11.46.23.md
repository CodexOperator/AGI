---
id: goal:g7.16.1.11.46.23
mint_id: 0d53bd2c5f4249b3a21744326109c8eb
type: goal
parents:
  - goal:g7.16.1.11.46
next_edges: []
confidence: 0.5
edited_by: director-general-1
goal_id: G7.16.1.11.46.23
goal_kind: subgoal
origin: goal
seeds:
  - doc:brainstorm-unify
  - hypothesis:g7161146-w2-identity-and-the-grid
tags:
  - brainstorm
  - wave-2
  - V8a
season: 3
status: active
title: "G7.16.1.11.46.23: V8a -- write.py and its build node (bin-write) retired, goal:g4.18.7 retired as superseded: 0 callers in the live pieces, skills, crons, hooks and RULES docs; the read route that replaces it is named by path"
town: local-maxxing
---
# goal:g7.16.1.11.46.23

## Why this exists
goal:g7.16.1.11.46 (the brainstorm bundle, wave 2): the council cut wave 2 from hypothesis:g7161146-w2-identity-and-the-grid (belam's brief 2, dcc71c13c1; alive's [decision] 18:22:54Z 10-25, 3/3 with all-is-one and self-perpetuating, read at trunk d2ab3c19b8), after the W1 gate read PASSED EXCEPT BANKED (council 18:11:02Z 10-25). Doc §23, §34.6. Box reading K4: write.py is a LIBRARY as well as a CLI: 23 extensions modules import it, 15 exec lines sit in .geometry, skills and hooks, CLAUDE.md names it 4 times and QUICKSTART.md 3 times, and 1222 node files mention it as history prose (aio 4: CLAUDE.md's first instruction reads a goal with it; the hourly board commit is 'write.py: town:local-maxxing'). Independent of the grid, so it runs in parallel once its read route is named. Owner atom a1 closes HERE (council R1).

## OWNER atoms placed here (doc:card-belam §7 rows, verbatim; they close to leaf:goal:g7.16.1.11.46.23 when this node lands)
| # | atom (owner ask, short) | state |
|---|---|---|
| a1 | "Retire write py for sure we don’t need it at all and need to retire that whole build node as the capsule wrapper now tags everything for us using standard read routes" | target:W2 brief 2 leaf V8a (write.py out; supersedes g4.18.7) |

## Target end-state
- The read route that replaces `write.py goal:<id> 'read body ...'` is named BY PATH in this leaf's THOUGHT before any build.
- write.py and bin-write are retired (`status: deprecated`, moved under deprecated/, never deleted); goal:g4.18.7 is retired as superseded.
- The board job's town-cell write moves to the piece that replaces it; CLAUDE.md's command table and skill agi-node-write are edited in the same land (RULES paths: they land with belam).

## Invariants
- Retire, never delete (CLAUDE.md).
- Mentions in node history are history, not callers: they stay.
- Every falsifier carries a mutant that must read RED; an unreadable input prints `unread` and exits 1, never 0 or a pass.

## Falsifier
1. Callers = 0: `git grep -l -E '(^|[^a-z_])(import write|from write import)|write\.py +[a-z:]'` over extensions, skills, .agi/nodes/.geometry, the hooks, CLAUDE.md and QUICKSTART.md prints nothing outside the retired node and deprecated/.
2. The board's next hourly commit after the land lands through the replacement (its subject no longer reads 'write.py:').
3. `python3 -m pytest extensions/agi/tests/ -q` passes with write.py retired; mutant: one import left in a live module reads RED in the caller grep.
4. The source file is gone: `git ls-files extensions | grep -c '/write\.py$'` = 0 (keep the slash: without it test_town_cell_write.py and test_write.py match too). Mutant: write.py left in place -> 1 -> RED.
5. The bytes survive: `git show <parent of the retiring commit>:extensions/agi/bin/write.py` reads, and build:bin-write's last grid version's payload equals that blob (its sha is named in the retiring commit's THOUGHT); build:bin-write sits under .agi/nodes/deprecated/build/ with status deprecated and payload_ref extensions/agi/bin/write.py unchanged; goal:g4.18.7 is retired in the same land. Mutant: a payload that differs from the parent's blob reads RED.

## Out of scope
goal:g7.16.1.11.46.15 SEAL · goal:g7.16.1.11.46.16 G1a · goal:g7.16.1.11.46.17 G1b-1 · goal:g7.16.1.11.46.18 G1b-2 · goal:g7.16.1.11.46.19 V1 · goal:g7.16.1.11.46.20 V2 · goal:g7.16.1.11.46.21 U3 · goal:g7.16.1.11.46.22 U6 · goal:g7.16.1.11.46.24 V4 · goal:g7.16.1.11.46.25 M9 · goal:g7.16.1.11.46.26 M10 · waves 3-4 · season 4 (§15) · the owner's banked items (card-belam §6)

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
alive 10-25 (mint, v1): cut by the council's word on brief 2 (alive [decision] 18:22:54Z 10-25, 3/3). The falsifier is the council's; the builder sharpens it in its first commit and names any change here.

director-general-1 10-25 (v2, step 1, nothing built yet). FALSIFIER CHANGE, named: items 4 and 5 are ADDED, both from the council's [decision] 18:49:12Z 10-25 rows (a) and (b) (3/3); items 1-3 are as minted.

THE READ ROUTE that replaces `write.py goal:<id> 'read body N:M'`, by path.
- A node in a checkout is a plain file `.agi/nodes/<type>/<name>.md`; for a goal `<name>` is the lowercased goal_id (goal:g5.34 -> `.agi/nodes/goal/g5.34.md`). `sed -n '1,60p' .agi/nodes/goal/<id>.md` reads it, `sed -n '/^## Falsifier/,/^## Out/p' <that file>` one section. Tried on this leaf, no python.
- Type dir unknown: `git grep -lE '^id: <id>$' -- .agi/nodes` (the lookup ~/bin/agi-wt line 4 runs). A post's RAM tree: `agi-wt pull <id>`, the file at `$d/$(head -1 $d/.p)`. Off the checkout: `git show core/season3/main:.agi/nodes/<type>/<name>.md`.
- CLAUDE.md line 4 and QUICKSTART.md line 14 move to this route in the RULES-doc land (belam).

HOW `retire` IS DONE WITHOUT write.py (council row (c), aio): write.py is NOT used for its own retire. A node is retired by `node_writer.retire_node(root, '<id>', note='<why>')` (extensions/agi/bin/node_writer.py:1423, a library that stays: status: deprecated + the move to .agi/nodes/deprecated/<type>/ as ONE act; `root` is the `.agi` dir; tried on a copy of build:bin-write in a scratch tree, result 'updated', moved to deprecated/build/, status deprecated, payload_ref untouched), or by the by-hand form of the three precedents 5d13b7f562, 01cd966283, 03e8c6d61f: `status: deprecated` + `deprecated_on: "<date>"` in the frontmatter and `git mv .agi/nodes/build/<n>.md .agi/nodes/deprecated/build/<n>.md`. Either way it is IN the SAME commit that removes the source file (a status-only deprecate is refused by verify; node_writer.py is not retired by this leaf, so the route outlives write.py).

WHERE A RETIRED write.py GOES (council 3/3 18:49:12Z): NOT extensions/agi/deprecated/. The retiring commit REMOVES extensions/agi/bin/write.py (plus the tests the census retires) and moves build:bin-write to .agi/nodes/deprecated/build/ with status deprecated, payload_ref kept; the last blob sha is named in that commit's THOUGHT; goal:g4.18.7 retires in the same land. The census names build:bin-write-guard as retired with it, or kept with a reason. 'Moved under deprecated/' in this leaf means the NODES.

CENSUS at the trunk (git grep, 10-25): write.py 4615 lines. Library importers outside tests: commands.py, rotate.py (10 sites), season.py, send.py (2), src/seatsig/countersign.py, using only submit (17), _load_seats (11), verb_set (2), Edit + EditError, _default_actor (2), _enforce_written_by. node_writer.py (1867 lines, imported by ~10 modules) stays. CLI-form `write.py <verb>` hits: 117 files under extensions (mostly tests and fixtures), 8 skills, 7 .geometry nodes (12 exec lines), CLAUDE.md x4, QUICKSTART.md x3.
Next tips, each to SM for the gate with a mutant: (a) the 8 library names move out of write.py, the 5 importers + their tests follow; (b) the exec lines and docs; (c) the board job's town-cell write through the replacement; (d) the retiring commit above.
director-general-1 10-26 (v3, tip 3a; council decisions alive 23:28:02Z 10-25 (the commit tail), 00:08Z-00:3xZ 10-26 (the re-cut), belam 00:3xZ 10-26 (g17_1_note)).
WHAT 3a DOES: the runtime shell-outs to write.py by variable move onto node_writer + node_commit.land (extensions/agi/bin/node_commit.py): council_report.write_body, failures --write-node, metrics_cell (the board's hourly job), sensei.apply_note, season._write_node. land() samples what is already dirty and REFUSES before writing (`commit_paths: <path> already dirty: refused, nothing written`; write.py's _pre_dirty as it was, fail-closed rc>=2 included), writes through update_node / replace_payload, then ONE by-exact-path commit under the suite-lock hold with a bounded index.lock retry; a sha check right before `git add` refuses a hand edit that lands during the wait. LOUD: every refusal is a CommitRefused with one named line and a non-zero exit. A checkout git cannot read (dubious ownership, a broken .git) is refused, a plain directory with no .git anywhere is said aloud (`node_commit: <root> is not a git checkout: written, not committed`): never a silent nothing. DROPPED as decided: the inflight markers / peer wait, the write.commit_message cell.
THE BOARD (falsifier 2): metrics_cell commits `board: town:local-maxxing (belam)`; board_job.SUBJECT_RE accepts `board:` and, for the commits the retired writer left unlanded at the cutover, `write.py:`. NAMED DROP ROW (DG1): after the first `board:` land, `git log` of posts/<post> shows 0 unlanded `write.py: town:` commits, then the alternative goes in ONE line with a lane row asserting `write.py:` fails. The job's START check waits the same bounded hold_wait_s node_commit uses (one loop, node_commit.wait_lock), then a lock still held = rc 3 `ERR: ... suite lock held past <n>s`, nothing written; a dirty node = rc 3, nothing written.
THE NAMED GAP: season._preflight_cells (PASS 0, SM.106) is deleted with write.py's written_by admission it reached. Until R-land flips to enforce, a written_by-violating season cell write lands with only R-land's would-refuse line. WIDER (alive 00:17:51Z): four schemas declare written_by ([config], [moral], [town], [vision]); write.py._enforce_written_by is their ONLY enforcer and R-land judges posts/seats ROWS only. ROW (V8a, BEFORE step 4 retires write.py): r-land's sibling judges, by signer, any commit in BASE..TIP changing a node whose type schema declares written_by (R1 ring, R3 unread, report mode, flipped with R-land's one mode cell); mutant: a director-signed edit of a moral node -> `would refuse (written_by: owner)`. Until it lands, step 4's THOUGHT names the gap.
g17_1_note REMOVED (belam's decision, no veto, council form: in THIS tip): goal:g17.1 was RENUMBERED to goal:g7.16 by da2edb3f9e (09-20, same mint_id e4b3e68394164a47847333d1929c70df), the closeout step was never re-pointed and refused at every Prime closeout for 5 weeks; nothing was lost (the closeout numbers live in COMPLETE.md, the card and git). Re-pointing it would append one note per closeout to a 500-line goal node against "body is state". PRIME_CLOSEOUT_STEPS is now ["push"]. ROWS: the three closeout lists and the real seam table no longer name g17_1_note (mutant: the name back -> RED), and a closeout run prints no g17_1_note line. Two older rotate.py mentions of the goal:g17.1 RULING (:13342, :13442) are history and stay.
FALSIFIER AMENDMENT (named; sharpened by the builder, council alive 23:28Z): item 1 gains the pattern `WRITE_PY|["']write\.py["']|/write\.py` (a caller built from a variable), with a mutant; item 2 reads `board: town:` as the new subject; the read route's anchor is CONTENT, never file line numbers (all-is-one 00:18:25Z: `read body N:M` is BODY-relative; before each 3b cut every replaced exec line is diffed byte-for-byte against the old read).
3b (council GO 00:17:51Z, one tip): W1 = plain Write/Edit in the stage's own worktree + `git commit -- <path>`, ending with `python3 extensions/agi/bin/links.py schema` + `links.py links` on the stage's tree before the commit; W2 = node_writer.update_node where a validated frontmatter set is the point; W3 = drop where the engine mints the node; READ = sed -n by CONTENT anchor / `git show REV:path` (cat-file blob for a bracketed path).
v3 delta (re-cut 3, director-general-1 10-26 ~01:4xZ): (1) R-land (tip 2c re-cut 2, 21c5c828c9, GATE259 RETURN): the mode is read BEFORE the ring; the ONE report-mode rc 1 is a BASE or TIP that does not rev-parse (it runs before the mode is known, the mode lives at BASE: fail closed). (2) metrics-cell.t.sh lane e3-an-unreadable-lock-state: the old lane put a stub `verification.py` in the scratch bin, but node_writer puts the REAL bin first on sys.path, so once the START check goes through node_commit.wait_lock the stub was never the module imported (rc 0, the cell written, caught only by running the lane AFTER the lexists edit). The lane now pre-loads the stub through a sitecustomize on PYTHONPATH and asserts the START refusal (rc 3, the command did not run, HEAD unmoved, nothing dirty, an ERR naming the unreadable state); mutant: metrics_cell's start-check `except` narrowed to SystemExit -> rc 1, the lane RED. The real policy reader only WARNs on a bad cell (suite_lock_policy never raises on one), so a stub is the only way to make it raise.
v3 re-cut 3 (director-general-1 10-26 ~03:2xZ, GATE263 RETURN; council words alive 02:48:46Z + all-is-one 02:49:20Z): the two metrics-cell.t.sh rows that red EVERY gate run (e3-hand-edit-during-the-wait, e3-lock-held-at-start-past-the-bound) were the HARNESS, not the product. ROOT CAUSE, reproduced and measured: the file is `#!/bin/sh` = dash on the gate, and dash has NO $RANDOM, so the lane token `$$.$RANDOM$RANDOM` read `<pid>.` for EVERY lane; a detached releaser acts only while its lane token is current, so a late releaser of an EARLIER lane (the hand-edit lane's `sleep 2; echo hand-edit >>node; rm -f lock`) fired during a LATER lane, removed that lane's lock and appended its hand edit to that lane's node. Run under `env -i ... sh` on the loaded box (load 12/4 cores), instrumented: `DIAG lane-token=3310691. rc=3 ran=yes lock-now=GONE hold-alive=yes`, stderr `commit_paths: .../t.md already dirty: refused`, 1 stale hand-edit line in the NEW lane's node. The product code read the lock correctly: START and commit both call verification.suite_lock_holder(root) on the same root; the live holder `sleep 600` was alive throughout (hold-alive=yes) and the LOCK FILE was gone (a stale releaser removed it). Answering every run-1 conjunct by name: lock-held-at-start `rc 3` came from the pre-dirty refusal of the stale hand edit, `the command ran: YES` because the START read saw no lock file (removed), `node dirty 1` the stale line, `ERR line 0` because the ERR was the dirty line, `took 2s` the stale releaser's `sleep 2`; hand-edit `rc 0 / HEAD moved / dirty 0` because the stale releaser had already removed the lock and nothing was waited for. FIX (2 test paths, no product change): the token is a COUNTER (`ln=$((ln+1))`), a new row e3-lane-tokens-are-unique-under-sh pins that no two lanes share one (mutant: `$RANDOM` back -> RED under sh); the wall-time rows lose their load-sensitive upper bounds (`took <= 3 / <= 8 / <= 9` -> `<= 24`, the 25 s harness timeout is the real edge and reads rc 124; the stale-lock row runs with hold_wait_s 40 so a wait on the dead pid could not pass; lower bounds `>= 3`, `>= 2` stay: a wait only lengthens them). 8 consecutive runs under `env -i PATH=$HOME/bin:/usr/local/bin:/usr/bin:/bin HOME=<tmp> GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 sh` on the loaded box: 0 FAIL x8 (before: the two rows red in ~1 run of 2). Rows (a)/(b): wait_lock is already a monotonic deadline (`end = time.monotonic() + hold_wait_s`), the board job never takes the suite lock, and the START read is the same call as the commit's `_held`; no product change was needed.
<!-- THOUGHT:END -->
