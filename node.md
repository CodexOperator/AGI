---
id: hypothesis:l4b23-promptfile-drop
mint_id: 056d533703ad4d498b97d342cfa18398
type: hypothesis
parents:
  - idea:l4b23-promptfile-drop
next_edges: []
confidence: 0.6
edited_by: sanctuary-helper
scaffold_hash: 469139a629db3a9e
season: 2
tags:
  - hypothesis
testable_claim: dispatch.py's --prompt-file reaches the parent brief when --tier parent is used, or is refused loudly -- never silently dropped as it is today (owner-reported defect, l4-plan A:40; trap 0am).
thought_session: sanctuary-helper-05
title: dispatch.py --prompt-file must reach the parent brief or refuse loudly
---
<!-- BODY:BEGIN -->
# hypothesis:l4b23-promptfile-drop

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
## L4.11 brief -- dispatch.py's --prompt-file is swallowed by brief.py for --tier parent

ROOT CAUSE, confirmed by reading the code (not guessed): `dispatch.py`
reads `--prompt-file` via `_read_prompt_file(args.prompt_file)` and passes
it as `addendum=` into every `adapter.build_command(...)` /
`_brief.assemble(...)` call site (dispatch.py:698, :736, :1376) --
tier-blind, so the addendum genuinely reaches `brief.assemble()` for a
`--tier parent` dispatch too. The drop happens ONE LEVEL DEEPER, inside
`assemble()` itself: `extensions/agi/bin/brief.py`, function `assemble()`
(defined ~line 1428). Its `tier == "parent"` branch (lines 1529-1548) calls
`_parent(agent_id=..., iter_n=..., cli_py=..., dispatch_py=..., target=...,
parallel=..., max_live=..., kid_ceiling=..., branch_name=..., branch_
worktree=..., branch_base=..., source_root=...)` -- **`addendum` is never
passed**, even though `assemble()` received it as a parameter. Compare the
fallback branch at the bottom of the same function (~line 1550), which
DOES pass `addendum=addendum` into `_kid(...)`. And `_parent()`'s own
signature (brief.py, search `^def _parent`) has no `addendum` parameter at
all -- unlike `_kid()` (lines 1053-1055), which declares
`addendum: str | None = None` and, when set, inserts a labelled
"WHAT THE LAST KID PRODUCED" segment (lines 1091-1100). So a `--tier
parent --prompt-file X` dispatch reads X's bytes, hands them to
`assemble()`, and `assemble()` discards them on the floor before `_parent`
ever sees them -- silent, no error, no line in the resulting brief.

FILE: extensions/agi/bin/brief.py (assemble()'s `tier == "parent"` branch
and `_parent()`'s signature/body).

CHANGE -- pick the one that is actually right, do not assume it's (a):
(a) give `_parent()` an `addendum: str | None = None` parameter mirroring
    `_kid()`'s pattern (a labelled segment, e.g. "FROM THE LAST ROUND" or
    similar parent-appropriate framing -- `_kid()`'s "WHAT THE LAST KID
    PRODUCED" wording is written for a kid reading its OWN parent's
    carry-forward; a parent reading a carry-forward from a PRIOR PARENT
    dispatch needs its own label, not a copy-paste), then thread
    `addendum=addendum` into the `_parent(...)` call in `assemble()`, or
(b) if `--prompt-file` was never meant to apply to `--tier parent` at all
    (a parent's brief is built fresh from its target node every time, not
    threaded from a prior parent's output the way a kid's is), then
    `dispatch.py` should REFUSE `--tier parent` combined with
    `--prompt-file` loudly at argument-parsing time instead of silently
    accepting and discarding it.
The plan's own hypothesis (this node's testable_claim) allows either
resolution: "reaches the parent brief... or is refused loudly -- never
silently dropped as it is today." Decide which is correct by reading
`_parent`'s existing docstring/purpose and `dispatch.py`'s own comments at
the three call sites (they explain what addendum is FOR); do not guess.

VERIFY: `python3 extensions/agi/bin/dispatch.py . <a test iter> --target
<any valid node> --tier parent --harness pi --dry-run --prompt-file
<a scratch file with distinctive text>` -- before your fix, confirm the
distinctive text is ABSENT from the dry-run's printed brief (first 20
lines + line count). After your fix: if you took (a), confirm the
distinctive text IS present in the printed brief; if you took (b), confirm
the same command now exits non-zero with a clear refusal message instead
of silently succeeding. Run ONLY the tests in whichever test file already
covers `brief.py`'s `assemble()` (grep for `def test_.*parent` in
extensions/agi/tests/test_brief.py if it exists) plus your new test --
never the full suite.

KID CEILING: 2. One file, one clear defect, one decision to make and
justify; a second kid is for review only if needed.

DO NOT: touch dispatch.py's argument parsing unless you chose option (b)
above, in which case that IS the file to touch instead of/in addition to
brief.py -- say which you edited and why. Do not add a build node. Do not
`git add -A`. Do not run `grid.py commit --all` on this seat branch --
end at `git commit` + `git push` on your own branch/worktree.

REPORT: write one `experiment` node whose `parents` is this hypothesis,
with a verdict on the testable claim (`proved` only if your before/after
verify above actually ran and holds). `evidence_runs` must be a list of
node ids that resolve in the corpus; your own experiment node counts once
it exists. List every verify command and its actual output in the body.
Say plainly which of (a)/(b) you took and why, quoting the docstring/
comment evidence that decided it.
