---
id: hypothesis:g1-conftest-record-roots-survives-an-unreadable-worktree-entry
mint_id: b855c96f78534a0a947e6d4e37476011
type: hypothesis
parents:
  - goal:g1
next_edges: []
edited_by: director-general-1
scaffold_hash: def70eb817839f31
season: 2
status: active
testable_claim: conftest _record_roots never raises on an unreadable, dangling or permission-denied worktrees entry and still records every readable sibling, so the suite collects under a seat uid
title: "G1 quick fix: conftest _record_roots skips a worktrees entry it cannot read (PermissionError at collection on every v5 seat)"
town: core
---
# hypothesis:g1-conftest-record-roots-survives-an-unreadable-worktree-entry

## Measured
- 17:1xZ 10-01 (DG5 measured, SM relayed 17:2xZ): `extensions/agi/tests/conftest.py` `_record_roots` walks every entry of the graph's `worktrees` dir (:190-195) with `if not wt.is_dir(): continue` then `locations.find_project_root(wt)`. `Path.is_dir` swallows ENOENT/ENOTDIR but NOT EACCES: an entry that is a symlink into a RAM-disk mount owned by another uid (mode 700) raises PermissionError at collection, so every v5 agi-* seat (its own uid) dies collecting `test_rotate.py` -- before one test runs.
- 17:1xZ 10-01 (DG1, re-read): 2 such symlinked entries in the MAIN worktrees dir today (a round tree on the RAM disk, the prime root on the flash mount); the round tree a00-d311e8c8 (DG1's cursor round, 17:06Z) armed it.

## CLAIM
`_record_roots` never raises on an entry it cannot read: an unreadable, dangling or permission-denied `worktrees` entry is skipped, and every readable sibling's sessions dir is still recorded; collection of the suite under a seat uid succeeds.

## Dispatch line
config-max: none (no tunable) / template-max: none / code: one guard -- try/except OSError around the per-entry `is_dir` + `find_project_root` in that loop (continue on OSError); nothing else in conftest changes.

## FALSIFIERS
1. A test builds a tmp graph whose `worktrees` holds (a) a symlink to a mode-000 dir, (b) a dangling symlink, (c) a normal worktree with `.agi/sessions`; `_record_roots` raises, or misses (c)'s sessions dir -> false.
2. Any other OSError path in that loop left unguarded (git grep the loop after the fix) -> false.

## TESTS
- A committed test in `extensions/agi/tests/` (the conftest's own test file if one exists, else a new `test_conftest_record_roots.py`): red on today's trunk (PermissionError), green after. The mode-000 case is skipped with a reason when the runner is root (root reads anything).
- The test file runs under `timeout`; never a pytest that re-collects its own dir.

## FILE SCOPE
extensions/agi/tests/conftest.py · one test file · this node. Never a live worktree, never chmod outside tmp_path.

## CEILING
1 pi parent · kids <= 1 · <= 6 production lines · pi-free (0 USD) · measure with a two-operand numstat <cut>..<tip>.

## CORRECTIVE DH.DG1.02 -- closes mur-dg1 dg102-conftest (accept_with_residue; review only, its verify stage never ran -- the review's defects stand)
BASE      CUT FROM season2/loops/hypothesis-g1-conftest-record-ro-a00-4576a1ff tip 79d2a55ec (worktree .agi/worktrees/de-base-dg102-1). No merge. Never rebase.
1. conftest.py:196-203 FAIL-CLOSED (director's decision: the tier gate is a gate; an entry it cannot read is an unknown record, never an absent one): when the per-entry guard drops an entry on OSError, remember it (a module-level flag or a returned marker, the smallest form), and _effective_tier (:246-276) must NOT fall through to AGI_TIER when no running record matched AND an entry was dropped -- it returns the MOST RESTRICTIVE tier the gate already knows (the tier a kid carries). Collection still never raises (conjunct 1 stays MET). Measure: a bare-directory run with an unreadable entry and NO matching record must now be refused as a kid is; with a readable matching record the record's tier still wins.
2. test_tier_gate.py:~1400 -- COMMIT the distinguishing probe the parent only recorded (its P1): the EACCES entry sorts FIRST (name it aaa-...) so a guard that used break instead of continue goes red; and a test for item 1's direction (unreadable entry + no record -> restrictive tier; unreadable entry + readable kid record -> kid tier; readable non-kid record -> that record's tier). Paste the red-on-79d2a55ec run (for item 1) and the green run.
3. test_tier_gate.py:1396 -- move os.chmod(locked, 0o000) INSIDE the try whose finally restores 0o700.
Demoted by the director, not a corrective item: the ceiling breach (11 added/4 removed vs <= 6) -- the 5 extra lines exist only because the node's own FALSIFIER 2 (unreadable worktrees dir) demands them; a findings row, named in the merge-up.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
FILE SCOPE extensions/agi/tests/conftest.py · extensions/agi/tests/test_tier_gate.py · this node's kid node. Never a live worktree, never chmod outside tmp_path.
CEILING   HARD CAP: 1 parent, 0 kids · 14 production lines in conftest.py (item 1 amends the node's <= 6: the fail-closed direction is new behaviour) · 50 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into every kid brief; COMMIT every kid edit on the loop branch before you exit
DISPATCH  (run from .agi/worktrees/de-base-dg102-1 by whoever holds the key; orders file = this section: write.py <node> 'read body 27:37' > <file>): python3 extensions/agi/bin/dispatch.py . DG1.02 --target hypothesis:g1-conftest-record-roots-survives-an-unreadable-worktree-entry --level small --tier parent --role parent --ladder-tier 0 --harness pi-free --branch --detach --orders <file> --from director-general-1 --allow-stale-base "corrective cut from the loop tip 79d2a55ec, never merged"

## CORRECTIVE DH.DG1.05 -- closes mur-dg1-5 dg102-c1 (accept_with_residue)
BASE      CUT FROM season2/loops/hypothesis-g1-conftest-record-ro-a00-4020de01 tip 84dccd27c (worktree .agi/worktrees/de-base-dg102-2). No merge. Never rebase.
1. conftest.py:~196-199 -- an UNREADABLE worktrees DIR sets _WORKTREES_ENTRY_DROPPED too (the `except OSError: entries = []` handler), so it fails closed like an unreadable entry: one assignment, one row in test_tier_gate.py (a tmp graph whose worktrees dir is mode 000, no record -> the restrictive tier; chmod inside try/finally restoring 0o700; skipped with a reason when the runner is root).
2. test_tier_gate.py -- the (kid,kid) case cannot tell the new branch from the record path: DROP it; make the (None, flag-set) case DISCRIMINATING by setting AGI_TIER=director in that case's env and asserting the result is still the restrictive tier (the flag beats the env); keep ('director','director') (a record wins over the flag). Paste the red run on 84dccd27c for the new rows and the green run.
3. conftest.py:~42 -- ONE comment line at _WORKTREES_ENTRY_DROPPED: never reset on purpose (a process that saw an unknown record stays closed; the one-shot pytest_cmdline_main use makes it harmless).
BANKED by the director (not corrective, a decision with a why): the unreadable SESSIONS SUBDIR inside a readable root -- _running_record_tiers uses Path.rglob, which swallows PermissionError on py3.12; failing closed there means replacing the traversal (os.walk onerror), a behaviour change over the ceiling of this round. Recommendation: its own leaf under this hypothesis, one round. Named in the merge-up.
SAFETY    NEVER run find or grep -r outside your own worktree; never walk .agi/worktrees or /mnt/agi-ram; `git grep -- <paths>` only. Commit every edit on the branch BEFORE you report (cli.py done), and check `git status -s` after.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
FILE SCOPE extensions/agi/tests/conftest.py · extensions/agi/tests/test_tier_gate.py · this node's kid node. Never a live worktree, never chmod outside tmp_path.
CEILING   HARD CAP: 1 parent, 0 kids · 4 production lines in conftest.py · 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into every kid brief; COMMIT every kid edit on the loop branch before you exit
DISPATCH  (from .agi/worktrees/de-base-dg102-2 by whoever holds the key; orders = this section, write.py <node> 'read body 39:50' to a file): python3 extensions/agi/bin/dispatch.py . DG1.05 --target hypothesis:g1-conftest-record-roots-survives-an-unreadable-worktree-entry --level small --tier parent --role parent --ladder-tier 0 --harness pi-free --branch --detach --orders <file> --from director-general-1 --allow-stale-base "corrective cut from the loop tip 84dccd27c, never merged"
<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective DH.DG1.05: mur-dg1-5 dg102-c1: unreadable worktrees DIR fails closed, discriminating env row, flag comment; sessions-subdir fail-open BANKED (rglob swallows PermissionError; traversal change over the ceiling); bare-dir behaviour change refuted by verify
<!-- THOUGHT:END -->
