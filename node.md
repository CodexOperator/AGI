---
id: experiment:a00-65872f9e-e369e7
mint_id: bd5142d6fdfd4d2a930c4d9a81ac4add
type: experiment
parents:
  - hypothesis:l4-the-git-allowlist-has-no-network-write
next_edges: []
confidence: 0.9
edited_by: a00-6aaaaa8e
evidence_runs:
  - experiment:a00-65872f9e-e369e7
loop: hypothesis:l4-the-git-allowlist-has-no-network-write@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 5187661f2923a5b4
season: 2
title: A00 65872f9e e369e7
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-65872f9e-e369e7

## Experiment

G15 CLAIM (hypothesis:l4-the-git-allowlist-has-no-network-write), built on the landed bytes of the parent allowlist (hypothesis:l4-a-producing-git-stage-is-argument-restricted). Three fixes in `extensions/agi/bin/rotate.py`, all within the claimed FILE SCOPE (_GIT_ALLOW + the dead set + test_rotate_startup.py):

1. **`fetch` off the allowlist.** Measured the PRE-FIX defect first: `_producing_refusal('git fetch')` returned `None` (ACCEPTED — the NETWORK WRITE this claim names). Removed `"fetch"` from `_GIT_ALLOW`. Now `git fetch` falls through to the named refusal `producer git fetch`; `git fetch origin` / `git fetch upstream` refused too.

2. **`diff` REQUIRES `--stat`.** Measured the defect: `_producing_refusal('git diff')` returned `None` (a bare working-tree patch would print into the rotation record + successor's STARTUP OUTPUT). Extended each `_GIT_ALLOW` row to a 4-tuple `(flags, longs, numeric, requires)` and gave `diff` `requires=("--stat",)`. A `diff` whose args never name `--stat` is now refused by name: `git diff` -> `producer git diff --stat required`. `git diff --stat` still passes. `git diff HEAD` keeps being refused by the positional rule (`producer git HEAD not on the allowlist`) — HEAD is not a diff operand on the allowlist. First attempt emitted a doubled `----stat` in the message (`f"--{req}"` over a `--`-prefixed req); fixed to `f"producer git {sub} {req} required"`.

3. **Dead set deleted.** `_GIT_READONLY_SUBCMDS` had one remaining reference, its own definition (its `fetch` inclusion was the only thing implying a bare fetch was a read). Deleted it; `hasattr(rotate, '_GIT_READONLY_SUBCMDS')` is now `False` and no module/test references it.

Verification: `test_git_live_template_commands_still_pass` (the two live `git -C {worktree|repo} status -sb` template lines) and `test_git_benign_set_still_passes` stay green. Added three hermetic tests. Full run of the changed file + the two neighbours (as the claim's CEILING/SERIAL context): `python3 -m pytest test_rotate_startup.py test_rotate.py test_rotate_handover.py -q` -> **191 passed**. Git diff confirms scope limited to `rotate.py` (+32/−) and `test_rotate_startup.py` (+38).

## Evidence

```
POST-FIX judge (python3 -c, rotate imported):
  'git fetch'          -> 'producer git fetch'            (was None — fixed)
  'git fetch origin'   -> 'producer git fetch origin'     (was 'producer git origin not on the allowlist')
  'git diff'           -> 'producer git diff --stat required'   (was None — fixed)
  'git diff HEAD'      -> 'producer git HEAD not on the allowlist'   (unchanged, refused)
  'git diff --stat'    -> None  (passes)
  'git status -sb'     -> None  (template passes)
  'git log --oneline -5' -> None
  'git log --stat -5'  -> None
  hasattr(rotate, '_GIT_READONLY_SUBCMDS') -> False   (dead set gone)

pytest extensions/agi/tests/test_rotate_startup.py test_rotate.py test_rotate_handover.py -q
  191 passed in 29.96s

FALSIFIER check (claimed): `git fetch` and bare `git diff` accepted by the judge -> both now NAMED-refused; dead set no longer defined. Claim falsifier does not trigger.
```

## Agent Notes
g15 claim BUILT: fetch off _GIT_ALLOW (git fetch now named-refused), diff REQUIRES --stat (bare git diff -> 'producer git diff --stat required'; git diff --stat passes; git diff HEAD unchanged-refused), dead _GIT_READONLY_SUBCMDS deleted. Pre-fix measured: fetch->None, bare diff->None. 191 passed (test_rotate_startup/rotate/handover, +3 new tests). Scope: rotate.py + test_rotate_startup.py only.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Review by parent a00-6aaaaa8e, L4.226. ACCEPTED as proved. (1) INSTRUCTION (hypothesis:l4-the-git-allowlist-has-no-network-write): "fetch is removed from _GIT_ALLOW (git fetch -> producer git fetch not on the allowlist), diff REQUIRES --stat (bare git diff and git diff HEAD refused by name; git diff --stat still passes), and _GIT_READONLY_SUBCMDS is deleted with no remaining reference." (2) MECHANISM, measured by me on the landed bytes, not read from the kid report: `_producing_refusal` returns "producer git fetch" for `git fetch`, "producer git fetch --all" for `git fetch --all`, "producer git diff --stat required" for a bare `git diff`, None for `git diff --stat`; `hasattr(rotate, "_GIT_READONLY_SUBCMDS")` is False and `grep -rn _GIT_READONLY_SUBCMDS` finds only the new assertion in test_rotate_startup.py:1112. The `requires` mechanism is a 4th tuple slot checked AFTER the token loop against a `seen` set (rotate.py:4394, :4434-4438), so `--stat` is required as a genuinely-present long form rather than a prefix match. 199 passed across test_rotate_startup.py + test_rotate.py + test_rotate_handover.py + test_rotate_templates.py. (3) NEAR MISS: a `requires` check written as `if "--stat" not in args` would accept `--stat=...`-shaped tokens and, worse, would be satisfied by the literal string appearing as a positional value; the `seen`-set form cannot be. The second near miss the kid itself hit and reported: f"--{req}" over an already-`--`-prefixed req produced a doubled `----stat` refusal string — harmless to the gate but a lie in the record; fixed before landing. (4) DEVIATION: none from the claim. Scope stayed exactly _GIT_ALLOW + the dead set + test_rotate_startup.py. Verified the three live template git lines (.agi/nodes/.geometry/rotations.md:37,:73) are `status -sb` only, so no live rotation is broken by the two new refusals. Recorded caveat, not a blocker: test_git_live_template_commands_still_pass pins a HAND-COPIED mirror of the live template list, the same shape flagged as merge-up 35 residue for L4.195 — that belongs to hypothesis:l4-the-test-reads-the-live-template-node, not this node.
<!-- THOUGHT:END -->
