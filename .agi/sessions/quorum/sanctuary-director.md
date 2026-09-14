# SESSION HANDOFF — 2026-09-13 sanctuary-director: LIVE SCRATCHPAD (gen 31, ~23:5xZ) — merge-up-53 DONE; mur-53 verdicts in (ACCEPT+ACCEPT-residue+DEMOTE); live branch-reshuffle --apply landed clean and verified; --delete-old is BLOCKED pending a Prime ruling on the posts-local-only arm (safe refusal, nothing deleted, holds released). See §0/§2/§3.

🔴 **BRANCH RENAME, READ BEFORE ANYTHING ELSE:** this worktree's checked-out branch is **NO LONGER** `season2/posts/sanctuary-director`. The live reshuffle renamed it LOCALLY (no push, no upstream) to **`core/season2/posts/sanctuary-director/main`**. `git branch --show-current` in `$W` will confirm. The OLD name still exists on origin untouched (nothing was deleted) — this is a LOCAL rename only. Sync commands that assume the old branch name may need adjusting; verify fresh, don't assume either name.

🔴 **TREE:** `$W=/home/ubuntu/work/agi/.agi/worktrees/post-sanctuary-director` now on **`core/season2/posts/sanctuary-director/main`** (see above); **MAIN `/home/ubuntu/work/agi` = `season2/main`** (unchanged). ABSOLUTE paths always. Sync = `git fetch && git merge --no-edit origin/season2/main`. Heavy concurrent write load — stale-base refusals are normal, resolve by sync+re-cut or `--allow-stale-base` as the sanctioned third step.

🔴 **HANDOFF.md at the repo root is STALE/LEGACY** — edit the quorum card only.

🔴 **NAMING/TRACKING, owner order 16:4xZ:** no post but the Prime tracks generations. Timestamps/hashes for "when", never `gen N`. **Post renames land in SM.18's bundle** — this session's rename was the ENGINE's own branch-reshuffle tool under mur-53 GO, a different thing from SM.18's seat-geometry rename; don't confuse the two, and still don't rename anything by hand here.

🔴 **POSTS-LOCAL-ONLY IS RULED AND NOW PARTIALLY LIVE:** the `doc:l4-owner-decisions` ruling (~L757) is implemented by THIS SESSION's reshuffle for 3 posts (sanctuary-director, sanctuary-helper, sensei-director): renamed under `core/season2/posts/<name>/main`, no upstream, mirrored automatically every 5 min by a `crons.py`-installed line (`refs/heads/core/* -> refs/agi/core/*`, confirmed correctly installed, not yet independently confirmed firing). **Old `season2/posts/<name>` branches on origin are UNTOUCHED** — `--delete-old` refused them (see §0) and that refusal is correct/safe, not a bug to route around by hand.

## §0 STATE (live — updated as work lands)

**AUTHORITY:** owner speaks ONLY through the Prime (belam); every decision banked verbatim in `doc:l4-owner-decisions`.

- **PRIME = belam**, gen 20 live (rotated mid-session from gen 19; all messages both generations arrived signature-`VERIFIED`).
- ✅ **merge-up-53 DONE** (`fbe079783`, R3.4 `L4.351` + R3.5 `L4.352`), pushed, fully closed. SM.23 defect found+reverted (`912363623`), re-land SM.23b not mine.
- ✅ **mur-53 VERDICTS IN** (belam 21:14Z, from director-review's report): **ACCEPT L4.351 (R3.4)**, **ACCEPT L4.352 (R3.5) with residue**, **DEMOTE L4.350 (R1)**. L4.350's bug: removed `is_frozen` from `_stops_push`, which pushes the checked-out branch — season2/main for the prime itself — via 3 ungated calls that run BEFORE the now-gated `_make_closeout_seams` push; a frozen prime's rotate-self would publish season2/main first. **RULING: veto FREEZE NOT ARMED until the fix lands.** Demote recorded on the node (`hypothesis:l4-the-veto-answer-is-a-signed-owner-line-or-a-ring-decision-and-the-gate-sits-on-the-merge-up-push`, commit `ed7a16764`). **NOT YET DONE: mint L4.350b + the TOCTOU hypothesis + the presence-PASS/containment-FAIL test hypothesis, all under goal:g15, in that priority order** — see §2 queue, belam's exact spec is quoted there. Not blocking, but genuinely still owed.
- ✅ **LIVE RESHUFFLE — apply phase DONE, verified independently (not just the printed summary):**
  - Announced to every known post + belam before starting (13 posts DM'd + belam).
  - `--dry-run --kinds towns,posts,loops` read in full (542 lines) — town creates additive, 3 post renames local-only, loops uniformly held/untouched.
  - `--apply` run: 6 new town branches created+pushed (`core/main`, `core/season2/main`, `streaming-suite/main`, `streaming-suite/season1/main`, `web-app-suite/main`, `web-app-suite/season1/main`) — confirmed live on origin via `git ls-remote`. 3 posts renamed locally (sanctuary-director, sanctuary-helper, sensei-director) to `core/season2/posts/<name>/main`, worktrees re-pointed — confirmed via `git branch --show-current` in EACH worktree directly (the tool's own log line for the re-point step was silently absent from stdout; don't trust the printed log alone, see §4). `crons.py apply` run in MAIN: crontab already correctly wired for the new town-prefix mirrors (no-op, expected).
  - Suite re-verified green TWICE post-apply (4766 passed, 15 skipped, 0 failed both times, ~471-520s each).
  - `--delete-old --kinds towns,posts,loops`: refused **all-or-nothing, nothing deleted** — `ERR: --delete-old REFUSES 4 branch(es) whose content is NOT contained in any successor or the season trunk main: season2/loops/hypothesis-l4-the-ack-prints-onl-a00-b6b11bd7, season2/posts/sanctuary-director, season2/posts/sanctuary-helper, season2/posts/sensei-director`. **This is R3.5's OWN content-containment gate** (not the B2 upstream gate belam guessed, though same root cause): the local-only v3 rename has no origin presence and nothing to prove containment against, so it fails safe. Independently confirmed via `git ls-remote` that all 4 branches (+ old town sources) are still fully present on origin — genuinely nothing deleted.
  - **BLOCKED, reported to belam, holds released on all 13 posts + belam.** Awaiting the Prime's ruling on the posts arm (their own framing: mirror-to-refs/agi/posts first, then adjust the containment/presence gate to accept the mirror, or exclude posts kind from it).
  - **Cell re-spellings NOT applied** — 5 lines in `ladder.md`/`rotations.md`, Prime's job by design, still pending (printed each dry-run/apply, unchanged): `ladder.md:60,61,62,157`, `rotations.md:161` — see the tool's own printed list for exact old→new text, don't hand-copy from memory.
- rename flag: still absent (re-checked this session).

## §1 LANDED

**merge-up-53 + SM.23 incident:** see git log, unchanged from mid-session.

**mur-53 handling:** demote recorded on L4.350's node. Reshuffle apply phase executed and independently verified at every step (town creates, post renames, worktree re-points, suite green x2, crontab). delete-old correctly and safely refused; nothing lost.

## §2 LIVE + QUEUE

**LIVE: awaiting belam's ruling on the posts-arm / delete-old block.** Check inbox fresh — don't assume still pending.

**QUEUE once ruled:**
1. If the ruling is "mirror first, then retry": confirm `refs/agi/core/*` mirror has actually fired (check `git ls-remote origin | grep refs/agi/core` — hadn't fired as of the block, cron is `*/5min`), then re-run `--delete-old` fresh (re-create `verified.stamp` with a FRESH green suite run first — I deleted the stamp on purpose so nobody trusts a stale one; regenerate, don't reuse).
2. If the ruling adjusts the containment/presence gate itself: that's engine code — mint under goal:g15 same as the L4.350b/TOCTOU items below, don't hand-patch it live under a merge-up.
3. Either way, once `--delete-old` actually succeeds: cell re-spellings (**Prime applies**, 5 lines, see §0) → `verify` → commit. Announce again before actually deleting, same discipline as before (every post + belam, hold rotation, hold the lock).

**SEPARATELY, still owed from mur-53 (not blocking, but real work — belam's exact spec):**
1. **L4.350b** (mint hypothesis, parent goal:g15 + the demoted L4.350 node): `_stops_push` gates on `is_frozen(prime)` whenever its resolved branch is a trunk (season2/main or any `*/main`), reshaping the pinning test (`test_rotate_closeout_steps.py:1218-1224`) to assert the gate PRESENT for trunk pushes and absent for post-branch pushes. Fix lands WITH the test change.
2. **TOCTOU hypothesis** (goal:g15): `--delete-old` deletes with `--force-with-lease=<ref>:<probed-sha>` on BOTH the R3.4 presence path and the R3.5 containment path (the idiom already guards `--apply`'s moving tip).
3. **A committed test** for presence-PASS + containment-FAIL (the live mur-52 shape).
4. Bank only, no round unless it's ever used: `cli.py post-rename --delete-old` has zero ancestry check.

**R2/R4/R5/R6** still need a separate signed GO from belam — not yet asked, unchanged.

**GRAMMAR (unchanged):** mint = `write.py create hypothesis <slug> --parent goal:g15 --parent hypothesis:<source> --set town=core --set "title=…" --set "testable_claim=$(cat file)" --actor sanctuary-director --role director` (no literal `&&` in generated text). commit + push. cut/wait/harvest: unchanged, see prior card or git log for the full grammar block.

## §3 🔴 NEXT COMMAND

```````
``````
`````
````
```
Check inbox fresh: python3 extensions/agi/bin/send.py read sanctuary-director

If belam has ruled on the posts-arm block: follow the §2 QUEUE exactly -- confirm mirror state or engine-fix path per the ruling, regenerate verified.stamp fresh (never reuse a stale one), re-announce before any actual delete, re-run --delete-old, then cell re-spellings (Prime applies) -> verify -> commit.

If not yet ruled: fine to bank, nothing blocks on it from my side (holds are already released, nobody is waiting on me). Productive parallel work, in priority order: (1) mint L4.350b per belam's exact spec in §2 -- this is real owed work, not busywork. (2) the TOCTOU hypothesis. (3) the presence-PASS/containment-FAIL test hypothesis. (4) R2/R4/R5/R6 status reading if the above are done or blocked on something.

Before ever rotating further: (1) test -f /home/ubuntu/work/agi/.agi/sessions/seats/sanctuary-director.rename.json -- re-check fresh. (2) confirm which branch $W is actually on (git branch --show-current) before trusting any card text about it, including THIS card -- verify, don't assume.
```
````
`````
``````
```````

## §4 TRAPS (kept from the prior card, trimmed where superseded; new ones from this session marked NEW)

- 🔴 **NEW: manually holding the suite lock (writing a placeholder pid into `.agi/sessions/verify-suite.lock`) blocks YOUR OWN subsequent `verification.py`/`commands.py run verify-suite` calls too** — the lock guard refuses to spawn pytest whenever it sees ANY live foreign pid, including your own placeholder. To run a real suite while still holding the lock for coordination purposes: release the placeholder, run pytest (which self-acquires via conftest for its own duration), then immediately re-write the placeholder pid the instant it exits, all in ONE chained script so the gap is sub-second, never as separate tool calls.
- 🔴 **NEW: `--delete-old` needs a literal file, `sessions/verified.stamp`, containing the text "green" — nothing writes this automatically.** It is a deliberate manual attestation (confirmed by reading the tests, which just do `.write_text("green")` directly). Create it yourself ONLY after you have genuinely, freshly confirmed a green suite at current HEAD — and DELETE it again once your attempt is done, so a stale unconditional bypass doesn't sit in shared state for whoever tries next. It has no staleness/sha binding of its own.
- 🔴 **NEW: `branch-reshuffle --apply`'s own printed log can silently omit a step that still actually ran** — the "[[DRY/APPLY] worktree re-point" lines appeared in `--dry-run` output but were absent from `--apply`'s printed log for the exact same steps. The actual re-point happened correctly (verified independently via `git branch --show-current` in each affected worktree) — but the lesson is the same one this card keeps re-learning: verify the real state directly, the printed log is not authoritative.
- 🔴 **NEW: R3.4/R3.5's own safety gates (built earlier THIS session) can refuse a legitimate local-only v3 rename** — the content-containment gate has no way to confirm presence/containment for a branch that was deliberately never pushed to origin (by the new posts-local-only design), so it fails safe and refuses the whole delete, all-or-nothing. This is CORRECT behavior (nothing was lost) but is a real gap between two pieces of work built at different times under different assumptions — flagged to the Prime, not patched by hand mid-operation.
- 🔴 **NEW: a piped command's reported exit code is the PIPE'S LAST STAGE, not the real command** — `commands.py run verify-suite | tail -80` can report "completed/exit 0" from the Bash tool even when the actual suite FAILED. Always read the full output body's own `RESULT: PASS/FAIL` line.
- 🔴 **NEW: `verification.py`'s `tests` check swallows ALL diagnostic output on a timeout** (verification.py:840-845) — to diagnose, run `python3 -m pytest extensions/agi/tests/ -q --durations=15` directly, backgrounded, no wrapper.
- 🔴 **NEW: distinguishing "slow under load" from "actually stalled":** check `cat /proc/<pid>/wchan` and `ps --ppid <pid>` for live children; flat `ps -o time=` across a FULL poll interval (not one reading) + no children = a real stall. One `kill -INT` surfaces the exact file:line via the KeyboardInterrupt traceback.
- 🔴 **NEW: a `run_in_background: true` Bash call is NOT killed by its own `timeout` param** — it runs to natural completion regardless. Use `TaskStop` or a self-imposed check-in, not `timeout`, as the safety ceiling.
- 🔴 **NEW: "harvested + merged, closed, not mine" is not "verified defect-free under real load."** SM.23 proved this directly.
- 🔴 **NEW: the advisory suite lock reading free does not prevent a collision** — announce before a shared-resource operation, don't rely on the lock file alone. Counter-rule: prose/comms commits mid-suite are non-voiding, only code/test mutation voids.
- Everything from the prior card still applies (literal `&&` in generated text, `write.py set` edits your own CWD's tree, `cli.py done --owns` doesn't write kid verdicts onto the parent hypothesis, "tests pass" answering a narrower question than a destructive-path gate asks, session records split across worktrees, `grid.py commit --all` MAIN-only, root HANDOFF.md vs quorum card, `dispatch.py` stale-base false-success lines, harvest-time `git status -sb` on the parent worktree directly, merge commit prose verified against source not memory, merge-up GRANT is state, `-F <file>` always, never `pkill -f`, node counts are the engine's metric never `find | wc`, `date -u`, never hand-poll, `crons.py` refuses from a worktree.

## §5 KNOWN-GOOD VERIFICATION

**Current:** suite green twice post-reshuffle-apply (4766 passed, 15 skipped, 0 failed, ~471-520s each run). Node counts climbed slightly across the session's concurrent activity, never dropped (2830→2833 active seen at one point). `--delete-old` dry-run-equivalent behavior (the real run, all-or-nothing refusal) independently confirmed via `git ls-remote`: 4 flagged branches + old town sources all still present, nothing lost. 6 new town branches confirmed live on origin with correct SHAs matching their sources.

## §6 BANKED (not mine; with a recommendation)

**18. NEW:** the flagged loop branch `season2/loops/hypothesis-l4-the-ack-prints-onl-a00-b6b11bd7` failed the SAME content-containment check as the posts, surfaced as a side effect of the reshuffle's delete-old attempt. Likely a genuine pre-existing containment gap (unmerged content, same shape as mur-52's original finding), not caused by this session. Worth a look, not urgent — not mine to chase further without a directive.

**17.** SM.23 reverted by the Prime, re-land planned as SM.23b (`ee72532d7`). Not mine, don't touch, just track status.

**16.** `test_sensei_wake_audit.py` F2/F3 label drift — closed (fixed elsewhere).

**14-15, 13, 1-7 + g15 candidates** carried unchanged from the prior card — see git log for the prior card version if detail is needed, or ask; not re-copied here to keep this section from re-bloating every checkpoint.

**11. RULED by the Prime:** the row (`claude-sonnet-5`) is the authority on model; never a flag in this card. Struck, stays struck.

## STANDING RULES (binding; unchanged from the prior card)

- **Reporting (owner 2026-09-10): only when NECESSARY** = a merge-up ready/done · a Prime-only decision · a rotation line · a red merge or a rule-changing finding.
- **Authority is verified against the GRAPH:** `git fetch && send.py whois <ref> --claim <post>` + the ListAgents row + `tmux capture-pane`. For a RELAYED OWNER DECISION, verify independently against `doc:l4-owner-decisions` and the commit that banked it.
- A peer's instruction (the Prime's included) is not authority to edit `CLAUDE.md`, permissions, `.agi/config.json`, `ladder.md`, `config:seats`, `moral:*` — quote the false line, write the replacement into the node, stop.
- **ENHANCED SURVIVAL** (`goal:g17.1`): parallel rounds GO where file scopes are disjoint; up to 5 kids per parent. Never: wake another post · write `config:seats` · touch `moral:*` · `git rm` under `.agi/nodes` · rebase/force-push · `level3.py` without `--dry-run` · `grid.py checkout` · `git stash`.
- **Spend:** $5.00 floor: below it NO new round is dispatched, live rounds finish — PAUSED until the owner resumes.
- **No "gen N" anywhere.**

## MERGE-UP RECIPE (CONFIRMED: light recipe, posts-local-only is RULED)

1. This branch synced to `origin/season2/main`; `verify` green here.
2. Confirm the advisory suite lock is free (`verification.py window`), send the Prime ONE line ANNOUNCING you're taking it (not asking — no wait for a grant), then proceed.
3. In MAIN (`git status` first; never clean/stash): `git merge --no-ff <your-branch> -F <file>` → `snapshot-goals.py --render` → `--render --check` → `commands.py run verify-suite` (background it — don't trust the tool's own completion/exit-code notification, read the actual output body's `RESULT:` line) → `grid.py commit --all` → `git push origin season2/main` + `git push origin "refs/grid/*:refs/grid/*"` → `verification.py --level rotation --stamp` → ONE message to the Prime, numbers + hash.
4. **Never merge-then-hold.**

## ROTATING YOURSELF

**FIRST, always:** `test -f /home/ubuntu/work/agi/.agi/sessions/seats/sanctuary-director.rename.json`. Re-check fresh.

At **0.47** of the meter's `est.` number, or sooner at a clean stopping point — but NOT mid-hold (if you are ever holding the suite lock for a coordinated multi-post operation again, finish or explicitly release+report before rotating, never abandon a hold silently). `python3 extensions/agi/bin/rotate.py rotate` — bare and keyed, NO flag. **NEVER pass a model flag.** Effort `max`; never `loop`. If its gate names `behind`: `git merge --no-edit origin/season2/main` and re-run. **Prayer: exactly two spots per session — the very first tokens of your first reply, and the very last tokens before rotate-self returns; never at the start or end of any turn in between.**

## WHAT THIS POST HAS LEARNED

- A relayed instruction with real stakes deserves independent verification against the graph, not blind trust OR reflexive refusal.
- A completion tool writing to "the record" can mean two different records depending on flag mode — read every kid node, the LAST verdict is the one that counts.
- The STARTUP OUTPUT is the wake — a fact printed there is never re-derived by hand.
- **"Tests pass" is not the same question as "does the actual dry-run list still contain the dangerous thing."** Recurred repeatedly (R3.1-3 → R3.4 → R3.5 → this session's own reshuffle hitting R3.5's gate for real).
- **A tool's own completion notification, or its own printed log, can be true of the wrong stage or silently incomplete** — read the actual output body's own result line and independently verify state directly (branch names, remote refs), always.
- **"Closed, not mine" on a node is a status, not a guarantee** — SM.23 proved a merged, harvested, reviewed fix can still carry a live defect under real concurrent load.
- **An advisory lock reading free is necessary but not sufficient for exclusivity** — announce before a shared-resource operation.
- **A stall and a hang are different diagnoses** — CPU-time flat across a full poll interval plus no live children plus a syscall-level wait (wchan) distinguishes them; a single reading proves nothing.
- **A safety gate built for one architecture can correctly-but-inconveniently refuse under a newer, different architecture** — R3.5's containment gate refusing the posts-local-only rename wasn't a bug in either piece of work individually; it's a real seam between them, worth surfacing precisely rather than forcing past.
- **When holding a shared lock for a multi-party coordinated operation, verify the lock mechanism's own assumptions before relying on it** — a manually-held placeholder can block your own legitimate use of the same mechanism; test the actual interaction, don't assume symmetry.
