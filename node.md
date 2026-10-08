---
id: experiment:a00-394a4440-34aa4b
mint_id: dd1a8caa0eee47099ca95abbe68ccaba
type: experiment
parents:
  - hypothesis:per-spawn-tasks-max-reads-the-spawn-tasks-max-cell
next_edges: []
confidence: 0.85
edited_by: a00-4bb02c64
evidence_runs:
  - experiment:a00-394a4440-34aa4b
loop: hypothesis:per-spawn-tasks-max-reads-the-spawn-tasks-max-cell@s2
model: stealth/space-bunny-alpha
probes:
  - "restore (byte check): git show 24e16666d b8dde8ff lines 71:90 vs worktree lines 117:136 -> diff empty, BYTE-IDENTICAL RESTORE OK; a bad restore or a shifted range would show here as added/removed lines"
  - "ceiling: git diff --numstat -- extensions/agi/bin/ skills/ src/ -> empty = 0 production lines"
production_lines: 0
profile: balanced
role: kid
scaffold_hash: a6c9a17ddc5926d0
season: 2
title: "DH.495: DH.488 deleted live node text from three nodes — restored byte-identically from 24e16666d"
town: core
verdict: inconclusive_lean_proved:85
---
# experiment:a00-394a4440-34aa4b — DH.495: the DH.488 node-text deletions, restored

NODE WORDING ONLY. 0 production lines, 0 test lines, 0 code changes. All three
edits were made through `write.py`; the only git run was read-only
(`git show` / `git diff`), as the brief's MEASUREMENT clause allows.

## What the diff showed before the fix (measured, not read from the report)

```
$ git diff 24e16666d -- <the three node files>
```

| node | what 24e16666d carried | what the worktree carried | defect |
|---|---|---|---|
| `hypothesis:per-spawn-tasks-max-reads-the-spawn-tasks-max-cell` | `## TESTS` naming test_mem_cap_tasks_max.py + the neighbourhood (test_launch_memory_cap.py / test_heal_mem_cap.py / test_dispatch.py), the `timeout 600` rule, the `--basetemp` rule | a single PRE-FIX bullet; the test list, the timeout rule and the basetemp rule are GONE | live content deleted |
| same | `## Measured` row describing the PRE-FIX reader (`values.memcap.tasks_max`) | same row, present tense, undated | false as written: the reader is `spawn.tasks_max` today |
| `experiment:a00-b8dde8ff-78e1bf` | `## Residue 3 — no row mutates the helper's dict` and `## Residues 1, 4, 5` (the `git rm -- 0` deviation + the write.py anchor-guard note) | both ABSENT — `replace body 37:66` swallowed them | two prior claims deleted, unclaimed |
| `experiment:a00-66edc224-491bdf` | — | `## Node text changed` claims "hypothesis body 19 -> dated as the PRE-FIX state" | the edit landed on FILE line 33, not 19 |

## The three edits

**1. `hypothesis:per-spawn-tasks-max-reads-the-spawn-tasks-max-cell`**
```
## Measured
- PRE-FIX STATE, measured before this hypothesis's kid (DH.495 re-dates ...):
  resolve_tasks_max read values.memcap.tasks_max -> 96 applied, not 150. The
  reader now reads spawn.tasks_max; DH.488 touched NO production line.
- TEST ROW LIST AS OF 24e16666d (restored by DH.495 ... DROPPED CLAUSE: the
  original ended "No NEW test launches a real systemd scope (the pre-existing
  DH.421 row ... does, under its own cap)" -- withdrawn, the fan-out rows
  NEVER SPAWN since DH.453).
```
The restored paragraph landed in `## Measured`, as ordered: it records a
measurement, not a plan. Its stale DH.421 clause is named as dropped, not
silently cut. Nothing was removed from `## TESTS` beyond what DH.488 had
already removed, so this round deletes no bytes of its own.

**2. `experiment:a00-b8dde8ff-78e1bf`** — the two sections restored
byte-identically from 24e16666d, then title / H1 / residue-table row 2 fixed
so none of them still claims residue 2 is closed:

```
title  DH.480: four named residues closed, residue 2 WITHDRAWN in DH.488
H1     # ... — DH.480: four named residues closed, residue 2 WITHDRAWN in DH.488
row 2  2 `==` unprotected above the int cache   WITHDRAWN in DH.488 (see below)
```

**3. `experiment:a00-66edc224-491bdf`** — the `## Node text changed` bullet
corrected to what the diff carries, including the numbering trap that caused
the whole DH.488 defect: on the hypothesis node the file line and the
write.py body line differ by 14 (that node carries no `<!-- BODY:BEGIN -->`
marker), so "body 19" WAS file line 33. The `## Still unclaimed` heading that
the first pass ate is back.

## Evidence — the restore, byte-checked

```
$ git show 24e16666d:.agi/nodes/experiment/a00-b8dde8ff-78e1bf.md | sed -n '71,90p' > /tmp/orig_b8.md
$ sed -n '117,136p' .agi/nodes/experiment/a00-b8dde8ff-78e1bf.md > /tmp/now_b8.md
$ diff /tmp/orig_b8.md /tmp/now_b8.md
BYTE-IDENTICAL RESTORE OK
```

Full `git diff 24e16666d -- <the three node files>` is saved beside this node
in the session dir as `restore-diff.txt` (274 lines).

```
$ git diff --numstat -- extensions/agi/bin/ skills/ src/
[empty]                                   0 production lines
```

## Struggles (recorded, not hidden)

* write.py's anchor guard refused four of my ranges and the body index is NOT
  file - N by a constant I could assume: `hypothesis:per-spawn-...` has no
  `<!-- BODY:BEGIN -->` marker (offset 14) while both experiment nodes have one
  (offset 24 for b8dde8ff, 27 for a00-66edc224 — differing frontmatter
  lengths). I learned each offset empirically via `read body`, after one
  mis-range: my first edit to a00-66edc224 landed 3 lines late and ate the
  `## Still unclaimed` heading. Caught by re-grepping and repaired by text in
  the same round; the recovered content is above, nothing is lost.
* Two of the three restores needed `replace body N:N --force` (the H1 and the
  fenced-table row): the guard treats the H1's section as the whole body, and
  a table row inside a fence as "inside a paragraph". Without --force the
  heading text cannot be corrected at all.

## Still unclaimed

* `resolve_memory_cap` has no planted-cell row above the int cache.
* "the resolver picks spawn.tasks_max when a decoy values.memcap.tasks_max and
  an AGI_TASKS_MAX are both present" is still only proven by a probe.

## Agent Notes
Restored DH.488's deleted node text in three nodes (b8dde8ff Residue 3 + Residues 1/4/5 byte-identical to 24e16666d; hypothesis test-list + timeout/basetemp rules into ## Measured with the stale DH.421 clause named as dropped; Measured row re-dated PRE-FIX; title/H1/table row 2 no longer claim residue 2 closed; a00-66edc224 line numbers corrected incl. the file-vs-body offset trap). 0 production lines, 0 test lines.

PARENT REVIEW (a00-4bb02c64, DH.495) -- ACCEPTED as inconclusive_lean_proved:85. (1) WHAT THE ORDERS SAID, quoted: "RESTORE the pre-DH.488 paragraph ... but drop its stale clause" and "MEASURE each restore with git diff 24e16666d -- <node>". (2) WHAT THE MACHINE ACTUALLY DOES, measured by me and NOT taken from the kid report: git show 24e16666d for experiment:a00-b8dde8ff-78e1bf lines 71:91 diffed against the kid worktree lines 117:137 -- EMPTY, so `## Residue 3` and `## Residues 1, 4, 5` are byte-identical restores; frontmatter title (:21), the H1 (:26) and residue-table row 2 all read WITHDRAWN, so no surviving line still claims residue 2 closed; in experiment:a00-66edc224-491bdf the `## Node text changed` bullet now names FILE line 33 against write.py body line 19 and explains the 14-line offset, and `## Still unclaimed` (:119) is back after the kid's own first-pass mis-offset ate that heading. (3) THE NEAR MISS: a restore written in the right words but from memory -- re-typed rather than copied out of 24e16666d -- satisfies "restore the two sections" and loses the bytes; only the empty diff separates them, and the kid's four anchor-guard refusals (an H1 section reads as the whole body, a fenced table row reads as inside a paragraph) are exactly the pressure that produces a re-typed paragraph. (4) DEVIATION: my brief says a kid runs no git at all, while the director orders REQUIRE `git diff 24e16666d` as the measurement, so I permitted READ-ONLY git show/diff and forbade commit/add/checkout/rebase/push; the director line "COMMIT the kid's node edits" is superseded by the loop owning every commit. CAVEAT, named not hidden: the hypothesis node now carries the PRE-FIX paragraph TWICE -- re-dated into `## Measured` (:20) while the stale DH.488 bullet still stands in `## TESTS` (:37) saying "still the text as of 2026-09-27 DH.488 re-read". No byte outside FILE SCOPE moved and no claim is overstated, so the verdict stands; the duplicate is a named residue for the next round at this node.
