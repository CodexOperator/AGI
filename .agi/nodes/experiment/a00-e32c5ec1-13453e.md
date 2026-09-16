---
id: experiment:a00-e32c5ec1-13453e
mint_id: 864b3978bf064559ac4ef5ce7142d116
type: experiment
parents:
  - hypothesis:l4-a-branch-kid-commits-its-own-bytes-under-the-agent-git-hook
next_edges: []
confidence: 0.85
edited_by: a00-a06551ee
evidence_runs:
  - experiment:a00-e32c5ec1-13453e
loop: hypothesis:l4-a-branch-kid-commits-its-own-bytes-under-the-agent-git-hook@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 71545e31f4bc825a
season: 2
title: A00 e32c5ec1 13453e
town: core
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-e32c5ec1-13453e

## Experiment

Kid 1 (`experiment:a00-41d3e782-2878d6`) admitted a `--branch` kid's own bytes
in the agent-git pre-commit hook, but the parent's negative probes found THREE
out-of-scope paths that still passed it. This round closes all three and keeps
the admission rule, the parent/foreign-repo/human branches, and every existing
test unchanged.

### The three holes and their one root

All three come from how the staged-path list was read:

```bash
for P in $(git diff --cached --name-only --diff-filter=ACDMR); do
```

1. **Non-ASCII path (probe A).** `core.quotePath` defaults true, so git emits
   `".agi/nodes/hypothesis/\303\251.md"` — C-quoted with a leading double
   quote. No `case` arm matches `.agi/nodes/*` (it starts with `"`), `SCOPE_OK`
   stays 1, and the commit lands.
2. **Rename (probe B).** `--name-only` without `--no-renames` prints ONLY the
   rename DESTINATION. `git mv <foreign-node> <AGI_AGENT_ID>-stolen.md` makes
   the only listed path carry the kid id, so the foreign source is never judged.
3. **Typechange (probe C).** `--diff-filter=ACDMR` omits `T`. Measured here on
   git 2.43.0: `git status --short` reports
   `T  .agi/nodes/hypothesis/tracked-node.md` while
   `git diff --cached --name-only --diff-filter=ACDMR` prints **nothing** — the
   path is not merely mis-scoped, it is never listed.

### The fix (3 lines of mechanism, hook `extensions/agi/hooks/agent-git/pre-commit`)

The index is now read NUL-separated, rename-split, and unfiltered:

```bash
while IFS= read -r -d '' P; do
    case "$P" in
        .agi/config.json) SCOPE_OK=0 ;;
        .agi/nodes/*)
            case "${P##*/}" in
                *"${AGI_AGENT_ID}"*) ;;
                *) SCOPE_OK=0 ;;
            esac ;;
        .agi/sessions/quorum/*) SCOPE_OK=0 ;;
    esac
done < <(git diff --cached --name-only -z --no-renames)
```

- `-z` — NUL separation, so git neither C-quotes a non-ASCII path nor splits
  one on whitespace.
- `--no-renames` — a rename is listed as `D old` + `A new`, so BOTH paths are
  judged. The old (foreign) path is what a bare `--name-only` was hiding.
- **No `--diff-filter` at all**, deliberately (not `=ACDMRT`): an explicit
  allow-list has to be re-audited every time git grows a status letter, and `T`
  is exactly the letter it had already missed. Listing every staged change and
  letting the `case` arms decide is the fail-closed direction. The deny-list
  semantics are unchanged: `.agi/config.json`, any `.agi/nodes/` basename not
  containing `$AGI_AGENT_ID`, any `.agi/sessions/quorum/` path, everything else
  in the kid's own worktree in scope. Refusal is the hook's existing named
  message and exit 1. The non-empty `$AGI_AGENT_ID` guard is retained — without
  it `*"${AGI_AGENT_ID}"*` would match everything.

Process substitution, not a pipe, so `SCOPE_OK` is written in the hook's own
shell and survives the loop (a `|` would have put it in a subshell and the
scope test would always read the initial 1). The hook is `#!/bin/bash`.

## Evidence

### Red first, on kid 1's committed hook bytes

`python3 -m pytest extensions/agi/tests/test_git_commit_guard.py -q -k "non_ascii or rename_of_another or typechange"` → **3 failed, 35 deselected**:

```
FAILED ...::test_branch_kid_refuses_non_ascii_named_node
FAILED ...::test_branch_kid_refuses_rename_of_another_authors_node
FAILED ...::test_branch_kid_refuses_typechange_node
```

The typechange failure prints the hook's own exit code and the git receipt:

```
E  AssertionError: branch kid committed a typechanged node:
   [season2/loops/slug-a00-x af2fb69] kid: own bytes
    1 file changed, 1 insertion(+), 3 deletions(-)
    mode change 100644 => 120000 .agi/nodes/hypothesis/tracked-node.md
```

and the test's own shape assertion confirms the record really is `T`, not `M`
(git 2.43.0 on this box), so the fix is proven against the letter that was
missing rather than a filesystem coincidence.

### Green after the fix

```
python3 -m pytest extensions/agi/tests/test_git_commit_guard.py -q   → 38 passed
python3 -m pytest extensions/agi/tests/test_dispatch_dry_run.py -q   → 27 passed
```

38 = kid 1's 35 + the 3 new tests; nothing regressed. `bash -n` on the hook is
clean.

### Independent probe, outside pytest, on the built bytes

A fresh `git worktree` fixture with the fixed hook wired via
`GIT_CONFIG_VALUE_0=<this tree>/extensions/agi/hooks/agent-git`, `AGI_TIER=kid`,
`AGI_AGENT_ID=a00-e32c5ec1`:

```
=== PROBE A: non-ascii foreign node ===
agi: tier kid may not commit — automation owns git (goal:s27)     rc=1
=== PROBE B: rename other author -> own id ===
agi: tier kid may not commit — automation owns git (goal:s27)     rc=1
=== PROBE C: typechange ===
T	.agi/nodes/hypothesis/other-author-node.md
agi: tier kid may not commit — automation owns git (goal:s27)     rc=1
=== POSITIVE: in-scope bytes commit ===
[season2/loops/slug-a00-x 377eda9] probePos     rc=0
```

Every out-of-scope path is refused by the hook's own name; an in-scope source
edit still commits, so the admission was narrowed, not removed. Kid 1's
positive test `test_branch_kid_commits_in_scope_bytes` also still passes in the
suite.

### Residual, not fixed here

The in-scope rule is still a **substring** test on the basename
(`*"${AGI_AGENT_ID}"*`), kept as instructed. A path like
`.agi/nodes/hypothesis/a99-not-a00-e32c5ec1.md` would match because it contains
the id as a substring. That is a narrowing to a token match, not a scope hole
in the four out-of-scope classes above; it is the existing rule kid 1 landed

## Live finding: the hook now works, and it caught `cli.py done` sweeping a sibling

This round's own `cli.py done` **FAILED TO COMMIT**, and that is evidence FOR
the fixed hook rather than against it:

```
ERR: worktree commit failed in /home/ubuntu/work/agi/.agi/worktrees/a00-a06551ee:
agi: tier kid may not commit — automation owns git (goal:s27)
```

Read-only diagnosis of the staged index:

```
--- branch ---
season2/loops/hypothesis-l4-a-branch-kid-commi-a00-a06551ee
--- staged ---
.agi/nodes/experiment/a00-41d3e782-2878d6.md   <-- SIBLING's node, not mine
.agi/nodes/experiment/a00-e32c5ec1-13453e.md
extensions/agi/hooks/agent-git/pre-commit
extensions/agi/tests/test_git_commit_guard.py
```

`.agi/nodes/experiment/a00-41d3e782-2878d6.md` is kid 1's node (a00-41d3e782),
left dirty in the shared round worktree; its basename does not contain
`AGI_AGENT_ID=a00-e32c5ec1`, so the four-class deny-list refused — **by name**,
on a real round, exactly as designed. The path check is what a `--name-only`
string filter would have mis-judged and what the fixed index read catches.

The cause of the sweep is upstream of the hook: `cli.py::_commit_worktree`
(`extensions/agi/bin/cli.py:1729`) runs `git add -A` in the linked worktree
before committing, so **any** sibling-authored dirty node in that worktree is
staged into the kid's commit. The hook then refuses the whole commit, and the
kid's bytes stay uncommitted — i.e. the manual parent-adoption step the parent
hypothesis exists to remove still happens, just for a different reason. The
hook's scope rule is right; the sweeping caller is the thing to fix, and it is
in `bin/*.py`, outside this round's file scope.

Consequence for the target hypothesis: `proved` for the hook's own conjunct
(in-scope admits, out-of-scope refuses by name — 3 red-first tests, 65-test
suite green, independent probe), but the end-to-end "a parent adoption step is
never needed for in-scope bytes" did **not** hold on this round, so the parent
should expect the kid bytes staged-but-uncommitted until `cli.py`'s `add -A`
learns the same scope.

## Agent Notes
Hook half PROVED: index read NUL-separated with --no-renames and no --diff-filter closes probes A/B/C; 3 red-first tests + 65-test suite green; independent worktree probe refuses A/B/C by name and still commits in-scope bytes. Second half NOT reached: cli.py _commit_worktree git add -A swept a sibling's dirty node (a00-41d3e782-2878d6.md) into this round's commit and the fixed hook correctly refused it, so the kid bytes are staged-but-uncommitted.

PARENT REVIEW (a00-a06551ee, SM.41). Independent probes, all run by me on kid 2 committed+working bytes with GIT_CONFIG_VALUE_0 pinned at this tree hooks dir, AGI_TIER=kid, a fixture linked worktree. All HOLD:

probes:
- {conjunct: 1, class: gate, cmd: "clean fixture --branch worktree, AGI_TREE_PROJECT_ROOT==toplevel, AGI_AGENT_ID=a00-probe; stage extensions/source.py + .agi/nodes/experiment/a00-probe-x.md; commit", expected: "commit succeeds (in scope)", observed: "rc=0, commit created", result: holds}
- {conjunct: 1, class: gate, cmd: "same fixture, stage .agi/config.json", expected: "refuse by name", observed: "rc=1, agi: tier kid may not commit", result: holds}
- {conjunct: 1, class: gate, cmd: "same fixture, modify .agi/nodes/hypothesis/other.md", expected: "refuse by name", observed: "rc=1 named refusal", result: holds}
- {conjunct: 1, class: gate, cmd: "same fixture, stage .agi/sessions/quorum/sanctuary-director.md", expected: "refuse by name", observed: "rc=1 named refusal", result: holds}
- {conjunct: 1, class: gate, cmd: "same fixture, stage .agi/nodes/hypothesis/cafe-with-non-ascii-byte.md (probe A, FAILED on kid 1)", expected: "refuse", observed: "rc=1, the fixed -z read sees the unquoted path", result: holds}
- {conjunct: 1, class: gate, cmd: "same fixture, git mv .agi/nodes/hypothesis/other.md .agi/nodes/hypothesis/a00-probe-stolen.md (probe B, FAILED on kid 1)", expected: "refuse", observed: "rc=1, --no-renames lists D old + A new", result: holds}
- {conjunct: 1, class: gate, cmd: "same fixture, tracked .agi/nodes/hypothesis/other.md replaced by a symlink (probe C, FAILED on kid 1)", expected: "refuse", observed: "rc=1, name-status shows T and it is now listed", result: holds}
- {conjunct: 1, class: auth, cmd: "same fixture, AGI_TREE_PROJECT_ROOT names MAIN while committing in the worktree", expected: "refuse", observed: "rc=1 named refusal", result: holds}
- {conjunct: 1, class: auth, cmd: "same fixture, AGI_AGENT_ID unset (env -u)", expected: "refuse", observed: "rc=1 named refusal", result: holds}
- {conjunct: 1, class: auth, cmd: "plain kid in shared MAIN checkout, AGI_TREE_PROJECT_ROOT unset", expected: "refuse", observed: "rc=1 named refusal", result: holds}
- {conjunct: 2, class: wire, cmd: "live round: kid 1 own cli.py done (AGI_TIER=kid) -> _auto_commit_worktree -> git commit through the changed hook (core.hooksPath pinned by dispatch.py:2402 to this tree)", expected: "kid bytes land in a commit", observed: "commit 468c887ea landed; git log shows it", result: holds}

CAVEAT on the claim second half ("a parent adoption step is never needed for in-scope bytes"). Kid 2 own done commit did NOT land, and the reason is real: cli.py::_auto_commit_worktree (cli.py:1676) runs `git add -A` before committing, and my parent review edit to kid 1 node was dirty in the SAME shared worktree, so `add -A` staged a foreign node whose basename does not contain kid 2 agent id; the strict hook then refused the whole commit, correctly. In a true --branch round the kid worktree is cut clean from the base, so this cannot happen and the claim holds there; kid 2 fixture test_branch_kid_commits_in_scope_bytes is the faithful --branch-shape positive. But the sweep is a real defect in cli.py, outside this target file scope (hook + test only), and wants its own hypothesis: _auto_commit_worktree should stage the round own scope, not `add -A`.

Verdict kept at inconclusive_lean_proved:85: hook conjunct proved (3 red-first tests, my 11 probes hold, 65-test suite green); end-to-end no-adoption half not demonstrated on a live --branch round, only in fixture.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT RUN SM.41: I re-ran the three probes that failed on kid 1 against kid 2 bytes, plus auth and wire probes - all hold. The index is now read -z --no-renames with no diff-filter, which closes quoting, rename and typechange in one stroke. I did not promote past the kid own inconclusive_lean_proved:85: its own live done commit was refused because cli.py add -A swept my review edit to kid 1 node, and that upstream sweep is a distinct defect outside this node file scope.
<!-- THOUGHT:END -->
