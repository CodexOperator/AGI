# sanctuary-director — L4 gen II slice (LIVE, session in progress)

Brief at `.agi/sessions/quorum/sanctuary-director.md` (gen I replaced it wholesale; it
carries the traps). This slice is the ledger and is written DURING the work.

## §0 State

| | |
|---|---|
| Seat | `.agi/worktrees/seat-sanctuary-director`, `seat/sanctuary-director@s2`, pushed |
| Me | `seat-sanctuary-director-68 [f84c57]`, tmux `agi-rc:@234` |
| Prime | `agi-c6 [cd7648]` @232 — 🔴 **address it as `agi-c6`, NOT `belam-S1-L4-I`**: that is the tmux WINDOW NAME and `SendMessage` bounces on it (measured this session). L3 prime @230 still alive and idle, never address it |
| Helper | `seat-sanctuary-helper-05 [3a4ed4]` @233, tip `8f8c40256`, NOT merged to season/s2 yet |
| Key | $7.87 of $15 at open, $1.00 floor untouched. Per-spawn keys bill ~$0.02/round — real burn is an order under the $3.00/round ceiling |
| Links | 1812 resolved, 0 broken · `write_guard check` silent, exit 0 |
| Suite | 2270 passed / 1 skipped (gen I, foreground, prime-cleared window). NOT re-run this session yet |

## §1 Plan

1. ✅ Verify inherited state from disk, not from the brief — done: L4.37 alive, helper busy,
   key read, prime address corrected.
2. ✅ **L4.06 CLOSED `proved`** — merged into the seat branch and pushed (`47e22a5a2`).
3. ✅ L4.39 minted, committed, pushed, dispatched — the follow-on L4.06's review found.
4. ⏳ Harvest L4.37 (`a00-bad8beca`, kid `a00-6b9a041c` returned `proved`, work staged,
   parent still running at ~19min). Its diff is ALREADY REVIEWED — see §2c.
5. ⏳ Take the helper's tip when its last round lands; merge BOTH into `season/s2` against
   the MERGE-BASE; suite ONCE in a prime-cleared window; `grid.py commit --all` THERE.
6. ⏸ L4.23 (ONE message router) — HELD, see §4. L4.05 — now UNBLOCKED (L4.06 landed), take
   it next. L4.40 (token counter) — queued behind L4.39, deliberately NOT bundled with it.

## §2 What landed

**L4.06 seeded and dispatched.** `hypothesis:l4-write-log-role-capture` under `goal:g13`,
sibling of L4.02's `l4-moral-written-by-carrier`. Claim = the assignment, 2-kid ceiling in
the node. Kid `a00-809c922f` returned `proved` (0.85) and its work is STAGED in the
parent's tree `a00-ea55a89f`; parent still running. Reviewed in the diff, not the report:
it threads `log_extra` through the three routines that reach `_log_write` from `write.py`
(`replace_payload`, `write_node`, `update_node`), adds `_log_provenance()` at
`write.py:892`, and merges into the EXISTING `extra` hook so the six base keys — built
before the merge, `sort_keys=True` — cannot be reordered. No second logging path. Correct
shape.

**Helper's L4.34/L4.36 reviewed and its debris fix verified in the bytes** (`b8c75c60f`):
0 occurrences of the pattern, paragraph intact, file still 58 lines, nothing truncated.

## §2c L4.37 reviewed AHEAD of its parent's verdict (so the harvest is not a bottleneck)

Kid `a00-6b9a041c`, `proved` (0.85). It reverses `sess_root` to the LOCAL worktree in
`dispatch.py` (~`:1064`), `cli.py` (`_session_root`) and `zoom.py` (~`:472`), and adds
`cli._legacy_fallback()` so a record that only exists in the main checkout — an in-flight
round, or a seat whose dirs predate the change — still resolves. Backward compatible by
construction.

**It honoured the one DO-NOT-MOVE constraint `goal:g17.13` named** and wrote a test
asserting it: the spawn budget STAYS on `shared_project_root`, because a tree-wide
concurrency bound that splits per worktree is not a bound.

**I ran the test file myself: 7 passed.** Including
`test_cli_done_from_a_worktree_resolves_the_main_session_record`, which asserts the OLD
routing and is still green through `_legacy_fallback`. `--numstat` says **68 insertions,
1 deletion, and the single deleted line is a comment header.** No assertion weakened,
removed or retargeted — checked, not assumed, because a round that reverses a rule is
exactly where a test gets quietly retargeted.

## §2b 🔴 REVIEW FINDING on L4.06 — accept the code, correct the record

The kid's THOUGHT says role and seat come from `AGI_ROLE`/`AGI_SEAT`, "already exported by
dispatch". **Half of that is false and I checked it rather than believing it.**
`AGI_ROLE` IS exported — `dispatch.py:707` and `:1394`. **`AGI_SEAT` is NOT.** Its only
occurrence in the whole `bin/` tree is help text at `dispatch.py:841` telling a human to
"Export AGI_SEAT=<name>". So for every dispatched agent, `seat` will be ABSENT in practice.

That is NOT a defect in the implementation — the claim required role/seat "when those are
resolvable" and absent-means-absent is exactly the specified behaviour, matching the
convention `node_writer.py:676` already documents. It IS an overclaim in the round's
written reasoning, and the reasoning is what a later reader trusts. Correct it in the node
at review; do not silently accept it, and do not demote the verdict for it.

Minor, non-blocking: `_log_provenance` re-derives role from the environment where
`node_writer._pick("role", "AGI_ROLE")` (`:728`) already does the same job for frontmatter.
Two resolvers for one fact is the shape this repo keeps paying to remove — worth one line
in the follow-on round, not worth reopening this one.

## §3 🔴 Where it stops / next command

Nothing is stopped. Four rounds live (`spawn_budget.py status`: L4.37 parent+kid, L4.38
parent+kid from the helper, L4.06 parent). Next command:

```
python3 extensions/agi/bin/spawn_budget.py status     # then harvest whatever has left it
git -C /home/ubuntu/work/agi/.agi/worktrees/a00-bad8beca status --porcelain   # BEFORE believing it empty
```

## §4 Judgement calls this session, recorded

1. **L4.05 is NOT a sibling of L4.06 — it is downstream of it.** `doc:l4-plan` §5.2 draws
   both as depending only on L4.02. But L4.05 (`links.py roles`, "name every node written
   by a role its schema does not admit") has nothing to read: `node_writer._log_write`
   (`node_writer.py:1110-1121`) builds every entry from six keys plus an optional `extra`
   dict, and **no caller passes an actor, role or seat** — read in two live entries in
   `.agi/sessions/write-log.jsonl`, not inferred. An L4.05 today reports nothing, and an
   empty-by-construction report reads as a clean bill of health. Recorded in the node's
   THOUGHT block; the prime accepted it into `goal:g17.1`.
2. **L4.25 is the HELPER's, already running** — `a00-f8c968ee`, branch
   `loop/hypothesis-l4b17-success-metrics...`, briefed at `dd1f9d343`. The prime's
   acknowledgement told me to run it; I checked the worktree list and the outstanding keys
   first and did not double-dispatch. **Check `git worktree list` and `provisioning.py
   status` before taking any round named to you second-hand.**
3. **L4.23 HELD, not dropped.** It is unblocked (dep L4.22 landed) and needs no owner go,
   but it rewrites `send.py`, which is how this seat reaches the prime at all, and four
   rounds are already live. Holding it until one lands is not idleness — stacking five
   reviews is how a round gets rubber-stamped. Take it once L4.37 or L4.06 is harvested.

## §4b Merge plan, computed in advance rather than discovered during the merge

🔴 **THE TWO SEATS HAVE DIFFERENT MERGE-BASES WITH `season/s2`.** Mine is `aafb4be0a`;
the helper's is `e7883b4e4`, older. Diff each branch against ITS OWN base or you will
misread what either seat is adding (mine 7 files, the helper's 60).

Conflict surface, checked file by file:
- **`GOALS.md` — the only conflict.** Both regenerate it. DERIVED: `snapshot-goals.py
  --render`, then `--render --check`. Never hand-resolved (gen I's v69).
- **`extensions/agi/bin/dispatch.py` — both sides touch it and it is CLEAN.** Same base
  blob `8437e8fd5`. Helper's hunk is at ~`:900` (L4.11's parent-tier `--prompt-file`
  refusal); L4.37's is at ~`:1064` (`sess_root`). 164 lines apart, no overlap.
- Verified `season/s2` carries NEITHER yet: `grep -c l4b23-promptfile-drop` on its
  `dispatch.py` returns 0, and `:1075` still reads
  `sess_root = locations.shared_project_root(root) or root`. Both are clean adds.
- Everything else is disjoint.

## §5 Verification sequence (known good, in this order)

```
python3 extensions/agi/bin/links.py links            # 0 broken
python3 extensions/agi/bin/write_guard.py check      # silent, exit 0
python3 extensions/agi/bin/snapshot-goals.py --render --check   # after ANY goal write
git commit && git push                               # GATE each on the last (gen I's v69 lesson)
```
🔴 `grid.py commit --all` REFUSES on a seat branch. It runs on `season/s2` only, after the
merge. Never pass `--allow-branch`.
