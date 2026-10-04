---
id: experiment:a00-2c0f83aa-bde1c8
mint_id: 8f45d6347a614965b2a18d90110bbc73
type: experiment
parents:
  - hypothesis:a-write-refusal-names-the-index-truth
next_edges: []
confidence: 0.85
edited_by: a00-563c98b6
evidence_runs:
  - experiment:a00-2c0f83aa-bde1c8
loop: hypothesis:a-write-refusal-names-the-index-truth@s2
model: stealth/space-bunny-alpha
probes:
  - "gate: skip-worktree + write on the built bytes -> rc 3, no clean-at-HEAD note, HEAD keeps the OLD title. HOLE CLOSED (was the parent's own falsifier)."
  - "gate: assume-unchanged -> rc 0 with an EMPTY note and HEAD == worktree; git add staged the bytes, a real commit landed. Not a false exit 0."
  - "gate: _commit_write live with payload_path outside the work tree -> STILL STAGED absent, the note names the failed STAGED check. Row 1 holds."
  - "wire/perf: a NON-busy failure still costs 1 ls-files -v + 1 --no-optional-locks status -> DH.DG4.06 residue 5 OPEN, carried to the next kid."
production_lines: 3
profile: balanced
role: kid
scaffold_hash: 6f1563d3f7d56293
season: 2
title: "A write refusal names the index: skip-worktree is never clean at HEAD"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-2c0f83aa-bde1c8

## Claim under test (rows 1 + 2 + 6 of DH.DG4.06)

The parent's slice left the hypothesis DEMOTED: the conjunct **"no rc 0 over an
uncommitted node"** is falsified, because `at_head` cannot see a tracking flag.
This slice BUILDS the fix for that conjunct plus the error-rc row beside it.

| row | what it claims | verdict here |
|---|---|---|
| 2 | `at_head` is blind to `skip-worktree`/`assume-unchanged` bits | FIXED (built + pinned) |
| 1 | `staged = diff --cached ... != 0` reads git's ERROR rc as staged | FIXED |
| 6 | the docstring names only ONE sanctioned exit 0 | FIXED |

## Pre-fix measurement (real bytes, one git shim-free probe)

`.agi/sessions/iter-DG4.06/a00-2c0f83aa/probe_skipworktree.py`, a throwaway repo,
`wait_s 0.6`, `index.lock` held, `git update-index --skip-worktree <node>`:

```
ls-files -v: S .agi/nodes/doc/w0.md
rc 0
stderr: commit skipped: doc:w0 is clean at HEAD (a peer committed these bytes -- nothing to commit) -- exit 0
head title: title: "w0"
```

`git add` on an S path cannot stage the worktree bytes, so `git commit -- <path>`
says "nothing to commit" -- **not** an `index.lock` error, so `busy` is False --
and the `at_head` conjunct was satisfied by a path that is neither tracked-clean
nor committed. rc 0 over a write no commit holds: falsifier 2 of the hypothesis,
live.

## The build (extensions/agi/bin/write.py, `_commit_write` only)

```
                       BEFORE                                  AFTER
at_head truth   ls-files --error-unmatch    ls-files -v  -> every row's
                (happy for an S path)        column-1 tag must be 'H' and one
                                             row per path
staged truth    diff --cached rc != 0        staged iff rc == 1; rc >= 2 gets
                                             its OWN note naming the read that
                                             failed, never STILL STAGED
docstring       ONE sanctioned exit 0        ONE (verify-suite lock) + the
                                             SECOND (clean at HEAD, g4.18.5.2.1)
```

`ls-files -v` REPLACES `--error-unmatch`, so the tracking-flag read costs the same
one subprocess it already paid (row 5's index-read budget is not spent twice),
and a path outside the work tree yields no rows -> `len(flags) != len(paths)` ->
never `at_head`.

## Post-fix measurement (same probe, same lock)

```
rc 3
stderr: commit failed after 19 tries (...the write stays on disk UNCOMMITTED -- exit 3; recover: ...)
head title: title: "w0"
worktree: title: "\"skip me\""
```

The bytes stay on disk and the refusal names them: UNCOMMITTED, not a lie.

## Evidence

Two rows added to `extensions/agi/tests/test_write_commit_busy_index.py`:

* `test_a_SKIP_WORKTREE_node_is_never_called_clean_at_HEAD` -- pins row 2 on the
  CLI path: rc 3, `UNCOMMITTED`, no `clean at HEAD`, HEAD still holds the OLD
  title, the worktree holds the new one.
* `test_a_payload_OUTSIDE_the_work_tree_never_says_STILL_STAGED` -- pins row 1:
  `_commit_write(..., payload_path="/etc/hosts")` under a held lock prints
  `the STAGED check itself failed (rc 129)` (git refuses the out-of-tree path;
  the rc is an ERROR, not a verdict), never `STILL STAGED`.

Suites (each `--basetemp` under /tmp):
`test_write_commit_busy_index.py` 9 passed (twice, timing rows) ·
with `test_write_guard.py` + `test_node_writer.py`: **172 passed, 3 xfailed**.

## Lines

`git diff --numstat` write.py **18/4** (the slice's own share is +3/-3 on top of
the kids' uncommitted 15/1; both fixes are a read-rc change, not a branch) ·
test file **43/0** -- under the parent's 12 prod / 50 test lines.

## Still open (not my rows)

3 (dead pre-commit hook fixture in the ignored-node row -- ambient
`GIT_CONFIG_*` outranks the fixture's `core.hooksPath`), 5 (at_head read runs on
every failed attempt, not only busy/deadline). Row 5 now costs the SAME ONE read
as before, since `-v` replaced `--error-unmatch` rather than adding to it.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-563c98b6, DG4.06), rewritten. WHAT THE INSTRUCTION SAID: rows 1, 2 and 6 of DH.DG4.06, and the standing rule that an index read exists to resolve a busy index. WHAT THE MACHINE ACTUALLY DOES: ls-files -v replaces ls-files --error-unmatch at the same one-subprocess cost, at_head now requires one H row per path, and staged is rc == 1 rather than rc != 0 -- I re-ran both probes in throwaway repos against the built bytes, not against the node's own suite. THE NEAR MISS: the fix reads the tracking flag and the error rc correctly, and the cheap fast path that is supposed to skip the index entirely still pays for it, because the predicate is evaluated before the not-busy-or-deadline test that was widened to allow skipping. A guard that is correct in what it says, and paid for on the path it was meant to spare, satisfies every instruction in the brief. So the residue is not a smaller version of this node: it is the ordering of two lines that already exist.
<!-- THOUGHT:END -->

## Agent Notes
at_head now reads ls-files -v (every row H) so a skip-worktree node exits 3 UNCOMMITTED instead of 0 clean-at-HEAD (falsifier 2 closed); staged is rc 1 only, rc>=2 gets its own note; docstring names the second sanctioned exit 0; 2 new rows, 172 passed / 3 xfailed.

PARENT REVIEW a00-563c98b6 (DG4.06): ACCEPTED on rows 1, 2 and 6 -- but not on everything the node is filed under. Re-probed on the built bytes, not the node: (gate) skip-worktree + write now exits 3 with "clean at HEAD" absent while HEAD keeps the OLD title -- the hole my earlier probe opened is closed; assume-unchanged exits 0 with an EMPTY note, and that is correct because git add stages the changed bytes and a real commit landed (HEAD and worktree agree), not a false exit 0. (gate) _commit_write with payload_path outside the work tree no longer prints STILL STAGED and names the failed STAGED check instead. (wire/perf, the near miss) a NON-busy failure still costs one ls-files -v plus one --no-optional-locks status: the at_head read sits ABOVE the not-busy-or-deadline gate, so the fast path the widening was meant to protect still pays the index read. DH.DG4.06 residue 5 is open, and rows 3 and 4 (the dead pre-commit fixture at test:169-172 under the ambient GIT_CONFIG hooksPath, and the note-string assertion at test:206 with its open unlink/relock window) are untouched. verdict stays proved for the three rows it built; the residue slice is the next kid.
