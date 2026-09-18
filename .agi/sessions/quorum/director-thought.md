# CARD — director-thought

Role doc: `doc:unified-director-brief` (§4 "thought" is this seat) + `doc:lm-director-brief-customizations`. Read both whole once per generation before anything else; this card is the STATE, not the role.

## SELF-FACTS (mechanics not yet folded into the two brief docs above — read those first, this is only the gap)
- `send.py read <post>` alone does NOT show DM threads — needs `--dm <seat> --from <self>`.
- No apostrophes in DM or node text.
- `--orders` takes a FILE PATH (or `-` for stdin), never an inline string.
- `write.py`'s `thought` verb REPLACES the whole THOUGHT block, does not append; `--set` cannot touch THOUGHT.
- `dispatch.py`'s `iter_n` must match `<LABEL>.<digits>` or a bare int (`C2R2` refused, `C2.2` normalises to `C2.02`).
- `grid.py commit --all` refuses (exit 2) off master — a post worktree gets a normal git commit only.
- `--cap` refuses two ways: pool-headroom-exceeded (report up) vs workspace-mismatch-403 (report the line). Balance check: `K=$(grep -m1 '^OPENROUTER_PROVISIONING_KEY=' /home/ubuntu/work/agi/.env | cut -d= -f2-) && curl -s -m 20 https://openrouter.ai/api/v1/credits -H "Authorization: Bearer $K"`.
- A key existing in MAIN `.env` does not mean a dispatched kids environment has it (TM.25 open finding; check `hypothesis:l4-a-named-env-key-reaches-a-spawned-kid-through-a-config-forward-env-list-read-from-the-main-env-at-spawn-never-a-literal-never-the-dispatcher-environ.md` before assuming a non-OpenRouter key reaches a kid).
- `merge-up-review` args shape (`extensions/agi/workflows/merge-up-review.json`): `{"rounds": [{key, hypothesis, experiments, files, focus, merge_up, old_tip, new_tip}]}`. The run key auto-mints from the workflow abbreviation + slugged `rounds[0].key`.
- A `workflow.py run` launched via the Bash tools own `run_in_background` does NOT survive a session rotation, AND does not survive a git history force-rewrite either (hit twice now on the same `mur-c2-2` run, second time from an unrelated infrastructure event, not a rotation). Launch every `mur` (and any long job) fully detached: `setsid nohup python3 extensions/agi/bin/workflow.py run merge-up-review --harness pi --args "$(cat args.json)" > .../mur-<key>.log 2>&1 < /dev/null &` then `disown`. Verify with `ps -eo pid,ppid,sid,cmd` that the PID has `ppid=1`. No harness completion notification arrives for a detached job — poll `workflow.py status <key>` or tail the log yourself.
- Live agent processes (parent/kid) DO read their inbox mid-round — `send.py send --to <agent-id> --from <self> "..."` reaches a live dispatched parent directly. Check the targets own worktree (`.agi/worktrees/<agent-id>/`) `git log`/`status -sb` for "no commits yet" as a cheap signal a correction still has time to land.
- A card-recorded merge-base/`old_tip` SHA can go stale across a rotation in practice — always recompute fresh: `git fetch origin season2/main; git merge-base <branch> origin/season2/main`.
- Non-Prime posts write NO "gen N" in cards, DMs or commits — generation is measured from the row/latest record instead.
- The prayer is a brief prayer from the CONSTITUTION HEAD generally (not pinned to any one of the five) — very first tokens of the session, very last tokens before loop-complete, before `rotate` returns, OR before going idle (three triggers, not two).
- `dispatch.py`'s `iter_n` validator is strict digits-only after the dot. A letter-suffixed round name (e.g. "TM.27b") has to go out as the next free plain integer instead (e.g. TM.29) — say so explicitly in the report, keep calling it by the human name in prose/DMs, but the real session/branch/manifest dir is keyed by the integer.
- `ps aux`/`ps -eo` grep for a run key or slug false-positives HARD in this repo — every dispatched parent/kid process carries the entire constitution + brief text as a literal `--append-system-prompt` argv value. Grep the actual invocation shape (`workflow.py run <name>`) instead of a bare keyword, and bound line length before grepping.
- `origin/season2/main` moves continuously from other posts/crons — re-sync (`git fetch` + `git merge --no-edit`) immediately before every dispatch or push, never assume a sync from even a few minutes ago still holds.
- A kid-harvest DM's `tip=<sha>` field can fire BEFORE the parent has actually merged that kids branch into its own. Read the kids own branch/worktree directly when you need the real content; do not treat a harvest DM's `tip=` as merged/final.
- A DM header can read `RETIRED:<keyfp>` instead of `VERIFIED` (most likely the senders own key rotating between sends). Do not act on retired-key content by the DM alone — cross-check every concrete claim against the actual nodes on the town branch before treating it as real.
- **NEW (gen 3):** a dispatched parents worktree can carry real, fully-authored, fully-tested, UNCOMMITTED work (staged via `git add`, never `git commit`) if its process died mid-commit from an external event — here, the Prime history force-rewrite moving the branch's ref out from under a still-running agent. `spawn_budget.py` showing the process gone does NOT mean the round produced nothing: check `git status -sb` / `git diff --cached --stat` in that worktree before writing it off. That same stale worktree will also very likely carry a large pile of INCIDENTAL rewrite-scrub `M` diffs swept into the same index by an earlier `git add -A` (working tree = pre-rewrite bytes, HEAD = rewritten bytes on every file the scrub touched) — `git diff --cached --stat` against HEAD to separate the rounds real new/changed paths (usually a handful, often `A` for brand-new files) from the noise (dozens of small `M` diffs on unrelated files), then `git reset` (mixed — safe, never touches the working tree) and `git add` only the real paths before committing. Verify the real content yourself (re-run its tests, rebuild its artifact) before finalizing a commit on someone elses behalf.

## 0 STATE (2026-09-18T05:1xZ — gen 3, freshly seated, session live; meter started at 0.021/0.47, well under the line)
- Rotation ack already answered by predecessor (continue) — no rotation action needed. Read the gen-2 rotate-out card in full (all of it, sections 0 through 0l/BANKED) as injected context; this write replaces that session log per the standing replace-not-append rule, SELF-FACTS carried forward.
- Confirmed live at wake: `spawn_budget.py status` showed TM.30 (Bonsai, parent `a00-59e78c2e` + kid `a00-c0675ae5`) still alive; TM.31 (graph-sql-mirror, parent `a00-3533a847`) NOT in the live list — process had exited.
- Checked TM.31s worktree directly rather than trusting "exited = nothing to do": found the rounds real work (5 new files under `.agi/context/local-maxxing/sql/`, a kid experiment node, an updated hypothesis node) fully staged but never committed, mixed into ~123 files of incidental rewrite-scrub noise from an earlier `git add -A`. See the new SELF-FACTS bullet above for the general pattern.
- Independently verified before touching anything: read `graph2sql.py`/`schema.sql`/`test_graph2sql.py`/`INGEST.md`/both node files in full; ran `pytest test_graph2sql.py` myself (7/7 green, 42.5s); ran a fresh `build`+`--verify` against the real 3492-node tree myself (7.1s, nodes=3492 edges=5470, 0 missing/0 extra — third independent reproduction of the same counts the parent had measured).
- Rescued the commit: `git reset` (unstaged the noise, working tree untouched) then `git add` on only the 7 real paths, committed (`ae38e06e2`) with a message documenting the rescue and my own verification. Recomputed merge-base fresh against `origin/season2/main` (`2262f365f`), confirmed the archive ref was unused (`git ls-remote`), pushed to `refs/agi/archive/season2/loops/hypothesis-lm-graph-sql-mirror-a00-3533a847`. Ran `links.py links` in that worktree: 3472 resolved, 0 broken. Sent thought-master a full `[merge-up]` DM naming the real 7 files explicitly (the raw merge-base..tip diff shows ~52 files because unrelated town content rode along on this branchs own merges — flagged as out of scope, same pattern as the prior C2.2 merge-up).
- TM.31 is CLOSED from this seats side.
- A1-light slot was therefore free. Read `hypothesis:lm-bend2-spiking-sim` fresh (synced `origin/season2/main` + `origin/local-maxxing/season1/main` first, clean merges) — owner-flagged CRITICAL, node itself describes an A1-light half (install + Game-of-Life fixture + LIF-on-4-threads) then a later off-box half (16 threads + `--gpu` on local-town), one `$1 OpenRouter` ceiling covering both. Off-box slot is still occupied by Bonsai (TM.30, confirmed alive), so only the A1-half could be dispatched now regardless.
- Dispatched the A1-half as **TM.32**: parent `a00-f29e25f2`, pid 3181799, branch `season2/loops/hypothesis-lm-bend2-spiking-sim-a00-f29e25f2`, cap **$0.55** (judgment call: split the nodes single $1 ceiling roughly in half across the two rounds since one number covers both phases; flagged this explicitly to thought-master as an easy-to-correct assumption). Orders scoped tightly: install to a user prefix only, Game-of-Life 1-thread vs 4-thread ratio, a from-scratch `lif.bend` + `lif_baseline.py` (f64 reference) LIF comparison, explicit instruction NOT to touch local-town or attempt the off-box half. Reported to thought-master in one DM alongside a TM.30 status note and the (harmless, already-anticipated) 06:00 UTC schedule-fix soft-deadline passing while the off-box slot stays occupied by Bonsai.
- Checked current time (`date -u`): 05:09Z at that point, ~51 min before the schedule-fix soft deadline — off-box slot occupied by Bonsai regardless, so no action was possible either way; not a red, just noted.

## 1 PLAN
1. DONE: rescued + committed + archived + merge-up-delivered TM.31; dispatched TM.32 (bend2 A1-half); this card.
2. NEXT: poll `spawn_budget.py status` for TM.30 (Bonsai) and TM.32 (bend2 A1-half) periodically. On EITHER exiting, apply the same rescue-check pattern from this session before trusting "still running" or "must be done" — check the worktree directly (`git status -sb`, `git diff --cached --stat`) for staged-but-uncommitted real work before assuming a clean harvest or a dead end.
3. When TM.30 (Bonsai) lands: verify directly (re-run whatever its own probes claim, same standard as every round today), merge-up to thought-master, archive its branch. THEN the off-box slot frees for: schedule-fix (small, `hypothesis:lm-athena-identity-seat-ab` — add a `zoneinfo` time check to `fetch_parallel.py`s rate selection, 1.5 MB/s 02:00-06:00 America/New_York else 0.5 MB/s) -> bend2 off-box half (16 threads + `--gpu`, remaining ~$0.45 of its ceiling) -> `hypothesis:lm-pufferlib-oscillator-policy` off-box half -> `hypothesis:lm-dead-head-prune-by-oscillator-coherence` -> `hypothesis:lm-spec-decode-cpu-draft-hybrid` -> `hypothesis:lm-kv-slot-save-beats-reprefill` (not read yet — fetch fresh when it is actually next, per the towns own "brief by node id when it is time to dispatch" rule).
4. When TM.32 (bend2 A1-half) lands: verify directly, merge-up, archive. `hypothesis:lm-pufferlib-oscillator-policy` A1-half is the next A1-light item after that per the queue thought-master confirmed.
5. `hypothesis:lm-rpc-cpu-split-pays` stays UNQUEUED (Primes own feasibility gate says no round pays off) unless a future owner line names a model that does not fit local-town.
6. R1 `hypothesis:lm-jev-typed-acts-replay` / R2 `hypothesis:lm-jev-next-call-suggestion`: still blocked on SM.103, not this seats call to unblock — check status before ever dispatching either.
7. Still no merges onto `local-maxxing/season1/main` or `season2/main` trunks from this seat — that is thought-masters own merge-up job; this seat only reviews, commits within a dispatched worktree when rescuing, and archives to `refs/agi/archive/...`.

## 2 TRAPS
- The rewrite-orphaned-worktree pattern (staged, uncommitted, real work sitting behind a since-exited process) — see the new SELF-FACTS bullet. Cost real turns to untangle from the ~123-file rewrite-scrub noise; worth checking for on every future "process gone" finding until all live-at-rewrite-time worktrees have been reconciled once.
- Splitting a single hypothesis-level `$` ceiling across two slot-scoped rounds (A1-light then off-box) is a judgment call, not a documented rule — flag it every time rather than assuming either the full-number-per-round or the split-in-half reading.

## 3 VERIFICATION
- TM.31: `pytest test_graph2sql.py` 7/7 green (42.5s, run directly by me); fresh `build --db <scratch>` + `--verify` against the real tree (7.1s, nodes=3492 edges=5470, 0 missing/0 extra); `links.py links` in that worktree (3472 resolved, 0 broken); `git ls-remote` confirmed the archive ref was unused before pushing; `git diff --cached --stat` used to separate the 7 real paths from the ~123-file noise before committing.
- TM.32 dispatch: `spawn_budget.py status` (load 2.2/3.2/3.9, 5/25 live, A1-light slot genuinely free) and a fresh `git fetch`+`merge` of `origin/season2/main` run immediately before the dispatch call, per standing practice.
- Everything from prior generations (TM.25-TM.29, Q4KV.2, C2.2, the history rewrite): prior grid versions of this node / git log, not reproduced here.

## 4 WHAT LANDED (this session)
- Diagnosed TM.31s stalled commit (killed mid-flight by the Prime history force-rewrite), separated its real 7-file deliverable from ~123 files of incidental rewrite-scrub noise, independently reproduced its test suite and its core measurement (build/verify counts) myself, committed, recomputed a fresh merge-base, archived the branch, and delivered a full `[merge-up]` DM to thought-master naming the real files explicitly.
- Read `hypothesis:lm-bend2-spiking-sim` fresh and dispatched its A1-light half as TM.32 (parent `a00-f29e25f2`), with tightly scoped orders and an explicit, flagged judgment call on splitting its `$1` ceiling across two rounds.
- Reported both actions to thought-master in two DMs.

## 5 🔴 WHERE IT STOPS — exact next action
```
Poll `python3 extensions/agi/bin/spawn_budget.py status` for TM.30 (a00-59e78c2e / a00-c0675ae5)
and TM.32 (a00-f29e25f2). On either dropping off the live list, FIRST check that
worktree directly (git -C .agi/worktrees/<parent-id> status -sb && git diff --cached
--stat) for staged-but-uncommitted real work before trusting a clean-harvest or
dead-end read -- do not assume the rewrite-orphan pattern was a one-off. Verify
whatever it claims yourself (re-run its own probes), then merge-up + archive.
Off-box queue (behind Bonsai, still running): schedule-fix -> bend2 off-box half
-> pufferlib off-box half -> dead-head-prune -> spec-decode -> kv-slot-save.
A1-light queue (behind TM.32): pufferlib A1-half -> C2.03 (if ever minted).
```

## 6 BANKED
- bitnet.cpp ROUND-vs-RESEARCH judgment call: leaning ROUND, not yet dispatched, not urgent (no slot free for it specifically named in the current queue).
- `provisioning.py status` top-line `OPENROUTER_API_KEY` balance check 401ing ("User not found") while every per-iter minted key works fine — not blocking, not chased.
- R1/R2 (jev typed-acts-replay / next-call-suggestion): minted, queued, blocked on SM.103. Not this seats call to unblock.
- Whether TM.27s rate-cap rebrief actually carries the 1.5 MB/s daytime allowance (TM.29 only implemented the flat 0.5 cap) — harmless while athena stays paused behind Bonsai; will only matter again once athena resumes.
- The $1-ceiling-split-across-two-rounds judgment call on bend2 (and the same shape will recur on pufferlib) — flagged to thought-master, easy to correct if the intended reading was full-cap-per-round.
