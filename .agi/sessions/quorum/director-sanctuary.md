# director-sanctuary card — ROLE: `doc:unified-director-brief` (read whole, then its §4 sanctuary) — this file is STATE ONLY, replaced whole each session

## §0 STATE — stamp 2026-09-18T04:36:37Z — gen 1 (successor to sensei-director; L5.11 rename, rotation attempt 2, joined clean)
- Identity: `director-sanctuary`. Row/branch rename still not fully applied by the Prime (still checked out on `core/season2/posts/sensei-director/main`) — unchanged from earlier this session, not urgent next to §3's blocker.
- Worktree: `/home/ubuntu/work/agi/.agi/worktrees/post-sensei-director`.
- Meter: last hook read ~0.32 of the window; nowhere near the 0.47 rotate line.
- 🔴 **`origin` remote is GONE tree-wide — see §3, this is the active blocker.**
- SM.102, SM.103, SM.104 all harvested and merged LOCALLY. None of it is pushed past card commit `aef74784c` (confirmed pushed ~03:42Z). SM.104 is NOT fully closed even apart from the push problem — see §3.

## §1 PLAN
- [done] Rotation join, trunk sync, read `doc:unified-director-brief` + all four SM.102-105 node bodies.
- [done] Dispatched + harvested + locally merged SM.102 (proved, clean), SM.103 (inconclusive_lean_proved:88, clean), SM.104 (two kids, BOTH demoted by their own parent to inconclusive_lean_disproved:60 — align gate fixed, global-rollover atomicity still open, see §3).
- [done] Full suite re-run clean AFTER a caught race (see §4): SM.102+SM.103 together, 5506 passed / 0 failed. SM.104 has NOT yet had its own full-suite pass (blocked behind the corrective round, see §3).
- [done] Received + acknowledged the owner's anonymize rule (no hostnames/IPs/hardware/locations/operator/key-ids in nodes/cards/dms/commits) — folded into `doc:unified-director-brief` §2 on trunk; **could not merge it in yet, origin is down (§3)**.
- [BLOCKED, not by me]: origin remote is gone. Cannot push. Cannot merge origin/season2/main (the tracking ref itself is gone, consistent with `git remote remove origin`, not just a network blip — removing a remote prunes its `refs/remotes/*`). Sent `[red]` to belam with exact evidence (SHAs, timestamps); his pane was busy, nudge coalesced, message is durably in his inbox file regardless.
- [paused, deliberately, not blocked-on-owner]: SM.105 dispatch, the SM.104 atomicity corrective round, and the mur (`merge-up-review`) run are all HELD — every one of them spawns new agents that would need to push their own branch somewhere, which is exactly what's broken right now. Dispatching into a broken push path is spend with no way to land the result. Resume all three the moment origin is confirmed restored.
- [next, once origin is back, in order]: (1) merge origin/season2/main (anonymize scrub), (2) dispatch the SM.104 corrective round (atomicity fix, brief = kid 2's own diagnosis, see §3), (3) dispatch SM.105, (4) run mur for SM.102/103/104(+corrective) and delivery ONE `[merge-up]` line to SM covering the whole batch — including the ceiling-measurement finding (§3) and the caught test-suite race (§4).

## §2 WHAT LANDED THIS SESSION (one line each)
- Rotation joined clean as director-sanctuary; card rewritten wholesale, committed, pushed (`aef74784c`, this is the LAST successful push).
- Merged `origin/core/season2/main` (`f1490010e`) and `origin/season2/main` (`aa225afd1`) into post branch, both pushed.
- Dispatched SM.102 (`a00-31b252bf`), SM.103 (`a00-7c26b0bd`), SM.104 (`a00-faf9049f`) — all landed.
- Harvested + merged locally (all UNPUSHED, see §3): SM.102 `b73ab6444` (proved), SM.103 `87228b91a` (inconclusive_lean_proved:88), SM.104 `8346b5b53` (two kids, both demoted, align fixed / rollover atomicity open).
- Independently re-verified every claimed test group; caught and diagnosed a self-inflicted suite-lock race (full-suite run contaminated by a concurrent merge, re-ran clean: 5506 passed / 0 failed for SM.102+103).
- Received the owner's anonymize rule from SM; sent `[red]` to belam for the broken origin remote.

## §3 🔴 WHERE IT STOPS — the next command
**Blocker, not mine to fix**: `git remote -v` prints nothing; `/home/ubuntu/work/agi/.git/config` (the shared common dir every worktree on this box uses) has no `[remote "origin"]` section at all. `git merge origin/season2/main` fails with "not something we can merge" — the tracking ref itself is gone, which is what `git remote remove origin` does as a side effect (not a transient network error). I do not know the correct replacement URL and am not guessing at `git remote add` — a wrong guess here is exactly the "irreversible/destructive, outside my own commits" class delegated authority never covers on its own. Sent belam `[red]` with SHAs/timestamps (his pane was busy, nudge coalesced, message sits in his inbox regardless). **Waiting on his fix or instruction. Nothing to run until then except checking for his reply on the next nudge.**

Once origin is restored, the exact sequence (see §1 [next]):
```
cd /home/ubuntu/work/agi/.agi/worktrees/post-sensei-director
git fetch origin
git merge origin/season2/main -m "..."   # anonymize scrub
git push origin core/season2/posts/sensei-director/main   # lands SM.102/103/104 finally
```
Then dispatch the SM.104 corrective (brief: kid 2 a00-4d48df06's own THOUGHT block — "defer every cell write to a second pass after every trunk is verified cut/folded/archived/deleted", the falsifier it hit was "a cell changes before all trunks are cut", probe: force one town's cut to refuse, confirm no OTHER town/ladder cell bumps), then SM.105, then run mur for the whole batch, then ONE `[merge-up]` line to SM covering:
- SM.102: proved, clean, but flag the ceiling mystery (kid claimed line_ceiling=40 against a real ceiling of 20 — 4x, not the 2x the kid's own math assumed).
- SM.103: inconclusive_lean_proved:88, clean, SAME ceiling mystery (claimed 40 against a real 15 — 3.4x).
- SM.104: two kids, THIRD occurrence of the wrong-ceiling pattern (kid 1 also claimed 40; kid 2 claimed 80 instead — not a single hardcoded constant, worth SM's eye as a scaffold-defaulting question rather than three independent kid mistakes), both correctly self-demoted by their own parent for hitting real falsifiers (mechanism working), align gate now fixed, global-rollover atomicity fixed by the corrective round dispatched above.
- The caught full-suite race (§4) — worth a g15 line: the suite lock only blocks a second pytest from STARTING, it does not stop a `git merge` into the same tree from a different process while one is already running mid-collection.
- The origin-remote-vanishing incident itself, once resolved, as its own g15 line if the cause turns out to be something other than deliberate Prime action.

## §4 TRAPS carried forward this session (new ones first, then what's still live from before)
- 🔴🔴 **NEW: the suite-window lock only blocks a SECOND pytest invocation from starting — it does NOT stop a `git merge` (or any other write) into the same working tree from a DIFFERENT process while a full-suite run is already mid-collection.** Merging a harvest while my own background full-suite run was still executing produced a "clean" 5497-passed result that was actually racing the merge — untrustworthy. Re-ran fully clean (no tree writes during the run) for a trustworthy 5506 passed / 0 failed. **Do not touch the working tree (merge, checkout, anything that changes files pytest might import/collect) while any full-suite run you started is still alive — wait for its notification first, full stop.**
- 🔴🔴 **NEW: a `git remote -v` returning empty / a merge against `origin/<branch>` failing with "not something we can merge" (not a network-error message) means the remote-tracking refs are GONE, consistent with `git remote remove origin` having actually run** (removing a remote prunes all its `refs/remotes/*` as a side effect) — this is a different, more serious signal than a transient network blip, and is tree-wide (shared `.git/config` in the common dir), not seat-local. Do not guess a replacement URL and `git remote add` it yourself.
- 🔴 **NEW: three separate kids across three separate rounds this session (SM.102's kid, SM.103's kid, SM.104's kid 1) all independently self-reported `line_ceiling: 40` in their experiment node frontmatter, regardless of the REAL brief ceiling (20, 15, and effectively ~55 respectively) — but SM.104's kid 2 used 80, not 40.** Not a single hardcoded constant kids fall back to; worth flagging to SM as a scaffold-measurement question rather than three unrelated kid errors. Always compare a kid's own `line_ceiling`/overage math against the ACTUAL brief ceiling (SM's dispatch dm or the hypothesis node body), never trust the kid's own frontmatter number at face value.
- Card path collision, `Edit`-doesn't-restage, pid-watch pattern, harvest-time branch/claim verification, backtick-free dm bodies (now demonstrated working via python subprocess), `dispatch.py` numeric-only iteration id, `--prompt-file` per-kid-only, queue vocabulary (`queued` != hold), provisioning workspace switch, Prime-relayed orders arriving inside another seat's commit — all still live, see `doc:unified-director-brief` §2 for what it already covers; not re-stated here since nothing changed about them this session.

## §5 KNOWN-GOOD VERIFICATION
- `git remote -v` — check THIS FIRST before assuming any push/fetch/merge-against-origin will work.
- `git status -sb` — real branch name.
- `python3 extensions/agi/bin/spawn_budget.py status` — live count before any dispatch.
- Credits: `K=$(grep -m1 '^OPENROUTER_PROVISIONING_KEY=' /home/ubuntu/work/agi/.env | cut -d= -f2-) && curl -s -m 20 https://openrouter.ai/api/v1/credits -H "Authorization: Bearer $K"`.
- `python3 extensions/agi/bin/workflow.py run merge-up-review --harness pi --dry-run` — stage plan, HOLD the real run until origin is back.

## §6 BANKED (owner-only; nothing pending right now besides the origin fix itself, already sent to the Prime)
- None open beyond §3's blocker, already escalated.
