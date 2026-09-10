# sanctuary-director — L4 gen II slice (LIVE, session in progress)

Brief at `.agi/sessions/quorum/sanctuary-director.md` (gen I replaced it wholesale; it
carries the traps). This slice is the ledger and is written DURING the work.

## §0 State

| | |
|---|---|
| Seat | `.agi/worktrees/seat-sanctuary-director`, `seat/sanctuary-director@s2`, pushed |
| Me | `seat-sanctuary-director-68 [f84c57]`, tmux `agi-rc:@234` |
| Prime | **`agi-64 [61b9c9]` @235 = belam-S1-L4-II** (rotated in ~02:4xZ; verified by joining `tmux list-windows` @235 against its `ListAgents` row myself, not taken from its own message). 🔴 **address it as `agi-64`, NOT `belam-S1-L4-II`** — a tmux WINDOW NAME is not a SendMessage address and bounces (measured on L4-I). 🔴 **Two idle predecessors that read nothing: `agi-c6` @232 (L4-I) and `agi-05` @230 (L3). Never address either.** |
| Helper | `seat-sanctuary-helper-05 [3a4ed4]` @233, tip `8f8c40256`, NOT merged to season/s2 yet |
| Key | $7.87 of $15 at open, $1.00 floor untouched. Per-spawn keys bill ~$0.02/round — real burn is an order under the $3.00/round ceiling |
| Links | 1812 resolved, 0 broken · `write_guard check` silent, exit 0 |
| Suite | 2270 passed / 1 skipped (gen I, foreground, prime-cleared window). NOT re-run this session yet |

## §1 Plan

1. ✅ Verify inherited state from disk, not from the brief — done: L4.37 alive, helper busy,
   key read, prime address corrected.
2. ✅ **L4.06 CLOSED `proved`** — merged into the seat branch and pushed (`47e22a5a2`).
3. ✅ **L4.39 CLOSED `proved`** — merged and pushed. Found a spend hazard in review, §2d.
4. ⏳ Harvest L4.37 (`a00-bad8beca`, kid `a00-6b9a041c` returned `proved`, work staged,
   parent still running at ~19min). Its diff is ALREADY REVIEWED — see §2c.
5. ⏳ **Helper is CLOSED and holding — final tip `a6d8ec28c`, pushed.** L4.38 proved.
   Merge BOTH seats into `season/s2` against their OWN bases (they differ), suite ONCE in a
   prime-cleared window (asked for), `grid.py commit --all` THERE, push. **Only L4.37
   blocks this.**
6. ✅ **L4.05 CLOSED `proved`** — merged, pushed. The coverage census IS the finding.
7. ✅ **Owner instruction landed** (prayer scope) — all three director briefs, see §2e.
8. ⏳ **L4.42 DISPATCHED** — silent data loss in `write.py replace`, see §2f. Ahead of
   L4.40/L4.41 because losing bytes outranks a wrong error string.
9. ⏸ QUEUED, in this order, all owner-GO: **L4.40** (refusal message names the TYPE and the
   admitted roles; list shape for `written_by`) → **L4.41** (role resolution per the Prime's
   ruling) → the `[config]`/`[vision]` FLIP, only after L4.41's tests prove both branches.
   L4.23 (message router) still held. Token counter still queued.

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

## §2g Pre-verified for L4.41 so the round does not rediscover it

**The Prime's role-resolution design IS implementable — `config:seats` carries `role`.**
Checked in `.agi/nodes/.geometry/seats.md`: `belam` → `prime_director`, `sanctuary-director`
→ `director`, `sanctuary-helper` → `director`, `sanctuary-master` → `director`. So
`actor="belam-S1-L4-II"` resolves through the row named `belam`.

🔴 **Hazard to put IN L4.41's claim: LONGEST prefix must win, and an ambiguous match must
REFUSE.** A naive `startswith` scan over the rows picks whichever row it reaches first. No
pair collides today, but `belam` + a future `belam-S1` would, and the failure would be a
silent mis-resolution to the wrong role — which on a fail-closed gate means either a lockout
or a bypass, depending which way it lands.

**Also settled by that read:** once `[config]` admits `[owner, prime_director]`, this seat
(`role: director`) can no longer write config nodes. That is correct and already this seat's
standing rule — never write `config:seats`, bank it for the Prime — so the flip encodes an
existing constraint rather than imposing a new one.

**L4.40 is HELD behind L4.42, deliberately.** Both edit `submit()` — L4.42 at the replace
splice (`:616-625`), L4.40 at the `_enforce_written_by` call (`:555`). Well under a hundred
lines apart, in ONE function that gates every write in the system. Two concurrent rounds
there is the one merge I do not want to hand-resolve.

**Not a defect, checked and dropped:** `spawn_budget.py status` briefly listed a dead pid
after L4.05's parent exited. The leases (`.spawn-budget/*.lease`) self-clean; a later read
showed all four entries live. A transient race between exit and lease release, not
over-reporting. Recorded so it is not chased twice.

## §2f 🔴🔴 `write.py replace` SILENTLY DELETES THE RANGE VIA THE PYTHON API

**Measured on a real payload in this repo, not theorised.** `verb_replace(e, "payload",
"26:26", <path>)` then `submit(...)` returned `status='updated' payload_changed=True` while
`git diff --numstat` read **`0 1`** — zero insertions, one deletion. Caught ONLY by greping
the bytes afterwards (trap 0ah). `git checkout --` restored it; the edit then landed through
an explicit `e.replace_text`; nothing was lost.

**Cause:** `verb_replace` (`write.py:329-355`) records `edit.replace_from` and nothing else.
The ONLY code turning it into `edit.replace_text` is `main()` at **`:1184-1191`** — the CLI
path. `submit` (`:616-625`) splices `edit.replace_text`, still `""` for an API caller, and
`_splice_range` (`:700-727`) faithfully splices nothing.

🔴 **IT IS A LOADED GUN IN THIS VERY BRIEF.** The brief says drive the Python API for long
prose (the script form splits on the doubled ampersand) AND names `replace` as the
partial-write verb. **Following both instructions destroys the range.**

**UNTIL L4.42 LANDS:** use the CLI form, or set `e.replace_text` explicitly. **Grep the
bytes after every replace regardless.** The helper's line-51 fix used the CLI form and is
NOT affected — checked, and it was told so rather than left to wonder.

## §2e Owner instruction, 2026-09-09 — the prayer closes a SESSION, not a turn

Verbatim: *"You don't have to do a prayer at the end of each turn, only at the end of your
session when you rotate or have no other actionable items left."*

Landed in **all three** director briefs, because the default is the durable home but the
quorum files are what the running seats actually read:
`extensions/agi/briefs/prime-director-successor.md:26` (the overall default, edited as the
payload of `build:briefs-prime-director-successor`) · `quorum/sanctuary-director.md` ·
`quorum/sanctuary-helper.md`.

The default brief and `skills/agi/SKILL.md:176` **already said "session"**; the two quorum
briefs said *"the literal last tokens YOU EMIT"*, which reads as every turn — that
ambiguity is why it was being done every turn. 🔴 **Carry this into any brief you write for
a successor.**

## §2d 🔴 `--seat` IS NOT A FREE WAY TO POPULATE `AGI_SEAT` — it changes the MODEL

Found reviewing L4.39, missed by both the kid and the parent. Two `--dry-run` invocations
differing ONLY by that flag:

```
with    --seat sanctuary-director  ->  AGI_MODEL=claude-opus-5      AGI_SEAT=sanctuary-director
without --seat                     ->  AGI_MODEL=~z-ai/glm-flash-latest   (no AGI_SEAT at all)
```

That is `--seat` working exactly as documented — the seat's row in `config:seats` overrides
harness/model/effort/settings from the ladder's (tier, role) class table. The consequence is
new only because L4.39 gives a **provenance** reason to reach for the flag. Add `--seat` to a
routine parent dispatch so the `seat` key lands and you have silently moved that dispatch
from a flash-class model to Opus, at a multiple of the cost, meaning only to fill a log field.

🔴 **THE CHEAP PATH, which L4.39 built on purpose:** `export AGI_SEAT=<name>` in the
DIRECTOR's own environment and dispatch **without** `--seat`. `_resolved_seat`'s inherited
branch carries it to every child and leaves model selection alone. Recorded in
`experiment:a00-c1445c42-213b7d`.

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
