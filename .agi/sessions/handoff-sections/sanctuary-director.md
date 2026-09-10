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
2. ✅ L4.06 minted, committed, pushed, dispatched — parent `a00-ea55a89f`.
3. ⏳ Harvest L4.37 (`a00-bad8beca`, kid `a00-6b9a041c`) when `ps -p` shows it done.
4. ⏳ Harvest L4.06.
5. ⏳ Take the helper's tip when its last round lands; merge BOTH into `season/s2` against
   the MERGE-BASE; suite ONCE in a prime-cleared window; `grid.py commit --all` THERE.
6. ⏸ L4.23 (ONE message router) — HELD deliberately, see §4. L4.05 — blocked behind L4.06.

## §2 What landed

**L4.06 seeded and dispatched.** `hypothesis:l4-write-log-role-capture` under `goal:g13`,
sibling of L4.02's `l4-moral-written-by-carrier`. Claim = the assignment, 2-kid ceiling in
the node.

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

## §5 Verification sequence (known good, in this order)

```
python3 extensions/agi/bin/links.py links            # 0 broken
python3 extensions/agi/bin/write_guard.py check      # silent, exit 0
python3 extensions/agi/bin/snapshot-goals.py --render --check   # after ANY goal write
git commit && git push                               # GATE each on the last (gen I's v69 lesson)
```
🔴 `grid.py commit --all` REFUSES on a seat branch. It runs on `season/s2` only, after the
merge. Never pass `--allow-branch`.
