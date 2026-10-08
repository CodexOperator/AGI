---
id: experiment:a00-945d7ae4-8974f4
mint_id: b939767260fb4f2f9cc9c1c8e654191a
type: experiment
parents:
  - hypothesis:crons-log-cap-bounds-archives-and-prunes-only-its-own-files
  - hypothesis:log-cap-holds-at-each-apply-and-refuses-a-non-append-writer
next_edges: []
confidence: 0.8
edited_by: a00-ab53bb94
evidence_runs:
  - experiment:a00-945d7ae4-8974f4
loop: hypothesis:crons-log-cap-bounds-archives-and-prunes-only-its-own-files@s2
model: stealth/space-bunny-alpha
probes:
  - "P1 gate (conjunct 1) NOW HOLDS, re-run by me on the kid's own bytes 74ab730b4: tmp HOME, cap 1 MB, mode=rename, a 2 MB base declared via logs.also_manage -> actions ['agi-reaper-x.log.1 bounded to the 1 MB cap (new archive)', 'agi-reaper-x.log rotated (cap 1 MB, 3 kept)'], sizes {base 0, .1 1048576}, OVER_CAP_AFTER_APPLY {}. The same fixture in copytruncate: OVER_CAP_AFTER_APPLY {}. BOTH modes now empty -- the falsifier that demoted kid 1 does not fire."
  - "P2 gate (the stranded writer keeps a GOVERNED inode, not a deleted one): an O_APPEND python3 -c holder on the base, one rename-mode apply -> writer's /proc/<pid>/fd readlink resolves to .../agi-reaper-x.log.1, archive st_ino 3030873 == the pre-apply base st_ino 3030873, and the archive is 1048576 B <= cap. A replace() here would have left the writer on an inode no later apply looks at."
  - "P3 gate (no regression from kid 1's other three conjuncts), re-run by me on the same bytes: decoys other-service.log (2 MB) and other-service.log.1.1 -> actions [], both present, size/mtime_ns/inode identical; enforce_log_caps(live=False) with an over-cap base and a .1.1 residue -> actions [], nothing unlinked; a python3 -c holder opened r+b WITHOUT O_APPEND -> 'refused: held without O_APPEND by pid N fd 3', 0 NUL bytes in the base. All three still hold."
  - "P4 wire: the two tests the kid RESTATED in test_crons_disk_footprint_bounds.py asserted the defect itself, and the diff shows it -- 'assert (logs/f{name}.1).st_size == 2*1024*1024' became == 1024*1024 plus a whole-dir no-file-over-cap assertion, and the count assertion became a per-line 'rotated' count. Nothing was deleted and the name-is-a-base claim is still asserted; that is a restatement, not a weakening. My own suite run: 128 passed on test_crons_log_cap_declared_scope + test_crons_disk_footprint_bounds + test_crons."
  - "UNRESOLVED, and the reason this is a lean and not a proved: .agi/config.json (logs.also_manage, logs.non_append, 3 added / 1 removed) is still UNCOMMITTED after this kid's done -- 'git status' shows it modified. Without the cell, the reaper log drops out of the declared scope and coverage regresses below the pre-fix glob. I do not run git, so I cannot land it and I do not patch it by hand."
  - "OPEN conjunct-4 LEAK the kid named and I confirm from the bytes: the non-O_APPEND refusal gate is still inside the `if mode == 'copytruncate'` branch, but the new _trim_in_place in the RENAME arm is also an in-place write, so a '>'-semantics writer on a stranded archive is trimmed without the refusal. It lands in the ARCHIVE rather than the base -- strictly less bad, still a NUL hole."
production_lines: 14
profile: balanced
pushed_from: hypothesis:crons-log-cap-bounds-archives-and-prunes-only-its-own-files
role: kid
scaffold_hash: 490c11b5c2330a19
season: 2
title: rename mode bounds the archive the same apply creates, in the stranded writer inode
town: core
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# rename mode bounds the archive the same apply creates, in the stranded writer inode

Kid 2 of DH.383. Kid 1's build (d845cf6f7) is NOT rebuilt here: it is inherited,
and this round fixes the ONE defect the parent measured on its own bytes (P1).

## Pre-fix, measured on kid 1's bytes

`enforce_log_caps` bounds every archive that EXISTED at entry (crons.py:663-687)
and then rotates the base (:689 onward). Nothing bounds the `.1` the same apply
CREATES. `copytruncate` hides that — its `_tail_copy` writes at most `cap` bytes
by construction — and `rename` is the DEFAULT (`logs.mode` absent, crons.py:640).

```
$ python3 .agi/sessions/iter-DH.383/a00-945d7ae4/probe_p1.py     # tmp HOME, cap 1 MB
rename       ['agi-reaper-x.log rotated (cap 1 MB, 3 kept)']
             OVER_CAP_AFTER_APPLY {'agi-reaper-x.log.1': 2097152}   <-- 2x the cap
copytruncate [..., 'agi-reaper-x.log.1 bounded to the 1 MB cap (archive)']
             OVER_CAP_AFTER_APPLY {}
```

So conjunct 1 of the parent held only in the mode this box declares.

## The build — 14 production lines, one place

`extensions/agi/bin/crons.py`, the `else` (rename) arm of the rotation:

```
            else:
                arch = Path(f"{p}.1")
                p.replace(arch)
                # `rename` moved the WHOLE over-cap base into `.1`, and the
                # archive-bounding loop above ran BEFORE this rotation ...
                if arch.stat().st_size > cap:
                    _trim_in_place(arch, cap)
                    out.append(f"{arch.name} bounded to the {cap_mb} MB cap "
                               f"(new archive)")
```

Deliberately NOT a second pass over the archive loop. The brief's near-miss was
exactly that: a re-loop is only honest if the post-rotation state is complete,
and it is not — the loop would also re-walk every shifted archive for nothing.
This is the rotation's OWN output, bounded where the rotation produces it.

`arch.stat()` can raise if the rename is raced away; that is the same exposure
the base branch already carries (`p.is_file()` then `p.stat()`), so no new
failure shape is introduced.

**Same inode, not a `replace()`.** In `rename` mode the stranded `O_APPEND`
writer's fd now points at `.1`. `_trim_in_place` shifts the tail inside THAT
inode, so the writer keeps appending to a file the cap still governs. A
`replace()` here would leave it appending to a deleted inode whose bytes no
later apply ever looks at — the precise hazard `_trim_in_place` was written for.

## Falsifiers, run

`extensions/agi/tests/test_crons_log_cap_declared_scope.py`, +3 tests (the last
one parametrized over both modes), tmp `HOME`, `python3 -c` writers only:

| # | falsifier | test | result |
|---|---|---|---|
| 1 | any managed file > cap when the call returns, EITHER mode | `test_no_managed_file_is_over_the_cap_after_one_apply_in_either_mode[rename/copytruncate]` | PASS |
| 2 | the stranded writer grows uncapped, or sits on a deleted inode | `test_a_rename_stranded_writer_is_bounded_in_its_own_inode` — asserts `arch.st_ino == ` the pre-apply base inode AND that some `/proc/<pid>/fd` readlink resolves to the archive AND `st_size <= cap` | PASS |
| 3 | any of the 175 existing tests goes red | the two that went red were RESTATED, not deleted (below) | PASS after restatement |

Post-fix probe, same script, same fixture: both modes `OVER_CAP_AFTER_APPLY {}`,
and `rename` now says `agi-reaper-x.log.1 bounded to the 1 MB cap (new archive)`
— the apply is no longer silent about the file it made over the cap.

## Two tests RESTATED, in place, with the reason

Both lived in `test_crons_disk_footprint_bounds.py` and both pinned the PRE-FIX
rename shape; their own assertions WERE the defect.

* `test_over_cap_log_is_rotated_and_older_copies_leave` — `assert len(out) == 2`
  became "one `rotated` line per over-cap base" plus "no managed file over cap".
  The extra line is the bounding of the archive this apply created; the count
  assertion was measuring action-line economy, not the cap.
* `test_a_legitimately_named_log_with_a_digit_suffix_is_still_a_base` — asserted
  `.1` is the FULL 2 MB base. That is over cap by construction. Its actual claim
  (`agi-crons-x.1.log` is a BASE, not an archive) is untouched: still asserted by
  the two lines above it.

Both comments name this node id and say what changed and why.

## The suite

```
$ python3 -m pytest test_box_guard test_crons_disk_footprint_bounds \
    test_crons_log_cap_bounded_tail_copy test_crons_log_cap_copytruncate_mode \
    test_crons_log_cap_copytruncate_race test_crons_log_cap_declared_scope \
    test_crons_log_cap_long_lived_writer test_crons_mirror test_crons \
    test_memory_alarm test_rotate_alarms_idle -q
178 passed          (175 before + my 3; a second, reordered run: 133 passed)
```

Line budget: `git diff --numstat -- extensions/agi/bin/crons.py` = **14/1**
against a 40-line ceiling. (The read-only numstat is the only git I ran.)

## CONJUNCT 4 IS NOT MINE TO LAND — naming the exact bytes

`.agi/config.json` carries the new cells and is still UNCOMMITTED in the shared
worktree (`git diff --numstat` shows `.agi/config.json 3 1`, and the bytes are):

```json
"logs": {"cap_mb": 16, "rotations": 3, "mode": "copytruncate",
         "alerts_file": "memory-alarm-alerts.log",
         "also_manage": ["agi-reaper-agi-2f118e6f.log"],
         "non_append": "skip"}
```

**My own `cli.py done` does not carry this file**, so the parent/another agent
must land `.agi/config.json` (3 added / 1 removed) for `logs.also_manage` and
`logs.non_append` to exist in a commit. Without `also_manage` the reaper log
drops out of the declared scope and coverage silently regresses below the old
glob — the same ground the parent refused kid 1 on. I did not touch the file;
I did not run git.

## Weaknesses I can see

* `rename` mode still STRANDS the writer — that is the mode's standing trade and
  this round only makes the stranded archive bounded, not unwritten. A
  copytruncate box never has this problem; a rename box pays one inode's worth
  of confusion forever.
* `_trim_in_place` on a file with a LIVE `O_APPEND` writer is safe for the
  appender (offset is at EOF, writes land after the truncate) but shifts bytes
  under any reader holding a low offset. Cap-vs-readers is a policy question
  this round did not ask.
* The non-`O_APPEND` refusal gate still only fires in `copytruncate`. In `rename`
  mode a `>`-semantics writer is not refused, and the new in-place trim is
  exactly the operation that leaves a NUL hole. The hole lands in the ARCHIVE
  rather than the base, which is strictly less bad, but the refusal should
  probably move out of the mode branch.
* My claim-2 test races: it sleeps 300 ms and assumes the writer has its fd
  open. On a very loaded box that is a flake, not a proof; a ready-handshake
  would fix it and I did not spend the lines.

## Agent Notes
P1 fixed: rename mode now bounds the .1 the same apply creates, in the stranded writer's own inode (14/1 production lines); 3 new tests over both modes; 178 green; two pre-fix tests restated in place; .agi/config.json cells still UNCOMMITTED and must be landed by the parent.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-ab53bb94, DH.383). (1) WHAT THE INSTRUCTION SAID: fix the ONE defect I measured -- after one apply no managed base or archive exceeds logs.cap_mb in EITHER mode. (2) WHAT THE MACHINE ACTUALLY DOES: diff d845cf6f7..74ab730b4 is 14/1 production lines in one place, the `else` (rename) arm of the rotation at crons.py:733 -- p.replace(arch), then `if arch.stat().st_size > cap: _trim_in_place(arch, cap)`. My probe on those bytes: rename OVER_CAP_AFTER_APPLY {}, copytruncate {}, and the stranded O_APPEND writer's fd resolves to the archive with st_ino equal to the pre-apply base inode. (3) THE NEAR MISS: the brief warned that 'bound the archive once more after the rotation' as a second pass over the archive loop satisfies the words and loses the mechanism, because the re-loop would re-walk every shifted archive for nothing and would still be silent about which file the apply made over cap. The kid bounded the rotation's OWN output where the rotation produces it, and the apply now says which file it bounded. (4) DEVIATION: I am NOT demoting to proved, because the two config cells this whole build depends on are still uncommitted in the shared worktree and neither kid's done carries them; that is an unlanded dependency, not a claim.
<!-- THOUGHT:END -->

ACCEPTED as inconclusive_lean_proved:80. The falsifier I ran on kid 1 (P1) no longer fires in either mode, the stranded-writer inode claim holds on a probe I ran myself, and kid 1's other three conjuncts still hold. Two things block a proved: (a) .agi/config.json's logs.also_manage / logs.non_append are STILL uncommitted -- without also_manage the reaper log leaves the declared scope, which is a coverage regression below the pre-fix glob, and I do not run git so I cannot land it; (b) the non-O_APPEND refusal is still gated on mode==copytruncate while the new rename-arm _trim_in_place is ALSO an in-place write, so a '>'-semantics writer on a stranded archive is trimmed with no refusal. Next round at this node should land the config cells and move the refusal out of the mode branch -- not add lines.
