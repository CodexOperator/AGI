# director-sanctuary card — ROLE: `doc:unified-director-brief` (read whole, then its §4 sanctuary) — this file is STATE ONLY, replaced whole each session

## §0 STATE — stamp 2026-09-18T03:41:51Z — gen 1 (successor to sensei-director; L5.11 rename, rotation attempt 2, joined clean)
- Identity: `director-sanctuary`. Inbox/send.py now resolve correctly under the new name (confirmed via live nudge + `send.py read`). Row/branch rename NOT fully applied yet: still checked out on `core/season2/posts/sensei-director/main` (`git status -sb` is the source of truth, never card prose). Rotation record shows 54/64 rename surfaces auto-applied at join (logs, acks, dm logs, card, inbox); the remaining 10 (worktree-dir move, branch renames, tmux window/session) are explicitly the Prime's own follow-up ("verifies tmux + whois") — confirmed pending, not blocking, not mine to force.
- Worktree: `/home/ubuntu/work/agi/.agi/worktrees/post-sensei-director` (old path, still live and functional — do not assume the renamed path exists yet).
- Meter: last hook read 0.1513 of the window several tool-calls back (rising since); nowhere near the 0.47 rotate line.
- Live (mine): 3 parents, dispatched clean this session, pi/deepseek-v4.1-flash, no file overlap —
  - SM.102 `a00-31b252bf` pid 2341596 branch `season2/loops/hypothesis-l4-the-formation-owne-a00-31b252bf`
  - SM.103 `a00-7c26b0bd` pid 2342222 branch `season2/loops/hypothesis-l4-a-named-env-key-re-a00-7c26b0bd`
  - SM.104 `a00-faf9049f` pid 2343876 branch `season2/loops/hypothesis-l4-a-town-season-roll-a00-faf9049f`
  - Background pid-watch running (task `b4il31qlv`), breaks on first completion, one notification.
- Not mine: TM.29 (thought-master's own parent+kid) — leave alone, uses the 4th fleet slot.
- Credits at last read: 65 total / 23.76 used (~$41 headroom). Re-read fresh before dispatching SM.105.

## §1 PLAN
- [done] Rotation join; merged trunk TWICE (town `core/season2/main`, then global `season2/main` ladder — both hit stale-base independently, both fixed); read `doc:unified-director-brief` (now the ROLE doc — supersedes this card's old §0-§2 prose, which is deleted, not restated) and all four SM.102-105 node bodies in full.
- [done] Dispatched SM.102 + SM.103 + SM.104 together per the owner's batching rule (`doc:l5-owner-decisions` 086f687f9): sanctuary's fleet share is 3 of 4 live parents (thought holds 1); independence = no file overlap, confirmed (write.py+schemas / dispatch-env-seam+config.json / season.py+helpers).
- [next] Harvest each as it lands (see §3 for the exact sequence). **NEW process, owner ruling on `goal:g17.1` (relayed by SM 01:52Z): I now run `workflow.py run merge-up-review` myself before reporting** — not SM. Any `[red]` the review finds is mine to fix in-loop before delivery, never sent up unresolved. Deliver ONE `[merge-up]` line per landing (or one batch line, my call) = branch tip sha + merge-base sha + files/tests numbers + mur run key + per-slice verdicts + one proposed g15 line per finding.
- [queued, not a hold] SM.105 (workflow slice isolation + 3600s wall/extension) — drains automatically once one of the 3 above lands and a slot frees. Per the brief's queue vocabulary: `queued` is never a hold; nothing here needs SM's re-confirmation to proceed.
- [STOP condition — owner ruling, msg 03:16Z verbatim]: once SM.102, SM.103, SM.104, SM.105 all land on `core/season2/main` with every review residue closed (fixed in-loop or demoted with the measured reason) — **no new rounds, no new nodes, idle at card.** Do not self-start the old pre-rotation backlog (spawn-budget-meter-wait ceiling 45, heal-loop disk guard ceiling ~130, author-composes-repeat-then-global-stages) without a fresh order; they are effectively banked by this ruling, not cancelled.

## §2 WHAT LANDED THIS SESSION (one line each)
- Rotation joined clean as director-sanctuary (this is attempt 2; attempt 1's rc=2 refusal belongs to the predecessor's session, already reported to belam then).
- Merged `origin/core/season2/main` into post branch — 62 files, clean, no conflicts — pushed `f1490010e`.
- Merged `origin/season2/main` (global ladder trunk, separate stale-base hit) — 6 files, clean — pushed `aa225afd1`.
- Read `doc:unified-director-brief` + SM.102/103/104/105 node bodies whole.
- Dispatched SM.102, SM.103, SM.104 (all rc=0 after the trunk syncs).

## §3 🔴 WHERE IT STOPS — the next command
Waiting on the background pid-watch (task `b4il31qlv`; pids 2341596 / 2342222 / 2343876) for the FIRST of SM.102/SM.103/SM.104 to finish. On that notification, per round:
```
cd /home/ubuntu/work/agi/.agi/worktrees/post-sensei-director
git fetch origin
git branch -a | grep -i <slug fragment of the finished round>
MB=$(git merge-base HEAD <branch>); git diff --stat "$MB" <branch>
<read every kid node the round produced — grep THOUGHT:BEGIN count <= 1 each>
git merge --no-ff <branch> -m "<msg>"
<run the round's own test file + its FILE SCOPE neighbourhood>
<if the round touched a shared/cross-cutting file (write.py for SM.102 counts), run the FULL suite before trusting green>
python3 extensions/agi/bin/workflow.py run merge-up-review --harness pi --dry-run   # inspect the resolved args/stage plan FIRST, this is a brand new process for this seat
python3 extensions/agi/bin/workflow.py run merge-up-review --harness pi --args '<resolved>'
<fix any [red] finding in-loop: own g15 fix round, or demote the verdict with the measured reason — never send it up unresolved>
git push origin core/season2/posts/sensei-director/main
<send.py send sanctuary-master with the ONE [merge-up] line — body via scratch file + python subprocess, see §4>
```
Once one of the 3 lands and a slot frees: re-check `spawn_budget.py status`, re-read credits fresh, dispatch SM.105 (`hypothesis:l4-a-failed-repeated-stage-slice-never-aborts-its-siblings-and-a-manifest-stage-carries-its-own-timeout`) as the next round id after SM.104.

## §4 TRAPS carried forward (only what `doc:unified-director-brief` does NOT already cover)
- Card path collision: this worktree's card and the root checkout's file at the same relative path are DIFFERENT content — always the full worktree-prefixed absolute path for Read/Write/Edit here.
- `Edit` does not re-stage a file already `git add`-ed before the edit — re-`git add` immediately before any commit that follows an Edit on an already-staged path.
- pid-watch (`run_in_background` + `kill -0` loop + `sleep 30`, break on count-drop) is the sanctioned way to wait on a live round — confirmed working again this session. Never `ScheduleWakeup` / the `/loop` dynamic-wakeup mechanism here — this seat is not a `/loop` session and that sentinel fights this card's own protocol.
- Harvest-time: verify every claimed file against the branch diff individually (a claimed deliverable can simply not exist on the reported branch); a harvest's real work can live on a KID-named branch even when the parent branch shows nothing (`git branch -a | grep <slug>` for siblings); a kid node can read as an empty template immediately post-merge — re-read after the actual `--no-ff`, not before; a full-suite run (not just the neighbourhood) is required for any round touching a shared/cross-cutting file — a green narrow run does not prove the wire is connected (measured directly this rotation on a prior round, not this one).
- **NEW, supersedes the old apostrophe-workaround**: per the unified brief, dm/note bodies are now BACKTICK-FREE and never carry `$(` — write the body to a scratch file and pass it via a python subprocess, not raw single-quoted shell text.
- `dispatch.py`'s iteration id is numeric-only after the dot. `--prompt-file` is per-kid only and never reaches the parent's own brief — the target node's body IS the parent's brief; a direct dm to the parent's agent id is the only other channel that reaches it.
- Queue vocabulary (brief §2, precise, new this session): `minted` = node exists; `queued` = minted + in my queue, I drain it myself at stated priority whenever a slot is free, **never a hold**; `[decision] hold <node>` is the ONLY hold phrase; `dispatch now <node>` is the ONLY phrase ordering an immediate jump; `dispatched` = a live parent round exists.
- Provisioning workspace can switch mid-session (mint 403 "Workspace not found") — Prime-only fix, report `[red]` with the exact line, never hand-edit `.env`/config.
- A Prime-relayed order can arrive first as a line inside another seat's own card commit or node note — skim unfamiliar commit subjects during every trunk merge.
- The rotation-boundary bugs this session's join actually hit (rename-post staged-plan drift, after_join grepping the old post name, pin racing an early poll before the successor's first reply) are now all tracked as fresh `l5-*` `goal:g15` hypothesis nodes already on trunk (arrived via my own two merges) — informational, someone else's (director-belam's) round, not mine to chase.

## §5 KNOWN-GOOD VERIFICATION
- `git status -sb` — real branch name, never card prose.
- `python3 extensions/agi/bin/spawn_budget.py status` — live count + whose iter, before any dispatch.
- Credits: `K=$(grep -m1 '^OPENROUTER_PROVISIONING_KEY=' /home/ubuntu/work/agi/.env | cut -d= -f2-) && curl -s -m 20 https://openrouter.ai/api/v1/credits -H "Authorization: Bearer $K"` — absolute path, whole-account pool.
- `python3 extensions/agi/bin/workflow.py run merge-up-review --harness pi --dry-run` — see the resolved stage plan before spending on a real mur run.
- `python3 extensions/agi/bin/workflow.py list` / `status` — registered workflows, recent run keys.

## §6 BANKED (owner-only; nothing pending right now)
- None open. The old pre-rotation backlog (§1 above) is parked by the owner's finish-set-then-stop ruling, not escalated.
