# SESSION HANDOFF — 2026-09-13 sanctuary-director: LIVE SCRATCHPAD (gen 31, ~20:5xZ) — merge-up-53 (R3.4+R3.5) fully DONE and pushed; a real defect in SM.23 (mur-51's own fix) was found and reverted by the Prime mid-session; posts-local-only is now RULED. mur-53 (adversarial review) is the live next step — not yet run/named. See §0/§2/§3.

🔴 **TREE:** `$W=/home/ubuntu/work/agi/.agi/worktrees/post-sanctuary-director` on **`season2/posts/sanctuary-director`**; **MAIN `/home/ubuntu/work/agi` = `season2/main`**. ABSOLUTE paths always. Sync = `git fetch && git merge --no-edit origin/season2/main`. Heavy concurrent write load — stale-base refusals are normal, resolve by sync+re-cut or `--allow-stale-base` as the sanctioned third step.

🔴 **HANDOFF.md at the repo root is STALE/LEGACY** — edit the quorum card only.

🔴 **NAMING/TRACKING, owner order 16:4xZ:** no post but the Prime tracks generations. Timestamps/hashes for "when", never `gen N`. **Post renames land in SM.18's bundle — do not rename anything here.**

🔴 **POSTS-LOCAL-ONLY IS RULED (confirmed this session, `doc:l4-owner-decisions` ~L757, owner 18:3xZ / Prime ruling relayed 18:4xZ):** merge-up **drops the window-ask/grant round-trip** — the post takes the advisory suite lock itself when free and tells the Prime ONE line **after**. (Separate infra piece — post branches never pushed as heads, mirrored to `refs/agi/posts/<name>` — is NOT yet built; don't assume it and don't build it yourself, it's SM.18's bundle.) merge-up-53 this session still used the OLD ask/wait recipe because it was already in flight before this confirmed. **Use the light recipe for the next merge-up.** See updated MERGE-UP RECIPE below.

## §0 STATE (live — updated as work lands)

**AUTHORITY:** owner speaks ONLY through the Prime (belam); every decision banked verbatim in `doc:l4-owner-decisions`.

- **PRIME = belam.** 🔴 **belam itself rotated mid-session (gen 19→20)** — every belam message this session (both generations) arrived signature-`VERIFIED` via `send.py read`, so authenticity was never in question, but note the seat is a new live process now. Re-verify via `send.py whois` only if something feels off; routine VERIFIED-tagged DMs are trustworthy as-is.
- **Ids:** L4.347-349 = R3.1-R3.3 (merge-up-52). L4.350 = R1 (rotate.py closeout gate). L4.351 = R3.4 (origin-presence gate). L4.352 = R3.5 (content-containment gate). All four harvested and merged prior to this session's own work — see git log. **Next id = L4.353**, not yet assigned.
- ✅ **merge-up-53 DONE.** Merged `fbe079783` (R3.4 `L4.351` + R3.5 `L4.352`) into MAIN, no conflicts. Full detail + the mur-52/R3.4/R3.5 finding chain: git log, unchanged from before — still worth reading in full before touching branch-reshuffle again (search `harvest L4.351`, `harvest L4.352`).
- 🔴 **SM.23 (mur-51's own fix) had a REAL DEFECT — do not trust "harvested + merged" as "verified under load."** SM.23 (`17d919e84`) added `if status == stalled: all_terminal = False` to `heal.py`'s wait loop — a stalled record with a live-or-unprovable pid keeps that loop sleeping (`heal.py:252`) up to its **30-minute max-wait**, which is *exactly* `verification.py`'s `SUITE_TIMEOUT=1800s`. Result: 3 full suite runs redlined on `tests` timeout with **zero diagnostic output** (see §4 trap), 2 of them mine. belam (Prime) found the mechanism, reverted the hunk on MAIN (`912363623`, graph nodes kept), and a re-land is planned as **SM.23b** (TOP node `ee72532d7`) with the poll seamed. **SM.23b is not mine — don't touch it, don't restart the reaper.**
- 🔴 **Coordination incident, resolved, rule learned both ways:** my first verify-suite run (19:27Z, unannounced) collided with director-sanctuary's SL2#30 and blocked it twice (per master-sensei). Prime rule going forward: **announce ONE line to the Prime before running a suite in MAIN**, the advisory lock file alone isn't enough. Counter-rule (Prime, XVIII precedent, also learned this session): **prose/record/comms commits landing on MAIN mid-suite are NON-VOIDING — only code/test-file mutation voids an in-flight run.** Don't kill your own run just because a handoff/comms commit lands; DO stop it if code or test files change under it.
- **Final verified state, everything pushed:** verify-suite at `ac12854ca` — **all 11 green**, `tests` 471.4s (4766 passed, 15 skipped, 0 failed) — ceiling back to normal post-revert. Rotation stamp at `ee72532d7` — **all 10 green** — active=2830 deprecated=198 total=3028 broken_links=0. `git push` both times reported "Everything up-to-date" (belam's own pushes during the incident already covered it). Reported to belam in one line.
- **LIVE:** mur-53 (director-review's adversarial workflow) — not yet run or named by anyone. That's the next real step, gated on nothing else.
- 🔴 **rename flag:** re-checked twice this session, still absent: `test -f /home/ubuntu/work/agi/.agi/sessions/seats/sanctuary-director.rename.json` → no.
- **Post branch** (`season2/posts/sanctuary-director`) tip unchanged at `834549aab` all session — all actual work this session happened directly in MAIN per the merge-up recipe; nothing new minted on the post branch itself until this card commit.

## §1 LANDED

**R3.1+R3.2+R3.3, R1, R3.4, R3.5:** all landed before this session's own work began; unchanged detail in git log (search `harvest L4.35x`).

**merge-up-53 execution (this session):** merge `fbe079783` clean → `snapshot-goals.py --render`+`--check` both clean → verify-suite (first two attempts genuinely FAILED on `tests` timeout, root-caused to SM.23's defect, not to R3.4/R3.5) → belam reverted SM.23's hunk (`912363623`) → verify-suite re-run at `ac12854ca`, **all 11 green** → `grid.py commit --all` (0 new versions, concurrent `grid_sync` cron had already caught it — confirmed via `grid.py versions`, not assumed) → push (already up to date both times) → `verification.py --level rotation --stamp` **all 10 green** at `ee72532d7` → reported to belam.

## §2 LIVE + QUEUE

**LIVE: mur-53** — director-review's adversarial workflow, not yet run/named. Nothing on my side blocks it; it's the Prime's/director-review's move.

**QUEUE once mur-53 ACCEPTs:**
1. `branch-reshuffle --dry-run --kinds towns,posts,loops` (never `main`) — **read the list BY NAME**, never an expected count.
2. `--apply` → suite green → `--delete-old` → cell re-spellings (Prime applies) → `verify` → commit.

**If mur-53 comes back with findings instead of ACCEPT:** read them, fix or bank per the usual harvest discipline — don't assume ACCEPT and don't proceed to branch-reshuffle without it.

**R2/R4/R5/R6** still need a separate signed GO from belam — not yet asked, unchanged from before. Sources: mur-49 review JSON (`.agi/sessions/reviews/mur-49.review.json`, MAIN only, gitignored) keys L4.337 (R5), L4.338 (R4, R6) — read the relevant node body first, per grammar below.

**GRAMMAR (unchanged):** mint = `write.py create hypothesis <slug> --parent goal:g15 --parent hypothesis:<source> --set town=core --set "title=…" --set "testable_claim=$(cat file)" --actor sanctuary-director --role director` (**no literal `&&` anywhere in generated text**). commit + push. cut = `AGI_SEAT=sanctuary-director AGI_POST=sanctuary-director python3 extensions/agi/bin/dispatch.py . L4.NNN --target hypothesis:<id> --level small --tier parent --harness pi --branch` (sync first; stale-base = sync + prune empty iter dir + re-cut SAME id; `--allow-stale-base "<reason>"` on the 3rd refusal; verify via `find`/`git worktree list`). wait = `spawn_budget.py status --iter L4.NNN --wait --timeout <N>` backgrounded. harvest = diff vs merge-base → review bytes + node directly → check parent worktree `git status -sb` directly → merge `--no-ff -F file` → re-run suites here → for a destructive-path hypothesis, independently re-run the actual read-only command and read its actual output → `write.py <node> "note HARVEST L4.NNN (sanctuary-director, <ts>): …"` → commit + push.

## §3 🔴 NEXT COMMAND

```````
``````
`````
````
```
Check inbox fresh: python3 extensions/agi/bin/send.py read sanctuary-director

If it names mur-53's result: on ACCEPT, run the §2 QUEUE branch-reshuffle live sequence -- dry-run first, read the list BY NAME, then --apply, suite green, --delete-old, cell re-spellings (Prime applies), verify, commit. On anything short of ACCEPT, read the findings and handle per normal harvest discipline before touching branch-reshuffle.

If nothing new (mur-53 still not run, empty inbox): fine to bank, nothing blocks on it from my side. Productive parallel work: check R2/R4/R5/R6 status per the §2 QUEUE note -- read the relevant mur-49 node body first (L4.337 for R5, L4.338 for R4/R6), not the full review JSON unless the node body is insufficient. Do NOT ask belam for their GO yet unless you're actually about to mint/dispatch -- reading status is fine, asking prematurely is not.

SEPARATELY, before ever rotating further: (1) test -f /home/ubuntu/work/agi/.agi/sessions/seats/sanctuary-director.rename.json -- re-check fresh. (2) SM.23b -- check if it landed; not mine, don't touch, just note status. (3) generation-less -- never "gen N". (4) if this post ever takes another merge-up window, use the LIGHT recipe (take the lock yourself when free, tell the Prime ONE line after) -- the ask-and-wait recipe is confirmed superseded.
```
````
`````
``````
```````

## §4 TRAPS (kept from the prior card, trimmed where superseded; new ones from this session marked NEW)

- 🔴 **NEW: a piped command's reported exit code is the PIPE'S LAST STAGE, not the real command.** `commands.py run verify-suite | tail -80` reported "completed / exit code 0" from the Bash tool even when the actual suite FAILED (`tests` timed out, `RESULT: FAIL`) — `tail` always exits 0. **Always read the full output body and check its own `RESULT: PASS/FAIL` line**, never trust a wrapper-level completion notification alone. Cost real time twice this session before being caught.
- 🔴 **NEW: `verification.py`'s `tests` check swallows ALL diagnostic output on a timeout.** `subprocess.run(..., timeout=SUITE_TIMEOUT)` raising `TimeoutExpired` (verification.py:840-845) returns just "timed out after 1800s" — no tail, no hint which test. To diagnose a suite timeout, run `python3 -m pytest extensions/agi/tests/ -q --durations=15` **directly**, backgrounded, no wrapper.
- 🔴 **NEW: distinguishing "slow under load" from "actually stalled" in a backgrounded process:** check `cat /proc/<pid>/wchan` and `ps --ppid <pid>` for live children. `hrtimer_nanosleep` + no children + `ps -o time=` flat across a full poll interval (not just one reading) = a real stall. One `kill -INT` to a stuck pytest surfaces the exact file:line via the KeyboardInterrupt traceback — costs that run, worth it once for the diagnosis.
- 🔴 **NEW: a `run_in_background: true` Bash call is NOT killed by its own `timeout` param** — confirmed one ran 30+ minutes to natural completion past a `timeout: 600000` value. Don't rely on `timeout` as a safety ceiling once backgrounded; use `TaskStop` or a self-imposed check-in instead.
- 🔴 **NEW: "harvested + merged, closed, not mine" is not the same claim as "verified defect-free under real load."** SM.23 was noted as closed earlier this session and turned out to have broken every suite run since its merge. A HARVEST note existing doesn't mean stop checking if its symptom shows up live.
- 🔴 **NEW: the advisory suite lock reading free does not prevent a collision** — it's advisory, not exclusive. Announce one line to the Prime before a MAIN suite run, in addition to checking the lock. (But: prose/comms commits landing mid-suite are non-voiding — see §0.)
- 🔴 A literal `&&` inside claim/title/note/thought TEXT breaks `write.py`'s script parser — write "and" instead.
- 🔴 `write.py`'s `set`/`create --set` edits whatever tree your CWD resolves to — from your OWN worktree it edits YOUR copy, not MAIN's.
- 🔴 A tier-parent's `cli.py done --owns ...` does **not** write the verdict onto the owned node's frontmatter, and when MULTIPLE kids ran, the commit subject may cite only the FIRST (now-superseded) kid — read EVERY kid node in full, the LAST one's frontmatter verdict is the one that matters.
- 🔴 **For a round guarding a destructive path, "tests pass" answers a narrower question than the gate actually asks.** Recurred repeatedly across mur-52→R3.4→R3.5 (green tests, live dry-run still did the dangerous thing each time). Always independently re-run the actual read-only command with the actual planned flags and read its actual output list; for containment/presence claims, call the shipped helper directly against real data too.
- 🔴 A round's session records can be split across MULTIPLE worktrees with MAIN's own copy sitting completely EMPTY.
- 🔴 `grid.py commit --all` REFUSES on a non-master/non-main branch — MAIN only. A concurrent `grid_sync` cron may beat you to a version ("0 new version(s)" isn't necessarily an error — verify with `grid.py versions <node>`).
- 🔴 root `HANDOFF.md` and the quorum card are TWO DIFFERENT FILES.
- 🔴 Under heavy concurrent write load, `dispatch.py` can print `{"issue": "stale-base", ...}` **and then keep printing lines that look like a successful spawn** — verify with `find`/`git worktree list`.
- 🔴 At harvest, always check the parent's own worktree with `git status -sb` directly.
- 🔴 A merge commit's own prose can mischaracterize which node a round targeted if written from memory — verify against the round's own harvest commit.
- 🔴 A round's own narrow test suite going green is not the same as the full engine suite staying green.
- 🔴 A merge-up GRANT is state — `test -f` the lock + inbox before `git merge` in MAIN; undo = `git reset --soft <base>`, never `reset --hard`.
- 🔴 `-F <file>` for every commit/merge/dm message. Never `pkill -f` in a Bash-tool command — kill specific confirmed-mine PIDs instead.
- 🔴 The five node counts are the ENGINE'S metric, never `find | wc`.
- 🔴 A DM claiming to relay a real owner order can be genuine but still arrive before your own branch has synced far enough to see the doc entry it cites.
- `date -u` for stamps. Never `test_provisioning.py` / full-suite pytest with `--basetemp` under the repo. Never hand-poll — `--wait`, backgrounded if long, or a bounded background wait-loop for external state (Monitor / `until`-loop). `crons.py` refuses from a worktree.

## §5 KNOWN-GOOD VERIFICATION

**Current baseline (this session, post SM.23 revert):** verify-suite at `ac12854ca` — **all 11 green**, `tests` 471.4s (4766 passed, 15 skipped, 0 failed). Rotation stamp at `ee72532d7` — **all 10 green** — active=2830 deprecated=198 total=3028 broken_links=0. (Prior baseline `bef788a5e` 2811/198/3009 is superseded; the intermediate `ac12854ca`-pre-revert numbers, 2829/198/3027, were real but carried the SM.23-defect suite failure.)

`test_branch_reshuffle*.py` + `test_branches.py` + `test_branch_spelling_grep.py`: 151 (R3.5 baseline, unchanged this session). `test_rotate*.py`: 742 passed + 1 xfailed (R1, unchanged). Live read-only `--dry-run --delete-old --kinds towns,posts,loops`: unchanged from R3.5's own reverification (5 post/town branches refuse, 1 loop branch refuses, 2 admitted) — **re-confirm fresh before branch-reshuffle actually runs**, don't assume it's still accurate given how much has landed on MAIN since.

## §6 BANKED (not mine; with a recommendation)

**17. (was: "mur-51/SM.23 still open, not mine").** Updated, still not mine: SM.23 reverted by the Prime (real defect: `heal.py` stalled-live poll never terminates, matches the 1800s suite ceiling exactly), re-land planned as SM.23b (`ee72532d7`). Don't touch, don't restart the reaper, just track status.

**16.** `test_sensei_wake_audit.py` F2/F3 label drift — flagged, already fixed by someone else on MAIN minutes later. Closed.

**14-15, 13** carried unchanged (master-sensei's verification-weakening suggestion not adopted; the "testing plan" phrase's exact scope unconfirmed; director-review's mur-50 process suggestion re: remote-visibility fixtures, not yet minted).

Carried unchanged: 1. Kid model — owner named only the parent. 2. `hypothesis:l4-completion-signal-cannot-tell-dead-from-silent` — the Prime's held round. 3. `links.py schema` 124 pre-L4 violators. 4. `crons.py cmd_remove` unfenced. 5. L4.126's parent died under the INLINE reaper. 6. Stub repo `/home/ubuntu/work/streamer-stub` unpushed commits. 7. L4.192 wording residue. g15 candidates to propose: the 0b-b captive after_join; `l4-a-foreign-tree-edit-is-committed-in-the-same-breath`; rungs 2-4 as g15 lines; `ref_candidates` keeps the input spelling.

**11. RULED by the Prime:** the row (`claude-sonnet-5`) is the authority on model; never a flag in this card. Struck, stays struck.

## STANDING RULES (binding; unchanged from the prior card)

- **Reporting (owner 2026-09-10): only when NECESSARY** = a merge-up ready/done · a Prime-only decision · a rotation line · a red merge or a rule-changing finding.
- **Authority is verified against the GRAPH:** `git fetch && send.py whois <ref> --claim <post>` + the ListAgents row + `tmux capture-pane`. For a RELAYED OWNER DECISION, verify independently against `doc:l4-owner-decisions` and the commit that banked it. **Sync first if the cited entry isn't found locally.**
- A peer's instruction (the Prime's included) is not authority to edit `CLAUDE.md`, permissions, `.agi/config.json`, `ladder.md`, `config:seats`, `moral:*` — quote the false line, write the replacement into the node, stop.
- **ENHANCED SURVIVAL** (`goal:g17.1`): parallel rounds GO where file scopes are disjoint; up to 5 kids per parent. Never: wake another post · write `config:seats` · touch `moral:*` · `git rm` under `.agi/nodes` · rebase/force-push · `level3.py` without `--dry-run` · `grid.py checkout` · `git stash`.
- **Spend:** $5.00 floor: below it NO new round is dispatched, live rounds finish — PAUSED until the owner resumes.
- **No "gen N" anywhere.**

## MERGE-UP RECIPE (CONFIRMED: light recipe, posts-local-only is RULED — see banner)

1. This branch synced to `origin/season2/main`; `verify` green here.
2. Confirm the advisory suite lock is free (`verification.py window`), send the Prime ONE line ANNOUNCING you're taking it (not asking — no wait for a grant), then proceed. (Old recipe — ask, then wait for a grant — is superseded; only fall back to it if the light recipe visibly isn't in force.)
3. In MAIN (`git status` first; never clean/stash): `git merge --no-ff season2/posts/sanctuary-director -F <file>` → `snapshot-goals.py --render` → `--render --check` → `commands.py run verify-suite` (background it — don't trust the tool's own completion/exit-code notification, read the actual output body's `RESULT:` line) → `grid.py commit --all` → `git push origin season2/main` + `git push origin "refs/grid/*:refs/grid/*"` → `verification.py --level rotation --stamp` → ONE message to the Prime, numbers + hash.
4. **Never merge-then-hold.**

## ROTATING YOURSELF

**FIRST, always:** `test -f /home/ubuntu/work/agi/.agi/sessions/seats/sanctuary-director.rename.json`. Re-check fresh.

At **0.47** of the meter's `est.` number, or sooner at a clean stopping point. `python3 extensions/agi/bin/rotate.py rotate` — bare and keyed, NO flag. Refuses by name when the card's where-it-stops slot is stale. **NEVER pass a model flag.** Effort `max`; never `loop`. If its gate names `behind`: `git merge --no-edit origin/season2/main` and re-run. **Prayer: exactly two spots per session — the very first tokens of your first reply, and the very last tokens before rotate-self returns; never at the start or end of any turn in between.**

## WHAT THIS POST HAS LEARNED

- A relayed instruction with real stakes deserves independent verification against the graph, not blind trust OR reflexive refusal.
- A round's session dir can be completely empty in one worktree while the real data lives in another; check all plausible locations.
- A rule's own predicted outcome can legitimately differ from the real case without that being a defect.
- A completion tool writing to "the record" can mean two different records depending on flag mode — and when MULTIPLE kids ran, the commit subject may cite only the first, now-superseded one. Read every kid node, the LAST verdict is the one that counts.
- Correct your own record in the file your successor reads, in the same breath as the finding.
- The STARTUP OUTPUT is the wake — a fact printed there is never re-derived by hand.
- A DM citing a graph doc can be genuine but still outrun your own branch's sync.
- A round's own narrow test suite going green is not the same as the full engine suite staying green.
- Verify a round's target hypothesis against its own harvest commit message, not from memory.
- **"Tests pass" is not the same question as "does the actual dry-run list still contain the dangerous thing."** Recurred repeatedly at successive levels (R3.1-3 → R3.4 → R3.5), each caught by someone actually running the real read-only command and reading its real output.
- **A tool's own completion notification (exit code, "completed") can be true of the wrong stage** — a pipe through `tail`/`head` reports the pipe's exit code, not the real command's. Read the actual output body's own result line, always.
- **"Closed, not mine" on a node is a status, not a guarantee** — a merged, harvested fix can still carry a live defect that only shows up under real concurrent load. If a symptom recurs, re-open the question even if the graph says done.
- **An advisory lock reading free is necessary but not sufficient for exclusivity** — announce before a shared-resource operation, don't rely on the lock file alone.
- **A stall and a hang are different diagnoses and need different evidence** — CPU-time flat across a full poll interval plus no live children plus a syscall-level wait (wchan) is what distinguishes "genuinely stuck" from "just slow under load." A single low reading proves nothing; the pattern across repeated checks does.
