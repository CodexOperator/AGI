---
id: experiment:a00-fbab4084-04210e
mint_id: 59a348580a394cefb98f59ad41c93a6e
type: experiment
parents:
  - hypothesis:l5-reshuffle-dry-run-and-apply-agree-on-an-existing-town-tip
next_edges: []
confidence: 0.9
edited_by: a00-dc5c503d
evidence_runs:
  - experiment:a00-fbab4084-04210e
line_ceiling: 40
loop: hypothesis:l5-reshuffle-dry-run-and-apply-agree-on-an-existing-town-tip@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "parent probe PROBE 1 (regression guard) on the merged bytes: fixture with origin core/main at a wrong tip and NO local branch; --dry-run --kinds towns and --apply --kinds towns", "expected": "round 1 classification survives -- both arms NO-OP, rc 0, remote tip unmoved, no local dup", "observed": "dry rc 0 and apply rc 0 both printed '[NO-OP] core/main already on origin (no create)', no ERR, remote tip unmoved, no local branch created", "result": "pass"}
  - {"conjunct": 1, "class": "gate", "cmd": "parent probe PROBE 2 (regression guard): local core/main at a DIFFERENT tip, origin ABSENT; --dry-run vs --apply", "expected": "round 2 classification survives -- plan proposes no create it cannot perform, names the refusal; apply refuses rc 1, never force-moves", "observed": "dry rc 0 with no 'git branch core/main' and the REFUSED 'DIFFERENT tip' line; apply rc 1 refuses; local tip unmoved", "result": "pass"}
  - {"conjunct": 1, "class": "gate", "cmd": "parent probe PROBE 4 (the round-3 falsifier): fixture with the origin remote REMOVED; --dry-run --kinds towns and --apply --kinds towns", "expected": "no printed verb claims work that did not happen; both arms classify the same trunk set and name the missing origin; apply performs nothing", "observed": "apply printed NO '[APPLY] branch create' and created zero branches (heads unchanged); dry proposed no create/push; both arms printed 'ERR: v3 town creates need an origin remote; 6 planned trunk(s) not created and not pushed'; apply rc 1", "result": "pass"}
production_lines: 17
profile: balanced
role: kid
scaffold_hash: debec34dd41d3b75
season: 2
title: No-origin v3 town creates refuse by name in both arms
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-fbab4084-04210e

## Experiment

Round 3 (kid a00-fbab4084) of `hypothesis:l5-reshuffle-dry-run-and-apply-agree-on-an-existing-town-tip`.
Rounds 1+2 are merged in this tree; this round fixes the THIRD disagreement, on
the `has_origin` axis of `_rs_v3_run`'s town-create block.

**Chosen design: (a) — refuse the section BY NAME when there is no origin
remote, identically in both arms, performing nothing in either.**

Why (a) and not (b): the two legs below are gated `not dry and has_origin`, so
with no origin the run performs nothing; and with no remote the origin state of
every planned trunk is UNKNOWN — exactly the round-1 `failed` shape, which is
already "REFUSED BY NAME, apply rc-honest". Treating a missing remote as one
more instance of that shape is ONE design for both axes, not a second one.
Shape (b) (create the local branch anyway) would have to grow a resume/local-
tip classification for the no-origin path too, because `git branch <t> <tip>`
hard-fails on a re-run where the local trunk already exists — more surface than
this round's ceiling allows.

Implementation (`extensions/agi/bin/cli.py`, `_rs_v3_run`, +17/-2 production lines):
the planned trunk list is materialised once, the header prints only when
`has_origin`, otherwise ONE `ERR:` line names the refusal on stderr and every
planned trunk name is collected into `refused` (the round-1/2 collector), and
the loop iterates an empty list. The collect-not-abort shape is preserved: the
post-rename, main and loop sections still run.

### Pre-fix (measured before the edit)

Repro on a `_v3_repo(with_town_nodes=True)` fixture with the origin remote
removed (`git remote remove origin`), `--apply --kinds towns`:

```
=== rc 0 ===
  town set: town:* nodes (3 towns)
  v3 town creates (3 towns):
    [APPLY] branch create (v3): git branch core/main season2/main
[APPLY] branch push (new): git push -u origin core/main
    [APPLY] branch create (v3): git branch core/season2/main season2/main
[APPLY] branch push (new): git push -u origin core/season2/main
    ... 6 create + 6 push [APPLY] lines in all ...
apply: local renames + worktree re-points done; remote legacy branches NOT deleted (see --delete-old)

NEW LOCAL BRANCHES: []      <-- six [APPLY] verbs, zero branches
```

The new test failed first, on the merged bytes:

```
$ python3 -m pytest extensions/agi/tests/test_branch_reshuffle_v3.py -q -k no_origin_remote_refuses
>       assert "need an origin remote" in plan.stderr, plan.stderr
E       AssertionError: branches.py: deprecated alias used: master -> season1/main
E       assert 'need an origin remote' in 'branches.py: deprecated alias used: master -> season1/main\n'
1 failed, 67 deselected
```

### Post-fix

```
$ python3 -m pytest extensions/agi/tests/test_branch_reshuffle_v3.py -q -k no_origin_remote_refuses
1 passed, 67 deselected in 0.59s
```

Same repro, after the edit — no `[APPLY]` line anywhere, nothing created, rc 1:

```
=== rc 1 ===
  town set: town:* nodes (3 towns)
apply: local renames + worktree re-points done; remote legacy branches NOT deleted (see --delete-old)

STDERR: ERR: v3 town creates need an origin remote; 6 planned trunk(s) not created and not pushed
        ERR: v3 town creates: 6 trunk(s) refused: core/main, core/season2/main,
        streaming-suite/main, streaming-suite/season1/main, web-app-suite/main, web-app-suite/season1/main

NEW LOCAL BRANCHES: []
```

Both arms print the SAME `ERR:` line (the plan arm exits 0, apply exits 1 — the
round-2 rule: a plan proposes, an apply answers for it). The test asserts
exactly that: same refusal line in both arms, no `[APPLY]`, no `git branch `
line, and `_heads()` byte-identical before/after the apply.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_branch_reshuffle_v3.py \
    extensions/agi/tests/test_branch_reshuffle.py extensions/agi/tests/test_cli.py -q
156 passed, 34 warnings in 65.21s (0:01:05)
```

(155 on the merged bytes + this round's one new test = 156; no drop.)

Real-tree DRY ONLY, `git ls-remote --heads origin | wc -l` identical before and
after (13 -> 13); every planned trunk printed `[NO-OP]` because every one is
already on origin — the `has_origin = True` path is untouched:

```
$ python3 extensions/agi/bin/cli.py branch-reshuffle --dry-run --kinds main,towns
    [NO-OP] core/season2/main already on origin (no create)
    [NO-OP] local-maxxing/main already on origin (no create)
    ... 9 [NO-OP] trunk lines ...
  v3 main: season<n>/main stays (remote-visible); master add-only, kept (frozen season-1 name)
dry-run: nothing changed
```

Production lines (`git diff --numstat`, cli.py): 17 added, 2 deleted.
Test file excluded from the ceiling per the dispatch orders.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-dc5c503d, L5.06). Accepted, proved, verdict KEPT. The bytes close the third disagreement I measured on round 2: with the origin remote removed, `--apply --kinds towns` printed six `[APPLY] branch create (v3)` lines and created zero branches, because the real work sits behind `if not dry and has_origin:`. Kid 3 took design (a) and made the miss loud in both arms: the section is refused by name (cli.py:4865-4881, `ERR: v3 town creates need an origin remote; N planned trunk(s) not created and not pushed`, naming every planned trunk) and the loop iterates `planned if has_origin else []`, so neither arm proposes or performs a create. My PROBE 4 (parent-run, merged bytes) confirms it: apply printed NO `[APPLY] branch create`, created zero branches (local heads unchanged), and both arms named the missing origin; apply rc 1, dry rc 0. The verb no longer claims work that did not happen. My PROBE 1 and PROBE 2 re-run on the merged bytes confirm rounds 1 and 2 were NOT regressed (NO-OP for a present trunk; no create line for a refused wrong-tip trunk; apply still refuses rc 1 and never force-moves). Round suite re-run by the parent on the merged bytes: test_branch_reshuffle_v3 + test_branch_reshuffle + test_cli = 156 passed (round 2 was 155; +1 = this round test). Live-tree DRY-ONLY: `git ls-remote --heads origin | wc -l` 13 before and after, rc 0, "dry-run: nothing changed".
<!-- THOUGHT:END -->

## Agent Notes
no-origin v3 town creates now REFUSED BY NAME in both arms (same ERR line, nothing created/pushed either arm); has_origin=True untouched; test added, 156 pass, real-tree dry 13->13
