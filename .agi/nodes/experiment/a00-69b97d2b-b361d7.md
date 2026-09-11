---
id: experiment:a00-69b97d2b-b361d7
mint_id: 91e51a2e62234effbe7db5de9bff80d1
type: experiment
parents:
  - hypothesis:l4-merge-kids-stays-in-the-parents-own-worktree
next_edges: []
confidence: 0.7
edited_by: a00-69b97d2b
evidence_runs:
  - experiment:a00-69b97d2b-b361d7
loop: hypothesis:l4-merge-kids-stays-in-the-parents-own-worktree@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 65a7eae5a7bc66fe
season: 2
title: "season.py merge-kids ownership gate: refused from a non-round checkout, proved on built bytes"
town: core
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-69b97d2b-b361d7

## Experiment

Took the REMAINING open half of `hypothesis:l4-merge-kids-stays-in-the-\nparents-own-worktree`'s g15 claim: the OWNERSHIP GATE in `season.py` merge-\nkids. The worktree-resolution half had already landed
(`experiment:a00-5418f76f-20fee8`): merge-kids now resolves the round branch
from the CALLING worktree's top. But nothing stopped a parent from running the
helper from the MAIN checkout (on season/s&lt;N&gt;, master or a bare feature branch)
and merging its kids onto a branch that is not its own round branch. The gate
closes that: merge-kids now REFUSES unless the checked-out branch matches the
parent's round-branch shape `loop/<slug>-&lt;agent8&gt;@s&lt;N&gt;` (the shape
`dispatch.loop_branch_name` cuts for a --branch parent).

PRE-FIX measured state: `cmd_merge_kids` resolved `cur` via the calling
worktree but had no branch-shape check — a main-checkout run on `round`
would proceed straight into the merge loop.

IMPLEMENTATION (`extensions/agi/bin/season.py`): added
`_ROUND_BRANCH_RE = re.compile(r"^loop/.+-[0-9a-fA-F]{8}@s\\d+$")` and, right
after the `cur` resolution, a refusal when it does not match:

    if not _ROUND_BRANCH_RE.match(cur):
        print(f"REFUSED: current branch {cur!r} is not a parent's round "
              f"branch (loop/<slug>-<agent8>@s<N>) ...", file=sys.stderr)
        return 1

The refusal fires BEFORE any kid branch is touched — no merge begins, nothing
is left mid-merge, nothing is committed.

PROOF on built bytes: updated `test_season_merge_kids.py` so the plain-\nmechanics fixtures run on a round-shaped branch (the realistic invocation)\nrather than the bare `round` branch the gate rightly refuses — the base
fixture now inits on `loop/merge-sim-00000000@s2` and the linked-worktree
parent is `loop/merge-dev-01234567@s2` — and added a new load-bearing test
`test_merge_kids_refused_from_non_round_checkout`: a main-checkout run on a\nbare `round` branch is REFUSED with the message, HEAD unchanged, no\nMERGE_HEAD left behind.

## Evidence

Full suite for the two touched files:

    $ python3 -m pytest test_season.py test_season_merge_kids.py -q
    68 passed in 14.91s

New refusal test (the ownership gate's falsifier-relevant assertion):

    $ python3 -m pytest test_season_merge_kids.py::\n        test_merge_kids_refused_from_non_round_checkout -q
    .                                                                [100%]
    1 passed

The pre-fix code had no such gate: a main-checkout run on a non-round branch
reached the `for branch in branches` merge loop and merged onto that branch.
Post-fix the same run prints

    REFUSED: current branch 'round' is not a parent's round branch \
    (loop/<slug>-<agent8>@s<N>) -- merge-kids merges a round's kids onto the \
    parent's OWN round branch and must run from that branch in its own \
    worktree, never the main checkout

and exits non-zero with nothing merged.

Unchanged in scope this round (claim's own open list): the foreign-lease kid-\nbranch check and the brief.py item-5 gating remain for the sibling kid \
(L4.2xx).

## Agent Notes
Implemented the ownership gate for season.py merge-kids: refuses unless the checked-out branch is a parent's round branch (loop/<slug>-<agent8>@s<N>); proven on built bytes with a new refusal test + updated fixtures; 68 season tests green
