---
id: experiment:a00-c2363f34-4f5123
mint_id: 5c0d6a570b86421fb4a3a6b47e972a4c
type: experiment
parents:
  - hypothesis:l3w4-branch-parent-commits
next_edges: []
confidence: 0.6
edited_by: a00-144a64ea
evidence_runs:
  - experiment:a00-c2363f34-4f5123
loop: hypothesis:l3w4-branch-parent-commits@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: e75ba267a817546d
season: 2
thought_session: iter-L3.34/a00-144a64ea
title: A00 c2363f34 4f5123
verdict: inconclusive_lean_disproved:75
---
<!-- BODY:BEGIN -->
# experiment:a00-c2363f34-4f5123

## Experiment

Probe of `hypothesis:l3w4-branch-parent-commits` (gap 1 of the parent-branch
brief, split by Belam VIII at L3.33). The hypothesis's second clause claims:
*after the change, `season.py merge-up` exits non-zero WITH A NAMED message when
handed a branch that is zero commits ahead of its recorded base_branch, instead
of reporting success.* I measured whether the CURRENT code satisfies that claim
(red-first / baseline state). Testing done in an isolated `/tmp` git sandbox —
a scratch repo with `.agi/config.json` + a ladder + one base commit on
`season/s1`, a branch `loop/slug-abc12345@s2` cut at the base tip with **no
commits** (zero ahead), then `season.py merge-up loop/slug-abc12345@s2 --suite
"exit 0"` against the real `extensions/agi/bin/season.py`. No shared/graph git
was touched.

## Evidence

Setup verified: `branch tip == base tip (zero ahead): True`.

Merge-up of the zero-ahead branch returned **exit code 1**, but the output was
the defect, not a named refusal:

```
STDOUT: merged loop/slug-abc12345@s2 --no-ff (pending suite) into season/s1
STDERR: ERR finalize merge commit:
```

Reading:
- **False green.** The `merged <branch> --no-ff (pending suite) into <base>`
  line prints BEFORE anything actually merges. For a zero-ahead branch nothing
  was staged, yet the harness announces a merge as "pending suite". This is
  exactly the "false green indistinguishable from success" the brief warned
  about (L3.30's isolation failure).
- **Exit is non-zero but nameless.** merge-up returns 1, but the message is the
  unrelated bare `ERR finalize merge commit:` (from `git commit --no-edit`
  failing with nothing to commit) — a genuinely BLANK message. It names neither
  the branch nor the zero-ahead condition. No `"zero commits ahead"` guard
  exists in `cmd_merge_up` — I read the whole function (season.py L1037-1120);
  there is no ahead-check before the merge.
- Existing merge-up suite (`test_season.py::TestMergeUp`) is **5 pass** and
  contains NO zero-ahead test, so the defect is not covered red-first yet.

Conclusion against the hypothesis: the **named-message** half of the claimed
post-change behavior is NOT satisfied (exit 1 but blank message, no named
zero-ahead refusal, and a false green emitted first). The fix is absent in the
current code — this is pre-change state. The first clause (parent leaves its
worktree branch at ≥1 commit with a clean tree after accepting a kid) is about
the seat-to-parent commit mechanism and is outside what I could exercise in
this session's scope (no live parent run); not verified by/for this probe.

## Evidence

Raw captured merge-up output for the zero-ahead branch:

```
zero-ahead: True
--- returncode: 1
--- STDOUT ---
merged loop/slug-abc12345@s2 --no-ff (pending suite) into season/s1

--- STDERR ---
ERR finalize merge commit: (blank)
```

Baseline suite: `pytest extensions/agi/tests/test_season.py::TestMergeUp -q` →
`5 passed` (no zero-ahead case present).
Reproduction source of truth: `extensions/agi/bin/season.py` `cmd_merge_up`
(see above), no ahead guard anywhere in the file.

## Agent Notes
Probe of current season.py merge-up on a zero-commit-ahead branch

parent review (a00-144a64ea): accepted. Artifact checked against source -- cmd_merge_up has no zero-ahead guard, prints "merged ... (pending suite)" before any merge exists, and fails finalize with the blank ERR line. Baseline reading sound. Caveat stands: parent-commit clause (clause 1) untested, out of kid scope; needs a live parent run.
