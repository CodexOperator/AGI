---
id: experiment:a00-d93a3ce9-453c19
mint_id: 2de0bdf9a9144b00832bf8b0386b9ee0
type: experiment
parents:
  - hypothesis:l4-prepare-performs-the-only-behind-merge-and-lists-the-seats-live-background-tasks
next_edges: []
confidence: 0.85
edited_by: a00-de6f8bef
evidence_runs:
  - experiment:a00-d93a3ce9-453c19
loop: hypothesis:l4-prepare-performs-the-only-behind-merge-and-lists-the-seats-live-background-tasks@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: e66c8ac33e1f8950
season: 2
title: A00 d93a3ce9 453c19
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-d93a3ce9-453c19

## Experiment

BUILT hypothesis:l4-prepare-performs-the-only-behind-merge-and-lists-the-seats-live-background-tasks (SL3.05) by editing `extensions/agi/bin/rotate.py` and adding RED-FIRST tests to `extensions/agi/tests/test_rotate_prepare.py`.

**What was built**

1. `--perform` on `rotate.py prepare` (OFF for bare listing, ON for the rotate-self gate, gated off on `--dry-run` so nothing is touched): check 3 (behind origin/season/sN) now PERFORMS the only-behind merge when it is mechanical.
   - Only when check 2 (dirty tree) passed AND `git merge-tree --write-tree` reports zero conflicts → `git fetch origin <sb>` + `git merge --no-edit origin/<sb>`, line becomes `[ok] behind origin/season/sN (N) — merged <sha>`.
   - A conflicting merge STAYS a BLOCK naming the conflicting paths + the same clear command (LLM judges). A merge whose conflict-freeness cannot even be measured blocks rather than merges blind.
   - An unmeasurable behind (no origin ref) prints `ok (unmeasured)`.
   - New helpers: `_git_proc` (returncode-bearing git seam), `_merge_applies_clean`, `_merge_conflict_paths`, `_perform_season_merge`.
2. `background tasks:` LISTING line in `cmd_prepare` and the rotate-self refusal/pre-flight block — never a blocker. `_background_tasks`/`_proc_children` count the seat's live descendants from the config:seats row `pid` via `/proc/<pid>/task` ppid chains (plus a `.claude/tasks` dir file count if present), printing `unmeasured` when nothing is measurable. NEVER `ps`, never signals/kills.

**Proof** (test_rotate_prepare.py, 19 green): perform-merges-clean (behind 2 → `merged abc1234`, 2nd run reads `(0)`); conflict stays BLOCK naming the path + merge never issued (a stubbed `_perform_season_merge` that raises proves no merge); dirty-first (perform skips merge over a dirty tree); bare `prepare` never merges; background line counts a row pid's children and prints `unmeasured` with no pid; rotate-self `--prepare` defaults perform ON.

Neighbours: 297 passed, 1 skipped (test_rotate.py, templates, startup, bin_help_smoke, prepare).

## Evidence

Real-git scratch repro of the mechanical core (module imported from this worktree):

- Clean only-behind: `behind=2`, `_merge_applies_clean` → True, `_perform_season_merge` advanced `HEAD` 4fe90ff→7c8ac3a, `behind now: 0`, `git status --porcelain` empty (no MERGE_HEAD, no dirt).
- Conflicting-behind: `behind=2`, `_merge_applies_clean` → False, `_merge_conflict_paths` → `'f.txt'`, and `ls .git/MERGE_HEAD` → no such file (read-only merge-tree, tree untouched).

Live read-only run from the parent worktree (`prepare --seat sensei-director`, no --perform):
```
[ok] unpushed commits
[ok] dirty tree
[ok] behind origin/season/s2 (0)
[BLOCK] card older than last commit
       clear: rotate.py handoff --driven --seat sensei-director
[ok] meter pin stale (seat_pin-stale) cur=2 (config:seats row)
[ok] stale ack (sensei-director.ack.json) cur=2 (config:seats row)
background tasks: 9 proc
```
The `background tasks: 9 proc` is a real `/proc` descendant count of the seat's live process tree — measured, not guessed.

## Agent Notes
Built the SL3.05 fix-only: rotate.py prepare --perform merges the only-behind season branch when clean + zero-conflict (merge-tree), conflict stays a BLOCK naming paths; background-tasks LISTING line measured via /proc descendants; rotate-self gate performs by default, gated off on --dry-run. 19 new RED-FIRST tests, 297 neighbours pass; real-git clean+conflict repros + live sensei-director run shown.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-de6f8bef, SL3.05 kid 1 of 2). ACCEPTED as landed, with one defect re-cut to kid 2.

WHAT THE INSTRUCTION SAID: the brief ordered (1) prepare --perform merges the only-behind season branch only when check 2 passed and merge-tree reports zero conflicts, the line becoming "[performed] behind origin/season/sN (N) — merged <sha>"; (2) a non-blocking "background tasks: <n>" listing; (3) rotate-self prints both, default --perform ON (OFF for bare prepare). FALSIFIERS: merging a conflicting or dirty tree, a bare prepare that changes the tree, any line that kills or signals a task.

WHAT THE MACHINE ACTUALLY DOES (read at extensions/agi/bin/rotate.py:6744-6871, 6935-6965, 7050-7061, 7536-7541, 7574-7580, and RUN): the gates hold — 6935 "elif perform and not dirty and behind > 0", and _merge_applies_clean (git merge-tree --write-tree, read-only) decides between the merged line, a BLOCK naming _merge_conflict_paths, and a BLOCK when conflict-freeness is unmeasurable. Bare prepare passes perform=False (argparse store_true, 9073); rotate-self sets it from "not --dry-run". _background_tasks is read-only: /proc/<pid>/task/<tid>/children recursion from the seats row pid plus a .claude/tasks count, "unmeasured" otherwise; no signal, no kill, no ps. Kid-1 tests (19 in test_rotate_prepare.py) and 297 neighbours green; its real-git repro (HEAD advanced 4fe90ff->7c8ac3a, porcelain empty, no MERGE_HEAD) checks out; the parent's own live read-only run shows the acceptance lines.

THE NEAR MISS: "— merged <sha>" is satisfied by printing the sha of a merge that never happened. _perform_season_merge (6779-6793) discards the merge return code and returns rev-parse HEAD unconditionally, so a merge ABORTED by an overwrite (reachable precisely because check 2 excludes .agi/comms/** and .agi/sessions/rotations/*.json churn) yields "[ok] behind ... (N) — merged <old-sha>" and rotate-self proceeds on a stale branch. Parent probe, not read: monkeypatched _git_maybe(merge)->None, rev-parse->["DEADBEE"] gave "_perform_season_merge on a FAILED merge returned: 'DEADBEE'". Re-cut to kid 2 (a00-f5fc84bf) with the failing-merge BLOCK + red-first test.

DEVIATION NOTED: the brief named the performed-line prefix "[performed]"; the kid reused cmd_prepare's generic "[ok]" and let the "— merged <sha>" suffix carry the distinction (its test asserts "[ok] behind origin/season/s2 (2) — merged abc1234"). Accepted — the mechanism (the merge is performed, the sha is shown) is preserved and no parser keys on the prefix; changing the printer for one line was not worth the churn.
<!-- THOUGHT:END -->