---
id: hypothesis:g73314-the-box-audit-scans-the-files-that-move-between-boxes-and-box-root-names-this-box
mint_id: f7fe58789d704c0e9f0306e42de0304a
type: hypothesis
parents:
  - goal:g7.33.14
next_edges: []
confidence: 0.6
edited_by: director-general-1
season: 2
testable_claim: "With box.root set to the real root (/data/work/agi) and the audit scanning only the files that move between boxes (a `box.scan` cell of path prefixes: extensions/, skills/, src/, .claude/, .agi/context/, .agi/nodes/.geometry/), `python3 extensions/agi/bin/paths.py audit | grep -c ': box:'` lists only real portable box literals (9 on trunk 8083ec340, in 9 files), each either derived from box.repo or a placeholder, or named in box.allow; the config-cell exemption of test_retired_box_prefix.py retires and goal:g7.33.14 clause 1 becomes satisfiable. Without the scan scope the same root flags 1,829 hits in 294 files, 94 percent of them generated records."
title: "The box audit scans the files that move between boxes, and box.root names THIS box: the stale cell is not the problem, the scan scope is"
town: core
---
# hypothesis:g73314-the-box-audit-scans-the-files-that-move-between-boxes-and-box-root-names-this-box

## Measured
- Finding (belam 21:2xZ via SM 21:2xZ): config.json box.root = <home>/work/agi is stale for this box (the live repo is /data/work/agi; belam added box.repo = /data/work/agi, 12e8065cc, for the AA1.M install and left box.root alone: pointing it at the live repo flags 290 tracked files, 67 today, and reddens the paths check). The question handed to DG1: what should the leak scanner look for on THIS box?
- paths.py audit lists box literals of four cells (root, logs_dir, tmux_session, user) plus HOME_RE over `git ls-files`; it exits 1 on ANY finding and is already red today: 8,668 findings in 1,273 files with the stale cells (box 380, home 4,584, user 2,203, tmux 1,499, logs 2). It is a lister, not a gate; the one gate on this prefix is test_retired_box_prefix.py (class-based: T1-T5), which carries ONE config-cell exemption for exactly this cell ("two owners ... the goal's clause must gain a config-cell exemption or clause 1 stays unsatisfiable").
- Nothing renders from the stale cell: crons.py `_substitute` resolves {root} from the renderer's own computed values and says so ("never boxes.box_cells(root), whose live cells belong to a foreign box"). So the stale root costs no wrong path today; it costs a goal clause and a misleading cell.
- goal:g7.33.14's own end-state says config.json's `root` (and logs_dir) MUST match the box. So the cell should be corrected; belam's objection is the audit's reach, not the value.
- Measured on trunk 8083ec340 (in-process, boxes.box_cells patched to root=/data/work/agi, the audit's own findings(); box class only): 1,829 hits in 294 files: .agi/sessions 1,176 hits / 190 files (rotation records 1,164) · datasets 553 / 49 · node prose 91 / 46 · portable code and pieces 9 hits / 9 files: engine-root.md:56 `WorkingDirectory=/data/work/agi`, guard.md:112, extensions/agi/guard/guard-init.sh:175, skills/agi-corrective/SKILL.md:30, 3 files under extensions/, 2 other. The 1,449 hits the correction adds over the stale value are 94 percent generated records that are never copied to another box.
- logs_dir (<home>/logs) and user (the origin box account) are stale the same way (user flags 2,203 hits); they are the same question, not measured separately here.

## CLAIM
With box.root set to the real root (/data/work/agi) and the audit scanning only the files that move between boxes (a `box.scan` cell of path prefixes: extensions/, skills/, src/, .claude/, .agi/context/, .agi/nodes/.geometry/), `python3 extensions/agi/bin/paths.py audit | grep -c ': box:'` lists only real portable box literals (9 on trunk 8083ec340, in 9 files), each either derived from box.repo or a placeholder, or named in box.allow; the config-cell exemption of test_retired_box_prefix.py retires and goal:g7.33.14 clause 1 becomes satisfiable. Without the scan scope the same root flags 1,829 hits in 294 files, 94 percent of them generated records.

## Dispatch line
config-max: YES, two cells, the Prime's: box.root = /data/work/agi and a new `box.scan` prefix list (box.repo/alias/hub are not [box].md fields, so a new cell is unscanned too; if `scan` is added to [box].md it is a schema edit) / template-max: none / code: paths.py `files()` honours box.scan, a test in test_paths_audit.py; the 9 portable hits fixed by the build that owns each (engine-root.md:56 and the install derive from box.repo: DG3's A-acts). NOT dispatched: needs belam's GO on the two cells (a Prime decision, banked to SM with this recommendation).

## FALSIFIERS
1. After the cells and the build: `python3 extensions/agi/bin/paths.py audit | grep -c ': box:'` equals the count of named box.allow entries plus 0 (every portable hit fixed or allowed by name); `.agi/config.json` `box.root` = /data/work/agi.
2. `env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_paths_audit.py extensions/agi/tests/test_retired_box_prefix.py -q` passes with the config-cell exemption deleted (T2 says every EXEMPT entry must still be live, so deleting the cell value from the stale one retires the entry by construction).
3. Negative: no record under .agi/sessions or datasets/ is read by the audit when box.scan is set; `paths.py audit | grep -c '^.*\.agi/sessions'` prints 0.

## TESTS
test_paths_audit.py gains one case: a scratch repo with a box literal in a scanned file and in an unscanned record: only the scanned one is listed. The retired-prefix test drops its config-cell exemption.

## FILE SCOPE
extensions/agi/bin/paths.py · extensions/agi/tests/test_paths_audit.py · extensions/agi/tests/test_retired_box_prefix.py (the exemption) · .agi/config.json (belam's cells). Never the live trunk ref.

## CEILING
1 parent · kids <= 1 · +12 production lines · +25 test lines · 0 USD · regular review.

## OUTCOME (DG1, 10-02 23:5xZ; belam [decision] 23:2xZ + 23:3xZ, landed bae704905 by SM)
- LANDED as ONE update: code 2507bad35 (boxes.scan_prefixes, paths.files honours box.scan, test_box_scan +27 test lines against a +25 ceiling, the retired-prefix config-cell exemption deleted) + belam/box-scan 3a6a7cbaf (box.root = the live repo, box.scan = the six prefixes). SM's gate on the landed tree: paths.py audit 1,152 findings (box 6, logs 2) against 8,708 on the tree before; engine suite 7,912 passed, 0 failed; the planted-path case is test_box_scan.
- NOT DONE, decided: logs_dir stays at the origin-box value. belam could not write the real path (the privacy guard refuses a literal logs path: ~/logs is a symlink into a registered home root) and offered a `{home}` expansion in paths.py instead (his [decision] 23:3xZ left the call to DG1). DG1 leaves it: the only thing a corrected logs_dir would change is the `logs` class, which reads 2 hits today, so the expansion would add engine code to move 2 lines of a lister that is not a gate; the cell stays a foreign-box literal the scanner still catches. Reopen only if the `logs` class grows.
- user stays the origin-box account on purpose (measured: user = belam adds 1,114 false hits, belam being also a post name).
- LEFT TO THE OWNING BUILDS, not this hypothesis: the 6 portable box hits (engine-root.md:56 WorkingDirectory derives from box.repo in belam's install; guard.md:112, guard-init.sh:175, skills/agi-corrective SKILL.md:30, one test, skills/agi-master-gate SKILL.md:91): each is fixed by the build that owns it or named in box.allow.

