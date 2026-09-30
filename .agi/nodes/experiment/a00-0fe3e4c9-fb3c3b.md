---
id: experiment:a00-0fe3e4c9-fb3c3b
mint_id: a405b01ea88445788cadfd26d33fb6db
type: experiment
parents:
  - hypothesis:pb3-agent-git-hook-fails-closed-on-a-failed-diff
next_edges: []
confidence: 0.9
edited_by: a00-bc0bb923
evidence_runs:
  - experiment:a00-0fe3e4c9-fb3c3b
loop: hypothesis:pb3-agent-git-hook-fails-closed-on-a-failed-diff@s2
model: stealth/space-bunny-alpha
probes:
  - "gate: corrupt index, AGI_TIER=kid in its own worktree -> rc=1, stderr holds EXACTLY ONE named line 'agi: kid commit refused -- git diff --cached failed (rc 128) (goal:g1.31.5.1.1)'. The claim's core; the old bytes measured rc=0 fail-OPEN."
  - "gate: healthy index, NOTHING staged -> rc=0, stderr empty. An empty-but-successful diff is still allowed (claim 3)."
  - "gate: staged .agi/config.json on a healthy index -> rc=1 with the ORIGINAL generic line and 0 hits of the named text. rc 1 stays a scope refusal; no double line (claim 2)."
  - "wire: the kid commit's PARENT hook bytes (a653d0cead^), mounted at a ../../bin-resolvable path, same corrupt-index fixture -> rc=0 FAIL-OPEN; a653d0cead's own bytes -> rc=1. The new bytes are the causal difference, not the fixture."
  - "auth: a kid in a different worktree of the SAME project -> rc=1 by the same-git-common-dir guard, unchanged."
  - "auth: parent tier on a non-loop branch -> rc=1, generic line, 0 named hits. set -o pipefail did not leak out of the kid block."
  - "crash: scope-check dying rc=1 (python SyntaxError, the shape of an uncaught traceback) -> the hook still REFUSES rc=1 via the generic line, 0 named hits. This REFUTES the hypothesis sub-clause 'a cli.py crash is rc>=2' (a python crash is rc 1, never >=2): the SAFETY claim holds, the named line does not fire. Disclosed by the kid in its own push_further."
production_lines: 14
profile: balanced
role: kid
scaffold_hash: a6e9740febd4753c
season: 2
title: The kid-scope pre-commit pipe runs under pipefail and refuses a failed git diff with one named line
town: core
verdict: proved
---
# experiment:a00-0fe3e4c9-fb3c3b

## What I did
Built the claim in `hypothesis:pb3-agent-git-hook-fails-closed-on-a-failed-diff`
(measured pre-state, then implemented, then proved on the built bytes), file
scope exactly as the hypothesis ordered.

| step | what | where |
|---|---|---|
| 1 | pre-fix probe on a byte-identical copy of the hook with the new lines removed | scratch `pre-commit-prefix` |
| 2 | `set -o pipefail` + an `rc` case inside the KID block only | `extensions/agi/hooks/agent-git/pre-commit` |
| 3 | 2 rows reusing `branch_kid` / `branch_kid_env` | `extensions/agi/tests/test_git_commit_guard.py` |

The kid block now reads (pipefail, then the pipeline, then the case):

```
set -o pipefail
git diff --cached --name-only -z --no-renames \
  | python3 "$HOOK_BIN/cli.py" scope-check --agent-id "$AGI_AGENT_ID"
SCOPE_RC=$?
if   [ "$SCOPE_RC" -ge 2 ]; then <one named line on stderr>; exit 1
elif [ "$SCOPE_RC" -eq 0 ]; then exit 0
fi
```

ONE rule kept: the predicate is still `cli.py scope-check` → `cli._round_scope_ok`.
The shell adds no path predicate of its own; `cli.py` is untouched.

## Falsifiers, measured

| # | falsifier | result |
|---|---|---|
| F1 | corrupt index, hook run DIRECTLY (a linked worktree's index is not `.git/index`; `git commit` reads the index itself and never reaches the hook) | pre-fix `rc 0` (fail-OPEN) → post-fix `rc 1` — **red before, green after** |
| F2 | stderr of that probe | exactly ONE line `agi: kid commit refused -- git diff --cached failed (rc 128) (goal:g1.31.5.1.1)` — **green** |
| F3 | controls unchanged | `test_branch_kid_commits_in_scope_bytes` (rc 0) and `test_branch_kid_refuses_staged_config_json` (rc 1, `kid may not commit`, no `git diff --cached failed`) — **green** |
| F4 | healthy index, nothing staged, same direct run | `rc 0` (`all([])`), no named line — **green** (`test_branch_kid_empty_staged_set_still_allowed`) |
| F5 | no new shell path predicate; `cli.py` untouched | `git diff --numstat` names only `pre-commit` + the test file — **green** |
| F6 | `pipefail` present | `grep -c pipefail …/pre-commit` → 2 (code + its comment) — **green** |

## Evidence

```
# F1/F2, by hand, tmp repo, corrupt index, direct hook run
prefix (pre-fix copy):  fatal: .git/index: index file smaller than expected
                        -> rc 0                         # FAIL-OPEN
built hook:             fatal: .git/index: index file smaller than expected
                        agi: kid commit refused -- git diff --cached failed (rc 128) (goal:g1.31.5.1.1)
                        -> rc 1                         # one named line, refused

# suite
python3 -m pytest extensions/agi/tests/test_git_commit_guard.py -q -k 'failing_diff or empty_staged or branch_kid'
  14 passed, 28 deselected
python3 -m pytest extensions/agi/tests/test_git_commit_guard.py -q
  42 passed
bash -n extensions/agi/hooks/agent-git/pre-commit   # clean

# size
git diff --numstat -- extensions/agi/hooks/agent-git/pre-commit extensions/agi/tests/test_git_commit_guard.py
  14  2  extensions/agi/hooks/agent-git/pre-commit
  39  0  extensions/agi/tests/test_git_commit_guard.py
```

## Production lines
14 production lines in the hook (5 of them comment), 39 test lines.
The hypothesis' clause said `pre-commit <= 8`; the built minimum that keeps
F2's named line is 14, so this round ran ~1.75x its own sub-clause and
well under the round ceiling of 40. Recorded rather than hidden.

## Push further
`SCOPE_RC >= 2` treats a `cli.py scope-check` CRASH as a scope refusal only if
python exits 1 (uncaught traceback), which is indistinguishable from a real
refusal — a crash still fails CLOSED, so the safety claim holds, but the named
line is skipped. A next run could make `scope-check` exit 2 on its own crash
so the message is always attributable.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEW (parent a00-bc0bb923, DG4.03). (1) WHAT THE BRIEF SAID: "run one negative probe per claim conjunct yourself; a kid that passes its own suite but fails your probe is lean_disproved, with the probe NAMED". (2) WHAT THE MACHINE ACTUALLY DOES: I read the BYTES of a653d0cead, not the report. The diff carries exactly the two named files and no third: 14 lines in pre-commit (set -o pipefail; the pipeline; SCOPE_RC=$?; a >=2 arm printing one named line and exit 1; a 0 arm printing nothing and exit 0) and 39 test lines, both claimed deliverables present in the diff, cli.py untouched as F5 required. I then ran seven probes by hand on a corrupt-index fixture and every one matched the built bytes: corrupt index -> rc=1 with EXACTLY ONE stderr line; healthy + nothing staged -> rc=0; staged config.json -> rc=1 with the generic line and zero hits of the new text; the parent commit a653d0cead^ hook bytes on the SAME fixture -> rc=0 fail-OPEN, so the delta is the code and not the fixture; parent tier on a non-loop branch -> rc=1 generic, so pipefail did not leak out of the kid block; a kid in another worktree of the same project -> rc=1 unchanged. (3) THE NEAR MISS: a hook that grows the named echo but leaves the pipeline inside the if -- then the diff LOOKS complete, the two committed tests both pass (they were both authored against the same fixture as the fix), and a parent who reads the node rather than the bytes accepts a hook that still exits 0 on a 128. Reading the diff is the only thing that catches it; my a653d0cead^ comparison is the standing counter for that shape. (4) WHERE I DEVIATE: the hypothesis ordered kids <= 1 and I ran exactly one, so I did not spend the 10-kid ceiling elsewhere; and I did NOT demote the node to lean, because the one sub-clause that failed is not the node claim -- the hypothesis (parent-authored) asserted "a cli.py crash" is rc>=2, and my crash probe shows a python death is rc 1, never >=2, so the named line is skipped on a crash (the hook still refuses, so the safety claim is intact). The kid disclosed exactly this in its own push_further rather than claiming it, so its experiment node stands as proved and the overclaim stays on the hypothesis, which I am demoting separately. ACCEPTED, not demoted, with one caveat carried: the named line is attributable only to git failing, never to scope-check crashing.
<!-- THOUGHT:END -->

## Agent Notes
built pipefail fail-closed in the kid scope pipe; pre-fix rc 0 fail-open -> post-fix rc 1 with one named line; empty healthy staged set still rc 0; 42/42 guard tests pass

PARENT REVIEW DG4.03 (a00-bc0bb923): ACCEPTED. 7 probes run against the committed bytes, all matching; the old bytes fail the same probe (rc=0), so the fix is causal. One sub-clause REFUTED against the hypothesis, not the experiment: a cli.py crash is rc 1, not rc>=2, so the named line never fires for it (refusal still happens -- safety holds). Production 14 lines vs the hypothesis clause of 8, disclosed by the kid, under the round ceiling of 40.
