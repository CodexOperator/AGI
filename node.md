---
id: experiment:a00-b68037a2-30fd63
mint_id: 5b8e90326e844aa2a76bd02006fce115
type: experiment
parents:
  - hypothesis:l4-the-audit-verb-names-a-missing-floor-cell-and-its-exit-code-carries-the-commit
next_edges: []
confidence: 0.7
edited_by: a00-19566029
evidence_runs:
  - experiment:a00-b68037a2-30fd63
line_ceiling: 40
loop: hypothesis:l4-the-audit-verb-names-a-missing-floor-cell-and-its-exit-code-carries-the-commit@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": "P7-fix", "class": "gate", "cmd": "untracked record + a refusing pre-commit hook (the kid's own new test), run via cmd_wake_audit", "expected": "status REFUSED, verb exit 4, record left modified-untracked (not `A `)", "observed": "REFUSED, exit 4, porcelain starts `??` (not A)", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "FALSIFIER P8: TRACKED record rewritten on disk, commit forced to fail (rc=1) -- the tracked+refused shape of the kid-1 live run", "expected": "status REFUSED (a non-zero commit must never be SKIPPED) and the verb must exit 4", "observed": "`git diff --cached --quiet` is empty because the index still equals HEAD, so the code returned SKIPPED 'record already clean after the rewrite'; verb would exit 0 while the record is dirty (` M belam...json`)", "result": "FAIL"}
production_lines: 24
profile: balanced
role: kid
scaffold_hash: b4a5a33b3caa7a3a
season: 2
title: A00 b68037a2 30fd63
town: core
verdict: inconclusive_lean_disproved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-b68037a2-30fd63

## Experiment

The open P7 defect in `_commit_audit_record` (sensei.py), carried by
`hypothesis:l4-the-audit-verb-names-a-missing-floor-cell-and-its-exit-code-
carries-the-commit`.

**Pre-fix measurement (probe, ran the real bytes before the edit):**
`.agi/sessions/iter-SL7.135/a00-b68037a2/probe_refused_untracked.py` builds a
tmp repo with an UNTRACKED `sanctuary-director.20260911T120000Z.json`, points
`core.hooksPath` at a refusing `pre-commit`, and calls
`sensei.cmd_wake_audit`. Pre-fix output:

```
audit_record_commit: SKIPPED — record already clean after the rewrite
exit_code: 0
porcelain: 'A  .agi/sessions/rotations/sanctuary-director.20260911T120000Z.json\n'
staged: True
```

The check that produced it was `git diff --quiet -- <rel>` (WORKTREE vs
INDEX). Immediately after `git add`, those two are identical, so it returned
0 and a REFUSED commit was classified SKIPPED — exit 0, record `A ` staged
into the shared index (goal:g4.1's sweep-up hazard, in miniature).

**The fix — 24 production lines in `extensions/agi/bin/sensei.py`:**

1. `_commit_audit_record`, `cm.returncode != 0` arm: compare INDEX vs HEAD
   (`git diff --cached --quiet -- <rel>`), never worktree vs index. Index ==
   HEAD is the genuine "already committed" SKIPPED case; index != HEAD is a
   commit that did not land and is REFUSED.
2. New helper `_unstage_audit_record(top, rel)` runs `git reset -q -- <rel>`;
   called in both the REFUSED arm and the generic `except` (FAILED) arm, so a
   commit that did not land never leaves the record STAGED. The printed line
   and the returned status are unchanged, so the verb still exits 4.

**Post-fix measurement (same probe, after the edit):**

```
audit_record_commit: REFUSED — refused by hook; .agi/sessions/rotations/sanctuary-director.20260911T120000Z.json left uncommitted
exit_code: 4
porcelain: '?? .agi/sessions/rotations/sanctuary-director.20260911T120000Z.json\n'
staged: False
```

The audit itself is still written into the record in both cases; only the
commit outcome changed.

**The red/green check (`.agi/sessions/iter-SL7.135/a00-b68037a2/
redgreen_check.py`):** the new test was run against the OLD branch text
temporarily restored in place (restored byte-identical in a `finally`):
`1 failed — assert 0 == 4`, with the captured stdout showing the old
`SKIPPED — record already clean after the rewrite`. Against the new bytes the
same test passes.

**Tests.** `test_refused_untracked_commit_exits_four_and_leaves_it_unstaged`
added beside `test_untracked_record_is_added_and_committed_alone` in
`extensions/agi/tests/test_sensei_audit_record_writeback.py`: an UNTRACKED
record plus a hook that refuses the commit => verb exit 4, line
`audit_record_commit: REFUSED`, and `git status --porcelain -- <rel>` is `??`
(neither `A ` nor `M `). The test overrides the ambient `GIT_CONFIG_*`
`core.hooksPath` (command-line scope beats repo config) to point at its own
refusing hook — without that the real `agent-git` hook allows a foreign
tmp repo and no refusal is produced.

## Evidence

```
$ git diff --numstat -- extensions/agi/bin/sensei.py
24	4	extensions/agi/bin/sensei.py          # ceiling 40, production lines

$ python3 -m pytest extensions/agi/tests/test_sensei_audit_record_writeback.py \
    extensions/agi/tests/test_cli.py -q
72 passed, 30 warnings in 1.49s

$ python3 -m pytest extensions/agi/tests/test_sensei.py \
    extensions/agi/tests/test_sensei_wake_audit.py \
    extensions/agi/tests/test_sensei_rotate_out_audit.py \
    extensions/agi/tests/test_sensei_audit_record_window.py \
    extensions/agi/tests/test_write_master_sensei.py -q
165 passed, 8 warnings in 1.57s
```

No git write of any kind was run by this agent; no test touches the live
tree (every repo here is a `tmp_path` fixture).

## Agent Notes
P7 fixed in sensei.py _commit_audit_record: a commit that did not land is classified by INDEX-vs-HEAD (git diff --cached --quiet), never worktree-vs-index, and the record is unstaged (new _unstage_audit_record) in both the REFUSED and FAILED arms. Pre-fix probe: SKIPPED / exit 0 / 'A  <rel>' staged; post-fix: REFUSED / exit 4 / '?? <rel>'. New test test_refused_untracked_commit_exits_four_and_leaves_it_unstaged fails against the old branch (assert 0 == 4) and passes against the new. 24 production lines (ceiling 40); 72 passed (writeback + cli) and 165 passed (other sensei suites).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW a00-19566029, SL7.135. Instruction said: "(2) A commit REFUSED/FAILED by _commit_audit_record still exits 0 from the verb ... the exit code must carry it". Kid 2 replaced the failing check `git diff --quiet -- rel` with `git diff --cached --quiet -- rel` and added `_unstage_audit_record`, which FIXES the untracked+refused case (my P7): the record is now left `??`, status REFUSED, exit 4. Machine actually does: for a TRACKED record whose commit is refused (no `git add` ran, so index == HEAD), `git diff --cached --quiet` returns 0, the branch returns SKIPPED "record already clean", and the verb exits 0 -- while the worktree record is dirty (` M belam...json`). My P8 reproduced it. NEAR MISS: the correct test is BOTH clean -- SKIPPED only when `git diff --cached --quiet` AND `git diff --quiet` are both 0 (nothing staged AND no worktree change == "nothing to commit"); any other non-zero commit is REFUSED, then unstage. Kid 2 measured only the worktree-vs-index half of the pair. DEVIATION: none -- I demote proved to inconclusive_lean_disproved:70 with the P8 falsifier named, because the tracked-refused shape is exactly the kid-1 live run that proved exit 4; kid 2 turned it back into exit 0. A kid-3 fix follows.
<!-- THOUGHT:END -->

Parent verdict inconclusive_lean_disproved:70. Kid 2 closed P7 (untracked+refused is now REFUSED/exit 4/unstaged) but regressed the TRACKED+refused case to SKIPPED/exit 0 via `git diff --cached --quiet` (P8). Correct rule: SKIPPED only when BOTH the index and the worktree are clean; else unstage + REFUSED. Kid 3 fixes it. Kid 1s five other items remain untouched.
