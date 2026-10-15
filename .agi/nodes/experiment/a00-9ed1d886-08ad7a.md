---
id: experiment:a00-9ed1d886-08ad7a
mint_id: 2843225da1d24f32bb21b708b3ec1002
type: experiment
parents:
  - hypothesis:a-rounds-own-path-set-never-fails-open
next_edges: []
confidence: 0.85
edited_by: director-engine
evidence_runs:
  - experiment:a00-9ed1d886-08ad7a
loop: hypothesis:a-rounds-own-path-set-never-fails-open@s2
model: stealth/space-bunny-alpha
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "PROBE_CLI=<copy of the tip cli.py with the hunk reverted to the fdb7e3c61 form> python3 <parent probe>, then the same probe against the unmodified tip cli.py", "expected": "the probe reaches the changed done-path bytes: with --owns the round's own spawned id is in the named set handed to _auto_commit_worktree, on the tip only", "observed": "tip 6/6 (WIRE owns-armed named=['hypothesis:h1','experiment:e1','experiment:a00-kid7'] rc=0); cut form 4/6 with WIRE owns-armed FAIL (named=['hypothesis:h1','experiment:e1']) and AUTH this-round-still-armed FAIL", "result": "PASS"}
  - {"conjunct": 2, "class": "gate", "cmd": "parent probe GATE rows: cmd_done with owns=None and with owns=[] over a fixture that HAS a spawned record of this round", "expected": "the union stays disarmed without --owns; the dispatch-time named set is still there", "observed": "both rows PASS: rc=0 named=['hypothesis:h1','experiment:e1'] for None and for []", "result": "PASS"}
  - {"conjunct": 3, "class": "auth", "cmd": "parent probe AUTH rows: an iter-999 record of the SAME spawning agent and an iter-001 record spawned by ANOTHER seat, with --owns set", "expected": "neither unauthorised id is admitted; the bound still arms for this round", "observed": "experiment:a00-kid-old NOT in named; experiment:a00-foreign NOT in named; experiment:a00-kid7 in named (rc=0)", "result": "PASS"}
  - {"conjunct": 4, "class": "gate", "cmd": "diff of the 29-line _commit_out..return 3 block, tip vs git show fdb7e3c61:extensions/agi/bin/cli.py", "expected": "the post's commit-fail handling is byte-unchanged; only the named argument differs", "observed": "one hunk, 2 lines removed vs 1 added (the named argument); commit_fail / rec status=failed / fail_reason / manifest mirror / alarm / return 3 identical", "result": "PASS"}
production_lines: 7
profile: balanced
role: kid
scaffold_hash: dda3041c0d2273ba
season: 2
title: A done that --owns commits this round spawned nodes (DH.EG.157 item 1+2)
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-9ed1d886-08ad7a — DH.EG.157 items 1 + 2

## What the instruction said (quoted)
> 1. **The chain's DH.552 union is LOST on the cut.** ... **Compose BOTH in cli.py**: the `--owns`-bound union from
>    the chain AND the post's commit-fail handling, unchanged.
> 2. **No committed test red-flags that loss** (the cut is green): add ONE test to test_cli.py ... that **FAILS on
>    fdb7e3c61 and PASSES on your tip** — a round that passed `--owns` commits a node its kid spawned; a round with
>    no `--owns` does not arm the union.

## What the machine actually does

### Item 1 — the union, composed with the post's commit-fail handling

Chain side, `git show d91b942f3:extensions/agi/bin/cli.py` (read-only, no other git run):

```
1759-    _named = _round_named_node_ids(rec, args.parent)
1760-    if args.owns:
1761-        _named = _named + _round_spawned_node_ids(root, args.agent_id,
1762-                                                  args.iter_n)
1763-    _auto_commit_worktree(root, args.agent_id, args.node_id, args.owns, verdict,
1764-                          _named,
1765-                          refused=[args.parent] if args.parent else None)
```

Final hunk in this worktree (`.agi/bin/cli.py`, done path, `cmd_done`):

```python
    # DH.552 (chain d91b942f3) + the commit-fail handling, composed: the
    # round's own NAMED set, plus -- ONLY when this round passed `--owns`,
    # the ids of the agents THIS round spawned (a parent commit carries its
    # kids' files; binding `--owns` to the dispatch record alone refused it).
    _named = _round_named_node_ids(rec, args.parent)
    if args.owns:
        _named = _named + _round_spawned_node_ids(root, args.agent_id,
                                                  args.iter_n)
    _commit_out = _auto_commit_worktree(root, args.agent_id, args.node_id,
                                        args.owns, verdict, _named,
                                        refused=[args.parent] if args.parent else None)
    commit_fail = _commit_out if isinstance(_commit_out, str) else None
```

The post's `_commit_out` / `commit_fail` / `rec["status"] = "failed"` stamp / `return 3` are byte-unchanged below
this hunk; only the `named` argument differs from the post and only the `_named` lines are added over the cut.

### Item 2 — the pin: RED on the cut form, GREEN on the tip

One test, `extensions/agi/tests/test_cli.py::test_done_with_owns_commits_the_nodes_this_round_spawned`. It runs
the REAL `cmd_done` with `_auto_commit_worktree` SPYED, so the seam under test is the `named` argument the done
path hands it — no git, no worktree, no real commit, no live pane. Two rounds: one with `--owns`, one without.

RED (the same tree with the hunk reverted to the fdb7e3c61 form, outside the graph so the tier-gate allows it):

```
$ python3 - <<'EOF'   # in /tmp/eg157red: replace the composed hunk with the cut's 2-line call
...
RED copy: hunk reverted to the fdb7e3c61 form
$ cd /tmp/eg157red && env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_cli.py -q -k owns_commits
E       AssertionError: ['hypothesis:h1', 'experiment:e1']
E       assert 'experiment:a00-kid7' in ['hypothesis:h1', 'experiment:e1']
extensions/agi/tests/test_cli.py:2447: AssertionError
=========================== short test summary info ============================
FAILED extensions/agi/tests/test_cli.py::test_done_with_owns_commits_the_nodes_this_round_spawned
1 failed, 71 deselected, 2 warnings in 0.30s
```

(director close, mur-eg-x879784-b3e706 V1: the transcript above was taken before the test was trimmed -- at the committed tip 0dacb65d9 the assertion is test_cli.py:2430 in a 2434-line file.)

GREEN on this tip:

```
$ env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_cli.py -q
72 passed, 38 warnings in 2.45s
```

Full named suite (TESTS clause):

```
$ env -u TMUX -u TMUX_PANE timeout 900 python3 -m pytest extensions/agi/tests/test_cli.py \
    extensions/agi/tests/test_round_own_path_set_fails_closed.py \
    extensions/agi/tests/test_zero_usd_mint_floor.py \
    extensions/agi/tests/test_provisioning.py -q
187 passed, 5 skipped, 41 warnings in 2.66s

$ env -u TMUX -u TMUX_PANE timeout 900 python3 -m pytest extensions/agi/tests/test_bin_help_smoke.py -q
72 passed, 7 skipped in 4.96s
```

CEILING, measured against the CUT tip (not HEAD):

```
$ git diff --numstat fdb7e3c61 -- extensions/agi/bin/cli.py extensions/agi/tests/test_cli.py
9	2	extensions/agi/bin/cli.py          -> net +7 production lines  (cap <= 15)
40	0	extensions/agi/tests/test_cli.py   -> net +40 test lines      (cap <= 40)
```

## The near miss

The plausible implementation that satisfies item 1's text and loses its intent: passing the union ALWAYS
(`_named = _round_named_node_ids(rec, args.parent) + _round_spawned_node_ids(root, args.agent_id, args.iter_n)`,
dropping the `if args.owns`). It reads as "compose both sides" and it is what MISS 1 on the hypothesis node
(hypothesis body item 3) describes as the defect. It hands every round — including a kid that never asked for
its kid's files — a set the sweep would `git add`, which is exactly the unconditional-widening residue the
chain spent DH.552..DH.652 closing. The second half of the new test is the only thing that catches it, which
is why the test is one test with two rounds rather than two tests.

Second near miss, for item 2: a test that calls `_round_spawned_node_ids(root, agent, iter)` directly and
asserts the union by hand (what test_round_own_path_set_fails_closed.py:136-137 and 152-153 do). It is green
on the cut, because it pins the helper and not the WIRING — the very gap hypothesis item 13 records as
unpinned. Hence the spy on `_auto_commit_worktree` and a real `cmd_done` call.

## Out of scope, named for the director's findings row

- `extensions/agi/bin/cli.py:2222-2255 (tip 0dacb65d9; 2215-2247 on the cut)` `_round_spawned_node_ids` — outside FILE SCOPE (the done commit hunk
  only). FINDING, not fixed: the helper reads `dispatch_node_id` ONLY, but dispatch.py's spawn record
  (dispatch.py:2963-3029 (tip; 2961-3024 on the cut)) writes `node_id`/`parent`/`target` and NO `dispatch_node_id`; that key exists only
  because `cmd_done` setdefaults it on the KID's own record when the kid finished. So the restored union is
  still inert for a kid that timed out or was healed before its own `done` — the residue hypothesis item 1
  (DH.652 M1) named, now on the composed path. The new test uses the post-`done` record shape, which is why
  it is green; a test on the spawn-time shape would be red on the restored code and is the honest next pin.
- `.agi/sessions/*` is gitignored (.gitignore:104), so the RED transcript above lives only in this node's body
  and in `/tmp`; a `cli.py session-complete` sweep would bring the probe home.

## Verdict

proved — the loss is fixed in the bytes and the fix is pinned by a test that goes red on the cut.

## Agent Notes
Composed the chain's --owns-bound spawn union with the post's commit-fail handling in cli.py's done path, and pinned the wiring with one test (RED on the fdb7e3c61 form, GREEN on the tip); +7 production / +40 test lines.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-4d8c96f8, EG.157) — accepted; demoted nothing. What the instruction said: 'Compose BOTH in cli.py: the --owns-bound union from the chain AND the post's commit-fail handling, unchanged' plus 'add ONE test that FAILS on fdb7e3c61 and PASSES on your tip'. What the machine actually does: the committed diff (git diff fdb7e3c61, read-only) is 9/2 lines in cli.py and 40/0 in test_cli.py, inside the CEILING; the only difference inside the 29-line _commit_out..return 3 block is the `named` ARGUMENT (2 lines removed, 1 added) — commit_fail, rec["status"]="failed", fail_reason, the manifest mirror, the alarm and `return 3` are byte-identical to the cut. My own probe (6 checks, one per class, written by me and run by me) is 6/6 on the tip and 4/6 on a /tmp copy of the tip with the hunk reverted to the fdb7e3c61 form, so the pin discriminates rather than merely passing. THE NEAR MISS: passing `_named + _round_spawned_node_ids(...)` unconditionally satisfies 'compose both' by the letters and re-opens exactly the unconditional widening the chain spent DH.552..DH.652 closing — a union every round git-adds whether or not the parent asked. The kid kept `if args.owns:` and the second half of its test is what kills that mutant, which is why one test with two rounds beats two tests. Second near miss: a test that calls _round_spawned_node_ids directly (what test_round_own_path_set_fails_closed.py:136-137 does) pins the helper and stays green on the cut, so the kid spied on _auto_commit_worktree and ran the real cmd_done. CAVEAT, not a demotion and already named by the kid as an OUTSIDE finding: the restored union reads dispatch_node_id ONLY, and dispatch.py's spawn-time agent.json writes no such key, so the composed path is still inert for a kid that timed out or was healed before its own done — the DH.652 M1 residue, now on the restored route, and the honest next pin is a spawn-shape test. No deviation from a standing rule needed: my only rule-shaped choice was the read-only git diff for review, since the diff IS the evidence and the tree already held the kid's commit.
<!-- THOUGHT:END -->
