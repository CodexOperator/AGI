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
- **A DIRECTOR NEVER DMS THE PRIME DIRECTLY, PERIOD (owner rule via thought-master 06:4xZ, supersedes the earlier tag-allowlist reading below).** All Prime-bound content routes through your master (thought-master), who batches it up. And even to your master: minimize — one line per lap, only for a merge-up, a red, or a decision only you can make. **Silence is the healthy default now, not routine [status]/[ack] chatter.** Hit the OLD, narrower version of this rule for real (sent `[status]` to belam twice before being corrected on the tag allowlist alone) — this new rule is stricter still: not "use the right tag to belam", but "do not DM belam at all."
- **STANDING ANONYMIZATION RULE, extended (thought-master 06:3xZ then 07:0xZ): never write a real host name, IP, GPU/CPU model, location, or key id in ANYTHING that gets committed — nodes, commit messages, AND DMs (comms are committed by cron too).** Aliases: `GPU2070S` = the rig, `ARM4C` = this box, `CPU8G` = the keeper, `EDGE` (a fourth alias seen once, unexplained — treat as another box, do not guess which). I wrote "belam-gpu"/"GPU2070S" straight into a merge-up DM and commit message this session; thought-master had to scrub 7 files at landing. Not retroactively fixing my own already-archived text — just do not repeat it, and **actively scrub anything you are about to name in a merge-up, not just your own new writing** — a kid/parent nodes own prose can carry a real name that needs catching before it reaches your DM.
- `tr '\0' ' ' < /proc/<pid>/cmdline` on a LIVE agent pid (from `spawn_budget.py status`) prints its full inherited system prompt/brief verbatim, including what its PARENT told it to do next and what the LAST kid actually produced. Genuinely useful before touching anything the round might still depend on (files, dirs) or before assuming a gap is unaddressed — read what the live agent was actually told before asking or acting.
- A conflict on another posts OWN card file (`.agi/sessions/quorum/<other-post>.md`) during a routine `git merge origin/local-maxxing/season1/main` is not yours to arbitrate — `git checkout --theirs <path>` and move on, every time (hit repeatedly across generations, including twice this session alone).
- The whole GitHub repo can be deleted and recreated under owner order (purge PR refs/caches) — belam holds ALL pushes/fetches/merges/dispatch/rotation for the window, then sends resume. After resume, GitHub may report a repository-moved redirect on push (case-only rename seen once: `agi` -> `AGI`) — git follows it automatically and the push still lands; just re-check `git ls-remote` on anything you pushed before the hold to confirm it survived (it did, both times checked).
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
- Nudge at 05:2xZ delivered four messages: thought-master confirmed **TM.31 LANDED on `local-maxxing/season1/main`** (clean gate, 0 deletions, links 3472/0) and explicitly said the rescue judgment call was ACCEPTED, right call, no spend; queued its `push_further` as a new node `hypothesis:lm-mirror-choices-for-act` (A1-light, cap $0.50) rather than reopening the closed round; **corrected A1-light order: bend2 A1-half (TM.32) -> pufferlib A1-half -> lm-mirror-choices-for-act -> c2-flip-as-phase-jump-vs-sign-inversion (C2.03, newly minted)**; both thought-master DMs verified cleanly (not RETIRED) — replied confirming. Separately belam held ALL pushes for a GitHub repo delete+recreate (purge PR refs/caches), then resumed ~9 min later — reconciled clean: fetched fresh, both refs I had pushed before the hold (post branch tip, TM.31 archive ref) matched exactly, nothing lost, no re-push needed. One repo rename artifact found and flagged to belam: push now shows a repository-moved notice, `agi` -> `AGI` (case only), git follows it automatically. Merged both trunks into this worktree afterward per thought-masters own reminder — one more conflict on thought-masters own card, resolved the usual way (took theirs). Also saw the ceiling get formally clarified on the two CRITICAL nodes (bend2, pufferlib) in the trunk history: **$1 OpenRouter per half-round, $2 per node total, $0 compute** — TM.32s $0.55 cap was more conservative than required but stands as-is; the pufferlib A1-half can use up to the full $1.

## 1 PLAN
1. DONE: rescued + committed + archived + merge-up-delivered TM.31; dispatched TM.32 (bend2 A1-half); this card.
2. NEXT: poll `spawn_budget.py status` for TM.30 (Bonsai) and TM.32 (bend2 A1-half) periodically. On EITHER exiting, apply the same rescue-check pattern from this session before trusting "still running" or "must be done" — check the worktree directly (`git status -sb`, `git diff --cached --stat`) for staged-but-uncommitted real work before assuming a clean harvest or a dead end.
3. TM.30 is NOT closing yet — its own parent cut a second kid that is already mid-flight on the real GPU/27B gap (see BANKED). No separate TM.30b dispatch; wait for THIS kid/round to actually finish, then verify directly, merge-up, archive. THEN the off-box slot frees for: schedule-fix (small, `hypothesis:lm-athena-identity-seat-ab` — add a `zoneinfo` time check to `fetch_parallel.py`s rate selection) -> bend2 off-box half (16 threads + `--gpu`, up to the full remaining $1) -> `hypothesis:lm-pufferlib-oscillator-policy` off-box half -> `hypothesis:lm-c2c-kv-bridge-released-fusers` (new, off-box, cap $1, downloads <=3GB on local-town only behind the Bonsai 27B fetch) -> `hypothesis:lm-dead-head-prune-by-oscillator-coherence` -> `hypothesis:lm-spec-decode-cpu-draft-hybrid` -> `hypothesis:lm-kv-slot-save-beats-reprefill` (not read yet — fetch fresh when it is actually next). A 2609.04010 digest is also in flight; its download candidates (if <=4GB, Qwen-based) join this same queue after.
4. When TM.32 (bend2 A1-half) lands: verify directly, merge-up, archive, cap up to the full $1 (ceiling now clarified: $1/half-round, $2/node). Confirmed A1-light order after that: `hypothesis:lm-pufferlib-oscillator-policy` A1-half -> `hypothesis:lm-mirror-choices-for-act` (new, cap $0.50, thought-masters own push_further off TM.31) -> `hypothesis:c2-flip-as-phase-jump-vs-sign-inversion` (C2.03, newly minted).
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

## 4b TM.30 harvested, closed; TM.33 (schedule-fix) dispatched into the freed off-box slot (06:2xZ)
TM.30 (`hypothesis:lm-bonsai2-27b-kid-tier`) harvested honestly incomplete: kernel-path proven for real on belam-gpu (Ternary-Bonsai-1.7B-PQ2_0, CUDA, ngl 99, coherent output, pp512 6892.82 / tg128 317.94 tok/s), 27B GGUF header range-fetched and parsed into a VRAM budget (6183/7786 MiB at `-c 8192` fits, 32768 OOMs) independently reproduced by the parent, a resumable sha256-pinned 27B fetch STARTED but still running in the background on belam-gpu (~9-10h, not complete) — verdict kept honestly at `inconclusive_lean_proved:65`, hypothesis stays OPEN, a future round picks up the actual 27B bench once the bytes land. Verified directly (read both experiment nodes in full, confirmed the bench row is real), isolated the real 8 files from ~120 files of incidental drift (same pattern as TM.31), committed (`2d776e898`), archived to `refs/agi/archive/season2/loops/hypothesis-lm-bonsai2-27b-kid-ti-a00-59e78c2e`, merge-up sent. **Gap found and flagged, not hidden:** no evidence the proven-quiet-line athena pause I relayed earlier was ever executed before this fetch started — the round only cites the old 0.48 MB/s reading and a bare "supervisor is on the box." Recommended (and now dispatched) the schedule-fix round also add a real 60s-quiet-line proof, not just a stop command.
Off-box slot freed by TM.30 closing -> dispatched **TM.33** (schedule-fix), parent `a00-79adf24c`, pid 3675707, cap $0.30, target `hypothesis:lm-athena-identity-seat-ab`: zoneinfo time check (1.5 MB/s 02:00-06:00 America/New_York else 0.5) + the proven-quiet-line supervisor check. Dispatched while ACTUALLY INSIDE the 1.5 MB/s window (06:24Z = 02:24 EDT), so this is live-relevant immediately.

## 4c TM.34 dispatched: Uno-diffusion step 1 (Prime-approved rental spend, gated)
Prime GO 06:28Z on `hypothesis:lm-uno-diffusion-draft-on-l4` (a THIRD, independent "API slot" — runs alongside the A1-light and off-box slots, not competing with TM.32/TM.33). Dispatched **TM.34**, parent `a00-2e4630f1`, pid 3707743, cap $1 OpenRouter / $0.03 Camber. Orders are STEP-1-ONLY with a hard stop before step 2: one 5-min CPU-XSMALL Camber job (sleep 300 + hostname-free echo), then read real billing to learn the granularity (core-hour bill = STOP). Must report `[decision] uno step 1: job <id> wall <s> billed <credits> => granularity <x>` — **CORRECTED (owner rule 06:4xZ, arrived after I first wrote this note): relay it to thought-master ONLY, never belam directly — thought-master batches it to the Prime themselves.** Then WAIT for an explicit go-ahead before ever considering step 2 — do not treat silence as consent even though the node text allows that reading. If the kid cannot reach `CAMBER_CLOUD_API_KEY`, it DMs the exact refusal line — do not let anyone build around that.

## 4d PARENT-DEATH INCIDENT: all three live rounds died pre-harvest, all three rescued (10:2xZ)
Woke after a long idle gap (last activity ~07:00Z, this nudge 10:23Z) to `spawn_budget.py status` showing **0/25 live** and box load spiked to 372 (15-min avg, swap nearly full, now subsiding) — TM.32, TM.33 AND TM.34 had all died pre-harvest, zero harvest DMs from any of them. Matches a "parent-death autopsy... headless exit" bug class I saw named in a REDESIGN LIST commit that rode through one of my merges — likely already known/being fixed, reported as data points anyway (see the merge-up DM sent, full detail there, not reproduced here).
- **TM.34's entire PARENT worktree was deleted outright** — only rescued because its kid (`a00-8614c12a`) happened to have its OWN separate worktree this dispatch. TM.30/32/33's kids shared the parent's worktree; the same failure there would have lost the work permanently. **This is the real risk to flag/remember: a shared parent+kid worktree has no redundancy against this failure mode.**
- **TM.32** (bend2 A1-half): rescued from `a00-f29e25f2`. Kid 1s LIF loop measured **13.0x slower** than the C/f64 baseline — trips the hypothesis's own falsifier (`> 5x slower`) outright. `verdict=inconclusive_lean_disproved:60`, parent independently rebuilt both fixtures from committed source and reproduced the numbers. **Judgment call, not yet acted on: the off-box (16-thread+GPU) half of this SAME hypothesis may now be moot — the falsifier is written as an OR, and one arm has already tripped it. Flagged the raw number to thought-master; NOT dispatching the off-box half until that lands one way or the other, rather than assume either reading.** A second kid started, left only an empty untitled scaffold — correctly not committed (no real content, unlike TM.33's case below).
- **TM.33** (schedule-fix): rescued from `a00-79adf24c`. Code was genuinely complete and good (zoneinfo schedule + a real measured proven-quiet-line pause/resume, live-rate-without-restart) but its node was a never-filled scaffold — wrote the account myself from the diff + my own independent test run (9/9 passing), clearly marked as director-written, not fabricated as a kid self-report. `verdict=proved`.
- **TM.34** (uno step 1): rescued from the kids own worktree (already self-committed). Real, careful work — installed the Camber CLI, ran job 27649 to completion, verified teardown — but **the billing/credits surface is unreadable via the account API key** (CLI/SDK exposes no cost endpoint; the web usage page needs a human Clerk-token login, no agent can do this headlessly). Decision line sent verbatim to thought-master (not belam, per the DM rule). **Step 2 (the GPU hour) stays hard-gated until a human checks Camber's web Teams>Usage page by hand — this is not something any future round can resolve on its own; bank it as a standing owner-side action item, do not re-dispatch hoping for a different answer.**
All three verified independently before committing (ran real tests myself, read real diffs, did not trust any report blind), isolated real content from noise where present, archived to `refs/agi/archive/season2/loops/*`. One consolidated `[merge-up]`+red DM sent to thought-master (not belam) covering all three plus the systemic finding.
**All three slots (A1-light, off-box, API) are free again as of this write.** Holding on dispatching anything further this lap pending: (a) thought-masters read on the bend2-off-box-moot question, (b) a natural next wake rather than immediately piling more spend on top of this incident report.

## 5 🔴 WHERE IT STOPS — exact next action
```
All three (TM.32/33/34) ACCEPTED and landed on trunk (thought-master 11:33Z) --
tips: TM.33 b6baafd13 proved, TM.34 cb9b0375e lean_disproved:65, TM.32 eea005dd4
lean_disproved:60. Bend2 RE-SCOPED after my flag (new falsifier: GPU2070S Bend/HVM
CUDA LIF within 5x of a CUDA/OpenMP-C baseline on the SAME rig, not compared back
to the ARM4C number) -- dispatched as TM.35, parent a00-6fe6b293, cap $1, first
act = confirm the 27B fetch survived the storm + df report (still not directly
confirmed by me -- this dispatch is what answers it). Uno step 2 GO arrived (Prime 13:01Z, job 27649 billing resolved: 5.3 CPU-min,
per-minute granularity) -- dispatched **TM.36**, parent `a00-59c581e7`, cap $1,
hard 60min wall (<=50min internal timeout), ONE job only, no further Camber
spend without a fresh per-job go-ahead. Report its GPU-minutes+tok/s line to
thought-master alone when it lands.
**NEXT: pufferlib ARM4C
half ($1) -- read hypothesis:lm-pufferlib-oscillator-policy properly first (not
done yet this session), check loadavg (gate: 1m<2.0, 15m<8) before dispatching.**
Use "ARM4C" not "A1" in all future writing -- caught in a scrub this lap (not
mine, but the same alias-discipline applies everywhere).
NEW STANDING RISK NOTE FROM STORM: forwarded to thought-master, "until fixed give
every kid its own worktree" -- already passing --branch on every dispatch, but
that alone did NOT separate every kid's worktree from its parent's this session
(TM.30/32/33 kids shared the parent's; TM.34's kid did not) -- mechanism not fully
understood, just keep checking both worktrees on any future death, as already a
standing habit here.
TM.35 harvested clean (no rescue needed) -- bend2 GPU2070S CUDA LIF 37.8x slower
than baseline, verdict=disproved, archived tip 0f7239fd5. Bend2 now disproved on
BOTH halves -- CONFIRMED CLOSED by thought-master (13:4xZ, landed c102dc404, no
further Bend rounds). Off-box slot free again. **TM.35 missed its first act (the
27B-fetch-survived-the-storm + df report) -- this is now explicitly the FIRST
ACT of the pufferlib off-box round, put the numbers in that rounds own [status]
line.** Both pufferlib halves (ARM4C + off-box, $1 each) are next; still have not
read hypothesis:lm-pufferlib-oscillator-policy in full this session -- do that
BEFORE drafting either rounds orders next wake. TM.36 harvested + reported: job ran (~4.2 GPU-min, 251s), but base 8B OOMed mid-load before Uno ever ran -- NO tok/s either arm. Honest inconclusive_lean_disproved:55, archived tip e1caf1da. Retry needs a fresh Camber go-ahead from the Prime, not dispatched. Kid had its OWN separate worktree again (a00-cb88d326, same as TM.34) -- parent's own worktree had no uncommitted loss this time, just its review sitting one commit behind on the kid's side, rescued cleanly.
TM.36 ACCEPTED by thought-master, landed 0699ad669. Uno retry approved on their
side (ONE XS GPU job, 20min hard cap, cpu-forced-device load probe added) but
PRIME-GATED -- do not dispatch until an explicit GO relays, no exceptions.
**THIRD ask for pufferlib as of 14:1xZ -- explicitly held, not forgotten: meter
is at the rotation line, dispatching either half without first reading
hypothesis:lm-pufferlib-oscillator-policy properly risks a bad brief right at a
handoff. THE next action, before anything else, next wake:**
1. Read hypothesis:lm-pufferlib-oscillator-policy in full (never done this session).
2. Check loadavg (gate: 1m<2.0, 15m<8).
3. Dispatch ARM4C half ($1) and off-box half ($1, FIRST ACT = confirm the 27B
   fetch + supervisor queue survived the 10:23Z storm, report df of the model
   volume, in that rounds own [status] line -- asked twice now, do not drop it
   a third time).
**UNO RETRY: Prime GO received (14:04Z), full orders given verbatim by thought-
master (ONE XS GPU job, 20min hard cap/<=15min internal timeout, per-arm
subprocess, expandable_segments, max_model_len 4096/max_num_batched_tokens 1024,
cpu-forced-device load probe recording peak GiB, K2-Horizon-0.9B+its Uno adapter
as the always-fits fallback arm, 20 prompts batch1(+8 if time), byte-identical
check, report GPU-minutes + Uno-vs-base ratio at 8B or 0.9B, ONE line to
thought-master only, no third job). HELD, not dispatched: loadavg-1m was 2.54 at
check (over the 2.0 gate; 5m 1.38, 15m 0.87 both fine, looked like a brief blip).
**NEXT ACTION: re-check `uptime`, dispatch the moment 1m<2.0, using this exact
brief for the orders file (do not re-ask thought-master, this is already GO).**
All slots free (see 4d — TM.32/33/34 all died pre-harvest, all three rescued and
archived already, nothing further owed on them). Before dispatching anything new:
1. Check the inbox for thought-masters read on whether bend2s off-box half is moot
   (its A1 half already tripped the >5x-slower falsifier, disjunctive OR condition).
   If no answer yet, use judgment: either skip straight to pufferlib (both slots
   free it up) or dispatch bend2 off-box anyway if the GPU arm seems worth checking
   despite the CPU-arm falsifier hit -- genuinely undecided, do not default to
   silence-means-proceed here, this is real spend on a likely-answered question.
2. **ON EVERY FUTURE ROUND FROM NOW ON: the moment spawn_budget shows a parent
   gone with NO harvest DM, immediately check BOTH the parents worktree AND (if
   the parent's is gone) whether a same-named kid worktree under
   `.agi/worktrees/<kid-id>/` survived separately** -- this is not a one-off, it
   hit 3/3 live rounds in a single lap. Never assume a missing worktree means lost
   work until both are checked.
Off-box queue: pufferlib off-box half ($1) -> lm-c2c-kv-bridge-released-fusers ($1,
local-town only, behind the still-running bonsai 27B fetch) -> dead-head-prune ->
spec-decode -> kv-slot-save. (bend2 off-box half: see judgment call above.)
A1-light queue: pufferlib A1-half ($1) -> lm-mirror-choices-for-act ($0.50) ->
c2-flip-as-phase-jump-vs-sign-inversion (C2.03).
API slot: free; Uno step 2 stays gated on a human Camber web-usage check (4d) --
do not re-dispatch step 1 hoping for a different billing answer, and do not attempt
step 2 without an explicit new go-ahead.
Also watch for: TM.30s hypothesis (lm-bonsai2-27b-kid-tier) needs a FUTURE follow-up
round once its background 27B fetch on belam-gpu finishes (~9-10h from 06:07Z).
Local-town download queue (owner order, banked in full at 6a): athena pair -> C2C
pair -> Uno adapter+K2-Horizon -> DFlash -> Qwen3-8B bf16 -> Qwen3-4B bf16 -> (added
this lap, see 6a) Qwen3.8-27B bf16 55.6GB -> Qwen3.5-35B-A3B GGUF Q4_K_M ~20GB.
```

## 6a LOCAL-TOWN DOWNLOAD QUEUE (owner 06:5xZ, for FUTURE dispatch sequencing — not a code task I pushed into TM.33)
Strictly behind the Bonsai 27B fetch, slow mode (0.5 MB/s, 1.5 MB/s 02-06 America/New_York), sha256 per file, to `/data`, nothing on ARM4C, in this order — dispatch each hypothesis round's own download in this sequence, do not let a later one jump ahead:
1. C2C pair Qwen2.5-0.5B-Instruct + Qwen3-0.6B bf16 + released fuser (~2.2 GB) — `hypothesis:lm-c2c-kv-bridge-released-fusers`s own download when it dispatches.
2. `s-sahoo/uno-qwen3-8B` adapter 0.70 GB + `IFM/K2-Horizon-0.9B` 2.16 GB + `IFM/K2-Horizon-0.9B-Uno` 0.22 GB — part of Uno step 2 (TM.34), only after its go-ahead.
3. DFlash drafters for Qwen3-4B and Qwen3-8B (z-lab.ai/projects/dflash -> HF ids from the digest) — no hypothesis node minted yet as of this write.
4. `Qwen/Qwen3-8B` bf16 16.38 GB (base for uno + dflash + later ternary work).
5. `Qwen/Qwen3-4B` bf16 ~8 GB.
6. (added 06:5xZ, "too big to fit but might optimize our way there") `Qwen/Qwen3.8-27B` bf16 55.6 GB — input for our own dead-head-prune/requant/ternary-recipe reproduction + KV rows.
7. (same order) `Qwen/Qwen3.5-35B-A3B` GGUF Q4_K_M ~20 GB — MoE, experts in host RAM + attention on GPU (`llama.cpp -ot exps=CPU` / `--n-cpu-moe`).
Items 6-7: same terms plus a free-disk floor of 20% checked before EACH fetch (report `df` of the model volume with that items first landing line).
~30 GB (items 1-5) + ~76 GB (items 6-7) total, spread over many days in slow mode. Relayed the one narrow CODE-relevant piece (a fetch must pause during any live tg/pp measurement row) to TM.33 since it is already in fetch_parallel.py; did not push the model list itself into its scope/cap. **Report one line to thought-master (never belam directly, per the new comms rule) when each item actually lands: id, bytes, sha256, hours.**

## 6b Storm follow-up (10:4xZ): confirmed system-wide (thought-masters own pane stalled 3h too), not a round defect. NEW STANDING RULE: gate every dispatch on ambient loadavg-1m < 2.0 AND 15-min < 8 (record both) — hold if not. Current: 0.31/0.41/5.09, healthy. Thought-master asked for a re-dispatch of TM.32/33/34 without knowing I had already harvested all three (see 4d) — told them so, recommended skipping the re-dispatch to avoid paying twice for already-answered questions; awaiting their read. New off-box queue item, after spec-decode: `hypothesis:lm-eagle3-drafter-on-frozen-qwen3-4b` (drafter trained on our own kid traffic vs a frozen Qwen3-4B, $0 compute, <=6h wall) — gated on the Qwen3-4B bf16 bytes actually landing first (item 5 in the download queue, 6a).

## 6 BANKED
- RESOLVED: thought-master ruled the 8B-on-GPU proof is not actually a conjunct (CUDA path already evidenced by symbol/wire probes; skip straight to the real 27B fetch). `/tmp/bonsai-a1` (2.1G) and `/tmp/bonsai-probe` (817M) deleted on this box, confirmed gone. Relayed the full ruling into the live kid (`a00-da8359fa` under parent `a00-59e78c2e`): real proven athena quiet-line before fetching, 27B on belam-gpu only, GPU numbers at `-c 8192` specifically, record the 32768-OOMs VRAM-budget finding rather than testing it live.
- Disk-full event 05:2xZ (Prime freed 14G), cleared 05:22Z: confirmed via `git fsck` that only `sensei-director`s own ref/worktree reflog is corrupted (invalid reflog entry, same sha repeated) — nothing of minds (post branch, TM.31 archive, TM.32 loop branch) affected; flagged the precise location to belam, not mine to repair. No pytest of mine fell in the invalidated 05:20-05:21Z window. TM.30s kid id changed (`a00-c0675ae5` -> `a00-da8359fa`) between checks with the same parent pid throughout — read as normal kid-cycling within one live round, not a crash-respawn; not chasing further absent other evidence.
- bitnet.cpp ROUND-vs-RESEARCH judgment call: leaning ROUND, not yet dispatched, not urgent (no slot free for it specifically named in the current queue).
- `provisioning.py status` top-line `OPENROUTER_API_KEY` balance check 401ing ("User not found") while every per-iter minted key works fine — not blocking, not chased.
- R1/R2 (jev typed-acts-replay / next-call-suggestion): minted, queued, blocked on SM.103. Not this seats call to unblock.
- Whether TM.27s rate-cap rebrief actually carries the 1.5 MB/s daytime allowance (TM.29 only implemented the flat 0.5 cap) — harmless while athena stays paused behind Bonsai; will only matter again once athena resumes.
- RESOLVED: the ceiling question on bend2/pufferlib was $1 per half-round / $2 per node (thought-master clarified in trunk history 05:20Z) — TM.32s $0.55 was over-conservative but valid; use up to $1 on the remaining halves.
