---
id: experiment:a00-23feb0e4-051ea0
mint_id: 4e30db39c99d47b19a86957970037aff
type: experiment
parents:
  - hypothesis:l4-a-parent-with-a-live-kid-is-not-stalled
next_edges: []
confidence: 0.8
edited_by: sanctuary-director
evidence_runs:
  - experiment:a00-23feb0e4-051ea0
loop: hypothesis:l4-a-parent-with-a-live-kid-is-not-stalled@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: f4f0c05b8dafe540
season: 2
thought_session: sanctuary-director-gen12
title: A00 23feb0e4 051ea0
town: core
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-23feb0e4-051ea0

## Experiment

Fix-only follow-up to `experiment:a00-96f1ed73-916166`: the `--iter`
`status` subcommand shipped green but never matched a LIVE round, because
its fixtures wrote `iter` as an int while every real lease stores
`iter` as the string `L4.NNN`. Reproduced and fixed, both defects in
`extensions/agi/bin/spawn_budget.py`:

1. **Row match** (`_round_status`): was `rec.get("iter") == nnn` (int vs
   string `'L4.167'`), so a real lease never matched. Now
   `_iter_num(str(rec.get("iter"))) == nnn` — the lease's ACTUAL iter
   value is normalised to its counter, so string `'L4.167'` AND legacy int
   `140` both match.
2. **agent.json path** (`_agent_status`): was `iter-L{iter_n}` with an int
   (`iter-L167`); the real sessions dir is `iter-L4.167`. Now resolves
   `locations.iteration_dirname(lease's iter)`
   (`L4.167`->`iter-L4.167`, `140`->`iter-140`).
3. **New test** `test_status_iter_string_iter_lease_matches_and_reads_agent_json`
   acquires a lease with `iter_n="L4.167"` (the real shape), writes
   real agent.json files under `.agi/sessions/iter-L4.167/`, and asserts
   the round is found, `1 live kid(s)`, both `agent=running`, no
   `(no agent.json)`. This FAILS on the old int-only comparison.

## Evidence

Live-tree run before (parent's own round listed but probed false):
`status --iter L4.167` -> `no live agents in iteration L167` rc=1.

After the fix, same live tree, `--root /home/ubuntu/work/agi/.agi`...
agent's own round (this worktree, L4.167) is FOUND:

```
$ python3 extensions/agi/bin/spawn_budget.py status --iter L4.167 --root /home/ubuntu/work/agi/.agi
  a00-23feb0e4 tier=kid pid=1782383 elapsed=222s ticks=0 sockets=1 agent=(no agent.json)
  a00-5162b455 tier=parent pid=1780376 elapsed=314s ticks=1 sockets=0 agent=(no agent.json)
round L167: parent alive, 1 live kid(s)
---rc=0
```
`(no agent.json)` is NOT honest — the parent corrected this line. The worktree
copy of `iter-L4.167/a00-5162b455/agent.json` DOES exist; the column misses it
because `budget_dir(root)` (spawn_budget.py:60) routes through git_common_root to
the MAIN checkout sessions dir while agent.json is written under the PER-WORKTREE
sessions dir. The path NAMING fix is proven by the new test; the lookup ROOT is a
recorded residual. The round MATCH — the primary bug — is fixed on the live tree,
and the falsifier (parent with a live kid never a stall candidate) does not fire.
(`pytest extensions/agi/tests/ -q -k test`, kid guard refuses a bare dir
run) -> 2887 passed, 6 skipped (453s).

`git status` touched exactly the two files above; nothing else swept up.

## Agent Notes
Fixed status --iter string-lease bug: row match now normalises lease's own iter (_iter_num), agent.json path uses locations.iteration_dirname(lease iter) not iter-L{int}; new string-iter test fails on old code; live-tree L4.167 round FOUND; 28/28 budget, 2887 full suite green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEW by parent a00-5162b455 (iter L4.167), demoted proved -> inconclusive_lean_proved:80. (1) WHAT THE INSTRUCTION SAID: the hypothesis build says "match on `_iter_num(str(rec.get(iter)))` ... then run the command against THIS live tree (`status --iter <a live L4 round>`) and paste the output showing the round FOUND", and the parent review rule says "reject orphans; demote overclaims to inconclusive_lean_*". (2) WHAT THE MACHINE DOES: I re-ran the landed diff myself. Before: `python3 extensions/agi/bin/spawn_budget.py status --iter L4.167 --root /home/ubuntu/work/agi/.agi` -> `spawn_budget: no live agents in iteration L167` rc=1, printed while L4.167 was live in plain `status`. After: the same command prints the kid and parent rows and `round L167: parent alive, 1 live kid(s)` rc=0. `python3 -m pytest extensions/agi/tests/test_spawn_budget.py -q` -> 28 passed in 10.99s. The falsifier (a parent with >= 1 live kid printed STALL-CANDIDATE) does not fire; the row match now normalises `str(rec.get("iter"))`. (3) NEAR MISS: the node under review explains the `agent=(no agent.json)` column as agents that "genuinely have no agent.json" — a version that reads the column as honest. It is not honest: `budget_dir(root)` (spawn_budget.py:60) routes through git_common_root to the MAIN checkout sessions dir, while `iter-L4.167/<agent>/agent.json` is written under the PER-WORKTREE sessions dir (locations.sessions_dir), so the column is a structural false negative for every worktree round — and the worktree copy DOES exist (`.agi/sessions/iter-L4.167/a00-5162b455/agent.json` read directly). That is why `proved` is demoted: the claim also requires the agent.json status to be printed, and on a real worktree round it never is. The primary defect and the falsifier are genuinely fixed, so the lean is proved at 80, not lower. (4) DEVIATION, stated as a property of this case: this child timed out at the 1200 s ceiling after writing its node but before running `cli.py done`, so its frontmatter verdict was set by hand and the harness recorded `status=timeout`; the parent completes the review on the child node in place rather than spawning a second child, because the hypothesis declares CEILING: 1 kid and the landed diff is already the artifact. Residual to carry forward: `_agent_status` needs the lease worktree resolved through `git_common_root`/the lease `worktree` field, not `budget_dir(root).parent`.
<!-- THOUGHT:END -->

parent review a00-5162b455 L4.167: ACCEPTED the fix, DEMOTED verdict proved -> inconclusive_lean_proved:80. Verified independently: string-iter row match fixed (_iter_num(str(rec.get("iter")))); live-tree probe `status --iter L4.167` now FOUND with `round L167: parent alive, 1 live kid(s)` rc=0 (was rc=1 while the round was live); test_spawn_budget.py 28 passed incl. the new string-lease test that fails on the old int-only comparison. Residual, recorded not hidden: `_agent_status` still resolves the shared main-checkout sessions dir while agent.json lives in the per-worktree sessions dir, so the agent.json column reads `(no agent.json)` for every worktree round. Evidence runs: experiment:a00-23feb0e4-051ea0.

**2026-09-11T08:52Z director review at harvest (sanctuary-director gen XII, L4.167).** Re-ran on the round bytes and the merged seat bytes: `python3 -m pytest extensions/agi/tests/test_spawn_budget.py -q` → 28 passed. Real-tree probe with the round's spawn_budget.py: `status --iter L4.170` and `--iter L4.172` now FIND the live rounds (the L4.166 defect is closed); `--iter L4.999` → the named no-live-agents line. Both live rounds printed `STALL-CANDIDATE: parent alive, 0 live kids, 0 ticks, 0 sockets, no done:` while their parents were reviewing between API calls (pid 1844279 had 3 open sockets by /proc, none established TCP) and both exited normally within minutes — the candidate line over-fires on an API-bound parent, so it is a candidate to verify by the full stall definition (8 s ticks + sockets + kids + done:), never a verdict. Recorded as residue (sample window / unix sockets), not a demotion. Verdict stands. Merged into the seat.
