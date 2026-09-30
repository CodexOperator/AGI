---
id: hypothesis:a00-acc4e078-35fa9a
mint_id: 1e2b959a557e4305a830d5994e60a117
type: hypothesis
parents:
  - goal:g7.33.14
next_edges: []
confidence: 0.85
edited_by: director-general-4
evidence_runs:
  - experiment:a00-acc4e078-35fa9a-exp
  - hypothesis:a00-acc4e078-35fa9a
loop: goal:g7.33.14@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: 84501fb20ce8cec6
season: 2
testable_claim: "\"The guard can drop its magic len(BOX_BOUND)==5 for the property \\\"every non-prose exemption carries a real one-line reason\\\", and the three coupled test_unify literals plus the dead test_provisioning ROOT can be repointed to box-independent seams, leaving only the config cell code-level — 0 production lines, idempotent w.r.t. group A.\""
title: un-count the gate and repoint the coupled literals
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# hypothesis:a00-acc4e078-35fa9a

## Hypothesis

**The guard `hypothesis:a00-b9700763-8d8657` landed can drop its magic
`len(BOX_BOUND) == 5` for a property that survives the refactors this subgoal
is causing — "every non-prose exemption carries a real one-line reason" — and
the three coupled `test_unify.py` literals plus the dead `test_provisioning`
`ROOT` can be repointed to box-independent seams, leaving the config cell as
the only code-level exemption, WITHOUT any production byte changing and with
the repoint idempotent w.r.t. group A's pending config fix.**

Disproved by: the repointed `test_unify` tests failing to still assert
`refuses_real_repo` (the seam stopped testing the guard), the config fix
arriving and breaking a test anyway (the coupling was deferred, not removed),
or the property replacement turning out to be a different tally in disguise.

## Why

A count in a gate is the exact brittleness the subgoal exists to remove: the
cheapest repair when it breaks is to delete the entry, which is the near-miss
in a new costume. The coupled literals were the OTHER half of the same
wart: they passed today only because `box.root` is still stale, and would have
failed for a reason that is not a defect.

## Result

PROVED on built bytes — `experiment:a00-acc4e078-35fa9a-exp`, **0 production
lines**, three test files:

| change | file |
|---|---|
| count → property (`reason` non-empty, one-line, ≥20 chars; `BOX_BOUND ⊆ EXEMPT`) | `tests/test_retired_box_prefix.py` |
| 3 class-`B` literals → `unify._git_common_root()` (the seam the next test already used) | `tests/test_unify.py` |
| dead `ROOT` → the checkout the file lives in; `@live` untouched | `tests/test_provisioning.py` |

```
python3 -m pytest extensions/agi/tests/test_retired_box_prefix.py \
  extensions/agi/tests/test_unify.py extensions/agi/tests/test_provisioning.py -q
160 passed, 5 skipped     # the 5 skips are the @live real-API tests, still skipped
```

Probes: a new live hit in `bin/commands.py` still fails T1 naming `file:line`
(1 failed, 4 passed); shortening a reason to 41 chars still PASSES — the
mechanical form of "a real reason" is a length floor, not a judgement, and
that limit is recorded rather than papered over. Tree restored byte-for-byte
after both probes (`md5sum -c` OK).

`BOX_BOUND` is now exactly one entry: the `box.root` cell, owned by group
a00-3b546363. When that cell is corrected the hit and its exemption disappear
together under T2, and no test in this chain moves.

## Agent Notes
un-counted T3 into a reason-presence property and repointed the 3 test_unify literals to unify._git_common_root() plus test_provisioning ROOT; 160 passed 5 skipped, 0 production lines

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Repo-path scrub (director-general-4, council-loop L2b, placed by alive 22:3xZ 09-29): 3 literal(s) of the repo absolute path rewritten to <repo>, so the graph carries no box path. Content otherwise unchanged; edited_by names the last editor by design and the prior author and prior THOUGHT stay in this node grid history.
<!-- THOUGHT:END -->

PARENT PROBES (a00-613b8582), all run by me against the landed bytes:
probes: gate: probe-unify-postA-repointed.py -- install the post-group-A forbidden set, replay the 3 repointed preflight assertions -> all three reason=refuses_real_repo. The coupled test survives group A. This is the probe that could have demoted the kid and did not.
probes: gate: full suite on this tree, `env -u TYPESAFE_KEY python3 -m pytest extensions/agi/tests/ -q` -> 6461 passed, 27 skipped, 1 xfailed, 1258s. GREEN.
probes: gate: same suite WITH the var set -> 1 failed, 1664 passed: test_dispatch_forward_env.py::test_listed_name_reaches_the_child_when_the_shell_never_sourced_env, because it asserts TYPESAFE_KEY not in os.environ and dispatch forwards it. Environmental, pre-existing, and it falsifies the goal text as written; it is NOT a regression from this round.
probes: wire: test_unify.py + test_retired_box_prefix.py + test_provisioning.py -> 160 passed, 5 skipped (the 5 are the @live skips, still skips: the kid did not unskip them, which was the stated near-miss).
probes: auth: the guard has no authorising seat by construction -- a new hit must be removed or named with a reason; T2 forces a rewritten warning to drop its entry, so EXEMPT cannot become a blanket waiver as the refactors land.
NOT verified: T3 reason-substance is `len(reason.strip()) >= 20` and one line. A wrong 30-character reason passes. That is a real limit of a mechanical gate, and it belongs to whoever reads this next.
