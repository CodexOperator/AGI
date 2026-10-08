---
id: experiment:a00-13760331-46977b
mint_id: e321ed0c560646198b8e228063aad568
type: experiment
parents:
  - hypothesis:l4-branches-follow-the-season-grammar
next_edges: []
confidence: 0.9
edited_by: a00-325f2fa0
evidence_runs:
  - experiment:a00-13760331-46977b
loop: hypothesis:l4-branches-follow-the-season-grammar@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 9fae0e618a00294f
season: 2
title: A00 13760331 46977b
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-13760331-46977b

## Experiment

KID C of the L4.312 FIX-ONLY round — my region: two rotate.py functions,
`_fd_rounds` (first-decision) and `_harvest_loop_branches` (harvest-table),
plus their tests. No dispatch.py / cli.py / verification.py / crons.py /
branches.py touched (KID A/B/D own those).

**The defect (measured pre-fix):** a round cut on the NEW grammar
`season2/loops/<slug>-<agent>` (what dispatch.py mints today) was invisible
to both tools. `_fd_rounds` enumerated `git branch --list 'loop/*@s{season}'`
then gated on `branch.startswith("loop/")` — the eager glob only ever matched
the legacy spelling, so a canonical round never reached the manifest join.
`_harvest_loop_branches` ran `for-each-ref refs/heads/loop` and matched a
`^(.*)-(a00-[0-9a-f]{8})@s(\d+)$` regex — again legacy-only. The point saw no
open rounds; harvest-table attributed nothing.

**The fix (implemented):** both functions now enumerate local refs ONCE
(`git for-each-ref --format=%(refname:short) refs/heads`) and classify each
short name in Python through `branches.parse` — the ONE branch-name grammar.
A round is any branch whose kind is loop in EITHER spelling: canonical
`season<n>/loops/<slug>-<agent>` (parse kind == "loop"), or the deprecated
`loop/<slug>-<agent>@s<n>` (parse returns it as an "alias" whose canonical is
the loop), handled by a shared `_branch_loop(short) -> (is_loop, season)`
helper. Every existing discriminator kept:

- `_fd_rounds`: the seat-season filter (canonical season must equal the
  seat's season, read from `branches.parse(...)["season"]`), the
  already-merged-into-the-seat skip, and the manifest-join ownership
  (agent id from the branch must appear in the seat's own iteration
  manifests — NOT weakened to ancestry or a glob).
- `_harvest_loop_branches`: first-branch-per-agent wins; the printed name is
  the EXACT `git` name so the harvest merge line cites a branch that exists.
- `_fd_agent_from_branch` made spelling-agnostic (strip a trailing `@s<N>`,
  take the last path segment, grab the trailing `a00-<hex>`).

Two `@s<N>` glob/regex grammars deleted; none kept.

**Tests (hermetic fixtures, both spellings):**
- first-decision: a repo with BOTH a legacy `loop/x-a00-<id>@s2` and a
  canonical `season2/loops/x-a00-<id>` round → first-decision lists BOTH by
  exact git name, pre-fills the canonical round's kid + verdict; the legacy
  one still works.
- first-decision: a canonical round merged `--no-ff` into the seat branch is
  an ancestor → SKIPPED ("no open rounds for this seat"), same discriminator
  that closes a legacy round.
- harvest-table: a canonical `season2/loops/<slug>-a00-feedbeef` round with a
  seat manifest naming it → harvest-table attributes branch + kid +
  diffstat node path, and the season fallback resolves from the canonical
  loop. (Legacy attribution covered by the existing
  `test_parent_named_round_reports_branch_kids_verdict`.)

## Evidence

Env scrubbed (`env -u TMUX -u TMUX_PANE`) so the project pre-commit guard does
not read this kid's AGI_* env on fixture commits. Full rotate + harvest +
branches suites green:

```
extensions/agi/tests/test_rotate_first_decision.py: 11 passed in 1.54s
extensions/agi/tests/test_harvest_table.py:          11 passed in 4.10s
extensions/agi/tests/test_branches.py:                45 passed in 0.15s
all 18 rotate/harvest/sensei-rotate test files:      502 passed in 114.22s
```

The prior 19 tests in the two touched files all still pass alongside the 3 new
ones (9 fd + 2 new fd, 9 harvest + 1 new harvest).

## Agent Notes
rotate.py _fd_rounds + _harvest_loop_branches now read branch names via branches.parse so canonical season2/loops/<slug>-<agent> rounds (and legacy loop/@sN) are both seen by first-decision and harvest-table; season from branches.parse, exact git name printed, manifest-join and merged-skip preserved. 505 tests (502 rotate/harvest + 45 branches) green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
WHAT THE INSTRUCTION SAID (parent brief L4.312, KID C of 4): "(both functions) see only loop/*@s<N> -- read branch names through branches.parse (kind == loop, either spelling); fixture with a season2/loops/x-y round expects it listed."
WHAT THE MACHINE ACTUALLY DOES, measured by the parent on the kid bytes: `pytest test_rotate_first_decision.py test_harvest_table.py` -> 22 passed; `_fd_rounds` now enumerates `git for-each-ref refs/heads` and classifies each short name through a new `_branch_loop` helper that calls `branches.parse`, keeping the seat-season filter, the already-merged `merge-base --is-ancestor` skip and the manifest-join ownership; `_harvest_loop_branches` does the same enumeration and keys the mapping on `_fd_agent_from_branch`, now spelling-agnostic. The two `@s<N>` glob/regex grammars are gone; the printed name is still the exact git short name.
THE NEAR MISS: adding a second `season<N>/loops/*` glob beside the `loop/*@s<N>` one satisfies "a canonical round is listed" and loses the mechanism -- the canonical season would have to be derived from the glob itself and the ownership join would then key on a name shape instead of the grammar; the third spelling (if the grammar ever grows one) would be invisible again. Classifying through `branches.parse` is the property that makes both tools grammar-following rather than pattern-matching.
DEVIATION: none. `_fd_agent_from_branch` became slightly MORE permissive (it now accepts a branch with no trailing `@s<N>`), which is harmless for the manifest join because an unresolvable id still yields "".
PARENT REVIEW: accepted at proved. The node IS the run and the fixture pins both spellings plus the merged-canonical skip.
<!-- THOUGHT:END -->
